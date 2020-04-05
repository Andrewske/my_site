from django.apps import AppConfig


class MusicMinionConfig(AppConfig):
    name = 'music_minion'

    def ready(self):
        from music_minion import repeat
        print("Ready Captain")
        #repeat.start()
        
