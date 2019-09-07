import requests
import json
import jieba
from flask import Flask, request, Response
app = Flask(__name__, static_url_path='')

import nagisa
tagger = nagisa.Tagger(
        vocabs='cantonese/model.vocabs',
        params='cantonese/model.params',
        hp='cantonese/model.hp')

def q(s):
    return "{}".format(tagger.tagging(s))

@app.route("/api")
def get():
    r = request.args.get('text', '')
    if r == "":
        return Response(json.dumps({'status':"error", 'message':"empty input"}))
    return Response(json.dumps({'status':"ok", 'message':q(r), 'request':r}, ensure_ascii=False),
            mimetype="application/json")


@app.route('/')
def index():
    return app.send_static_file('index.html')#

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5003, debug=True)
