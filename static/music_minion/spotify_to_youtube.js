console.log("Loaded This JS!")

// $(document).ready(function(event){
//     //After the document loads we get the users spotify playlists
//     getSpotifyPlaylists();


//     /*
//         On click of the Get Tracks button we call getTracks() which:
//         1. Gets Spotify Tracks
//         2. Creates a card for the first track
//         3. Searches Youtube for the first track
//         4. C
//     */
//     $(document).on('click', '#get-playlist-tracks', function(event){
//         event.preventDefault();
//         let playlist_id =$('#playlist-dropdown').val();
//         //timeFunction(spotify_playlist_call(playlist_id));
//         timeFunction(getTracks(playlist_id));
        
//     });

//     $(document).on('click', '#next-spotify', function(event){
//         event.preventDefault();
//         loadTrack('next', 'spotify');
//     });

//     $(document).on('click', '#previous-spotify', function(event){
//         event.preventDefault();
//         loadTrack('previous', 'spotify');
//     });

//     $(document).on('click', '#next-youtube', function(event){
//         event.preventDefault();
//         loadTrack('next', 'youtube');
//     });

//     $(document).on('click', '#previous-youtube', function(event){
//         event.preventDefault();
//         loadTrack('previous', 'youtube');
//     });

//     $(document).on('click', '#confirm', function(event){
//         event.preventDefault();
//         //confirm this pairing
//         let spotifyTrack = document.getElementById("spotify-card-data").firstElementChild.id.split("-")[1]
//         let youtubeTrack = document.getElementById("youtube-card-data").firstElementChild.id.split("-")[1]
//         let state = confirmTracks(spotifyTrack, youtubeTrack);
//         if (state == 'finished') {
//             finish();
//         }
//     });

//     $(document).on('click', '#reject', function(event){
//         event.preventDefault();
//         //reject this pairing
//         let spotifyTrack = document.getElementById("spotify-card-data").firstElementChild.id.split("-")[1]
//         let youtubeTrack = document.getElementById("youtube-card-data").firstElementChild.id.split("-")[1]
//         let state = rejectTracks(spotifyTrack, youtubeTrack);
//         if (state == 'finished') {
//             finish();
//         }
//     });

//     $(document).on('click', '#show-confirmed', function(event){
//         event.preventDefault();
//         showTracks('confirmed');
//     });

//     $(document).on('click', '#show-rejected', function(event){
//         event.preventDefault();
//         showTracks('rejected');
//     });

//     $(document).on('click', '#save-playlist', function(event){
//         event.preventDefault();
//         savePlaylist();
        
//     });
// });


// /*
//     Main Functions
// */

// async function getTracks(playlist_id) {
//     try {
//         await timeFunction(spotifyPlaylistCall(playlist_id, cleanTracks))

//         /*
//         for(var i = 0; i < spotifyTracks.length; i++) {
//             let track = await getYouTubeTracks(spotifyTracks[i],i);
//             youtubeTracks[track[0]] = track[1];
//         };
//         */
        

//         createTrackCard(spotifyTracks[0], 'spotify');
        
//         await timeFunction(searchYoutube(spotifyTracks[0], cleanTracks))
//         currentYoutubeTrack = youtubeTracks[currentSpotifyTrack];

//         createTrackCard(currentYoutubeTrack[0], 'youtube');

//     } catch(error) {
//         console.error("error", error);
//     };
// };

// /*
//     Spotify Calls
// */

// //Function to get a users spotify playlists
// function getSpotifyPlaylists() {
//     $.ajax ({
//         type:'GET',
//         url: 'https://api.spotify.com/v1/users/'+username+'/playlists',
//         dataType:'json',
//         data: {'limit':50},
//         beforeSend: function (xhr) {
//             xhr.setRequestHeader ("Authorization", "Bearer " + spotify_token);
//         },
        
//         success: function(data) {
//             console.log(data['items']);
//             buildDropdown(
//                 data['items'],
//                 $('#playlist-dropdown'),
//                 'Select a playlist',
//             );
//         },
//         error: function(rs, e){
//             console.log(rs.responseText)
//         }
//     })
// };

// //Function to get the tracks from a Spotify Playlist
// async function spotifyGetPlaylistTracks(playlist_id, cleanTracks) {
//     await $.ajax({
//         type:'GET',
//         url:'https://api.spotify.com/v1/playlists/' + playlist_id + '/tracks',
//         data: {'market':'from_token'},
//         dataType:'json',
//         beforeSend: function (xhr) {
//             xhr.setRequestHeader ("Authorization", "Bearer " + spotify_token);
//         },
//         success: function(data) {
//             //Before returning data we clean the response
//             cleanTracks(data, 'spotify')
//         },
//         error: function(rs, e){
//             console.log(rs.responseText)
//         }
//     });
// };


// /* Youtube Calls*/

// //Function to search Youtube using name and artists from the Spotify track
// async function searchYoutube(track, cleanTracks) {
//     let trackId = track['id'];
//     let trackName = track['name'];
//     let trackArtists = track['artists'];
//     await $.ajax({
//         type:'GET',
//         url:'https://www.googleapis.com/youtube/v3/search',
//         data : {
//                 'part':'snippet',
//                 'maxResults':5,
//                 'order': 'relevance', //date, rating, relevance, title, videoCount, viewCount
//                 'q':trackArtists + ' - ' + trackName,
//                 'type':'video', //channel, playlist, video
//                 //'videoCategoryId': None, Maybe use music?
//             },
//         dataType:'json',
//         beforeSend: function (xhr) {
//             xhr.setRequestHeader ("Authorization", "Bearer " + youtube_token);
//         },
//         success: function(data) {
//             //Before returning data we clean the response
//             cleanTracks(data,'youtube',trackId)
//         },
//         error: function(rs, e){
//             console.log(rs.responseText)

//         }
//     });
// };





// /*
//     MISC Functions
// */

// //Function for timing other functions
// async function timeFunction(callback) {
//     t0 = performance.now();
//     let results = await callback;
//     t1 = performance.now();
//     console.log("Get tracks took " + (t1-t0) + "seconds");
//     return results
// };

// //Function to build the playlist dropdown menu from users Spotify PLaylists
// function buildDropdown(result, dropdown, emptyMessage) {
//     $('#playlist-dropdown').html();
//     dropdown.append('<option value="">' + emptyMessage + '</option>');

//     if(result != '') {
//         $.each(result, function(k,v) {
//             dropdown.append('<option value="' + v.id + '">' + v.name + '</option>');
//         });
//     }
// }

// //Function to clean the track response from Spotify and Youtube calls
// function cleanTracks(data, platform, trackId=null) {
//     if(platform=='spotify') {
//         let newTracks = []
//         data['items'].forEach(track => {
//             let artists = track.track.map((artists) => artists.name)
//             //let artists = [];
//             //track.track.artists.forEach(artist => {
//             //    artists.push(artist.name);
//             //    });
//             newTracks.push({
//                 'id': track.track.id,
//                 'name': track.track.name,
//                 'href': track.track.href,
//                 'img_url': track.track.album.images[0].url,
//                 'artists': artists.join(', '),
//                 });
//             });
//         spotifyTracks = newTracks;
//     } else if(platform=='youtube') {
//         let newTracks = []
//         data['items'].forEach(track => {
//             newTracks.push({
//                 'id':track['id']['videoId'],
//                 'name':track['snippet']['title'],
//                 'artists':track['snippet']['channelTitle'],
//                 'img_url':track['snippet']['thumbnails']['high']['url']
//             });
//         youtubeTracks[trackId] = newTracks
//         })
//     }
// };