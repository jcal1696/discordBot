import random
from abbreviations    import abbr
from contractionsDict import cont
from pymongo          import MongoClient
from nltk             import pos_tag

class discordBot:

    stopword = '\x02'
    dbclient = MongoClient('insert URI here')
    db = dbclient.dictionary
    collection = db.words

    def __init__(self,**kwargs):
        self.chattiness = kwargs.get("chattiness")
        self.chain_length = kwargs.get("chain_length")
        self.max_words = kwargs.get("max_words")
        self.replies_to_generate = kwargs.get("replies_to_generate")

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

    def generate_reply(self,seed):
        gen_words = []
        for i in range(self.max_words):
            tagged = seed.split(",")
            print(tagged)
            gen_words.append(tagged[2])
            print(gen_words)
            next_tagged = self.collection.distinct(seed)
            if not next_tagged:
                break
            else:
                if len(next_tagged) > 1:
                    k = random.randint(0,len(next_tagged)-1)
                    next_tagged = next_tagged[k]
                    next_word = next_tagged.split(",")[0]
                else:
                    next_word = next_tagged[0].split(",")[0]
            print(next_word)
            print(next_tagged)
            if isinstance(next_tagged,list):
                halfseed = tagged[2:] + next_tagged[0].split(",")
            else:
                halfseed = tagged[2:] + next_tagged.split(",")
            print(halfseed)
            seed = ','.join(halfseed)
            print(seed)
        return ' '.join(gen_words)

    def log(self,message):
        replies = []
        tagged = list(self.split_message(message))
        for i in range(len(tagged) - 2):
            key = ','.join(tagged[i][0] + tagged[i][1])
            post = {
                key: ','.join(tagged[i][2])
            }
            self.collection.insert(post,check_keys=False)
            best_reply = ''
            for i in range(self.replies_to_generate):
                generated = self.generate_reply(seed=key)
                if not generated:
                    return "no generated messages"
                else:
                    if len(generated) > len(best_reply):
                        best_reply = generated
            if best_reply:
                replies.append(best_reply)
        if len(replies):
            return random.choice(replies)
