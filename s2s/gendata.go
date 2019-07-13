package main

import (
	"fmt"
	"strconv"
	"strings"

	"github.com/moul/number-to-words"
)

func main() {
	language := ntw.Languages.Lookup("en")
	for i := 0; i < 1000000; i++ {
		w := strings.Replace(language.IntegerToWords(i), "-", " ", -1)
		fmt.Printf("%s\t%s\n", w, strings.Join(strings.Split(strconv.Itoa(i), ""), " "))
	}
}
