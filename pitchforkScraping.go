package main

import (
	"fmt"
	"net/http"

	"strings"

	"golang.org/x/net/html"
)

const (
	HEADING = "Staff Lists:"
)

type entry struct {
	artist string
	song   string
}

func checkIfTheresNewline(s string) {
	for _, value := range s {
		switch value {
		case '\n':
			fmt.Print("theres a new line char")
		case '\t':
			fmt.Print("theres a tab line char")
		}
	}
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

	var artistFieldNext, songFieldNext, inTag bool = false, false, false // use it to check whether TextToken follows StartTagToken
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
			if artistFieldNext == false && currentToken.Data == "h1" { // heading 1 contains artist's name
				fmt.Println("Data: ", currentToken.Data)
				artistFieldNext = true // next pass should be a TextToken
			} else if artistFieldNext == true && currentToken.Data != "h2" { // next was true, but next pass isn't song name
				artistFieldNext = false
			}
		case html.EndTagToken:
			inTag = false
		case html.TextToken:
			currentToken := z.Token()
			if strings.HasPrefix(currentToken.String(), HEADING) {
				continue
			}
			if artistFieldNext == true && songFieldNext == false && inTag == true { // previous pass was StartTagToken h1
				fmt.Println("Artist:", currentToken)
				fmt.Println("Data: ", tag)
				songFieldNext = true
				checkIfTheresNewline(currentToken.String())
				//current := entry{}
				//current.artist =
			} else if artistFieldNext == true && songFieldNext == true && inTag == true {
				fmt.Println("Song: ", currentToken)
				fmt.Println("Data: ", tag)
				songFieldNext = false
			}
		}
	}

}

func main() {
	url := "http://pitchfork.com/features/staff-lists/9700-the-200-best-songs-of-the-1980s/"
	getArtistsAndSongs(url)
}
