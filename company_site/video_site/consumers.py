import json
from channels.generic.websocket import WebsocketConsumer

from .modules.UserAccounts import UserFunctions as uf
from .modules.Bookmarks import BookmarkFunctions as bf
from .modules.WatchHistory import WatchHistoryFunctions as whf

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
            user_settings = uf.getUserSettingsByUser(self.user)
            user_settings.max_age_restriction = int(expression)
            user_settings.save()

        elif key == "bookmark":
            expression = text_data_json['expression']
            bookmark_key = text_data_json['bookmark_key']

            try:
                # Removes bookmark
                bf.deleteBookmarkEntry(self.user, bookmark_key)
            except:
                # Creates bookmark
                bf.createBookmarkEntry(self.user, bookmark_key)

        elif key == "video_time":

            if self.user.is_authenticated:
                time = int(text_data_json['current_time'])
                movieId = int(text_data_json['movie_id'])

                try:
                    # Update current watch entry
                    whf.updateWatchEntry(self.user, movieId, time)
                except:
                    # Create new watch entry
                    whf.createWatchEntry(self.user, movieId, time)
