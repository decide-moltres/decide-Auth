from django.db import models


# Create your models here.

class UserProfile(AbstractBaseUser):
    SEX_OPTIONS = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    )
    related_political_party = models.CharField(_('Related political party'),max_length=30, blank=True)
    birthdate = models.DateField(_('Birthdate'),null=True)
    sex = models.CharField(_('Sex'),max_length=1, choices=SEX_OPTIONS, null=True)
    related_user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True,
    )
