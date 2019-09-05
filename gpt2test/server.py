import requests
import json
import argparse
import torch
import torch.nn.functional as F
import pytorch_transformers
from tokenizations import tokenization_bert
from pytorch_transformers import GPT2LMHeadModel

import common


from flask import Flask, request, Response
app = Flask(__name__, static_url_path='')

parser = argparse.ArgumentParser()
parser.add_argument('--model_path',type=str, default="models/bud", required=False)
parser.add_argument('--vocab_path',type=str, default="cache/bud_vocab.txt", required=False)
parser.add_argument('--port',type=int,default=4500,required=False)
parser.add_argument('--index',type=str,default="index.html",required=False)

args=parser.parse_args()


unk_idx = open(args.vocab_path).read().split('\n').index('[UNK]')
device = "cuda" if torch.cuda.is_available() else "cpu"
tokenizer = tokenization_bert.BertTokenizer(vocab_file=args.vocab_path)
model = GPT2LMHeadModel.from_pretrained(args.model_path)
model.to(device)
model.eval()

@app.route("/api")
def get():
    prefix = request.args.get('text', '')
    
    length = 300
    temperature = 1
    topk = 8
    topp = 0

    context_tokens = tokenizer.convert_tokens_to_ids(tokenizer.tokenize(prefix))
    out = common.sample_sequence(
        model=model, length=length,
        context=context_tokens,
        temperature=temperature, top_k=topk, top_p=topp, device=device,
        unk_idx = unk_idx
    )
    out = out.tolist()
    text = tokenizer.convert_ids_to_tokens(out[0])
    for i, item in enumerate(text[:-1]):  # 确保英文前后有空格
        if common.is_word(item) and common.is_word(text[i+1]):
            text[i] = item + ' '
    for i, item in enumerate(text):
        if item == '[MASK]':
            text[i] = ''
        if item == '[CLS]' or item == '[SEP]':
            text[i] = '\n'
    text = ''.join(text).replace('##', '').strip()
    
    return Response(json.dumps({'status':"ok", 'message':text, 'request':prefix},
        ensure_ascii=False), mimetype="application/json")


@app.route('/')
def index():
    #return app.send_static_file('index.html')
    return app.send_static_file(args.index)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=args.port, debug=True)
