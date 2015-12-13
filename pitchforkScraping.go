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

type entry struct {
	artist string
	song   string
}

func getArtistsAndSongs(url string) {
	resp, err := http.Get(url)
	// can we open it?
	if err != nil {
		fmt.Println(err)
		return
	}

	b := resp.Body
	// see https://godoc.org/golang.org/x/net/html
	z := html.NewTokenizer(b)
	defer resp.Body.Close()

	var inTag bool = false // use it to check whether TextToken follows StartTagToken
	var tag string
	//var entries []entry
	for {
		tt := z.Next()
		switch tt {
		case html.ErrorToken:
			fmt.Println(z.Err())
			return // exit loop
		case html.StartTagToken:
			inTag = true
			currentToken := z.Token()
			tag = currentToken.Data
		case html.EndTagToken:
			inTag = false
		case html.TextToken:
			currentToken := z.Token()
			if strings.HasPrefix(currentToken.String(), OPEN) { // the title of the article has an h1 tag
				continue
			} else if strings.HasPrefix(currentToken.String(), CLOSE) { // last lines of article with h1 tag
				break
			} else if tag == "h1" && inTag == true { // previous pass was StartTagToken h1
				fmt.Println("Artist:", currentToken)
				//current := entry{}
				//current.artist =
			} else if tag == "h2" && inTag == true {
				fmt.Println("Song: ", currentToken)
			}
		}
	}
}

func main() {
	url := "http://pitchfork.com/features/staff-lists/9700-the-200-best-songs-of-the-1980s/"
	getArtistsAndSongs(url)
}
