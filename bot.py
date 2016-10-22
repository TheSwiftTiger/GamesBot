import discord
from discord.ext import commands
import asyncio
import random

bot = commands.Bot(command_prefix="!")


@bot.event
async def on_ready():
    print("GamesBot")
    print('-' * 10)


bot.load_extension('currency')
bot.load_extension('slots')
bot.load_extension('items')


@commands.command(pass_context=True)
async def say(self, ctx, txt: str):
    txt = ctx.message.content.split("say ")[-1]

with open('token.txt', 'r') as toke:
    token = toke.readline
bot.run(token)
