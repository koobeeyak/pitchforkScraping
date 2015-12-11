package main

import (
	"fmt"
	"github.com/tucobenedicto/util"
	"golang.org/x/net/html"
	"net/http"
	"os"
)

func main() {
	// check if we have any arguments
	// see github.com/tucobenedicto/util
	if util.NoArguments() {
		fmt.Println("No arguments entered.")
		return
	}
	// take first arg as URL for now
	url := os.Args[1]
	resp, err := http.Get(url)
	// can we open it?
	if err != nil {
		fmt.Println(err)
		return
	}

	b := resp.Body
	// see https://godoc.org/golang.org/x/net/html
	z := html.NewTokenizer(b)

	var songInfoFieldsNext bool = false // use it to check whether TextToken follows StartTagToken
	type entry struct {
		artist string
		song   string
	}
	//entries := make([]entry, 2)
	for {
		tt := z.Next()
		//fmt.Println("tt: ",tt) // prints type of token
		//fmt.Println(z.Token())
		switch tt {
		case html.ErrorToken:
			fmt.Println(z.Err())
			return // exit loop
		case html.StartTagToken:
			currentToken := z.Token()
			if songInfoFieldsNext == false && currentToken.Data == "h1" { // heading 1 contains artist's name
				songInfoFieldsNext = true // next pass should be a TextToken
				continue
			} else if songInfoFieldsNext == true && currentToken.Data != "h2" { // next was true, but next pass isn't song name
				songInfoFieldsNext = false
			}
		case html.TextToken:
			currentToken := z.Token()
			if songInfoFieldsNext == true { // previous pass was StartTagToken h1
				if currentToken.Data != "" {
					fmt.Println("Printing artist: ", currentToken)
				}
			}
		}
	}
}
