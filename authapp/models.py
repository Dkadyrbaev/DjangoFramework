from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.timezone import now
from datetime import timedelta


class ShopUser(AbstractUser):
    avatar = models.ImageField(
        upload_to='users_avatars',
        blank=True,
    )
    age = models.PositiveIntegerField(
        verbose_name='Возраст',
        default=18,
    )
    activation_key = models.CharField(
        max_length=128,
        blank=True,
    )
    activation_key_expires = models.DateTimeField(
        default=(now() + timedelta(hours=48)),
        null=True,
        blank=True,
    )

    @property
    def is_activation_key_expired(self):
        try:
            if now() <= self.activation_key_expires:
                return False
        except Exception as e:
            pass
        return True


class ShopUserProfile(models.Model):
    MALE = 'M'
    FEMALE = 'W'

    GENDER_CHOICES = (
        (MALE, 'Мужчина'),
        (FEMALE, 'Женщина'),
    )

    user = models.OneToOneField(
        ShopUser,
        null=False,
        db_index=True,
        on_delete=models.CASCADE,
    )
    about = models.TextField(
        verbose_name='О себе',
        blank=True,
        null=True,
    )
    gender = models.CharField(
        verbose_name='пол',
        choices=GENDER_CHOICES,
        blank=True,
        max_length=2,
    )

    @receiver(post_save, sender=ShopUser)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            ShopUserProfile.objects.create(user=instance)

    @receiver(post_save, sender=ShopUser)
    def save_user_profile(sender, instance, **kwargs):
        instance.shopuserprofile.save()
