import discord
import asyncio

import config as cfg



class Responses():
    def __init__(self):
        # {message_id: {"userID": user_id, "stage": 1}}
        self.queue = {}
        self.guild = None

    async def addReactions(self, messageObject, emojis):
        for emoji in emojis:
            await messageObject.add_reaction(emoji)

    async def sendMessage(self, userObject, message):
        try:
            return await userObject.send(message)
        except Exception as e:
            print(f"An error occurred while sending a DM - {e}")

    async def addToQueue(self, userObject):
        messageObject = await self.sendMessage(userObject, cfg.QUESTION_ONE)
        await self.addReactions(messageObject, ["👍", "👎"])
        self.queue[messageObject.id] = {"userID": userObject.id, "stage": 1}

    async def parseReaction(self, reactionObject, userObject):
        emoji, messageObject = reactionObject.emoji, reactionObject.message
        if not messageObject.id in self.queue: return
        queueStage = self.queue[messageObject.id]["stage"]

        if queueStage == 1:
            if emoji in ["👍", "👎"]:
                del self.queue[messageObject.id]
            if emoji == "👎":
                await self.sendMessage(userObject, cfg.CANCELLATION_MSG)
                return
            newMessageObject = await self.sendMessage(userObject, cfg.QUESTION_TWO)
            await self.addReactions(newMessageObject, ["👍", "👎"])
            self.queue[newMessageObject.id] = {"userID": userObject.id, "stage": 2}

        elif queueStage == 2:
            if emoji in ["👍", "👎"]:
                del self.queue[messageObject.id]
            if emoji == "👎":
                await self.sendMessage(userObject, cfg.CANCELLATION_MSG)
                return
            newMessageObject = await self.sendMessage(userObject, cfg.QUESTION_THREE)
            await self.addReactions(newMessageObject, cfg.EMOJI_ROLES.keys())
            self.queue[newMessageObject.id] = {"userID": userObject.id, "stage": 3}

        elif queueStage == 3:
            if not emoji in cfg.EMOJI_ROLES: return
            del self.queue[messageObject.id]
            roleToAdd = self.guild.get_role(cfg.EMOJI_ROLES[emoji])
            memberObject = await self.guild.fetch_member(userObject.id)
            await memberObject.add_roles(*[roleToAdd])
            await self.sendMessage(userObject, cfg.CONFIRMATION_MSG)
