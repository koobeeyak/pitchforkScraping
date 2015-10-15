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
	for {
		tt := z.Next()
		//fmt.Println("tt: ",tt) // prints type of token
		//fmt.Println(z.Token())
		if tt == html.ErrorToken {
			fmt.Println("Here's the error token.")
			fmt.Println(z.Err())
			break // exit loop
		} else if tt == html.StartTagToken {
			currentToken := z.Token()
			if songInfoFieldsNext == false && currentToken.Data == "h1" { // heading 1 contains artist's name
				songInfoFieldsNext = true // next pass should be a TextToken
				continue
			} else if songInfoFieldsNext == true && currentToken.Data != "h2" { // next was true, but next pass isn't song name
				songInfoFieldsNext = false
			}
		} else if tt == html.TextToken {
			currentToken := z.Token()
			if songInfoFieldsNext == true { // previous pass was StartTagToken h1
				fmt.Println("Printing artist: ", currentToken) // Artist's name
				if currentToken.Data != "h2" {                 // not song name that follows artist name
					continue
				} else {
					fmt.Println(currentToken)
					songInfoFieldsNext = false
				}
				//fmt.Println("Next Token 1:",z.Next())
				//fmt.Println("Next Token 2:",z.Next())
				//fmt.Println("Token 2 Text:",z.Token())
				//fmt.Println("Next Token 3:",z.Next())
				//fmt.Println("Token 3 Text:",z.Token())
				//fmt.Println("Next Token 4:",z.Next())
				//fmt.Println("Token 4 Text:",z.Token())
				//fmt.Println("Next Token 5:",z.Next())
				//fmt.Println("Token 5 Text:",z.Token())
				//fmt.Println("Next Token 6:",z.Next())
			}
		}
	}
}
