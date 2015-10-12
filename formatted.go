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

	for {
		tt := z.Next()
		fmt.Println(tt) // prints type of token
		if tt == html.ErrorToken {
			fmt.Println("Here's the error token.")
			fmt.Println(z.Err())
			return // need this to exit the loop
		} else if tt == html.TextToken {
			fmt.Println("TEXT:", z.Token())
		} else {
			fmt.Println(z.Token())
		}
	}
}
