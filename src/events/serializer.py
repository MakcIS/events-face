from rest_framework import serializers

from src.events.models import Events, Places


class PlaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Places
        fields = ["name"]


class EventsSerializer(serializers.ModelSerializer):
    place = PlaceSerializer()

    class Meta:
        model = Events
        fields = ["id", "name", "date", "place"]
