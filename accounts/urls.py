# django Imports
from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from accounts.Apis.auth import *

# Local Project Imports

urlpatterns = [
    path('signup/', SignUpAPIView.as_view()),
    path('login/', LoginAPIView.as_view()),
    path('refresh-token', TokenRefreshView.as_view()),
    path('request-reset-password/', RequestResetPasswordAPIView.as_view()),
    path('verify-otp/', VerifyOTPAPIView.as_view()),
    path('reset-password/', ResetPasswordAPIView.as_view()),


]
