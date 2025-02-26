from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group

class Command(BaseCommand):
    help = 'Add default roles to Django Groups'

    ROLE_CHOICES = [
        ('student', 'Student'),
        ('admin', 'Admin'),
        ('alumni', 'Alumni'),
    ]

    def handle(self, *args, **options):
        for role_key, role_name in self.ROLE_CHOICES:
            group, created = Group.objects.get_or_create(name=role_name)
            if created:
                self.stdout.write(self.style.SUCCESS(f"Created group: {role_name}"))
            else:
                self.stdout.write(self.style.WARNING(f"Group '{role_name}' already exists."))
