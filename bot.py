import random
from abbreviations    import abbr
from contractionsDict import cont
from pymongo          import MongoClient
from nltk             import pos_tag

class discordBot:

    stopword = '\x02'                           # stopword to signal end of sentence
    dbclient = MongoClient('insert URI here')   # connect to MongoDB
    db = dbclient.dictionary                    # get database (this case it's called 'dictionary')
    collection = db.words                       # get collection from db (this case it's called 'words')

    # initialize with user-defined parameters
    def __init__(self,**kwargs):
        self.chattiness = kwargs.get("chattiness")
        self.chain_length = kwargs.get("chain_length")
        self.max_words = kwargs.get("max_words")
        self.replies_to_generate = kwargs.get("replies_to_generate")

    # split message, replace contractions and abbreviations, tag with parts of speech
    def split_message(self,message):
        words = message.split()
        for word in words:
            if word.lower() in cont:
                message = message.replace(word,cont[word.lower()])
            if word.lower() in abbr:
                message = message.replace(word,abbr[word.lower()])
        words = message.split()
        tagged = pos_tag(words)
        # if the message is too short, don't bother
        if len(tagged) > self.chain_length:
            tagged.append(self.stopword)
            for i in range(len(tagged) - self.chain_length):
                yield tagged[i:i + self.chain_length + 1]

    # using key-value pairs stored in collection, generate reply
    def generate_reply(self,seed):
        gen_words = []
        for i in range(self.max_words):
            tagged = seed.split(",")
            gen_words.append(tagged[2])
            
            # find all values with this key
            next_tagged = self.collection.distinct(seed) 
            
            # if there is no value at that key, either it's the end of the sentence or the bot hasn't seen this key yet
            if not next_tagged:
                break
            else:
                # if there is more than one value at this key, choose a random one
                if len(next_tagged) > 1:
                    k = random.randint(0,len(next_tagged)-1)
                    next_tagged = next_tagged[k]
                    next_word = next_tagged.split(",")[0]
                else:
                    next_word = next_tagged[0].split(",")[0]
            
            # for some reason, next_word will end up being either a list or array, so check to see if it's a list
            if isinstance(next_tagged,list):
                halfseed = tagged[2:] + next_tagged[0].split(",")
            else:
                halfseed = tagged[2:] + next_tagged.split(",")
            seed = ','.join(halfseed)
        return ' '.join(gen_words)

    # log message into db as key-value pairs, return random choice of generated messages
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
