import spotipy
import spotipy.util as util
import sys


#const
SEARCH_LIMIT = 50
PAGE_LIMIT = 15 # iterate through this number of page results


def find_songs(user):
    token = util.prompt_for_user_token(user,scope='user-library-read')
    if token:
        sp = spotipy.Spotify(token)
        songs = sp.current_user_saved_tracks(limit=10)
        print songs
    else:
        print "Can't get %s\'s token." % (user)

def add_song_to_playlist(user,song_uri,playlist_id):
    token = util.prompt_for_user_token(user,scope='playlist-modify-public')
    if token:
        sp = spotipy.Spotify(token)
        sp.user_playlist_add_tracks(user,playlist_id,song_uri)


def get_artist_uri(artist):
    sp = spotipy.Spotify()
    results = sp.search(artist, limit=SEARCH_LIMIT, type='artist')
    items = results['artists']['items']
    if len(items) > 0:
        for i in items:
            if i['name'] == artist:
                return i['uri']
    print "Couldn't find artist."


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
    print "Couldn't find the track"


if __name__ == "__main__":
    # TODO apparantly artist name is case sensitive
    # TODO leading space in songname won't work
    if len(sys.argv) < 2:
        print "Usage: \"Artist:Track\""
        sys.exit()
    else:
        args = sys.argv[1:]
        joined = " ".join(args)
        artist, song = joined.split(":")
        artist_uri = get_artist_uri(artist)
        song_uri = get_artists_song_uri(artist_uri, song)
    add_song_to_playlist("1223788894",[song_uri],"spotify:user:1223788894:playlist:1ckhN9MgnC7JtULrZOYCOM")
