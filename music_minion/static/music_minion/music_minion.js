<script>
    var spotifyTracks = null;
    var youtubeTracks = {};

    var currentSpotifyTrack = null;
    var currentYoutubeTrack = null;
    

    $(document).ready(function(event){
        
        //Get Spotify playlist tracks
        $(document).on('click', '#get_playlist_tracks', function(event){
            event.preventDefault();
            getTracks()
        });

    });


    function createDiv(data, callback){
        $(".track-list").append(`<div id="${data['id']}" class="row"></div>`);
        callback(data, 'spotify');
    };

    function createTrackCard(track, platform){
        console.log("creating card for " + platform)
        let trackCard = `
            <div id="${platform}-${track.id}" class="${platform}-track-card">
                <img class="track-card-img" src="${track.img_url}" alt="${track.img_url}">
                <div class="card-body">
                    <h3 class="card-title">${track.name}</h3>
                    <p class="card-text">${track.artists}</p>
                    <p class="card-text">${track.duration}</p>
                </div>
            </div>
            `;
        let divId = platform + "-card-data";
        let row = document.getElementById(divId);
        row.innerHTML = trackCard;
    };



    async function getTracks() {
        try {
            spotifyTracks = await getSpotifyTracks();

            for(var i = 0; i < spotifyTracks.length; i++) {
                let track = await getYouTubeTracks(spotifyTracks[i],i);
                youtubeTracks[track[0]] = track[1];
            };
            
            currentSpotifyTrack = spotifyTracks[0];
            currentYoutubeTrack = youtubeTracks[currentSpotifyTrack][0];
            console.log(currentSpotifyTrack);
            console.log[currentYoutubeTrack];
            createTrackCard(currentSpotifyTrack, 'spotify');
            createTrackCard(currentYoutubeTrack, 'youtube');

        } catch(error) {
            console.error("error", error);
        };
    };

    async function getSpotifyTracks(){
        //remove any tracks loaded
        let spotify_tracks = document.getElementById('spotify-tracks');
        spotify_tracks.innerHTML = '';

        var form = document.playlist;
        let playlistId = form.playlist.value;
        let use = 'list';
        let tracks = null
        let userId = '{{ user.id }}';

        //Make an Ajax request to the Get Playlist tracks URL
        await $.ajax({
            type:'POST',
            url: '{% url "get_playlist_tracks" %}',
            data: {'user_id':userId, 'playlist_id':playlistId, 'csrfmiddlewaretoken': '{{ csrf_token }}', 'use': use},
            dataType:'json',
            success: function(data){
                console.log("We got some tracks")
                //Take the resonse and add a Card for each Spotify track
                if(data){
                    data.forEach((track) => {
                        createTrackCard(track, 'spotify');
                    });
                    tracks = data
                } else {
                    console.log('No tracks');
                }}, 
            error: function(rs, e){
                console.log(rs.responseText);
            }
        });
        return tracks
    };

    async function getYouTubeTracks(track, i) {
        let trackId = track['id'];
        let trackName = track['name'];
        let trackArtists = track['artists'];
        let userId = '{{ user.id }}';
        let trackData = await $.ajax({
            type:"POST",
            url:'{% url "get_youtube_tracks" %}',
            data: {'user_id':userId, 'track_id':trackId, 'artists':trackArtists, 'name':trackName, 'csrfmiddlewaretoken': '{{ csrf_token }}'},
            dataType:'json',
            success: function(data) {
                createTrackCard(data[i], 'youtube');
                return data
            },
            error: function(rs, e){
                console.log(rs.responseText)
                return "Nada"
            }
        });
        let returnValue = [trackId, trackData]
        console.log(returnValue)
        return returnValue
    };

</script>