package main

import (
	"flag"
	"net/http"

	"github.com/GeertJohan/go.rice"
	"github.com/golang/glog"
	"github.com/liuzl/goutil/rest"
)

var (
	addr = flag.String("addr", ":8080", "service address")
)

func main() {
	flag.Parse()
	defer glog.Flush()

	http.Handle("/api/four", rest.WithLog(FourHandler))
	http.Handle("/api/code", rest.WithLog(CodeHandler))
	http.Handle("/", http.FileServer(rice.MustFindBox("ui").HTTPBox()))

	glog.Info("server listen on ", *addr)
	glog.Error(http.ListenAndServe(*addr, nil))
}
