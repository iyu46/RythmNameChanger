 async def reset_nickname():
     with open('config/config.json') as f:
         inp = json.load(f)
     server = bot.get_guild(SERVER_ID)
     while server is not None:
         await server.get_member_named("Rythm#3722").edit(nick=inp['stored_nickname'])

@bot.event
async def on_user_update(before, after):
    # checks if bot edited its own nickname - if not, sets that nickname to be saved/cached
    if not before.id == BOT_ID:
        return
    with open('config/config.json') as f:
        inp = json.load(f)
    # check if bot is resetting to stored nickname
    if after.nickname == inp['stored_nickname']:
        return
    async for entry in guild.audit_logs(limit=1, action=discord.AuditLogAction.member_update):
        if entry.user.id != BOT_ID and entry.target.id == BOT_ID:
            newdata = { "active": inp['active'], "deletemsgs": inp['deletemsgs'], "stored_nickname": after.display_name }
            with open('config/config.json', 'w') as outfile:
                json.dump(newdata, outfile)


@bot.event
async def on_voice_state_update(member, before, after):
    # if Rythm left voice chat/times out (goes from in a channel to not in a channel)
    if member.id == RYTHM_ID and before.channel and not after.channel:
        await reset_nickname()