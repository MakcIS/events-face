from datetime import datetime, timedelta

import requests
from requests.exceptions import HTTPError
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from requests.exceptions import ConnectionError, JSONDecodeError, Timeout

from src.events.models import Events
from src.sync.models import EventsSync


class Command(BaseCommand):
    help = "Event synchronization"

    def get_event_from_url(self, url, params):
        while url:
            try:
                response = requests.get(url, params=params)
                response.raise_for_status()
                data = response.json()
                results = data.get("results", [])
                for event in results:
                    yield event
                url = data.get("next")
                params = None

            except (ConnectionError, Timeout, AttributeError, JSONDecodeError, HTTPError):
                break


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
                changed_at = None
            elif options.get("date"):
                changed_at = datetime.strptime(options.get("date"), "%Y-%m-%d").date()
                params["changed_at"] = str(changed_at)
            else:
                changed_at = datetime.now() - timedelta(days=1)
                changed_at = changed_at.date()
                params["changed_at"] = str(changed_at)
        except ValueError:
            raise CommandError("Wrong date format, need YYYY-MM-DD")
        except AttributeError:
            raise CommandError("EVENTS_API_URL setting not found in settings.py")

        created_counter, updated_counter = 0, 0
        for event in self.get_event_from_url(url, params):
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


        EventsSync.objects.create(created=created_counter, updated=updated_counter, changed_at=date)
        self.stdout.write(
            f"Дата синхронизации: {datetime.now().date()}\nСозданно:{created_counter}\nОбновленно:{updated_counter}\nДата обновления: {changed_at}"
        )
