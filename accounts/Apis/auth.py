from ..views import *


class SignUpAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            username = request.data.get('username')
            email = request.data.get('email').lower()
            password = request.data.get('password')

            missing = check_missing_fields(request.data, ['username', 'email', 'password'])
            if missing:
                return missing

            if CustomUser.objects.filter(username=username).exists():
                return Response({'status': 'fail','message': f'{BAD_REQUEST} - Username already exists'}, 
                                status=status.HTTP_400_BAD_REQUEST)

            if CustomUser.objects.filter(email=email).exists():
                return Response({'status': 'fail','message': f'{BAD_REQUEST} - Email already exists'}, 
                                status=status.HTTP_400_BAD_REQUEST)

            with transaction.atomic():
                user = CustomUser.objects.create_user(
                    username=username,
                    email=email,
                    password=password,
                )

            response_data = {
                'status': 'success',
                'message': f'{SUCCESS} - Account created successfully',
                'data': {
                    'user': {
                        'id': user.id,
                        'email': user.email,
                        'name': user.username
                    }
                }
            }
            return Response(response_data, status=status.HTTP_201_CREATED)

        except IntegrityError:
            return Response({"status": "fail","message": f"{BAD_REQUEST} - Username or Email already exists"}, 
                            status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({"status": "error","message": f"{INTERNAL_SERVER_ERROR} - Internal server error: {str(e)}"}, 
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class LoginAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            email = request.data.get('email').lower()
            password = request.data.get('password')

            missing = check_missing_fields(request.data,['email', 'password'])
            if missing:
                return missing

            user = authenticate(request,email=email,password=password)
            if not user:
                return Response({'status': 'fail','message': f'{BAD_REQUEST} - Email or Password is incorrect'}, 
                                status=status.HTTP_400_BAD_REQUEST)

            if not user.is_active:
                return Response({'status': 'fail','message': 'Account is inactive'}, 
                                status=status.HTTP_403_FORBIDDEN)

            tokens = get_tokens_for_user(user)

            response_data = {
                'status': 'success',
                'message': f'{SUCCESS} - User Login successfully.',
                'data': {
                    'access_token': tokens['access'],
                    'refresh_token': tokens['refresh'],
                    'user': {
                        'id': user.id,
                        'email': user.email,
                        'name': user.username                    
                    }
                }
            }
            return Response(response_data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"status": "error","message": f"{INTERNAL_SERVER_ERROR} - Internal server error: {str(e)}"}, 
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class RequestResetPasswordAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            email = request.data.get("email")

            if not email:
                return Response(
                    {
                        "status": "fail",
                        "message": "Email is required"
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

            email = email.strip().lower()

            user = CustomUser.objects.filter(
                email__iexact=email
            ).first()

            if not user:
                return Response(
                    {
                        "status": "fail",
                        "message": "User does not exist"
                    },
                    status=status.HTTP_404_NOT_FOUND
                )

            smtp_config = SMTPMail.objects.filter(
                is_deactive=False
            ).first()

            if not smtp_config:
                return Response(
                    {
                        "status": "fail",
                        "message": "SMTP configuration not found"
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

            uid = urlsafe_base64_encode(
                force_bytes(user.pk)
            )

            token = PasswordResetTokenGenerator().make_token(
                user
            )

            reset_link = (
                f"http://127.0.0.1:3000/reset-password/"
                f"{uid}/{token}/"
            )

            subject = "Reset Your Grocery Account Password"

            html_body = f"""
            <html>
            <body>
                <h2>Password Reset Request</h2>

                <p>Hello {user.first_name or user.email},</p>

                <p>You requested a password reset.</p>

                <p>
                    Click the button below to reset your password:
                </p>

                <a href="{reset_link}"
                   style="
                       background:#22c55e;
                       color:white;
                       padding:12px 20px;
                       text-decoration:none;
                       border-radius:5px;
                       display:inline-block;
                   ">
                    Reset Password
                </a>

                <br><br>

                <p>
                    If the button does not work, use this link:
                </p>

                <p>{reset_link}</p>

                <p>
                    If you did not request this,
                    please ignore this email.
                </p>

                <br>

                <p>
                    Grocery Delivery Team
                </p>
            </body>
            </html>
            """

            success, error_message = send_emails(
                smtp_config=smtp_config,
                recipient_email=user.email,
                subject=subject,
                html_body=html_body
            )

            if not success:
                return Response(
                    {
                        "status": "error",
                        "message": error_message
                    },
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )

            return Response(
                {
                    "status": "success",
                    "message": "Password reset link sent successfully"
                },
                status=status.HTTP_200_OK
            )

        except Exception as e:
            return Response(
                {
                    "status": "error",
                    "message": str(e)
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


        


class ResetPasswordAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            uid = request.data.get("uid")
            token = request.data.get("token")
            password = request.data.get("new_password")
            confirm_password = request.data.get("confirm_password")

            if not all([
                uid,
                token,
                password,
                confirm_password
            ]):
                return Response(
                    {
                        "status": "fail",
                        "message": "All fields are required"
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

            if password != confirm_password:
                return Response(
                    {
                        "status": "fail",
                        "message": "Passwords do not match"
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

            user_id = force_str(
                urlsafe_base64_decode(uid)
            )

            user = CustomUser.objects.get(
                pk=user_id
            )

            if not PasswordResetTokenGenerator().check_token(
                    user,
                    token
            ):
                return Response(
                    {
                        "status": "fail",
                        "message": "Reset link expired or invalid"
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

            user.set_password(password)
            user.save()

            return Response(
                {
                    "status": "success",
                    "message": "Password changed successfully"
                },
                status=status.HTTP_200_OK
            )

        except Exception:
            return Response(
                {
                    "status": "fail",
                    "message": "Invalid reset link"
                },
                status=status.HTTP_400_BAD_REQUEST
            )