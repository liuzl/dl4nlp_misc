import requests
import json
from flask import Flask, request, Response
app = Flask(__name__, static_url_path='')

from seq2seq.evaluator import Predictor
from seq2seq.util.checkpoint import Checkpoint

cp = Checkpoint.load("./experiment/checkpoints/2019_08_02_13_23_47/")
predictor = Predictor(cp.model, cp.input_vocab, cp.output_vocab)

def q(s):
    l = -len('<eos>')
    return "".join(predictor.predict(list(s)))[:l]

@app.route("/api")
def get():
    r = request.args.get('text', '')
    if r == "":
        return Response(json.dumps({'status':"error", 'message':"empty input"}))
    return Response(json.dumps({'status':"ok", 'message':q(r)}),
            mimetype="application/json")


@app.route('/')
def index():
    return app.send_static_file('index.html')#

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5001, debug=True)
