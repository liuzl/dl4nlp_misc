import nagisa

# After finish training, save the three model files (*.vocabs, *.params, *.hp).
nagisa.fit(train_file="sample.train", dev_file="sample.dev", test_file="sample.test", model_name="sample")

# Build the tagger by loading the trained model files.
sample_tagger = nagisa.Tagger(vocabs='sample.vocabs', params='sample.params', hp='sample.hp')

text = "福岡・博多の観光情報"
words = sample_tagger.tagging(text)
print(words)
#> 福岡/PROPN ・/SYM 博多/PROPN の/ADP 観光/NOUN 情報/NOUN
