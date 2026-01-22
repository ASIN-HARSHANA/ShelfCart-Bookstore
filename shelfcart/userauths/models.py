from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
import random

class User(AbstractUser):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=100)
    bio = models.CharField(max_length=180)
    
    
    is_active = models.BooleanField(default=True)
    
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username
    

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    image = models.ImageField(upload_to="image", null=True, blank=True)
    full_name = models.CharField(max_length=200, blank=True)
    bio = models.CharField(max_length=200, null=True, blank=True)
    phone = models.CharField(max_length=200, blank=True)
    verified = models.BooleanField(default=False)


    def __str__(self):
        return f"{self.user.username} - {self.full_name} - {self.bio}"
       
    

class ContactUs(models.Model):
    full_name = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    phone = models.CharField(max_length=200)
    subject = models.CharField(max_length=200) 
    message = models.TextField()


    class Meta:
        verbose_name = "Contact Us"
        verbose_name_plural = "Contact Us"
        

    def __str__(self):
        return self.full_name    
    
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


post_save.connect(create_user_profile, sender=User)    
post_save.connect(save_user_profile, sender=User)


class OTPVerification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='otps')
    otp_code = models.CharField(max_length=6)
    purpose = models.CharField(max_length=50, default='registration')
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    is_used = models.BooleanField(default=False)

    def __str__(self):
        return f"OTP {self.otp_code} for {self.user.email}"

    @property
    def is_expired(self):
        return timezone.now() > self.expires_at

    def is_valid(self, entered_otp):
        return not self.is_used and not self.is_expired and self.otp_code == entered_otp

    def mark_as_used(self):
        self.is_used = True
        self.save(update_fields=['is_used'])

    @classmethod
    def create_for_user(cls, user, purpose='registration', minutes_valid=1):  # ← Changed to 1 minute
        cls.objects.filter(user=user, purpose=purpose, is_used=False).delete()
    
        # Changed to 4-digit OTP (1000 to 9999)
        otp = str(random.randint(1000, 9999))  # ← 4 digits now
    
        expires_at = timezone.now() + timedelta(minutes=minutes_valid)
    
        return cls.objects.create(
            user=user,
            otp_code=otp,
        purpose=purpose,
            expires_at=expires_at
        )     