import spotipy
import spotipy.util as util
import sys


#const
SEARCH_LIMIT = 50
PAGE_LIMIT = 15


def find_songs(user):
    token = util.prompt_for_user_token(user)
    if token:
        print "\nGot token."
        sp = spotipy.Spotify(token)
        songs = sp.current_user_saved_tracks(limit=10)
        print songs
        pass
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
        tracks.extend(results['items'])
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
    if len(sys.argv) == 1:
        print "Usage: \"Artist: Track\""
        sys.exit()
    else:
        args = sys.argv[1:]
        joined = " ".join(args)
        artist, song = joined.split(":")
        artist_uri = get_artist_uri(artist)
        song_uri = get_artists_song_uri(artist_uri, song)
        print song_uri
