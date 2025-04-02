from datetime import datetime, timedelta

import requests
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from requests.exceptions import ConnectionError, JSONDecodeError, Timeout

from src.events.models import Events
from src.sync.models import EventsSync


class Command(BaseCommand):
    help = "Event synchronization"

    def fetch_url(self, url, params):
        created_counter, updated_counter = 0, 0

        def save_events(results):
            nonlocal created_counter, updated_counter
            for event in results:
                try:
                    id = event["id"]
                    name = event["name"]
                    date = datetime.fromisoformat(event["event_time"]).date()
                    status = event["status"]
                    _, created = Events.objects.update_or_create(
                        id=event["id"],
                        defaults={
                            "id": id,
                            "name": name,
                            "date": date,
                            "status": status,
                        },
                    )
                except KeyError:
                    continue

                if created:
                    created_counter += 1
                else:
                    updated_counter += 1

        while url:
            try:
                response = requests.get(url, params=params)
                if response.status_code == 200:
                    data = response.json()
                    results = data.get("results", [])
                    save_events(results)
                    url = data.get("next")
                    params = None
                else:
                    break
            except (ConnectionError, Timeout, AttributeError, JSONDecodeError):
                break

        return created_counter, updated_counter

    def add_arguments(self, parser):
        parser.add_argument("date", nargs="?", type=str, help="Date YYYY-MM-DD")
        parser.add_argument(
            "--all", action="store_true", required=False, help="All events"
        )

    def handle(self, *args, **options):
        try:
            url = settings.EVENTS_API_URL
            params = {}
            if options.get("all"):
                date = None
            elif options.get("date"):
                date = datetime.strptime(options.get("date"), "%Y-%m-%d").date()
                params["changed_at"] = str(date)
            else:
                date = datetime.now() - timedelta(days=1)
                date = date.date()
                params["changed_at"] = str(date)
        except ValueError:
            raise CommandError("Wrong date format, need YYYY-MM-DD")
        except AttributeError:
            raise CommandError("EVENTS_API_URL setting not found in settings.py")

        create, update = self.fetch_url(url, params)

        EventsSync.objects.create(created=create, updated=update, changed_at=date)
        self.stdout.write(
            f"Дата синхронизации: {datetime.now().date()}\nСозданно:{create}\nОбновленно:{update}\nДата обновления: {date}"
        )
