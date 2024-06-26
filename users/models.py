from django.db import models
from django.contrib.auth.models import AbstractUser
from rest_framework_simplejwt.tokens import RefreshToken
from datetime import datetime, timedelta
import uuid
import random

NEW, CODE_VERIFY, DONE, PHOTO_DONE = ('new', 'code_verify', 'done','photo_done')
EMAIL, PHONE = ('email', 'phone')

class User(AbstractUser):

    AUTH_STEP =(
        (NEW, 'new'),
        (CODE_VERIFY, 'code_verify'),
        (DONE, 'done'),
        (PHOTO_DONE, 'photo_done'),
    )

    AUTH_TYPE = (
        (EMAIL, 'email'),
        (PHONE, 'phone'),
    )

    bio = models.TextField()
    phone_number = models.CharField(max_length=13, db_index=True,unique=True)
    image = models.ImageField(upload_to="users/", default="users/default.jpg")
    auth_step = models.CharField(max_length=30, choices=AUTH_STEP, default=NEW)
    auth_type = models.CharField(max_length=30, choices=AUTH_TYPE)

    def clean_username(self):
        if not self.username:
            temp_username = f"instagram-{str(uuid.uuid4()).split('-')[-1]}"
            self.username = temp_username

    def clean_password(self):
        if not self.password:
            self.password=f"instagram-{str(uuid.uuid4()).split('-')[-1]}"

    def hash_password(self):
        if not self.password.startswith('pbkdf2_'):
            self.set_password(self.password)

    def clean_all(self):
        self.clean_username()
        self.clean_password()
        self.hash_password()

    def save(self, *args, **kwargs):
        self.clean_all()
        super(User, self).save(*args, **kwargs)

    def token(self):
        refresh = RefreshToken.for_user(self)

        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        } 
    
    def create_code(self, auth_type):
        code = "".join([str(random.randint(1,9)) for _ in range(5)])

        CodeVerification.objects.create(
            code=code,
            auth_type=auth_type,
        )

        return code

class CodeVerification(models.Model):
     
    AUTH_TYPE = (
        (EMAIL, 'email'),
        (PHONE, 'phone'),
    )
     
    code = models.CharField(max_length=5)
    auth_type = models.CharField(max_length=52,choices=AUTH_TYPE)
    expire_time = models.DateTimeField()
    is_verified = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if self.auth_type == EMAIL:
            self.expire_time = datetime.now() + timedelta(minutes=2)
        elif self.auth_type == PHONE :
            self.expire_time = datetime.now() + timedelta(minutes=2)

        super(CodeVerification, self).save(*args, **kwargs)
