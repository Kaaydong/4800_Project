import json
from channels.generic.websocket import WebsocketConsumer
import datetime

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

        elif key == "video_time":

            if self.user.is_authenticated:
                time = int(text_data_json['current_time'])
                movieId = int(text_data_json['movie_id'])

                movie = data.Movie.objects.get(pk=movieId)

                try:
                    # Update current watch entry
                    user_watch_entry = data.WatchEntry.objects.get(user_key=self.user, movie_key=movie)
                    user_watch_entry.watch_progress = time
                    user_watch_entry.updated_at = datetime.date.today()
                    user_watch_entry.save()
                
                except:
                    # Create new watch entry
                    user_watch_entry = data.WatchEntry(user_key=self.user, movie_key=movie, watch_progress=time, updated_at=datetime.date.today())
                    user_watch_entry.save()
