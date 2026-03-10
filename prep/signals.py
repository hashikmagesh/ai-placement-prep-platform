from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import UserProfile


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()

from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from django.utils import timezone
from .models import LoginActivity

@receiver(user_logged_in)
def track_login(sender, request, user, **kwargs):
    today = timezone.now().date()

    LoginActivity.objects.get_or_create(
        user=user,
        login_date=today
    )

from .models import PlacementProgress

@receiver(post_save, sender=User)
def create_progress(sender, instance, created, **kwargs):
    if created:
        PlacementProgress.objects.create(user=instance)