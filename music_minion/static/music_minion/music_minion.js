
var spotifyTracks = null;
var youtubeTracks = null;
const userId = '{{ user.id }}';

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
    const trackCard = `
        <div id="${track.id}" class="${platform}-track-card">
            <img class="track-card-img" src="${track.img_url}" alt="${track.img_url}">
            <div class="card-body">
                <h3 class="card-title">${track.name}</h3>
                <p class="card-text">${track.artists}</p>
                <p class="card-text">${track.duration}</p>
            </div>
        </div>
        `;
    let divId = track['id'];
    let row = document.getElementById(divId);
    row.innerHTML += row.innerHTML + trackCard;
};



async function getTracks() {
    try {
            spotifyTracks = await getSpotifyTracks();

            getYouTubeTracks();
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
                    createDiv(data[i], createTrackCard)
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

function getYouTubeTracks() {
    if(spotifyTracks !== null){
        let tracks = []
        for(var i = 0; i < spotifyTracks.length; i++){
            let trackId = spotifyTracks[i]['id'];
            let trackName = spotifyTracks[i]['name'];
            let trackArtists = spotifyTracks[i]['artists'];
            var youtubeRequest = $.ajax({
                type:"POST",
                url:'{% url "get_youtube_tracks" %}',
                data: {'user_id':userId, 'track_id':trackId, 'artists':trackArtists, 'name':trackName, 'csrfmiddlewaretoken': '{{ csrf_token }}'},
                dataType:'json',
                success: function(data){
                    if(data){
                        tracks.push(data)
                        for(var i = 0; i < data.length; i++){
                            createTrackCard(data[i], 'youtube');
                        };
                        return tracks;    
                    } else {
                        console.log('No Data');
                    }},    
                error: function(rs, e){
                    console.log(rs.responseText);
                }
            });
        };
    } else {
        console.log("There are no spotify tracks")
    }
};