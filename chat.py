import random
import discord
import asyncio
from bot         import discordBot
from discord.ext import commands

client = discord.Client()

chatbot = discordBot(chattiness=1, chain_length=2, max_words=30, replies_to_generate=3)

@client.event
async def on_ready():
    print('Logged in as ')
    print(client.user.name)
    print(client.user.id)
    print('------')

@client.event
async def on_message(message):
    channel = message.channel
    if message.author == client.user:
        return

    if random.random() < chatbot.chattiness:
        reply = chatbot.log(message.content)
        await client.send_message(channel,reply)

client.run('insert discord bot token here')
