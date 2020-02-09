from django import forms


class SoundCloudPlaylistForm(forms.Form):
    playlist = forms.CharField()


class SpotifySearchForm(forms.Form):

    def __init__(self, *args, **kwargs):
        self.genres_list = kwargs.pop('genres')
        super(SpotifySearchForm, self).__init__(*args,**kwargs)

        types = (
            ('track','track'),
            ('album','album'),
            ('artist', 'artist'),
            ('playlist','playlist'),
        )
        genres = [(genre, genre) for genre in self.genres_list]
        genres.insert(0, ('none', 'Choose Genre...'))
        self.fields['search_type'] = forms.ChoiceField(choices=types, initial={'track':'track'})
        self.fields['genre'] = forms.ChoiceField(choices=genres, required=False)
        self.fields['query'] = forms.CharField()

    