# Helper function to construct the email body

def construct_email_welcome(user_name, email):
    """Construct welcome email for new users"""
    subject = "Welcome to Forever - Your Style Journey Begins!"
    
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; background-color: #f4f4f4; margin: 0; padding: 20px; }}
            .container {{ max-width: 600px; margin: 0 auto; background: white; border-radius: 10px; overflow: hidden; }}
            .header {{ background: #000; color: white; padding: 30px; text-align: center; }}
            .content {{ padding: 30px; }}
            .button {{ display: inline-block; padding: 12px 24px; background: #000; color: white; text-decoration: none; border-radius: 5px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>Welcome to Forever!</h1>
            </div>
            <div class="content">
                <h2>Hi {user_name},</h2>
                <p>Thank you for joining Forever! We're excited to have you on board.</p>
                <p>Start exploring our latest collections and enjoy exclusive offers.</p>
                <a href="https://foreverbuy.in" class="button">Shop Now</a>
                <p>Use code <strong>WELCOME20</strong> for 20% off your first order!</p>
                <p>Happy Shopping!<br>Forever Team</p>
            </div>
        </div>
    </body>
    </html>
    """
    return subject, html_content



def construct_reset_password_email(user_name, email, reset_link):
    subject = "Reset Your Grocery Account Password"

    html_body = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>Password Reset</title>
    </head>

    <body style="
        margin:0;
        padding:0;
        background:#f5f7fa;
        font-family:Arial,sans-serif;
    ">

    <table width="100%" cellpadding="0" cellspacing="0">
        <tr>
            <td align="center">

                <table width="600" cellpadding="0" cellspacing="0"
                       style="
                            background:#ffffff;
                            margin:40px auto;
                            border-radius:16px;
                            overflow:hidden;
                            box-shadow:0 4px 20px rgba(0,0,0,0.08);
                       ">

                    <!-- Header -->
                    <tr>
                        <td align="center"
                            style="
                                background:#22c55e;
                                padding:35px;
                                color:white;
                            ">

                            <h1 style="margin:0;">
                                🛒 Grocery Delivery
                            </h1>

                            <p style="
                                margin-top:10px;
                                font-size:16px;
                            ">
                                Password Reset Request
                            </p>

                        </td>
                    </tr>

                    <!-- Content -->
                    <tr>
                        <td style="
                            padding:40px;
                            color:#333333;
                        ">

                            <h2>Hello {user_name},</h2>

                            <p>
                                We received a request to reset the password
                                for your Grocery Delivery account associated
                                with:
                            </p>

                            <p>
                                <strong>{email}</strong>
                            </p>

                            <p>
                                Click the button below to create a new password.
                            </p>

                            <div style="
                                text-align:center;
                                margin:35px 0;
                            ">

                                <a href="{reset_link}"
                                   style="
                                        background:#22c55e;
                                        color:white;
                                        padding:16px 35px;
                                        text-decoration:none;
                                        border-radius:8px;
                                        font-size:16px;
                                        font-weight:bold;
                                   ">
                                   Reset Password
                                </a>

                            </div>

                            <p>
                                This password reset link will expire in
                                <strong>24 hours</strong>.
                            </p>

                            <p>
                                If you didn't request this change,
                                you can safely ignore this email.
                            </p>

                            <p>
                                For security reasons,
                                your password will remain unchanged until
                                a new password is created.
                            </p>

                            <br>

                            <p>
                                Regards,<br>
                                <strong>Grocery Delivery Team</strong>
                            </p>

                        </td>
                    </tr>

                    <!-- Footer -->
                    <tr>
                        <td align="center"
                            style="
                                background:#f8f9fa;
                                padding:25px;
                                font-size:12px;
                                color:#777777;
                            ">

                            © 2026 Grocery Delivery

                            <br><br>

                            This is an automated email.
                            Please do not reply directly to this message.

                        </td>
                    </tr>

                </table>

            </td>
        </tr>
    </table>

    </body>
    </html>
    """

    return subject, html_body