import nagisa

# After finish training, save the three model files (*.vocabs, *.params, *.hp).
nagisa.fit(train_file="jp/sample.train", dev_file="jp/sample.dev", test_file="jp/sample.test", model_name="jp/sample")

# Build the tagger by loading the trained model files.
sample_tagger = nagisa.Tagger(vocabs='jp/sample.vocabs', params='jp/sample.params', hp='jp/sample.hp')

text = "福岡・博多の観光情報"
words = sample_tagger.tagging(text)
print(words)
#> 福岡/PROPN ・/SYM 博多/PROPN の/ADP 観光/NOUN 情報/NOUN
