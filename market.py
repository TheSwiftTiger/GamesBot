import discord
from discord.ext import commands
import asyncio
import random
import yaml
import items
import currency


def addmarket(ctx, uid, item, amount, price):
    with open('market.txt', 'r+') as c:
        market = "".join(c.readlines())
    market = yaml.load(market)
    if uid not in market:
        market[uid] = {item: [amount, price]}
    else:
        if item in market[uid]:
            market[uid][item] += amount
        else:
            market[uid][item] = amount

    with open('market.txt', 'w+') as c:
        c.write(str(market))


class Market:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_contex=True)