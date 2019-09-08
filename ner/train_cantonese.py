import nagisa

# After finish training, save the three model files (*.vocabs, *.params, *.hp).
nagisa.fit(train_file="cantonese/train.txt", dev_file="cantonese/dev.txt", test_file="cantonese/test.txt", model_name="cantonese/model")

# Build the tagger by loading the trained model files.
sample_tagger = nagisa.Tagger(vocabs='cantonese/model.vocabs', params='cantonese/model.params', hp='cantonese/model.hp')

text = "我唔系随便嘅人，我随便起来唔系人"
words = sample_tagger.tagging(text)
print(words)
#> 福岡/PROPN ・/SYM 博多/PROPN の/ADP 観光/NOUN 情報/NOUN
