from sclib import SoundcloudAPI, Track, Playlist

api = SoundcloudAPI()

class AddPlaylist(url):
    playlist = api.resolve(url)
    assert type(playlist) is Playlist

    playlist_tracks = {}

    for track in playlists.tracks:
        playlist_tracks['Name'] = track.name
        playlist_tracks['Artist'] = track.artist 
    
    return playlist_tracks