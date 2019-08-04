import nagisa

# Build the tagger by loading the trained model files.
sample_tagger = nagisa.Tagger(vocabs='cn/sample.vocabs', params='cn/sample.params', hp='cn/sample.hp')

while True:
    text = input(">>")
    words = sample_tagger.tagging(text)
    print(words)
