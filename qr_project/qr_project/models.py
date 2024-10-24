from django.db import models
from django.contrib.auth.models import User

from django.db import models

class QRCode(models.Model):
    words = models.TextField()  # Store the text/URL used to generate the QR code
    qr_code_image = models.ImageField(upload_to='qr_codes/')  # Store the QR code image
    generated_at = models.DateTimeField(auto_now_add=True)  # Store the generation timestamp

    def __str__(self):
        return f"QR Code for {self.words} - {self.generated_at}"
