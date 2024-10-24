# Generated by Django 5.1.2 on 2024-10-22 14:15

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='QRCode',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('words', models.TextField()),
                ('qr_code_image', models.ImageField(upload_to='qr_codes/')),
                ('generated_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]