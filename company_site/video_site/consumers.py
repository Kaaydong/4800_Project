import json
from channels.generic.websocket import WebsocketConsumer

from django.contrib.auth import get_user_model
from . import models as data
from user_forms import models as user_data_models

from django.core.serializers import serialize

from channels.db import database_sync_to_async


class ConnectionTest(WebsocketConsumer):
    def connect(self):
        self.user = self.scope["user"]
        self.accept()

    def disconnect(self, close_code):
        self.close()   

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        key = text_data_json['key']

        if key == "age_rating":
            expression = text_data_json['expression']

            # Save User Settings Interaction
            user_settings = user_data_models.Settings.objects.get(user_key=self.user)
            user_settings.max_age_restriction = int(expression)
            user_settings.save()

        elif key == "bookmark":
            expression = text_data_json['expression']
            bookmark_key = text_data_json['bookmark_key']

            try:
                # Removes bookmark
                user_bookmark = data.BookmarkEntry.objects.get(movie_key=bookmark_key)
                user_bookmark.delete()
            except:
                # Creates bookmark
                bookmark = data.BookmarkEntry(user_key=self.user, movie_key=data.Movie.objects.get(pk=bookmark_key))
                bookmark.save()


    # def receive(self, text_data):
    #     text_data_json = json.loads(text_data)
    #     expression = text_data_json['expression']
        
    #     try:
    #         data = ""

    #         data += "[ Users ]\n"
    #         for item in get_user_model().objects.all():
    #             data += serialize('json', [item,]) + "\n"

    #         data += "\n[ Settings ]\n"
    #         for item in models.Settings.objects.all():
    #             data += serialize('json', [item,]) + "\n"

    #         data += "\n[ Movies ]\n"
    #         for item in models.Movie.objects.all():
    #             data += serialize('json', [item,]) + "\n"

    #         data += "\n[ Genres ]\n"
    #         for item in models.Genre.objects.all():
    #             data += serialize('json', [item,]) + "\n"

    #         data += "\n[ Actors ]\n"
    #         for item in models.Actor.objects.all():
    #             data += serialize('json', [item,]) + "\n"

    #         data += "\n[ Movie Actor Entries ]\n"
    #         for item in models.MovieActorEntry.objects.all():
    #             data += serialize('json', [item,]) + "\n"

    #         data += "\n[ Movie Genre Entries ]\n"
    #         for item in models.MovieGenreEntry.objects.all():
    #             data += serialize('json', [item,]) + "\n"

    #         data += "\n[ Watch Entries ]\n"
    #         for item in models.WatchEntry.objects.all():
    #             data += serialize('json', [item,]) + "\n"

    #         data += "\n[ Bookmark Entries ]\n"
    #         for item in models.BookmarkEntry.objects.all():
    #             data += serialize('json', [item,]) + "\n"

    #     except Exception as e:
    #         print(e)

    #     self.send(text_data=json.dumps({
    #         "key": data,
    #     }))