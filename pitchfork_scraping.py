from bs4 import BeautifulSoup
import requests

def scrape_pitchfork(url):
    """
    Takes URL, returns dict of key: artist, value: song
    """
    response = requests.get(url)
    soup = BeautifulSoup(response.text,"html.parser")
    d = {}
    for entry in soup.find_all(class_ = "title"):
        artist = entry.find('h1').text
        song = entry.find('h2').text.strip()[1:-1] # remove whitespace and quotation marks
        d[artist] = song
    return d


if __name__ == "__main__":
    url = "http://pitchfork.com/features/staff-lists/9700-the-200-best-songs-of-the-1980s/"
    # TODO scrape all pages of feature
    d = scrape_pitchfork(url)
    for x in d:
        print "Artist:",x
        print "Song:",d[x]