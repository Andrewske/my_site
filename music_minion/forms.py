from django import forms

class SoundCloudPlaylistForm(forms.Form):
    playlist = forms.CharField()

    