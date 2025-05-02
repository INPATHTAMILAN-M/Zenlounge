import requests
from django.core.management.base import BaseCommand
from authapp.models import Country  # Adjust if your model is in another app

class Command(BaseCommand):
    help = "Load countries from Layercode API into the Country model"

    def handle(self, *args, **kwargs):

        self.stdout.write("Loading countries...")
        # Fetch country data from Layercode API
        Country.objects.all().delete()  # Clear existing countries if needed
        url = "https://valid.layercode.workers.dev/list/countries?format=select&flags=true&value=code"
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            countries = data.get("countries", [])

            created, skipped = 0, 0
            for country in countries:
                code = country.get("value")
                name = country.get("label").split(" ", 1)[1]  # Remove flag emoji

                obj, created_flag = Country.objects.get_or_create(code=code, defaults={"name": name})
                if created_flag:
                    created += 1
                else:
                    skipped += 1

            self.stdout.write(self.style.SUCCESS(f"✔ Loaded countries: {created} created, {skipped} skipped."))
        else:
            self.stderr.write("✘ Failed to fetch country data.")
