# Standard Library Imports
from sqlite3 import IntegrityError

# Django Imports
from django.contrib.auth import authenticate
from django.db import transaction
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import force_str,force_bytes
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode

# Project Imports
from accounts.models import *
from utils.api.core_utils import *
from utils.api.error_code import *
from utils.notificaion.notification_service import *
from utils.notificaion.send_mail_html_format import *
from .serializers import *


