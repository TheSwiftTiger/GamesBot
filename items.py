import discord
from discord.ext import commands
import asyncio
import random
import yaml


def giveitem(ctx, uid, item, amount):
    with open('items.txt', 'r+') as c:
        items = "".join(c.readlines())
    items = yaml.load(items)
    if uid not in items:
        items[uid] = {item: 1}
    else:
        if item in items[uid]:
            items[uid][item] += amount
        else:
            items[uid][item] = amount

    with open('items.txt', 'w+') as c:
        c.write(str(items))


def removeitem(ctx, uid, item, amount):
    with open('items.txt', 'r+') as c:
        items = "".join(c.readlines())
    items = yaml.load(items)
    items[uid][item] -= amount
    if items[uid][item] == 0:
        items[uid].pop(item)

    with open('items.txt', 'w+') as c:
        c.write(str(items))


def hasitem(ctx, uid, item):
    with open('items.txt', 'r+') as c:
        items = "".join(c.readlines())
    items = yaml.load(items)
    if uid not in items:
        items[uid] = {item: 1}
        return False
    return True


def checkitems(ctx, uid):
    with open('items.txt', 'r+') as c:
        items = "".join(c.readlines())
    items = yaml.load(items)
    if uid in items:
        return items[uid]
    return {}


class Items:
    def __init__(self, bot):
        self.bot = bot
        self.tradeoffers = {}
        self.trades = {}

    @commands.command(pass_context=True)
    async def inv(self, ctx, user: str="Self"):
        if user == "Self":
            user = ctx.message.author
        elif len(ctx.message.mentions) == 1:
            user = ctx.message.mentions[0]
        else:
            user = ctx.message.server.get_member_named(ctx.message.content.split("inv ", 1)[-1].strip())
            if user is None:
                await self.bot.say("No member with that name.")
                return

        items = checkitems(ctx, user.id)

        if len(items) == 0:
            await self.bot.say("{} has no items.".format(user.name))
            return
        formatted = "{} has {} items: \n```".format(user.name, len(items))

        for k, v in items.items():
            formatted += k + ": " + str(v) + "\n"

        formatted += "```"

        await self.bot.say(formatted)

    @commands.command(pass_context=True)
    async def trade(self, ctx, user: str):
        if len(ctx.message.mentions) == 1:
            user = ctx.message.mentions[0]
        else:
            user = ctx.message.server.get_member_named(ctx.message.content.split("trade ", 1)[-1].strip())
            if user is None:
                await self.bot.say("No member with that name.")
                return

        if user in self.tradeoffers:
            await self.bot.say("That user is already in a trade offer.")
            return

        if ctx.message.author in self.trades:
            await self.bot.say("You are already in a trade.")
            return
        if user in self.trades:
            await self.bot.say("That user is currently in a trade.")
            return

        self.tradeoffers[user] = ctx.message.author

        await self.bot.send_message(user, "{} wants to trade! Accept? (!y/!n)".format(ctx.message.author))
        await self.bot.send_message(ctx.message.author, "Requested trade.")

    @commands.command(pass_context=True)
    async def y(self, ctx):
        user = ctx.message.author
        if ctx.message.author not in self.tradeoffers:
            await self.bot.say("You are not in a trade offer with anyone.")
            return

        other = self.tradeoffers[ctx.message.author]
        if user in self.trades:
            await self.bot.say("You are already in a trade.")
            return
        if other in self.trades:
            await self.bot.say("That user is currently in a trade.")
            return

        self.tradeoffers.pop(user)

        self.trades[other] = [user, {}, False]
        self.trades[user] = [other, {}, False]

        await self.bot.send_message(other, "{} has accepted your request to trade.".format(user.name))
        await self.bot.say("Accepted trade.")

    @commands.command(pass_context=True)
    async def n(self, ctx):
        user = ctx.message.author
        if ctx.message.author not in self.tradeoffers:
            await self.bot.say("You are not in a trade offer with anyone.")
            return

        other = self.tradeoffers[ctx.message.author]

        self.tradeoffers.pop(user)
        await self.bot.say("Declined trade.")
        await self.bot.send_message(other, "{} has declined your request to trade.".format(user.name))

    @commands.command(pass_context=True)
    async def tradeadd(self, ctx, amount: int, item: str):
        if ctx.message.author not in self.trades:
            await self.bot.say("You are not in a trade with anyone.")
            return

        item = ctx.message.content.split(str(amount), 1)[-1].strip()

        user = ctx.message.author
        other = self.trades[ctx.message.author][0]

        useritems = self.trades[user][1]

        if self.trades[user][2]:
            await self.bot.say("You have already locked in.")
            return

        if item not in checkitems(ctx, user.id):
            await self.bot.say("You do not have this item.")
            return
        if checkitems(ctx, user.id)[item] < amount:
            await self.bot.say("You do not have enough of this item.")
            return
        if amount < 1:
            await self.bot.say("You cannot add negative or 0 items.")

        self.trades[other][2] = False

        useritems[item] = amount
        giving = ""
        recieving = ""
        for k, v in self.trades[other][1].items():
            recieving += k + ": " + str(v) + "\n"
        for k, v in useritems.items():
            giving += k + ": " + str(v) + "\n"
        await self.bot.say("{} {} added!\nTrade\n------\nGiving: ```{}```\nRecieving: ```{}```".format(amount, item, giving, recieving).replace("``````", "Nothing"))
        await self.bot.send_message(other, "{} added {} {}.\nTrade\n------\nGiving: ```{}```\nRecieving: ```{}```".format(user.name, amount, item, giving, recieving).replace("``````", "Nothing"))

    @commands.command(pass_context=True)
    async def traderemove(self, ctx, item: str):
        if ctx.message.author not in self.trades:
            await self.bot.say("You are not in a trade with anyone.")
            return

    @commands.command(pass_context=True)
    async def tradelock(self, ctx):
        if ctx.message.author not in self.trades:
            await self.bot.say("You are not in a trade with anyone.")
            return

        user = ctx.message.author
        other = self.trades[user][0]

        if self.trades[user][2]:
            self.trades[user][2] = False
        else:
            self.trades[user][2] = True
            await self.bot.say("You have unlocked in the trade.")
            await self.bot.send_message(other, "{} has unlocked in the trade.".format(user.name))

        if self.trades[user][2] and self.trades[other][2]:
            itemsuser = ""
            itemsother = ""
            for k, v in self.trades[other][1].items():
                itemsuser += k + ": " + str(v) + "\n"
                giveitem(ctx, user.id, k, v)
                removeitem(ctx, other.id, k, v)

            for k, v in self.trades[user][1].items():
                itemsother += k + ": " + str(v) + "\n"
                giveitem(ctx, other.id, k, v)
                removeitem(ctx, user.id, k, v)

            await self.bot.say("Accepted trade. New items:\n ```{}```".format(itemsuser).replace("``````", "Nothing"))
            await self.bot.send_message(other, "Accepted trade. New items:\n ```{}```".format(itemsother).replace("``````", "Nothing"))
            self.trades.pop(user)
            self.trades.pop(other)
        else:
            await self.bot.say("You have locked in the trade.")
            await self.bot.send_message(other, "{} has locked in the trade.".format(user.name))


def setup(bot):
    bot.add_cog(Items(bot))
