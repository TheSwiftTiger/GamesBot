import discord
from discord.ext import commands
import asyncio
import random


def givemoney(ctx, uid, give):
    with open('currency.txt', 'r+') as c:
        found = False
        member = ctx.message.server.get_member(uid)
        currency = c.readlines()
        for idx, v in enumerate(currency):
            if v.startswith(member.id):
                money = int(v.split("|")[-1])
                newl = v.split("|")[0] + "|" + str(money + give) + "\n"
                print(give)
                currency.pop(idx)
                currency.append(newl)
                print(v)
                print(newl)
                found = True
                break
        if not found:
            currency.append("{}|{}\n".format(member.id, give))
        with open('currency.txt', 'w+') as c:
            c.write("".join(currency))


def removemoney(ctx, uid, remove):
    print(remove)
    with open('currency.txt', 'r+') as c:
        found = False
        member = ctx.message.server.get_member(uid)
        currency = c.readlines()
        for idx, v in enumerate(currency):
            if v.startswith(member.id):
                money = int(v.split("|")[-1])
                if money < remove:
                    return False
                newl = v.split("|")[0] + "|" + str(money - remove) + "\n"
                currency.pop(idx)
                currency.append(newl)
                print(v)
                print(newl)
                found = True
                break
        if not found:
            currency.append("{}|{}\n".format(member.id, give))
        with open('currency.txt', 'w+') as c:
            c.write("".join(currency))
    return


def checkmoney(ctx, uid):
    with open('currency.txt', 'r') as currency:
        c = currency.readlines()
    bal = 0
    for i in c:
        if i.split("|")[0] == uid:
            bal = int(i.split("|")[-1].strip())
    return bal


class Currency:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True, no_pm=True)
    async def bal(self, ctx, user: str="Self"):
        if user == "Self":
            user = ctx.message.author
        elif len(ctx.message.mentions) == 1:
            user = ctx.message.mentions[0]
        else:
            user = ctx.message.server.get_member_named(ctx.message.content.split("bal ", 1)[-1].strip())
            if user is None:
                await self.bot.say("No member with that name.")
                return

        with open('currency.txt', 'r') as currency:
            c = currency.readlines()
        for i in c:
            if i.split("|")[0] == user.id:
                await self.bot.reply("{} has {} coins.".format(user.name, i.split("|")[-1].strip()))
                return
        await self.bot.reply("{} has no coins.".format(user.name))


def setup(bot):
    bot.add_cog(Currency(bot))
