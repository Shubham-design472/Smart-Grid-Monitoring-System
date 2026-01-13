from django.core.management.base import BaseCommand
from monitoring.models import GridData
from random import uniform, choice
from datetime import datetime, timedelta

class Command(BaseCommand):
    help = "Seed GridData with random demo data"

    def handle(self, *args, **kwargs):
        GridData.objects.all().delete()
        for i in range(50):
            GridData.objects.create(
                timestamp = datetime.now() - timedelta(minutes=50-i),
                voltage = round(uniform(210, 240), 2),
                current = round(uniform(4, 10), 2),
                anomaly = choice([False, False, False, True])
            )
        self.stdout.write(self.style.SUCCESS("Successfully seeded 50 GridData entries"))

