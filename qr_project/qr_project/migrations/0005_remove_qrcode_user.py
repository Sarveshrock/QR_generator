# Generated by Django 5.1.2 on 2024-11-09 08:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('qr_project', '0004_alter_qrcode_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='qrcode',
            name='user',
        ),
    ]
