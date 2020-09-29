# main.py
# Written in Python 3.7.3

import os
import json
#sys: temp import
import sys
import discord
with open('config/tokens.json') as f:
    data = json.load(f)

from discord.ext import commands
from discord.ext.commands import CommandNotFound

# define constants (be sure to set values in tokens.json before running!)
if 'BOT_TOKEN' in os.environ:
    BOT_TOKEN = os.environ['BOT_TOKEN']
else:
    BOT_TOKEN = data['bot_token']
API_KEY = data['bot_apiKey']
SERVER_ID = -1 #insert server ID here
BOT_ID = -1 #insert bot ID here
RYTHM_ID = int(235088799074484224)

bot = commands.Bot(command_prefix='!mbnc ')


@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')
    with open('config/config.json') as f:
        inp = json.load(f)
    if not inp['stored_nickname']:
        newdata = { "active": inp['active'], "deletemsgs": inp['deletemsgs'], "stored_nickname": "Rythm" }
        with open('config/config.json', 'w') as outfile:
            json.dump(newdata, outfile)



@bot.command(name='active', help='Sets whether or not the bot is currently active.')
async def active(ctx, state):
    # import saved configs in session
    with open('config/config.json') as f:
        inp = json.load(f)
    # try-catch check and convert input parameter to boolean, catch and end if invalid
    try:
        if state == "on":
            s = True
        elif state == "off":
            s = False
        else:
            await ctx.send('Input state is invalid')
            return
    except CommandNotFound:
        await ctx.send('Input state is invalid')
        return
    # compare input state to saved state and perform action
    if s == inp['active']:
        response = "active is already %s!" % s
        await ctx.send(response.lower())
    else:
        newdata = { "active": s, "deletemsgs": inp['deletemsgs'], "stored_nickname": inp['stored_nickname'] }
        with open('config/config.json', 'w') as outfile:
            json.dump(newdata, outfile)
        response = "active has been set to %s!" % s
        await ctx.send(response.lower())

@bot.command(name='deletemsgs', help='Sets whether or not the bot deletes the Now Playing message from the music bot it pulls from.')
async def deletemsgs(ctx, state):
    # import saved configs in session
    with open('config/config.json') as f:
        inp = json.load(f)
    # try-catch check and convert input parameter to boolean, catch and end if invalid
    try:
        if state == "on":
            s = True
        elif state == "off":
            s = False
        else:
            await ctx.send('Input state is invalid')
            return
    except CommandNotFound:
        await ctx.send('Input state is invalid')
        return
    # compare input state to saved state and perform action
    if s == inp['deletemsgs']:
        response = "deletemsgs is already %s!" % s
        await ctx.send(response.lower())
    else:
        newdata = { "active": inp['active'], "deletemsgs": s, "stored_nickname": inp['stored_nickname'] }
        with open('config/config.json', 'w') as outfile:
            json.dump(newdata, outfile)
        response = "deletemsgs has been set to %s!" % s
        await ctx.send(response.lower())
    
@bot.event
async def on_message(message):
    # check message for bot commands first
    await bot.process_commands(message)
    # check preconditions to make sure subroutine can run without issue
    with open('config/config.json') as f:
        inp = json.load(f)
    if not inp['active']:
        return
    if message.author == bot.user:
        return

    # check content of message, extract and concatenate string, check deletemsgs, set nickname
    if "**Playing** 🎶" in message.content and message.author.id == RYTHM_ID:
        stringLength = len(message.content) - 8
        n = message.content[15:stringLength]
        nickname = n
        if len(n) < 2:
            return
        if len(n) >= 32:
            nickname = n[0:32]
        if inp['deletemsgs']:
            await message.delete()
        await message.author.edit(nick=nickname)



@bot.command(name='exit', help='Stops script running on host system (debug).')
async def exit(ctx):
    await ctx.send("Ending process")
    sys.exit()

bot.run(BOT_TOKEN)