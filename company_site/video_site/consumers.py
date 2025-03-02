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
            users = serialize('json', get_user_model().objects.all())
            settings = serialize('json', models.Settings.objects.all())
            movies = serialize('json', models.Movie.objects.all())
            genres = serialize('json', models.Genre.objects.all())
            actors = serialize('json', models.Actor.objects.all())
            movieActorEntries = serialize('json', models.MovieActorEntry.objects.all())
            movieGenreEntries = serialize('json', models.MovieGenreEntry.objects.all())
            watchEntries = serialize('json', models.WatchEntry.objects.all())
            bookmarkEntries = serialize('json', models.BookmarkEntry.objects.all())

        except Exception as e:
            print(e)

        self.send(text_data=json.dumps({
            "users": users,
            "settings": settings,
            "movies": movies,
            "genres": genres,
            "actors": actors,
            "movieActorEntries": movieActorEntries,
            "movieGenreEntries": movieGenreEntries,
            "watchEntries": watchEntries,
            "bookmarkEntries": bookmarkEntries,
        }))