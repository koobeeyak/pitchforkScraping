from bs4 import BeautifulSoup
import requests, sys, urllib2, json

def get_soup(url):
	# need a User-Agent header to access page
	header = {
		'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36'
	}
	request = urllib2.Request(url, headers=header)
	page = urllib2.urlopen(request).read()
	soup = BeautifulSoup(page, "html.parser")
	return soup

def scrape_pitchfork(url):
	soup = get_soup(url)
	# there's a script in the html which pulls from json that's embedded right there on the page
	# once we isolate it, we can get all the artist and song information of the feature
	scripts = soup.find_all('script')
	# script starts with "window.App="
	start_of_json = "window.App="
	for script in scripts:
		if script.text.startswith(start_of_json):
			ignore_this = len(start_of_json)
			# get just the string of json, the -1 is for a semicolon at the end
			json_string = script.text[ignore_this:-1]
			pfork_json = json.loads(json_string)
	artists_and_songs = generate_dict_of_artists_and_songs(pfork_json)
	return artists_and_songs

def generate_dict_of_artists_and_songs(pfork_json):
	song_dict = {}
	features = pfork_json["context"]["dispatcher"]["stores"]["FeaturesStore"]
	feature_number = features["itemPages"][0]
	list_of_entries = features["items"][str(feature_number)]["body"]["en"]
	# list_of_entries is a list of lists of entries, 10 per page
	for page in list_of_entries:
		for entry in page:
			# information about the article is also kept here, avoid it
			if "custom_artist_display" not in entry["data"]:
				continue
			# we're usually looking for custom_artist_display field, but sometimes it's nested a little deeper
			elif entry["data"]["custom_artist_display"] == "":
				artist = entry["data"]["track"]["artists"][0]["display_name"]
				song = entry["data"]["track"]["title"].replace('"','')
			else:
				artist = entry["data"]["custom_artist_display"]
				song = entry["data"]["custom_track_name"].replace('"','')
			# e.g. can't find "Get Lucky [ft. Pharrell]", we only want "Get Lucky"
			if "[" in song:
				song = song.split("[")[0][:-1]
			song_dict[artist] = song
	return song_dict

def get_title(url):
	"""
	Scrape the title of the feature. This'll be used to name new playlist.
	"""
	soup = get_soup(url)
	h = soup.head
	title = h.find('title').text
	return title

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print "Enter base Pitchfork URL of \"Best Of\" feature to get list of artists and songs."
        print "Examples:"
        print "\"http://pitchfork.com/features/staff-lists/9700-the-200-best-songs-of-the-1980s/\""
        print "\"http://pitchfork.com/features/staff-lists/9765-the-100-best-tracks-of-2015/\""
        sys.exit()
    url = sys.argv[1]
    print get_title(url)
    songs = scrape_pitchfork(url)
    for artist in songs:
        print "Artist:", artist
        print "Song:", songs[artist]
