import random
from pymongo          import MongoClient
from nltk             import pos_tag
from abbreviations    import abbr
from contractionsDict import cont

class botTrainer:

    stopword = '\x02'
    dbclient = MongoClient('insert URI here')
    db = dbclient.dictionary
    collection = db.words

    def __init__(self,**kwargs):
        self.chain_length = kwargs.get("chain_length")

    def split_message(self,message):
        words = message.split()
        for word in words:
            if word.lower() in cont:
                message = message.replace(word,cont[word.lower()])
            if word.lower() in abbr:
                message = message.replace(word,abbr[word.lower()])
        words = message.split()
        tagged = pos_tag(words)
        if len(tagged) > self.chain_length:
            tagged.append(self.stopword)
            for i in range(len(tagged) - self.chain_length):
                yield tagged[i:i + self.chain_length + 1]

    def train(self,message):
        tagged = list(self.split_message(message))
        for i in range(len(tagged) - 2):
            key = ','.join(tagged[i][0] + tagged[i][1])
            post = {
                key: ','.join(tagged[i][2])
            }
            self.collection.insert(post,check_keys=False)
            print(post)

trainer = botTrainer(chain_length=2);
file = open('twitterconvos.txt','r',encoding='UTF-8')
for line in file:
    trainer.train(line)
