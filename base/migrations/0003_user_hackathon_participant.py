# Generated by Django 4.0.6 on 2022-11-10 21:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0002_user_bio_user_name_alter_user_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='hackathon_participant',
            field=models.BooleanField(default=True, null=True),
        ),
    ]
