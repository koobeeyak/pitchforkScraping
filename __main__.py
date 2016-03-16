from spotify_api import *
from pitchfork_scraping import *

# TODO handle requests over 100 song limit
# TODO remove text in brackets from song title to improve matches

def main():
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
    playlist_uri = create_and_return_playlist(user, playlist_name)
    add_song_to_playlist(user, l, playlist_uri)

if __name__ == "__main__":
    main()
