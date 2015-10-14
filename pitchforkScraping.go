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

	var next bool = false // use it to check whether TextToken follows StartTagToken
	for {
		tt := z.Next()
		//fmt.Println(tt) // prints type of token
		if tt == html.ErrorToken {
			fmt.Println("Here's the error token.")
			fmt.Println(z.Err())
			return // need this to exit the loop
		} else if tt == html.StartTagToken {
			tok := z.Token()
			if next == false && tok.Data == "h1" { // heading 1 contains artist's name
				next = true // next pass should be a TextToken
				continue
			}
			next = false // next was true, but next pass wasn't a TextToken
		} else if tt == html.TextToken {
			tok := z.Token()
			if next == true { // previous pass was StartTagToken h1
				fmt.Println(tok) // Artist's name
				next = false
			}
		}
	}
}
