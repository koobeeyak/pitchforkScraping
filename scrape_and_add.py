from spot import *
from pitchfork_scraping import *

#const
UPLOAD_LIMIT = 100 # Spotify API limits to 100 songs per request.

def get_list_of_song_uris(d):
    """
    Return list of song uris to be passed into Spotipy method user_playlist_add_tracks()
    """
    l = []
    i = 0
    for k in d:
        if i < UPLOAD_LIMIT:
            artist_uri = get_artist_uri(k)
            song_uri = get_artists_song_uri(artist_uri,d[k])
            if song_uri == None:
                print "Couldn't find song for %s: %s." % (k, d[k])
            else:
                l.append(song_uri)
                i += 1
        else: # reached upload limit
            break
    return l

# TODO handle requests over 100 song limit
# TODO remove text in brackets from song title to improve matches

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print "Please enter Spotify user URI (only ID number is needed) and appropriate Pitchfork \"Best Of\" URL."
        print "Examples:"
        print "\"http://pitchfork.com/features/staff-lists/9765-the-100-best-tracks-of-2015/\""
        print "\"http://pitchfork.com/features/staff-lists/9700-the-200-best-songs-of-the-1980s/\""
        sys.exit()
    else:
        user = sys.argv[1]
        url = sys.argv[2]
    d = scrape_pitchfork(url)
    l = get_list_of_song_uris(d)
    playlist_name = get_title(url)
    playlist_uri = create_and_return_playlist(user,playlist_name)
    add_song_to_playlist(user,l,playlist_uri)
