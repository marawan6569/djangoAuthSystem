# Generated by Django 4.0.6 on 2022-07-22 18:20

import authentication.validations
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0004_alter_user_phone_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='avatar',
            field=models.ImageField(blank=True, help_text='Supported content types: jpg, jpeg, png .', null=True, upload_to='avatars/'),
        ),
        migrations.AlterField(
            model_name='user',
            name='phone_number',
            field=models.CharField(help_text='Must be in E.164 format i.e. +xxxxxxxxxxx .', max_length=14, unique=True, validators=[authentication.validations.validate_phone_length, authentication.validations.validate_phone_starts_with_plus, authentication.validations.validate_phone_is_num], verbose_name='phone number'),
        ),
    ]
