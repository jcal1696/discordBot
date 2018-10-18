import random
import discord
import asyncio
from bot         import discordBot
from discord.ext import commands

# set up discord client
client = discord.Client()

# create new discordBot object with desired parameters
chatbot = discordBot(chattiness=1, chain_length=2, max_words=30, replies_to_generate=3)

# when bot is ready, print to console username and id
@client.event
async def on_ready():
    print('Logged in as ')
    print(client.user.name)
    print(client.user.id)
    print('------')

# when message is recieved, reply 
@client.event
async def on_message(message):
    channel = message.channel
    # if the message came from the bot, don't reply
    if message.author == client.user:
        return

    if random.random() < chatbot.chattiness:
        reply = chatbot.log(message.content)
        await client.send_message(channel,reply)

# run the bot        
client.run('insert discord bot token here')
