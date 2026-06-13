from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email
    

class SMTPMail(models.Model):
    smtp_id = models.AutoField(primary_key=True)
    action_type = models.CharField(max_length=255, null=True, blank=True)
    action_id  = models.IntegerField(null=True, blank=True)
    smtp_host = models.CharField(max_length=255, null=True, blank=True)
    smtp_port = models.IntegerField(null=True, blank=True)
    encryption_type = models.CharField(max_length=255, null=True, blank=True)
    smtp_host_user = models.CharField(max_length=255, null=True, blank=True)
    smtp_host_password = models.CharField(max_length=255, null=True, blank=True)
    from_email = models.CharField(max_length=255, null=True, blank=True)
    smtp_type = models.CharField(max_length=255, default='GENRAL',null=True, blank=True)
    verify_code = models.CharField(max_length=128, blank=True, null=True)
    verify_code_expire_at = models.DateTimeField(blank=True, null=True)
    is_deactive = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'sa_smtp_mail'
