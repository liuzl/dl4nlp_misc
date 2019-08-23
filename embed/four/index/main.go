package main

import (
	"encoding/csv"
	"flag"
	"io"
	"log"
	"os"

	"github.com/cheggaaa/pb"
	"github.com/jszwec/csvutil"
	"github.com/liuzl/goutil"
	"github.com/liuzl/store"
)

var (
	input  = flag.String("i", "four.csv", "file of csv to read")
	output = flag.String("o", "./db", "db dir to write")
	c      = flag.Int("c", 0, "file line count")
)

type Item struct {
	Code string `json:"code" csv:"code"`
	Text string `json:"text" csv:"text"`
}

func main() {
	flag.Parse()
	var count int
	var err error
	if *c > 0 {
		count = *c
	} else {
		count, err = goutil.FileLineCount(*input)
		if err != nil {
			log.Fatal(err)
		}
	}

	file, err := os.Open(*input)
	if err != nil {
		log.Fatal(err)
	}
	defer file.Close()

	r := csv.NewReader(file)
	dec, err := csvutil.NewDecoder(r)
	if err != nil {
		log.Fatal(err)
	}

	db, err := store.NewLevelStore(*output)
	if err != nil {
		log.Fatal(err)
	}
	defer db.Close()

	bar := pb.StartNew(count - 1)
	for {
		var item Item
		if err = dec.Decode(&item); err == io.EOF {
			break
		} else if err != nil {
			log.Fatal(err)
		}
		if err = db.Put(item.Code, []byte(item.Text)); err != nil {
			log.Fatal(err)
		}
		if err = db.Put(item.Text, []byte(item.Code)); err != nil {
			log.Fatal(err)
		}
		bar.Increment()
	}
	bar.FinishPrint("done!")
}
