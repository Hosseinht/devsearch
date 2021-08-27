from django.contrib.auth.models import User
from .models import Profile
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver


# @receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        user = instance  # sender= User, instance = instance of User
        profile = Profile.objects.create(
            user=user,
            username=user.username,
            email=user.email,
            name=user.first_name,
        )


def delete_user(sender, instance, **kwargs):
    user = instance.user
    # .user! one to one relationship. we need User.
    # user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    user.delete()


post_save.connect(create_profile, sender=User)
post_delete.connect(delete_user, sender=Profile)