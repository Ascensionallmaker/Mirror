import discord
import asyncio

import config as cfg
from responses import Responses



responses = Responses()



class Bot(discord.Client):
    async def on_ready(self):
        await bot.wait_until_ready()
        print (bot.user.name + " is ready")
        print ("ID: " + str(bot.user.id))
        responses.guild = bot.get_guild(cfg.SERVER_ID)

    async def on_member_join(memberObject):
        if memberObject.author.bot: return
        await responses.addToQueue(messageObject.mentions[0])

    async def on_reaction_add(self, reactionObject, userObject):
        if userObject.bot: return
        await responses.parseReaction(reactionObject, userObject)

    async def on_message(self, messageObject):
        if messageObject.author.bot: return
        if messageObject.content.startswith("!send") and len(messageObject.mentions) >= 1:
            if not messageObject.author.id in cfg.ADMIN_IDS: return
            await responses.addToQueue(messageObject.mentions[0])



bot = Bot()
bot.run(cfg.BOT_TOKEN)
