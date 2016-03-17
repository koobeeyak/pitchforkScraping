import spotipy
import spotipy.util as util
import sys

#const
SEARCH_LIMIT = 50
PAGE_LIMIT = 15 # iterate through this many pages of search results
UPLOAD_LIMIT = 100 # Spotify API limits to 100 songs per request

def add_song_to_playlist(user, song_uri_list, playlist_id):
    token = util.prompt_for_user_token(user, scope='playlist-modify-public')
    if token:
        sp = spotipy.Spotify(token)
        while len(song_uri_list) > UPLOAD_LIMIT:
            sp.user_playlist_add_tracks(user, playlist_id, song_uri_list[0:100])
            song_uri_list = song_uri_list[100:]
        sp.user_playlist_add_tracks(user, playlist_id, song_uri_list)
    else:
        print "Can't get %s\'s token." % (user)

def create_and_return_playlist(user, playlist_name):
    token = util.prompt_for_user_token(user, scope='playlist-modify-public')
    if token:
        sp = spotipy.Spotify(token)
        sp.user_playlist_create(user, playlist_name, public=True)
        playlists = sp.user_playlists(user)
        for playlist in playlists['items']:
            # find the playlist that was just made
            if playlist['owner']['id'] == user and playlist['name'] == playlist_name:
                return playlist['uri']
        print "Couldn't find playlist %s." % playlist_name
    else:
        print "Can't get %s\'s token." % (user)

def get_artist_uri(artist):
    sp = spotipy.Spotify()
    results = sp.search(artist, limit=SEARCH_LIMIT, type='artist')
    items = results['artists']['items']
    if len(items) > 0:
        for i in items:
            if i['name'] == artist:
                return i['uri']
        # we still can't find the artist, try changing "Tyler, the Creator" to "Tyler, The Creator"
        new_name = artist.title()
        print new_name
        # if this made some kind of change, start the loop again
        if new_name != artist:
            for i in items:
                if i['name'] == new_name:
                    return i['uri']
    print "Couldn't find the artist \"%s\"." % artist

def get_artists_song_uri(artist_uri, name):
    sp = spotipy.Spotify()
    result = sp.search(name, limit=SEARCH_LIMIT, type='track')
    results = result['tracks']
    tracks = results['items']
    limit = 0
    while results['next'] and limit <= PAGE_LIMIT:  # iterate through pages of results
        result = sp.next(results)
        results = result['tracks']
        tracks.extend(results['items']) # add additional results
        limit += 1
    for i in tracks:
        song_uri = i['uri']
        for a in i['artists']:
            if a['uri'] == artist_uri:
                return song_uri
    print "Couldn't find the track \"%s\"." % name

def get_list_of_song_uris(song_dict):
    """
    Return list of song URIs to be passed into Spotipy method user_playlist_add_tracks()
    """
    list_of_song_uris = []
    for artist in song_dict:
        artist_uri = get_artist_uri(artist)
        song_uri = get_artists_song_uri(artist_uri, song_dict[artist])
        if song_uri == None:
            print "Couldn't find the song URI for %s: %s." % (artist, song_dict[artist])
        else:
            list_of_song_uris.append(song_uri)
    return list_of_song_uris

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print "Search for Song URI. Usage: \"Artist:Track\""
        sys.exit()
    else:
        args = sys.argv[1:]
        joined = " ".join(args)
        artist, song = joined.split(":")
        artist_uri = get_artist_uri(artist)
        song_uri = get_artists_song_uri(artist_uri, song)
        if song_uri:
            print song_uri
