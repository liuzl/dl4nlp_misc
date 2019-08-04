import nagisa

# After finish training, save the three model files (*.vocabs, *.params, *.hp).
nagisa.fit(train_file="cn/sample.train", dev_file="cn/sample.dev", test_file="cn/sample.test", model_name="cn/sample")

# Build the tagger by loading the trained model files.
sample_tagger = nagisa.Tagger(vocabs='cn/sample.vocabs', params='cn/sample.params', hp='cn/sample.hp')

text = "好吧，天津大学是一所好大学"
words = sample_tagger.tagging(text)
print(words)
#> 福岡/PROPN ・/SYM 博多/PROPN の/ADP 観光/NOUN 情報/NOUN
