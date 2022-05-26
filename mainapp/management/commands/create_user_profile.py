from django.core.management.base import BaseCommand
from authapp.models import ShopUser, ShopUserProfile


class Command(BaseCommand):
    def handle(self, *args, **options):
        exclude_user_idx = ShopUserProfile.objects.only('user').values_list('user__id', flat=True)
        users = ShopUser.objects.exclude(id__in=exclude_user_idx).only('id').distinct()
        if users.exists():
            create_profiles = [ShopUserProfile(user=user) for user in users]
            ShopUserProfile.objects.bulk_create(create_profiles)


# class Command(BaseCommand):
#     def handle(self, *args, **kwargs):
#         users = ShopUser.objects.all()
#         for user in users:
#             user_profile = ShopUserProfile.objects.create(user=user)
#             user_profile.save()
