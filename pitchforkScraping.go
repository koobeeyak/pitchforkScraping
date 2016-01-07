// NOTE: this is currently NOT being used as part of scrape_and_app.py
// Keeping it here for reference of first attempt.
package main

import (
	"fmt"
	"net/http"

	"strings"

	"golang.org/x/net/html"
)

const (
	OPEN  = "Staff Lists:"
	CLOSE = "Soundplay"
)

type Entry struct {
	artist string
	song   string
}

type Entries []Entry

func getArtistsAndSongs(url string) (entries Entries) {
	// init variables
	var inTag bool = false
	var tag string
	e := Entry{}

	// try to open page
	resp, err := http.Get(url)
	if err != nil {
		fmt.Println("Couldn't open page: ", err)
		return
	}

	// init tokenizer
	b := resp.Body
	defer b.Close()
	z := html.NewTokenizer(b)

	for {
		tt := z.Next()
		switch tt {
		case html.ErrorToken:
			fmt.Println("Error, exited early.") // should return before hitting EOF here
			return
		case html.StartTagToken:
			inTag = true
			tag = z.Token().Data
		case html.EndTagToken:
			inTag = false
		case html.TextToken:
			currentToken := z.Token()
			if strings.HasPrefix(currentToken.String(), OPEN) { // the title of the article has an h1 tag
				continue
			} else if strings.HasPrefix(currentToken.String(), CLOSE) { // last lines of article with h1 tag
				return
			} else if tag == "h1" && inTag == true { // h1 tag indicates artist
				e.artist = currentToken.String()
			} else if tag == "h2" && inTag == true { // h2 tag indicates song
				e.song = currentToken.String()
				entries = append(entries, e)
				e = Entry{}
			}
		}
	}
}

func main() {
	url := "http://pitchfork.com/features/staff-lists/9700-the-200-best-songs-of-the-1980s/"
	final := getArtistsAndSongs(url)
	fmt.Println(final)
}
