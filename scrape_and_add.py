from spot import *
from pitchfork_scraping import *

def get_list_of_song_uris(d):
    l = []
    for k in d:
        artist_uri = get_artist_uri(k)
        song_uri = get_artists_song_uri(artist_uri,d[k])
        if song_uri == None:
            print "Couldn't find song for %s: %s." % (k, d[k])
        else:
            l.append(song_uri)
    return l


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print "Please enter Spotify user URI and playlist URI as arguments"
        sys.exit()
    else:
        user = sys.argv[1]
        playlist = sys.argv[2]
        print user, playlist
    url = "http://pitchfork.com/features/staff-lists/9700-the-200-best-songs-of-the-1980s/"
    d = scrape_pitchfork(url)
    l = get_list_of_song_uris(d)
    add_song_to_playlist(user,l,playlist)