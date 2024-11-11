from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class QRCode(models.Model):
    words = models.TextField()
    qr_code_image = models.ImageField(upload_to='qr_codes/')
    generated_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='qr_codes',default=1)  # ForeignKey for User

    def __str__(self):
        return f"QR Code for {self.words} - {self.generated_at}"

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    organization_name = models.CharField(max_length=100)
    employee_id = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.user.username}'s profile"

# Signals to automatically create and save UserProfile when a User is created
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

'''@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()'''


class UserVisit(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    visited_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} visited at {self.visited_at}"