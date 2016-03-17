from bs4 import BeautifulSoup
import requests, sys, urllib2, json, pprint

def get_soup(url):
	header = {
		'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36'
	}
	request = urllib2.Request(url, headers=header)
	page = urllib2.urlopen(request).read()
	soup = BeautifulSoup(page, "html.parser")
	return soup

def scrape_pitchfork(url):
        soup = get_soup(url)
	scripts = soup.find_all('script')
	start_of_json = "window.App="
	for script in scripts:
		if script.text.startswith(start_of_json):
			ignore_this = len(start_of_json)
			# get just the string of json, the -1 is for a semicolon at the end
			json_string = script.text[ignore_this:-1]
			pfork_json = json.loads(json_string)
	artists_and_songs = generate_dict_of_artists_and_songs(pfork_json)
	return artists_and_songs

def get_title(url):
	soup = get_soup(url)
	h = soup.head
	title = h.find('title').text
	return title

def generate_dict_of_artists_and_songs(pfork_json):
	d = {}
	features = pfork_json["context"]["dispatcher"]["stores"]["FeaturesStore"]
	feature_number = features["itemPages"][0]
	list_of_entries = features["items"][str(feature_number)]["body"]["en"]
	# list_of_entries is a list of lists of entries, 10 per page
	for page in list_of_entries:
		for entry in page:
			#pprint.pprint(entry["data"])
			if "custom_artist_display" not in entry["data"]:
				continue
			artist = entry["data"]["custom_artist_display"]
			song = entry["data"]["custom_track_name"].replace('"','')
			d[artist] = song
	return d

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print "Enter base Pitchfork URL."
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
