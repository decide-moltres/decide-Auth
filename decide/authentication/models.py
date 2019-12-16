from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class UserProfile(models.Model):
    SEX_OPTIONS = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    )
    related_political_party = models.CharField(('Related political party'),max_length=30, blank=True)
    birthdate = models.DateField(('Birthdate'),null=True)
    sex = models.CharField(('Sex'),max_length=1, choices=SEX_OPTIONS, null=True)
    related_user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True,
    )
