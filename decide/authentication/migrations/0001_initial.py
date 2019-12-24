# Generated by Django 2.0 on 2019-12-23 19:44

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0009_alter_user_last_name_max_length'),
        ('voting', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('birthdate', models.DateField(null=True, verbose_name='Birthdate')),
                ('sex', models.CharField(choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other')], max_length=1, null=True, verbose_name='Sex')),
                ('related_user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('related_political_party', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='PoliticalParty', to='voting.PoliticalParty')),
            ],
        ),
    ]
