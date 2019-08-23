package main

import (
	"flag"
	"net/http"
	"strings"
	"sync"
	"unicode"

	"github.com/golang/glog"
	"github.com/liuzl/goutil"
	"github.com/liuzl/goutil/rest"
	"github.com/liuzl/store"
	dbutil "github.com/syndtr/goleveldb/leveldb/util"
)

var (
	dbDir      = flag.String("db", "./db", "db dir")
	levelStore *store.LevelStore
	onceStore  sync.Once
)

func GetLevelStore() *store.LevelStore {
	onceStore.Do(func() {
		var err error
		if levelStore, err = store.NewLevelStore(*dbDir); err != nil {
			panic(err)
		}
	})
	return levelStore
}

func FourHandler(w http.ResponseWriter, r *http.Request) {
	glog.Infof("addr=%s  method=%s host=%s uri=%s",
		r.RemoteAddr, r.Method, r.Host, r.RequestURI)
	r.ParseForm()
	text := strings.TrimSpace(r.FormValue("text"))
	if text == "" {
		rest.MustEncode(w, &rest.RestMessage{"FAIL", "text parameter missing"})
		return
	}
	b, err := GetLevelStore().Get(text)
	if err != nil {
		rest.MustEncode(w, &rest.RestMessage{"FAIL", err.Error()})
		return
	}
	rest.MustEncode(w, &rest.RestMessage{"OK", string(b)})
}

func CodeHandler(w http.ResponseWriter, r *http.Request) {
	glog.Infof("addr=%s  method=%s host=%s uri=%s",
		r.RemoteAddr, r.Method, r.Host, r.RequestURI)
	r.ParseForm()
	code := strings.TrimSpace(r.FormValue("code"))
	if len(code) <= 0 || len(code) > 5 || !goutil.StringIs(code, unicode.IsDigit) {
		rest.MustEncode(w, &rest.RestMessage{"FAIL", "code format error"})
		return
	}
	var ret []map[string]string
	GetLevelStore().ForEach(dbutil.BytesPrefix([]byte(code)),
		func(k, v []byte) (bool, error) {
			kv := strings.Split(string(k), ":")
			ret = append(ret, map[string]string{kv[0]: kv[1]})
			return true, nil
		})
	rest.MustEncode(w, &rest.RestMessage{"OK", ret})
}
