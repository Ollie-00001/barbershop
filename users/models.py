
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
	if created:
		UserProfile.objects.create(user=instance)

class UserProfile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
	avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
	birth_date = models.DateField(blank=True, null=True)
	telegram_id = models.CharField(max_length=64, blank=True)
	github_id = models.CharField(max_length=64, blank=True)

	def __str__(self):
		return f"Profile of {self.user.username}"
