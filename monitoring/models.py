from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import AbstractUser

from django.contrib.auth.models import Group, Permission





class GridData(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    voltage = models.FloatField()
    current = models.FloatField()
    anomaly = models.BooleanField(default=False)
    attack_type = models.CharField(max_length=50, blank=True, null=True)  # e.g., FDI, Replay, DoS

    def __str__(self):
        return f"{self.timestamp} - V:{self.voltage}, I:{self.current}, Anomaly:{self.anomaly}"

class Profile(models.Model):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('operator', 'Operator'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='operator')

    def __str__(self):
        return f"{self.user.username} - {self.role}"


# 🔹 Automatically create/update Profile when User is created/updated
@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()



