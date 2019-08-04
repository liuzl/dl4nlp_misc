import nagisa

# Build the tagger by loading the trained model files.
sample_tagger = nagisa.Tagger(vocabs='jp/sample.vocabs', params='jp/sample.params', hp='jp/sample.hp')

while True:
    text = input(">>")
    words = sample_tagger.tagging(text)
    print(words)
