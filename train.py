import random
from pymongo          import MongoClient
from nltk             import pos_tag
from abbreviations    import abbr
from contractionsDict import cont

class botTrainer:

    stopword = '\x02'                           # stopword signals end of sentence
    dbclient = MongoClient('insert URI here')   # set up connection to MongoDB
    db = dbclient.dictionary                    # get your database (this case it's called 'dictionary')
    collection = db.words                       # get your collection from database (this case it's called 'words')

    # we let chain_length be an argument so initialize with whatever chain_length is chosen to be
    def __init__(self,**kwargs):
        self.chain_length = kwargs.get("chain_length")

    # split the message, replace contractions and abbreviations, and tag with parts of speech
    def split_message(self,message):
        words = message.split()
        for word in words:
            if word.lower() in cont:
                message = message.replace(word,cont[word.lower()])
            if word.lower() in abbr:
                message = message.replace(word,abbr[word.lower()])
        words = message.split()
        tagged = pos_tag(words)
        # if the message is too short, we won't bother with the message 
        if len(tagged) > self.chain_length:
            tagged.append(self.stopword)
            for i in range(len(tagged) - self.chain_length):
                yield tagged[i:i + self.chain_length + 1]

    # take the message, pass through split_message, then add to collection
    def train(self,message):
        tagged = list(self.split_message(message))
        for i in range(len(tagged) - 2):
            key = ','.join(tagged[i][0] + tagged[i][1])
            post = {
                key: ','.join(tagged[i][2])
            }
            self.collection.insert(post,check_keys=False)
            print(post)

# create botTrainer object with chain_length = 2, but you can make it 3 or 4 or whatever
trainer = botTrainer(chain_length=2);
file = open('twitterconvos.txt','r',encoding='UTF-8')
for line in file:
    trainer.train(line)
