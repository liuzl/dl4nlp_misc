import nagisa

text = 'Pythonで簡単に使えるツールです'
words = nagisa.tagging(text)
print(words)
#=> Python/名詞 で/助詞 簡単/形状詞 に/助動詞 使える/動詞 ツール/名詞 です/助動詞

# Get a list of words
print(words.words)
#=> ['Python', 'で', '簡単', 'に', '使える', 'ツール', 'です']

# Get a list of POS-tags
print(words.postags)
#=> ['名詞', '助詞', '形状詞', '助動詞', '動詞', '名詞', '助動詞']
