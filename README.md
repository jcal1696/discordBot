# discordBot

I will make this more detailed in time but college is hard and time consuming so I'll just put the basics down.

# i m p o r t a n t
I heavily based my code on the one made by Charles Leifer, [here](http://charlesleifer.com/blog/building-markov-chain-irc-bot-python-and-redis/). The difference is that I don't use IRCbot or Redis. Instead, I use discord.py and MongoDB, and I use mlab to help me organize my database. But yeah, check out that website to get a feel for how the bot works, he gives a good explanation on Markov Chains and using databases to store information.

# downloading packages and stuff
I used python 3.4, so make sure you have at least that version.
You're gonna want to download some packages like NLTK, discord.py, and pymongo. To do that just do this in python console:
```
pip install nltk
pip install discord
pip install pymongo
```
or from the command prompt:
```
python -m pip install nltk
python -m pip install discord
python -m pip install pymongo
```
You need to set up a database with MongoDB, and you can do that through [mlab.com](https://mlab.com/signup/)
You can follow the instructions [here](https://docs.mlab.com/) once you sign up.

You'll also need the discord application, you can download [here](https://discordapp.com/download). You'll have to create your own server too for your bot to join. 

Lastly, you need to set up the discord bot. Directions [here](https://discordpy.readthedocs.io/en/rewrite/discord.html).

So, once you do all that, you can just kind of copy the code I provided. Where it says 'Insert URI here', copy that from your database. Where it says 'Insert token here', you get that from discord.

# running the code
## training
You can train the bot on the twitter convos, or any other corpus. Just make sure it's plain text and in sentence form, unless you wanna edit the code to read any other format. Also make sure to replace the name of the file under train.py. Once you set up the training data, just run this:
```
train.py
```
or
```
python train.py
```
## chat bot
Just run this:
```
chat.py
```
or
```
python chat.py
```
Once the log in information from the bot shows up in the console, and the bot is online in your test server, you can start having fun with the bot.
