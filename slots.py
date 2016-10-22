import discord
from discord.ext import commands
import asyncio
import random
import currency


class Slots:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def slots(self, ctx, amount: int):
        user = ctx.message.author
        if currency.checkmoney(ctx, user.id) < amount:
            await self.bot.reply("you do not have enough coins.")
            return
        if amount < 1:
            await self.bot.say("You cannot bet negative amounts or 0.")
        emojis = ctx.message.server.emojis
        seven = [x for x in emojis if x.name == "sevenslots"][0]
        pseven = [x for x in emojis if x.name == "psevenslots"][0]
        diamond = [x for x in emojis if x.name == "diamondslots"][0]
        cherry = [x for x in emojis if x.name == "cherryslots"][0]
        bar = [x for x in emojis if x.name == "barslots"][0]
        bobomb = [x for x in emojis if x.name == "bobombslots"][0]
        dollar = [x for x in emojis if x.name == "dollarslots"][0]

        emotes = {seven: [0, 1], pseven: [2], diamond: [3, 4, 5, 6], cherry: [7, 8, 9, 10, 11, 12, 13], bar: [14, 15, 16, 17, 18], bobomb: [19, 20, 21, 22, 23, 24], dollar: [25, 26, 27]}
        metachoice = [random.randrange(28), random.randrange(28), random.randrange(28)]
        chosen = []

        for i in metachoice:
            for k, v in emotes.items():
                if i in v:
                    chosen.append(k)

        currency.removemoney(ctx, ctx.message.author.id, amount)

        await self.bot.say("".join([str(x) for x in chosen]))

        if chosen == [seven for x in range(3)]:
            await self.bot.say("You won {} coins!".format(amount * 10))
            currency.givemoney(ctx, ctx.message.author.id, amount * 10)
        elif chosen == [pseven for x in range(3)]:
            await self.bot.say("Jackpot! You won {} coins!".format(amount * 20))
            currency.givemoney(ctx, ctx.message.author.id, amount * 20)
        elif chosen == [diamond for x in range(3)]:
            multiplier = random.randrange(2, 6)
            await self.bot.say("You won {} coins!".format(amount * multiplier))
            currency.givemoney(ctx, ctx.message.author.id, amount * multiplier)
        elif chosen == [cherry for x in range(3)]:
            await self.bot.say("You won {} coins!".format(amount * 2))
            currency.givemoney(ctx, ctx.message.author.id, amount * 2)
        elif len([x for x in chosen if x == cherry]) == 2:
            await self.bot.say("You got your money back!")
            currency.givemoney(ctx, ctx.message.author.id, amount * 1)
        elif chosen == [bar for x in range(3)]:
            await self.bot.say("You won {} coins!".format(amount * 4))
            currency.givemoney(ctx, ctx.message.author.id, amount * 4)
        elif chosen == [bobomb for x in range(3)]:
            await self.bot.say("You won {} coins!".format(amount * 3))
            currency.givemoney(ctx, ctx.message.author.id, amount * 3)
        elif chosen == [dollar for x in range(3)]:
            await self.bot.say("You won {} coins!".format(amount * 5))
            currency.givemoney(ctx, ctx.message.author.id, amount * 5)
        else:
            await self.bot.say("You got nothing.")


def setup(bot):
    bot.add_cog(Slots(bot))
