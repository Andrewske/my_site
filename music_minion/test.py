from datetime import datetime, timedelta
import requests, json
import time

import spotify


spotify_track_data = spotify.SpotifyTrackData()
spotify_user_data = spotify.SpotifyUserData()

try:
    from urllib.parse import urlencode
except ImportError:
    from urllib import urlencode
import urllib

user_id = 'kevinbigfoot'
access_token = 'BQAWuM_WbzXJ5WSxCXO-pka9T-8-hVsHSPJblRKy686Zs6wA2peAZVvnAlPT_ibN50RPNiFJ8m-dZV7pIIKBdk5nRSQCaybVsfURoi1qu-t3JqclE_XCwxVdgBhdSceQFmiYaKHToLWJxBRJgL_as-Vp62EJe5YMO05cO1IWsu-yrmEB6T8XRuuE1qjQO5dM6PCPK4yi0PICxkcvMM0QaWtvuF2X6vI-w-s1GgwD6LJ8mxFIbJ3-D2aTud44PRA'

def dw_task_for_user():
    dw_task_users = SpotifyUser.objects.filter(dw_monthly = True).filter(dw_yearly = True)
    return dw_task_users


print(dw_task_for_user())

def none():
    for user in dw_task_users:
        time_since_updated = datetime.now() - user.dw_updated_at
        if time_since_updated.total_seconds() >= 60:
            if user.dw_monthly:
                SpotifyTrackData().discover_weekly_playlist(user.user_id, user.access_token, 'monthly')
                user.dw_updated_at = datetime.Now()
                user.save()
            if user.dw_yearly:
                SpotifyTrackData().discover_weekly_playlist(user.user_id, user.access_token, 'yearly')
                user.dw_updated_at = datetime.Now()
                user.save()
            messages.success(request, f'Background Test Complete.')
        else:
            messages.warning(request, f'No need to update')
        


playlist_url = 'https://open.spotify.com/playlist/66esoX3teBQdi0Z44Q12Qj?si=suhoNLyITW2Vu2Jb5iIgOg'
playlist_id = '66esoX3teBQdi0Z44Q12Qj'
tracks = ["4JpKVNYnVcJ8tuMKjAj50A","2NRANZE9UCmPAS5XVbXL00","24JygzOLM0EmRQeGtFcIcG"]
target_values = {'target_tempo':150}
min_values = {'min_tempo':145}
max_values = {'max_tempo':155}

#print(get_recommendations(access_token, limit=5, tracks=tracks, target_values=target_values, min_values=min_values, max_values=max_values))









