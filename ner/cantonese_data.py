import pycantonese as pc
import random, os
from sklearn.model_selection import train_test_split

def process_single_file(path):
    res = []
    data = open(path).read().split('\n')
    for i, line in enumerate(data):
        if line.startswith('*XX'):
            words = line.split('\t')[-1].split()
            pos = data[i+1].split('\t')[-1].split()
            pos = [p.split('|')[0] for p in pos]
            res.append([[a,b] if a!=b else [a, 'punct'] for a,b in zip(words,pos)])
    return res

corpus = pc.corpus.hkcancor()
data = [sent for file in corpus.filenames() for sent in process_single_file(file)]
random.shuffle(data)
train, test = train_test_split(data, test_size=0.2)

def save_file(file, data):
    with open(file, "w") as f:
        for sent in data:
            for token in sent:
                f.write(f'{token[0]}\t{token[1]}\n')
            f.write('EOS\n')

os.makedirs("cantonese", exist_ok=True)
save_file("cantonese/train.txt", train)
save_file("cantonese/test.txt", test)
save_file("cantonese/dev.txt", test)
