from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, Group

class Command(BaseCommand):
    help = 'Add users to the database'

    def handle(self, *args, **kwargs):
        users = [
            {'email': 'admin@gmail.com', 'password': 'admin', 'group': 'Admin'},
            {'email': 'psmkduraisamy@gmail.com', 'password': 'qazwsx', 'group': 'Alumni'},
            {'email': 'psmkvduraisamy@gmail.com', 'password': 'qazwsx', 'group': 'Student'},
        ]

        for user_data in users:
            email = user_data['email']
            password = user_data['password']
            group_name = user_data['group']

            if not User.objects.filter(email=email).exists():
                user = User.objects.create_user(username=email, email=email, password=password)
                group, created = Group.objects.get_or_create(name=group_name)
                user.groups.add(group)
                self.stdout.write(self.style.SUCCESS(f'Successfully added user: {email} to group: {group_name}'))
            else:
                self.stdout.write(self.style.WARNING(f'User with email {email} already exists.'))
