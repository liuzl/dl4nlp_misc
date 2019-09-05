import torch
import torch.nn.functional as F
import os
import argparse
from tqdm import trange
from pytorch_transformers import GPT2LMHeadModel

import common

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--device', default='0', type=str, required=False, help='生成设备')
    parser.add_argument('--length', default=100, type=int, required=False, help='生成长度')
    parser.add_argument('--batch_size', default=1, type=int, required=False, help='生成的batch size')
    parser.add_argument('--nsamples', default=1, type=int, required=False, help='生成几个样本')
    parser.add_argument('--temperature', default=1, type=float, required=False, help='生成温度')
    parser.add_argument('--topk', default=8, type=int, required=False, help='最高几选一')
    parser.add_argument('--topp', default=0, type=float, required=False, help='最高积累概率')
    parser.add_argument('--model_config', default='config/model_config.json', type=str, required=False,
                        help='模型参数')
    parser.add_argument('--tokenizer_path', default='cache/bud_vocab.txt', type=str, required=False, help='词表路径')
    parser.add_argument('--model_path', default='models/bud', type=str, required=False, help='模型路径')
    parser.add_argument('--prefix', default='如是我闻', type=str, required=False, help='生成文章的开头')
    parser.add_argument('--no_wordpiece', action='store_true', help='不做word piece切词')
    parser.add_argument('--segment', action='store_true', help='中文以词为单位')

    args = parser.parse_args()
    print('args:\n' + args.__repr__())

    if args.no_wordpiece:
        from tokenizations import tokenization_bert_without_wordpiece as tokenization_bert
    elif args.segment:
        from tokenizations import tokenization_bert_word_level as tokenization_bert
    else:
        from tokenizations import tokenization_bert

    os.environ["CUDA_VISIBLE_DEVICES"] = args.device  # 此处设置程序使用哪些显卡
    length = args.length
    batch_size = args.batch_size
    nsamples = args.nsamples
    temperature = args.temperature
    topk = args.topk
    topp = args.topp

    device = "cuda" if torch.cuda.is_available() else "cpu"

    tokenizer = tokenization_bert.BertTokenizer(vocab_file=args.tokenizer_path)
    model = GPT2LMHeadModel.from_pretrained(args.model_path)
    model.to(device)
    model.eval()

    if length == -1:
        length = model.config.n_ctx // 2
    elif length > model.config.n_ctx:
        raise ValueError("Can't get samples longer than window size: %s" % model.config.n_ctx)

    while True:
        raw_text = args.prefix
        context_tokens = tokenizer.convert_tokens_to_ids(tokenizer.tokenize(raw_text))
        generated = 0
        for _ in range(nsamples // batch_size):
            out = common.sample_sequence(
                model=model, length=length,
                context=context_tokens,
                temperature=temperature, top_k=topk, top_p=topp, device=device
            )
            out = out.tolist()

            for i in range(batch_size):
                generated += 1
                text = tokenizer.convert_ids_to_tokens(out[0])

                for i, item in enumerate(text[:-1]):  # 确保英文前后有空格
                    if common.is_word(item) and common.is_word(text[i + 1]):
                        text[i] = item + ' '

                for i, item in enumerate(text):
                    if item == '[MASK]':
                        text[i] = ''
                    if item == '[CLS]' or item == '[SEP]':
                        text[i] = '\n'
                print("=" * 40 + " SAMPLE " + str(generated) + " " + "=" * 40)
                text = ''.join(text).replace('##', '').strip()
                print(text)
        print("=" * 80)


if __name__ == '__main__':
    main()
