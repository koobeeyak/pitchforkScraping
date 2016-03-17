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
    playlist_name = get_title(url)
    playlist_uri = create_and_return_playlist(user, playlist_name)
    song_dict = scrape_pitchfork(url)
    list_of_song_uris = get_list_of_song_uris(song_dict)
    print "Creating playlist with URI: " + playlist_uri
    add_song_to_playlist(user, list_of_song_uris, playlist_uri)

if __name__ == "__main__":
    main()
