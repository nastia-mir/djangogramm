from django.core.management.base import BaseCommand
from ...models import DjGUser


class Command(BaseCommand):

    def handle(self, *args, **options):
        if not DjGUser.objects.filter(username="admin").exists():
            DjGUser.objects.create_superuser("nastasia.ua@gmail.com", "admin", "admin", "strongpassword")