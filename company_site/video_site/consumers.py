import json
from channels.generic.websocket import WebsocketConsumer

from django.contrib.auth import get_user_model
from . import models

from django.core.serializers import serialize

class ConnectionTest(WebsocketConsumer):
    def connect(self):
        self.accept()

    def disconnect(self, close_code):
        self.close()   

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        expression = text_data_json['expression']
        
        try:
            data = ""

            data += "[ Users ]\n"
            for item in get_user_model().objects.all():
                data += serialize('json', [item,]) + "\n"

            data += "\n[ Settings ]\n"
            for item in models.Settings.objects.all():
                data += serialize('json', [item,]) + "\n"

            data += "\n[ Movies ]\n"
            for item in models.Movie.objects.all():
                data += serialize('json', [item,]) + "\n"

            data += "\n[ Genres ]\n"
            for item in models.Genre.objects.all():
                data += serialize('json', [item,]) + "\n"

            data += "\n[ Actors ]\n"
            for item in models.Actor.objects.all():
                data += serialize('json', [item,]) + "\n"

            data += "\n[ Movie Actor Entries ]\n"
            for item in models.MovieActorEntry.objects.all():
                data += serialize('json', [item,]) + "\n"

            data += "\n[ Movie Genre Entries ]\n"
            for item in models.MovieGenreEntry.objects.all():
                data += serialize('json', [item,]) + "\n"

            data += "\n[ Watch Entries ]\n"
            for item in models.WatchEntry.objects.all():
                data += serialize('json', [item,]) + "\n"

            data += "\n[ Bookmark Entries ]\n"
            for item in models.BookmarkEntry.objects.all():
                data += serialize('json', [item,]) + "\n"

        except Exception as e:
            print(e)

        self.send(text_data=json.dumps({
            "key": data,
        }))