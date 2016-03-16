from bs4 import BeautifulSoup
import requests, sys

def scrape_page(response):
    """
    Returns dict of key: artist, value: song
    """
    soup = BeautifulSoup(response.text, "html.parser")
    d = {}
    for entry in soup.find_all(class_ = "title"):
        artist = entry.find('h1').text
        song = entry.find('h2').text.strip().replace(u'\u201c','').replace(u'\u201d','') # remove whitespace and quotation marks
        d[artist] = song
    return d

def scrape_pitchfork(url):
    """
    Scrapes base url, then attempts to crawl remaining pages of feature
    """
    if url[-1] != "/":
        url += "/"
    url += "1/"
    i = 1
    response = requests.get(url)
    d = {}
    while response.status_code != 404: # keep getting next page of feature until 404
        d.update(scrape_page(response))
        length = len(str(i)) + 1 # this is how much of url string will be replaced e.g. 2 for one digit, 3 for two digits
        i += 1
        url = url[:-length] + str(i) + "/" # crawling the next page
        response = requests.get(url)
    return d

def get_title(url):
    """
    Returns title of feature. This can be used to name playlist.
    """
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    h = soup.head
    title = h.find('title').text
    return title

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
