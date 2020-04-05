from datetime import datetime, timedelta
import requests, json
import time






track_ids = ['not here','4nSixmLLG59wyNkWDdL2uz', '5DagPSBZBY8AQ1ltpjr657', '1YAXlDiZCzF0BytvSiMxAF', '4k5hllgaGDKTDLG75YQq5X', '1dwfgrQ8vkmd3XYj8I7vYg', '3w6tAfkEExoLtlRqRhJA62', '658mr6VhcCKsUHoYV0JHsm', '41M18KwdxRCM8XqUof5zrL', '3gCF6JWBIyUxkKSA5GjCPR', '3WBxDJUNmanW53LVjNNkog', '0Tf9YHGzqKjrobap4L7M7z', '1cjCC05mETvLRWx3nDSPOY', '3dpqUjzdQ5nYDZJcVsdMg4', '3HxJT0JTRM3iZtRTTMqZtN', '1oHjsosZQW7J5vYEmDy3gJ', '5z5sA9z9PqN0pciTUnmkki', '7FbdXyyZOknEfjHxGmdQVp', '766BK7fV99BunraS0eb4CB', '16ZjWGIWEsSzCkV7LiEMVk', '3IHLWOub1HjwgV0JNwltGI', '5abRxzBqR8si654aef0DlS', '5OVCHoprm27fpExyxIknmi', '4BTzynsNHMyJCRPQs7RYyF', '64YtawRweU7QdwoIjsdlTL', '4bje319NyF9c2FWBIXet4V', '1BpXUxcpOk9Dh0acKAxfpN', '6W1JiP4OegWT19BGQupD0X', '2gYozgMeOj20xdVY6HvzKx', '1cexVs6lRgNpqHgugh7AUY', '5sBfFvXATlo46CVmjegzBi']
playlist_track_ids = ['4nSixmLLG59wyNkWDdL2uz', '5DagPSBZBY8AQ1ltpjr657', '1YAXlDiZCzF0BytvSiMxAF', '4k5hllgaGDKTDLG75YQq5X', '1dwfgrQ8vkmd3XYj8I7vYg', '3w6tAfkEExoLtlRqRhJA62', '658mr6VhcCKsUHoYV0JHsm', '41M18KwdxRCM8XqUof5zrL', '3gCF6JWBIyUxkKSA5GjCPR', '3WBxDJUNmanW53LVjNNkog', '0Tf9YHGzqKjrobap4L7M7z', '1cjCC05mETvLRWx3nDSPOY', '3dpqUjzdQ5nYDZJcVsdMg4', '3HxJT0JTRM3iZtRTTMqZtN', '1oHjsosZQW7J5vYEmDy3gJ', '5z5sA9z9PqN0pciTUnmkki', '7FbdXyyZOknEfjHxGmdQVp', '766BK7fV99BunraS0eb4CB', '16ZjWGIWEsSzCkV7LiEMVk', '3IHLWOub1HjwgV0JNwltGI', '5abRxzBqR8si654aef0DlS', '5OVCHoprm27fpExyxIknmi', '4BTzynsNHMyJCRPQs7RYyF', '64YtawRweU7QdwoIjsdlTL', '4bje319NyF9c2FWBIXet4V', '1BpXUxcpOk9Dh0acKAxfpN', '6W1JiP4OegWT19BGQupD0X', '2gYozgMeOj20xdVY6HvzKx', '1cexVs6lRgNpqHgugh7AUY', '5sBfFvXATlo46CVmjegzBi', '5DagPSBZBY8AQ1ltpjr657', '4k5hllgaGDKTDLG75YQq5X', '3w6tAfkEExoLtlRqRhJA62', '41M18KwdxRCM8XqUof5zrL', '3WBxDJUNmanW53LVjNNkog', '1cjCC05mETvLRWx3nDSPOY', '3HxJT0JTRM3iZtRTTMqZtN', '5z5sA9z9PqN0pciTUnmkki', '766BK7fV99BunraS0eb4CB', '3IHLWOub1HjwgV0JNwltGI', '5OVCHoprm27fpExyxIknmi', '64YtawRweU7QdwoIjsdlTL', '1BpXUxcpOk9Dh0acKAxfpN', '2gYozgMeOj20xdVY6HvzKx', '5sBfFvXATlo46CVmjegzBi', '5DagPSBZBY8AQ1ltpjr657', '4k5hllgaGDKTDLG75YQq5X', '3w6tAfkEExoLtlRqRhJA62', '41M18KwdxRCM8XqUof5zrL', '3WBxDJUNmanW53LVjNNkog', '1cjCC05mETvLRWx3nDSPOY', '3HxJT0JTRM3iZtRTTMqZtN', '5z5sA9z9PqN0pciTUnmkki', '766BK7fV99BunraS0eb4CB', '3IHLWOub1HjwgV0JNwltGI', '5OVCHoprm27fpExyxIknmi', '64YtawRweU7QdwoIjsdlTL', '1BpXUxcpOk9Dh0acKAxfpN', '2gYozgMeOj20xdVY6HvzKx', '5sBfFvXATlo46CVmjegzBi']

remaining_tracks = []

for track in track_ids:
    if track not in playlist_track_ids:
        remaining_tracks.append(track)

print(remaining_tracks)




