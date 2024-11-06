import discord
import json
import random
import asyncio
import datetime
import math
import pymongo
from pymongo import MongoClient
from discord import Embed
from discord.ext import commands
from utils import functions
from utils.emojis import emojis
from utils.color import color

cluster = MongoClient('mongodb+srv://blade:lolidkbruh12333333333@cluster0.wbxaj.mongodb.net/myFirstDatabase?retryWrites=true&w=majority')
db = cluster["blade"]
collection = db["economy"]
inventory = db["inventory"]
petsdb = db["pets"]
petinvdb = db["pets_inventory"]
premium = db["premium"]
blacklist = db["blacklist"]

def blacklist_check():
    def predicate(ctx):
        if blacklist.find_one({'_id': ctx.author.id}):
            return False
        return True
    return commands.check(predicate)

class economy(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(brief='check your or others profiles', description='economy')
    @commands.cooldown(1, 2, commands.BucketType.user)
    @blacklist_check()
    async def profile(self, ctx, user: discord.User=None):
        if user == None:
            user = ctx.message.author

            if not collection.find_one({"_id": ctx.message.author.id}):
                economy = {"_id": ctx.message.author.id, "money": 0, "level": 0, "bank_bal": 100, "bank":0, "multiplier": 1, "daily": 'none', "daily_time": 0, "weekly": 'none', "weekly_time": 0, "gamble_won": 0, "gamble_loos": 0, "passive": False}
                collection.insert_one(economy)

            if not inventory.find_one({"_id": ctx.message.author.id}):
                inv = {"_id": ctx.message.author.id, "shovel": False, "gun": False, "rod": False, "worms": 0, "fish": 0, "rabbits": 0}
                inventory.insert_one(inv)

            check = collection.find_one({"_id": ctx.message.author.id})
            check2 = inventory.find_one({"_id": ctx.message.author.id})

            if check["money"] < 500:
                profile_text = 'lol, your poor'
            elif check["money"] > 500:
                profile_text = 'you got some money, ig'
            elif check["money"] > 999999:
                profile_text = 'you are kinda rich'
            elif check["money"] > 999999999:
                profile_text = 'how did you got all this money'

            embed = discord.Embed(description=f'{emojis.reply2} wallet: ``{round(check["money"]):,}💵`` \n{emojis.reply} bank: ``{check["bank"]:,}💵 / {check["bank_bal"]:,}💵``', color=color.color)
            embed.set_author(name=f"{user.name}'s profile", icon_url=user.display_avatar)
            embed.add_field(name=f"{emojis.dash} prestige", value=f'{emojis.reply2} level: ``{check["level"]}`` \n{emojis.reply} multiplier: ``x{check["multiplier"]}``', inline=True)
            embed.add_field(name=f"{emojis.dash} gambled", value=f'{emojis.reply2}won: ``{check["gamble_won"]:,}💵`` \n{emojis.reply} lost: ``{check["gamble_loos"]:,}💵``', inline=True)
            embed.add_field(name=f"{emojis.dash} inventory", value=f'{emojis.reply2}fish: ``{check2["fish"]:,}`` \n{emojis.reply2} worms: ``{check2["worms"]:,}`` \n{emojis.reply} rabbit: ``{check2["rabbits"]:,}`` \n', inline=True)
            embed.set_footer(text=f'{profile_text}')
            await ctx.send(embed=embed)

        elif user:
            if not collection.find_one({"_id": user.id}):
                embed = discord.Embed(description=f'> {emojis.false} The user {user.mention} has no **Profile**', color=color.fail)
                await ctx.send(embed=embed)

            else:
                check = collection.find_one({"_id": user.id})
                check2 = inventory.find_one({"_id": user.id})

                if check["money"] < 500:
                    profile_text = 'lol, they poor.'
                elif check["money"] > 500:
                    profile_text = 'they got some money, ig.'
                elif check["money"] > 999999:
                    profile_text = 'they are kinda rich'
                elif check["money"] > 999999999:
                    profile_text = 'how did they got all this money?!'

                embed = discord.Embed(description=f'{emojis.reply2} wallet: ``{round(check["money"]):,}💵`` \n{emojis.reply} bank: ``{check["bank"]:,}💵 / {check["bank_bal"]:,}💵``', color=color.color)
                embed.set_author(name=f"{user.name}'s profile", icon_url=user.display_avatar)
                embed.add_field(name=f"{emojis.dash} prestige", value=f'{emojis.reply2} level: ``{check["level"]}`` \n{emojis.reply} multiplier: ``x{check["multiplier"]}``', inline=True)
                embed.add_field(name=f"{emojis.dash} gambled", value=f'{emojis.reply2}won: ``{check["gamble_won"]:,}💵`` \n{emojis.reply} lost: ``{check["gamble_loos"]:,}💵``', inline=True)
                embed.add_field(name=f"{emojis.dash} inventory", value=f'{emojis.reply2}fish: ``{check2["fish"]:,}`` \n{emojis.reply2} worms: ``{check2["worms"]:,}`` \n{emojis.reply} rabbit: ``{check2["rabbits"]:,}`` \n', inline=True)
                embed.set_footer(text=f'{profile_text}')
                await ctx.send(embed=embed)

    @commands.command(brief='turn passive mode on or off', description='economy')
    @commands.cooldown(1, 32, commands.BucketType.user)
    @blacklist_check()
    async def passive(self, ctx, turn):
        if not collection.find_one({"_id": ctx.message.author.id}):
            economy = {"_id": ctx.message.author.id, "money": 0, "level": 0, "bank_bal": 100, "bank":0, "multiplier": 1, "daily": 'none', "daily_time": 0, "weekly": 'none', "weekly_time": 0, "gamble_won": 0, "gamble_loos": 0, "passive": False}
            collection.insert_one(economy)
        check = collection.find_one({"_id": ctx.message.author.id})

        if turn == 'on' or turn == 'true':
            if check['passive'] == False:
                collection.update_one({"_id": ctx.message.author.id}, {"$set": {"passive": True}})
                embed = discord.Embed(description=f'> {emojis.true} You activated **passive** mode', color=color.success)
                await ctx.send(embed=embed)

            if check['passive'] == True:
                embed = discord.Embed(description=f'> {emojis.false} **Passive** mode is already **activated**', color=color.fail)
                await ctx.send(embed=embed)

        elif turn == 'off' or turn == 'false':
            if check['passive'] == True:
                collection.update_one({"_id": ctx.message.author.id}, {"$set": {"passive": False}})
                embed = discord.Embed(description=f'> {emojis.true} You deactivated **passive** mode', color=color.success)
                await ctx.send(embed=embed)

            if check['passive'] == False:
                embed = discord.Embed(description=f'> {emojis.false} **Passive** mode is already **deactivated**', color=color.fail)
                await ctx.send(embed=embed)
        else:
            embed = discord.Embed(description=f'> {emojis.false} You cant set **passive** mode to ``{turn}``. You can use ``on`` or ``off``', color=color.fail)
            await ctx.send(embed=embed)

    @commands.command(brief='check your balance', aliases=['bal'], description='economy')
    @commands.cooldown(1, 2, commands.BucketType.user)
    @blacklist_check()
    async def balance(self, ctx, user: discord.Member=None):
        if not collection.find_one({"_id": ctx.message.author.id}):
            economy = {"_id": ctx.message.author.id, "money": 0, "level": 0, "bank_bal": 100, "bank":0, "multiplier": 1, "daily": 'none', "daily_time": 0, "weekly": 'none', "weekly_time": 0, "gamble_won": 0, "gamble_loos": 0, "passive": False}
            collection.insert_one(economy)
        if user == None:
            user = ctx.message.author

            if not collection.find_one({"_id": ctx.message.author.id}):
                economy = {"_id": ctx.message.author.id, "money": 0, "level": 0, "bank_bal": 100, "bank":0, "multiplier": 1, "daily": 'none', "daily_time": 0, "weekly": 'none', "weekly_time": 0, "gamble_won": 0, "gamble_loos": 0, "passive": False}

                collection.insert_one(economy)
            check = collection.find_one({"_id": ctx.message.author.id})

            embed = discord.Embed(description=f'{emojis.reply2} wallet: ``{check["money"]:,}💵`` \n{emojis.reply} bank: ``{check["bank"]:,}💵 / {check["bank_bal"]:,}💵``', color=color.color)
            embed.set_author(name=f"{user.name}'s balance", icon_url=user.display_avatar)
            await ctx.send(embed=embed)

        elif user:
            if not collection.find_one({"_id": user.id}):
                embed = discord.Embed(description=f'> {emojis.false} The user {user.mention} has no **Profile**', color=color.fail)
                await ctx.send(embed=embed)

            else:
                check = collection.find_one({"_id": user.id})
                money = check["money"]

                embed = discord.Embed(description=f'{emojis.reply2} wallet: ``{check["money"]:,}💵`` \n{emojis.reply} bank: ``{check["bank"]:,}💵 / {check["bank_bal"]:,}💵``', color=color.color)
                embed.set_author(name=f"{user.name}'s balance", icon_url=user.display_avatar)
                await ctx.send(embed=embed)

    @commands.command(aliases=['iv'], brief='check your inventory', description='economy')
    @blacklist_check()
    async def inventory(self, ctx, user: discord.Member=None):
        if not collection.find_one({"_id": ctx.message.author.id}):
            economy = {"_id": ctx.message.author.id, "money": 0, "level": 0, "bank_bal": 100, "bank":0, "multiplier": 1, "daily": 'none', "daily_time": 0, "weekly": 'none', "weekly_time": 0, "gamble_won": 0, "gamble_loos": 0, "passive": False}
            collection.insert_one(economy)

        if not inventory.find_one({"_id": ctx.message.author.id}):
            inv = {"_id": ctx.message.author.id, "shovel": False, "gun": False, "rod": False, "worms": 0, "fish": 0, "rabbits": 0}
            inventory.insert_one(inv)

        if user == None:
            user = ctx.message.author
            check = collection.find_one({"_id": ctx.message.author.id})
            check2 = inventory.find_one({"_id": ctx.message.author.id})

            if check2["shovel"] == True:
                shovel = f'{emojis.true} *(owning)*'
            else:
                shovel = f'{emojis.false} *(not owning)*'

            if check2["rod"] == True:
                rod = f'{emojis.true} *(owning)*'
            else:
                rod = f'{emojis.false} *(not owning)*'

            if check2["gun"] == True:
                gun = f'{emojis.true} *(owning)*'
            else:
                gun = f'{emojis.false} *(not owning)*'

            embed = discord.Embed(color=color.color)
            embed.add_field(name=f"{emojis.dash} Items", value=f'{emojis.reply2} Shovel: {shovel} \n{emojis.reply2} Rod: {rod} \n{emojis.reply} Gun: {gun}', inline=True)
            embed.add_field(name=f"{emojis.dash} Caughed", value=f'{emojis.reply2} Fish: ``{check2["fish"]:,}`` \n{emojis.reply2} Worms: ``{check2["worms"]:,}`` \n{emojis.reply} Rabbit: ``{check2["rabbits"]:,}`` \n', inline=True)
            embed.set_author(name=f"{user.name}'s inventory", icon_url=user.display_avatar)
            await ctx.send(embed=embed)

        else:
            if not collection.find_one({"_id": user.id}):
                embed = discord.Embed(description=f'> {emojis.false} The user {user.mention} has no **Profile**', color=color.fail)
                await ctx.send(embed=embed)

            else:
                check = collection.find_one({"_id": user.id})
                check2 = inventory.find_one({"_id": user.id})

                if check2["shovel"] == True:
                    shovel = f'{emojis.true} *(owned)*'
                else:
                    shovel = f'{emojis.false} *(not owned)*'

                if check2["rod"] == True:
                    rod = f'{emojis.true} *(owned)*'
                else:
                    rod = f'{emojis.false} *(not owned)*'

                if check2["gun"] == True:
                    gun = f'{emojis.true} *(owned)*'
                else:
                    gun = f'{emojis.false} *(not owned)*'

                embed = discord.Embed(color=color.color)
                embed.add_field(name=f"{emojis.dash} Items", value=f'{emojis.reply2} Shovel: {shovel} \n{emojis.reply2} Rod: {rod} \n{emojis.reply} Gun: {gun}', inline=True)
                embed.add_field(name=f"{emojis.dash} Caughed", value=f'{emojis.reply2} Fish: ``{check2["fish"]:,}`` \n{emojis.reply2} Worms: ``{check2["worms"]:,}`` \n{emojis.reply} Rabbit: ``{check2["rabbits"]:,}`` \n', inline=True)
                embed.set_author(name=f"{user.name}'s inventory", icon_url=user.display_avatar)
                await ctx.send(embed=embed)

    @commands.command(aliases=['lb'], brief='check the money and prestige leaderboard', description='economy')
    @blacklist_check()
    async def leaderboard(self, ctx):
        money = discord.ui.Button(emoji='💵')
        prestige = discord.ui.Button(emoji='🏆')

        async def money_callback(interaction):
            if interaction.user != ctx.author:
                embed = discord.Embed(description=f"> {emojis.false} This is not your message", color=color.fail)
                await interaction.response.send_message(embed=embed, view=None, ephemeral=True)
                return
            else:
                rankings = collection.find().sort("money",-1)
                i = 1
                embed = discord.Embed(title=f"{emojis.blade} Leaderboard", description=f'{emojis.reply} Top 10: **Money** \n \n', color=color.color)
                for x in rankings:
                    try:
                        temp = self.client.get_user(x["_id"])
                        tempxp = x["money"]
                        embed.description += f"``{i}.`` **{temp.name}**: ``{tempxp:,}💵`` \n"
                        i += 1
                    except:
                        pass
                    if i == 11:
                        break
                await interaction.response.edit_message(embed=embed)

        async def prestige_callback(interaction):
            if interaction.user != ctx.author:
                embed = discord.Embed(description=f"> {emojis.false} This is not your message", color=color.fail)
                await interaction.response.send_message(embed=embed, view=None, ephemeral=True)
                return
            else:
                rankings = collection.find().sort("level",-1)
                i = 1
                embed = discord.Embed(title=f"{emojis.blade} Leaderboard", description=f'{emojis.reply} Top 10: **Prestige** \n \n', color=color.color)
                for x in rankings:
                    try:
                        temp = self.client.get_user(x["_id"])
                        tempxp = x["level"]
                        embed.description += f"``{i}.`` **{temp.name}**: ``Level: {tempxp}`` \n"
                        i += 1
                    except:
                        pass
                    if i == 11:
                        break
                await interaction.response.edit_message(embed=embed)

        rankings = collection.find().sort("money",-1)
        i = 1
        embed = discord.Embed(title=f"{emojis.blade} Leaderboard", description=f'{emojis.reply} Top 10: **Money** \n \n', color=color.color)
        for x in rankings:
            try:
                temp = self.client.get_user(x["_id"])
                tempxp = x["money"]
                temxp = x["level"]
                embed.description += f"``{i}.`` **{temp.name}**: ``{tempxp:,}💵`` \n"
                i += 1
            except:
                pass
            if i == 11:
                break

        money.callback = money_callback
        prestige.callback = prestige_callback

        view = discord.ui.View()
        view.add_item(item=money)
        view.add_item(item=prestige)
        await ctx.send(embed=embed, view=view)

    @commands.command(brief='shop to buy items or pets', description='economy')
    @blacklist_check()
    async def shop(self, ctx):
        if not inventory.find_one({"_id": ctx.message.author.id}):
            inv = {"_id": ctx.message.author.id, "shovel": False, "gun": False, "rod": False, "worms": 0, "fish": 0, "rabbits": 0}
            inventory.insert_one(inv)
        if not collection.find_one({"_id": ctx.message.author.id}):
            economy = {"_id": ctx.message.author.id, "money": 0, "level": 0, "bank_bal": 100, "bank":0, "multiplier": 1, "daily": 'none', "daily_time": 0, "weekly": 'none', "weekly_time": 0, "gamble_won": 0, "gamble_loos": 0, "passive": False}
            collection.insert_one(economy)

        check = collection.find_one({"_id": ctx.message.author.id})
        check2 = inventory.find_one({"_id": ctx.message.author.id})
        px = functions.get_prefix(ctx)

        material = discord.ui.Button(label="material")
        pets = discord.ui.Button(label="pets")
        if petsdb.find_one({"_id": ctx.message.author.id}):
            food = discord.ui.Button(label="food")

        async def material_callback(interaction):
            if interaction.user != ctx.author:
                embed = discord.Embed(description=f"> {emojis.false} This is not your message", color=color.fail)
                await interaction.response.send_message(embed=embed, view=None, ephemeral=True)
                return
            else:
                embed = discord.Embed(title=f'{emojis.blade} Economy Shop', color=color.color,
                description=f'{emojis.reply} *material things* \n \n> **shovel** ``10,000💵`` \n> **rod** ``10,000💵`` \n> **gun** ``15,000💵``')
                embed.set_footer(text=f'type {px}buy [item], to purchase a item')
                await interaction.response.edit_message(embed=embed, view=view)

        async def pets_callback(interaction):
            if interaction.user != ctx.author:
                embed = discord.Embed(description=f"> {emojis.false} This is not your message", color=color.fail)
                await interaction.response.send_message(embed=embed, view=None, ephemeral=True)
                return
            else:
                embed = discord.Embed(title=f'{emojis.blade} Economy Shop', color=color.color,
                description=f'{emojis.reply} *pets* \n \n> **dog** ``10,000💵`` \n> **cat** ``10,000💵`` \n> **spider** ``15,000💵`` \n> **snake** ``15,000💵`` \n> **monkey** ``25,000💵`` \n> **sloth** ``500.000💵`` \n> **unicorn** ``1,000,000💵``')
                embed.set_footer(text=f'type {px}buy [pet], to purchase a item')
                await interaction.response.edit_message(embed=embed, view=view)

        async def food_callback(interaction):
            if interaction.user != ctx.author:
                embed = discord.Embed(description=f"> {emojis.false} This is not your message", color=color.fail)
                await interaction.response.send_message(embed=embed, view=None, ephemeral=True)
                return
            else:
                embed = discord.Embed(title=f'{emojis.blade} Economy Shop', color=color.color,
                description=f'{emojis.reply} *food and drinks* \n \n')

                if petsdb.find_one({"_id": ctx.message.author.id})['pet'] == 'Spider':
                    embed.description += '> **flys** ``100💵`` \n> **insects** ``100💵`` \n> **water** ``100💵``'

                if petsdb.find_one({"_id": ctx.message.author.id})['pet'] == 'Snake':
                    embed.description += '> **rats** ``100💵`` \n> **water** ``100💵``'

                if petsdb.find_one({"_id": ctx.message.author.id})['pet'] == 'Dog':
                    embed.description += '> **steak** ``100💵`` \n> **water** ``100💵``'

                if petsdb.find_one({"_id": ctx.message.author.id})['pet'] == 'Cat':
                    embed.description += '> **fish** ``100💵`` \n> **milk** ``100💵``'

                if petsdb.find_one({"_id": ctx.message.author.id})['pet'] == 'Monkey':
                    embed.description += '> **bananas** ``100💵`` \n> **water** ``100💵``'

                if petsdb.find_one({"_id": ctx.message.author.id})['pet'] == 'Unicorn':
                    embed.description += '> **corn** ``100💵`` \n> **water** ``100💵``'

                if petsdb.find_one({"_id": ctx.message.author.id})['pet'] == 'Sloth':
                    embed.description += '> **leaf** ``100💵`` \n> **water** ``100💵``'

                embed.set_footer(text=f'type {px}buy [food], to purchase a item')
                await interaction.response.edit_message(embed=embed, view=view)

        material.callback = material_callback
        pets.callback = pets_callback

        view = discord.ui.View()
        view.add_item(item=material)
        view.add_item(item=pets)

        if petsdb.find_one({"_id": ctx.message.author.id}):
            food.callback = food_callback
            view.add_item(item=food)

        embed = discord.Embed(title=f'{emojis.blade} Economy Shop', color=color.color,
        description=f'{emojis.reply} *buy the things you need* \n \n> **shovel** ``10,000💵`` \n> **rod** ``10,000💵`` \n> **gun** ``15,000💵``')
        embed.set_footer(text=f'type {px}buy [item], to purchase a item')
        await ctx.send(embed=embed, view=view)

    @commands.command(brief='purchase a item from the shop', description='economy')
    @blacklist_check()
    async def buy(self, ctx, item, amount: int=None):
        if not inventory.find_one({"_id": ctx.message.author.id}):
            inv = {"_id": ctx.message.author.id, "shovel": False, "gun": False, "rod": False, "worms": 0, "fish": 0, "rabbits": 0}
            inventory.insert_one(inv)
        if not collection.find_one({"_id": ctx.message.author.id}):
            economy = {"_id": ctx.message.author.id, "money": 0, "level": 0, "bank_bal": 100, "bank":0, "multiplier": 1, "daily": 'none', "daily_time": 0, "weekly": 'none', "weekly_time": 0, "gamble_won": 0, "gamble_loos": 0, "passive": False}
            collection.insert_one(economy)

        check = collection.find_one({"_id": ctx.message.author.id})
        check2 = inventory.find_one({"_id": ctx.message.author.id})

        if item == 'flys' or item == 'fly' or item == 'insects' or item == 'insect' or item == 'bananas' or item == 'banana' or item == 'fish' or item == 'steak' or item == 'rats' or item == 'water' or item == 'milk' or item == 'corn' or item == 'leaf':
            if petsdb.find_one({"_id": ctx.message.author.id})['pet'] == 'Spider':
                if item == 'flys' or item == 'insects' or item == 'water':
                    if amount == None:
                        embed = discord.Embed(description=f'> {emojis.false} How many ``{item}`` do you want to **Buy**?', color=color.color)
                        await ctx.send(embed=embed)
                    else:
                        if item == 'flys' or item == 'fly':
                            pay = 100 * amount

                            if pay > check["money"]:
                                embed = discord.Embed(description=f'> {emojis.false} You dont have enough **Money**, you only have ``{check["money"]:,}💵``', color=color.fail)
                                await ctx.send(embed=embed)
                            else:
                                food = petinvdb.find_one({"_id": ctx.message.author.id})['flys']
                                petinvdb.update_one({"_id": ctx.message.author.id}, {"$set": {"flys": food + amount}})
                                embed = discord.Embed(description=f'> {emojis.true} You bought ``{amount}`` Flys for ``{int(pay):,}💵``', color=color.success)
                                await ctx.send(embed=embed)

                        if item == 'insects' or item == 'insect':
                            pay = 100 * amount

                            if pay > check["money"]:
                                embed = discord.Embed(description=f'> {emojis.false} You dont have enough **Money**, you only have ``{check["money"]:,}💵``', color=color.fail)
                                await ctx.send(embed=embed)
                            else:
                                food = petinvdb.find_one({"_id": ctx.message.author.id})['insects']
                                petinvdb.update_one({"_id": ctx.message.author.id}, {"$set": {"insects": food + amount}})
                                embed = discord.Embed(description=f'> {emojis.true} You bought ``{amount}`` Insects for ``{int(pay):,}💵``', color=color.success)
                                await ctx.send(embed=embed)

                        if item == 'water':
                            pay = 100 * amount

                            if pay > check["money"]:
                                embed = discord.Embed(description=f'> {emojis.false} You dont have enough **Money**, you only have ``{check["money"]:,}💵``', color=color.fail)
                                await ctx.send(embed=embed)
                            else:
                                water = petinvdb.find_one({"_id": ctx.message.author.id})['water']
                                petinvdb.update_one({"_id": ctx.message.author.id}, {"$set": {"water": water + amount}})
                                embed = discord.Embed(description=f'> {emojis.true} You bought ``{amount}`` Water for ``{int(pay):,}💵``', color=color.success)
                                await ctx.send(embed=embed)

                else:
                    embed = discord.Embed(description=f'> {emojis.false} You cant buy ``{item}`` for your **Pet**', color=color.fail)
                    await ctx.send(embed=embed)

            if petsdb.find_one({"_id": ctx.message.author.id})['pet'] == 'Snake':
                if item == 'rats' or item == 'rat' or item == 'water':
                    if amount == None:
                        embed = discord.Embed(description=f'> {emojis.false} How many ``{item}`` do you want to **Buy**?', color=color.fail)
                        await ctx.send(embed=embed)
                    else:
                        if item == 'rats' or item == 'rat':
                            pay = 100 * amount

                            if pay > check["money"]:
                                embed = discord.Embed(description=f'> {emojis.false} You dont have enough **Money**, you only have ``{check["money"]:,}💵``', color=color.fail)
                                await ctx.send(embed=embed)
                            else:
                                food = petinvdb.find_one({"_id": ctx.message.author.id})['rats']
                                petinvdb.update_one({"_id": ctx.message.author.id}, {"$set": {"rats": food + amount}})
                                embed = discord.Embed(description=f'> {emojis.true} You bought ``{amount}`` Rats for ``{int(pay):,}💵``', color=color.success)
                                await ctx.send(embed=embed)

                        if item == 'water':
                            pay = 100 * amount

                            if pay > check["money"]:
                                embed = discord.Embed(description=f'> {emojis.false} You dont have enough **Money**, you only have ``{check["money"]:,}💵``', color=color.fail)
                                await ctx.send(embed=embed)
                            else:
                                water = petinvdb.find_one({"_id": ctx.message.author.id})['water']
                                petinvdb.update_one({"_id": ctx.message.author.id}, {"$set": {"water": water + amount}})
                                embed = discord.Embed(description=f'> {emojis.true} You bought ``{amount}`` Water for ``{int(pay):,}💵``', color=color.success)
                                await ctx.send(embed=embed)

                else:
                    embed = discord.Embed(description=f'> {emojis.false} You cant buy ``{item}`` for your **Pet**', color=color.fail)
                    await ctx.send(embed=embed)

            if petsdb.find_one({"_id": ctx.message.author.id})['pet'] == 'Sloth':
                if item == 'leaf' or item == 'water':
                    if amount == None:
                        embed = discord.Embed(description=f'> {emojis.false} How many ``{item}`` do you want to **Buy**?', color=color.fail)
                        await ctx.send(embed=embed)
                    else:
                        if item == 'leaf':
                            pay = 100 * amount

                            if pay > check["money"]:
                                embed = discord.Embed(description=f'> {emojis.false} You dont have enough **Money**, you only have ``{check["money"]:,}💵``', color=color.fail)
                                await ctx.send(embed=embed)
                            else:
                                food = petinvdb.find_one({"_id": ctx.message.author.id})['leaf']
                                petinvdb.update_one({"_id": ctx.message.author.id}, {"$set": {"leaf": food + amount}})
                                embed = discord.Embed(description=f'> {emojis.true} You bought ``{amount}`` Leaves for ``{int(pay):,}💵``', color=color.success)
                                await ctx.send(embed=embed)

                        if item == 'water':
                            pay = 100 * amount

                            if pay > check["money"]:
                                embed = discord.Embed(description=f'> {emojis.false} You dont have enough **Money**, you only have ``{check["money"]:,}💵``', color=color.fail)
                                await ctx.send(embed=embed)
                            else:
                                water = petinvdb.find_one({"_id": ctx.message.author.id})['water']
                                petinvdb.update_one({"_id": ctx.message.author.id}, {"$set": {"water": water + amount}})
                                embed = discord.Embed(description=f'> {emojis.true} You bought ``{amount}`` Water for ``{int(pay):,}💵``', color=color.success)
                                await ctx.send(embed=embed)

                else:
                    embed = discord.Embed(description=f'> {emojis.false} You cant buy ``{item}`` for your **Pet**', color=color.fail)
                    await ctx.send(embed=embed)

            if petsdb.find_one({"_id": ctx.message.author.id})['pet'] == 'Dog':
                if item == 'steak' or item == 'water':
                    if amount == None:
                        embed = discord.Embed(description=f'> {emojis.false} How many ``{item}`` do you want to **Buy**?', color=color.fail)
                        await ctx.send(embed=embed)
                    else:
                        if item == 'steak':
                            pay = 100 * amount

                            if pay > check["money"]:
                                embed = discord.Embed(description=f'> {emojis.false} You dont have enough **Money**, you only have ``{check["money"]:,}💵``', color=color.fail)
                                await ctx.send(embed=embed)
                            else:
                                food = petinvdb.find_one({"_id": ctx.message.author.id})['steak']
                                petinvdb.update_one({"_id": ctx.message.author.id}, {"$set": {"steak": food + amount}})
                                embed = discord.Embed(description=f'> {emojis.true} You bought ``{amount}`` Steaks for ``{int(pay):,}💵``', color=color.success)
                                await ctx.send(embed=embed)

                        if item == 'water':
                            pay = 100 * amount

                            if pay > check["money"]:
                                embed = discord.Embed(description=f'> {emojis.false} You dont have enough **Money**, you only have ``{check["money"]:,}💵``', color=color.fail)
                                await ctx.send(embed=embed)
                            else:
                                water = petinvdb.find_one({"_id": ctx.message.author.id})['water']
                                petinvdb.update_one({"_id": ctx.message.author.id}, {"$set": {"water": water + amount}})
                                embed = discord.Embed(description=f'> {emojis.true} You bought ``{amount}`` Water for ``{int(pay):,}💵``', color=color.success)
                                await ctx.send(embed=embed)

                else:
                    embed = discord.Embed(description=f'> {emojis.false} You cant buy ``{item}`` for your **Pet**', color=color.fail)
                    await ctx.send(embed=embed)

            if petsdb.find_one({"_id": ctx.message.author.id})['pet'] == 'Cat':
                if item == 'fish' or item == 'milk':
                    if amount == None:
                        embed = discord.Embed(description=f'> {emojis.false} How many ``{item}`` do you want to **Buy**?', color=color.color)
                        await ctx.send(embed=embed)
                    else:
                        if item == 'fish':
                            pay = 100 * amount

                            if pay > check["money"]:
                                embed = discord.Embed(description=f'> {emojis.false} You dont have enough **Money**, you only have ``{check["money"]:,}💵``', color=color.fail)
                                await ctx.send(embed=embed)
                            else:
                                food = petinvdb.find_one({"_id": ctx.message.author.id})['fish']
                                petinvdb.update_one({"_id": ctx.message.author.id}, {"$set": {"fish": food + amount}})
                                embed = discord.Embed(description=f'> {emojis.true} You bought ``{amount}`` Fish for ``{int(pay):,}💵``', color=color.success)
                                await ctx.send(embed=embed)

                        if item == 'milk':
                            pay = 100 * amount

                            if pay > check["money"]:
                                embed = discord.Embed(description=f'> {emojis.false} You dont have enough **Money**, you only have ``{check["money"]:,}💵``', color=color.fail)
                                await ctx.send(embed=embed)
                            else:
                                milk = petinvdb.find_one({"_id": ctx.message.author.id})['milk']
                                petinvdb.update_one({"_id": ctx.message.author.id}, {"$set": {"milk": milk + amount}})
                                embed = discord.Embed(description=f'> {emojis.true} You bought ``{amount}`` Milk for ``{int(pay):,}💵``', color=color.success)
                                await ctx.send(embed=embed)

                else:
                    embed = discord.Embed(description=f'> {emojis.false} You cant buy ``{item}`` for your **Pet**', color=color.fail)
                    await ctx.send(embed=embed)

            if petsdb.find_one({"_id": ctx.message.author.id})['pet'] == 'Monkey':
                if item == 'bananas' or item == 'banana' or item == 'water':
                    if amount == None:
                        embed = discord.Embed(description=f'> {emojis.false} How many ``{item}`` do you want to **Buy**?', color=color.fail)
                        await ctx.send(embed=embed)
                    else:
                        if item == 'bananas' or item == 'banana':
                            pay = 100 * amount

                            if pay > check["money"]:
                                embed = discord.Embed(description=f'> {emojis.false} You dont have enough **Money**, you only have ``{check["money"]:,}💵``', color=color.fail)
                                await ctx.send(embed=embed)
                            else:
                                food = petinvdb.find_one({"_id": ctx.message.author.id})['bananas']
                                petinvdb.update_one({"_id": ctx.message.author.id}, {"$set": {"bananas": food + amount}})
                                embed = discord.Embed(description=f'> {emojis.true} You bought ``{amount}`` Bananas for ``{int(pay):,}💵``', color=color.success)
                                await ctx.send(embed=embed)

                        if item == 'water':
                            pay = 100 * amount

                            if pay > check["money"]:
                                embed = discord.Embed(description=f'> {emojis.false} You dont have enough **Money**, you only have ``{check["money"]:,}💵``', color=color.fail)
                                await ctx.send(embed=embed)
                            else:
                                water = petinvdb.find_one({"_id": ctx.message.author.id})['water']
                                petinvdb.update_one({"_id": ctx.message.author.id}, {"$set": {"water": water + amount}})
                                embed = discord.Embed(description=f'> {emojis.true} You bought ``{amount}`` Water for ``{int(pay):,}💵``', color=color.success)
                                await ctx.send(embed=embed)

                else:
                    embed = discord.Embed(description=f'> {emojis.false} You cant buy ``{item}`` for your **Pet**', color=color.fail)
                    await ctx.send(embed=embed)

            if petsdb.find_one({"_id": ctx.message.author.id})['pet'] == 'Unicorn':
                    if item == 'corn' or item == 'water':
                        if amount == None:
                            embed = discord.Embed(description=f'> {emojis.false} How many ``{item}`` do you want to **Buy**?', color=color.fail)
                            await ctx.send(embed=embed)
                        else:
                            if item == 'corn':
                                pay = 100 * amount

                                if pay > check["money"]:
                                    embed = discord.Embed(description=f'> {emojis.false} You dont have enough **Money**, you only have ``{check["money"]:,}💵``', color=color.fail)
                                    await ctx.send(embed=embed)
                                else:
                                    food = petinvdb.find_one({"_id": ctx.message.author.id})['corn']
                                    petinvdb.update_one({"_id": ctx.message.author.id}, {"$set": {"corn": food + amount}})
                                    embed = discord.Embed(description=f'> {emojis.true} You bought ``{amount}`` Corn for ``{int(pay):,}💵``', color=color.success)
                                    await ctx.send(embed=embed)

                            if item == 'water':
                                pay = 100 * amount

                                if pay > check["money"]:
                                    embed = discord.Embed(description=f'> {emojis.false} You dont have enough **Money**, you only have ``{check["money"]:,}💵``', color=color.fail)
                                    await ctx.send(embed=embed)
                                else:
                                    water = petinvdb.find_one({"_id": ctx.message.author.id})['water']
                                    petinvdb.update_one({"_id": ctx.message.author.id}, {"$set": {"water": water + amount}})
                                    embed = discord.Embed(description=f'> {emojis.true} You bought ``{amount}`` Water for ``{int(pay):,}💵``', color=color.success)
                                    await ctx.send(embed=embed)

        elif item == 'dog' or item == 'cat' or item == 'spider' or item == 'snake' or item == 'monkey' or item == 'unicorn':
            if not petsdb.find_one({"_id": ctx.message.author.id}):
                if premium.find_one({"_id": ctx.message.author.id}):
                    if item == 'dog':
                        if check["money"] > 10000:
                            new_money = check["money"] - 10000
                            collection.update_one({"_id": ctx.message.author.id}, {"$set": {"money": new_money}})

                            pets = {"_id": ctx.message.author.id, "pet": 'Dog', "name": 'Lucky', "health": 10, "hunger": 10, "thirst": 10, "hygiene": 10, "fun": 10, "love": 10, "energy": 10}
                            petsdb.insert_one(pets)
                            inv = {"_id": ctx.message.author.id, "steak": 0, "water": 0}
                            petinvdb.insert_one(inv)

                            embed = discord.Embed(description=f'> {emojis.true} You **purchased** a **Dog**', color=color.success)
                            await ctx.send(embed=embed)
                        else:
                            embed = discord.Embed(description=f'> {emojis.false} You cant buy a **Dog**, because it costs ``10,000💵`` and you have ``{check["money"]:,}💵``', color=color.fail)
                            await ctx.send(embed=embed)

                    if item == 'cat':
                        if check["money"] > 10000:
                            new_money = check["money"] - 10000
                            collection.update_one({"_id": ctx.message.author.id}, {"$set": {"money": new_money}})

                            pets = {"_id": ctx.message.author.id, "pet": 'Cat', "name": 'Garfield', "health": 10, "hunger": 10, "thirst": 10, "hygiene": 10, "fun": 10, "love": 10, "energy": 10}
                            petsdb.insert_one(pets)
                            inv = {"_id": ctx.message.author.id, "fish": 0, "milk": 0}
                            petinvdb.insert_one(inv)

                            embed = discord.Embed(description=f'> {emojis.true} You **purchased** a **Cat**', color=color.success)
                            await ctx.send(embed=embed)
                        else:
                            embed = discord.Embed(description=f'> {emojis.false} You cant buy a **Cat**, because it costs ``10,000💵`` and you have ``{check["money"]:,}💵``', color=color.fail)
                            await ctx.send(embed=embed)

                    if item == 'spider':
                        if check["money"] > 15000:
                            new_money = check["money"] - 15000
                            collection.update_one({"_id": ctx.message.author.id}, {"$set": {"money": new_money}})

                            pets = {"_id": ctx.message.author.id, "pet": 'Spider', "name": 'Fang', "health": 10, "hunger": 10, "thirst": 10, "hygiene": 10, "fun": 10, "love": 10, "energy": 10}
                            petsdb.insert_one(pets)
                            inv = {"_id": ctx.message.author.id, "flys": 0, "insects": 0, "water": 0}
                            petinvdb.insert_one(inv)

                            embed = discord.Embed(description=f'> {emojis.true} You **purchased** a **Spider**', color=color.success)
                            await ctx.send(embed=embed)
                        else:
                            embed = discord.Embed(description=f'> {emojis.false} You cant buy a **Spider**, because it costs ``15,000💵`` and you have ``{check["money"]:,}💵``', color=color.fail)
                            await ctx.send(embed=embed)

                    if item == 'snake':
                        if check["money"] > 15000:
                            new_money = check["money"] - 15000
                            collection.update_one({"_id": ctx.message.author.id}, {"$set": {"money": new_money}})

                            pets = {"_id": ctx.message.author.id, "pet": 'Snake', "name": 'Buttercup', "health": 10, "hunger": 10, "thirst": 10, "hygiene": 10, "fun": 10, "love": 10, "energy": 10}
                            petsdb.insert_one(pets)
                            inv = {"_id": ctx.message.author.id, "rats": 0, "water": 0}
                            petinvdb.insert_one(inv)

                            embed = discord.Embed(description=f'> {emojis.true} You **purchased** a **Snake**', color=color.success)
                            await ctx.send(embed=embed)
                        else:
                            embed = discord.Embed(description=f'> {emojis.false} You cant buy a **Snake**, because it costs ``15,000💵`` and you have ``{check["money"]:,}💵``', color=color.fail)
                            await ctx.send(embed=embed)

                    if item == 'monkey':
                        if check["money"] > 25000:
                            new_money = check["money"] - 25000
                            collection.update_one({"_id": ctx.message.author.id}, {"$set": {"money": new_money}})

                            pets = {"_id": ctx.message.author.id, "pet": 'Monkey', "name": 'Bob', "health": 10, "hunger": 10, "thirst": 10, "hygiene": 10, "fun": 10, "love": 10, "energy": 10}
                            petsdb.insert_one(pets)
                            inv = {"_id": ctx.message.author.id, "bananas": 0, "water": 0}
                            petinvdb.insert_one(inv)

                            embed = discord.Embed(description=f'> {emojis.true} You **purchased** a **Monkey**', color=color.success)
                            await ctx.send(embed=embed)
                        else:
                            embed = discord.Embed(description=f'> {emojis.false} You cant buy a **Monkey**, because it costs ``25,000💵`` and you have ``{check["money"]:,}💵``', color=color.fail)
                            await ctx.send(embed=embed)

                    if item == 'unicorn':
                        if check["money"] > 1000000:
                            new_money = check["money"] - 1000000
                            collection.update_one({"_id": ctx.message.author.id}, {"$set": {"money": new_money}})

                            pets = {"_id": ctx.message.author.id, "pet": 'Unicorn', "name": 'Glitter', "health": 10, "hunger": 10, "thirst": 10, "hygiene": 10, "fun": 10, "love": 10, "energy": 10}
                            petsdb.insert_one(pets)
                            inv = {"_id": ctx.message.author.id, "corn": 0, "water": 0}
                            petinvdb.insert_one(inv)

                            embed = discord.Embed(description=f'> {emojis.true} You **purchased** a **Unicorn**', color=color.success)
                            await ctx.send(embed=embed)
                        else:
                            embed = discord.Embed(description=f'> {emojis.false} You cant buy a **Unicorn**, because it costs ``1,000,000💵`` and you have ``{check["money"]:,}💵``', color=color.fail)
                            await ctx.send(embed=embed)

                    if item == 'Sloth':
                        if check["money"] > 500000:
                            new_money = check["money"] - 500000
                            collection.update_one({"_id": ctx.message.author.id}, {"$set": {"money": new_money}})

                            pets = {"_id": ctx.message.author.id, "pet": 'Sloth', "name": 'Sid', "health": 10, "hunger": 10, "thirst": 10, "hygiene": 10, "fun": 10, "love": 10, "energy": 10}
                            petsdb.insert_one(pets)
                            inv = {"_id": ctx.message.author.id, "leaf": 0, "water": 0}
                            petinvdb.insert_one(inv)

                            embed = discord.Embed(description=f'> {emojis.true} You **purchased** a **Sloth**', color=color.success)
                            await ctx.send(embed=embed)
                        else:
                            embed = discord.Embed(description=f'> {emojis.false} You cant buy a **Sloth**, because it costs ``500,000💵`` and you have ``{check["money"]:,}💵``', color=color.fail)
                            await ctx.send(embed=embed)
                else:
                    px = functions.get_prefix(ctx)
                    embed = discord.Embed(description=f'> {emojis.false} This command is a **Premium** only feature, to learn more about it, join our [``Support Server``](https://discord.gg/snore)', color=color.color)
                    await ctx.send(embed=embed)
            else:
                embed = discord.Embed(description=f'> {emojis.false} You **already** have a **Pet**', color=color.fail)
                await ctx.send(embed=embed)

        elif item == 'shovel':
            if check2["shovel"] == False:
                if check["money"] > 10000:
                    new_money = check["money"] - 10000
                    collection.update_one({"_id": ctx.message.author.id}, {"$set": {"money": new_money}})
                    inventory.update_one({"_id": ctx.message.author.id}, {"$set": {"shovel": True}})

                    embed = discord.Embed(description=f'> {emojis.true} You **purchased** a **Shovel**', color=color.success)
                    await ctx.send(embed=embed)
                else:
                    embed = discord.Embed(description=f'> {emojis.false} You cant buy a **Shovel**, because it costs ``10,000💵`` and you have ``{check["money"]:,}💵``', color=color.fail)
                    await ctx.send(embed=embed)
            else:
                embed = discord.Embed(description=f'> {emojis.false} You **already** have a **Shovel**', color=color.fail)
                await ctx.send(embed=embed)

        elif item == 'rod':
            if check2["rod"] == False:
                if check["money"] > 10000:
                    new_money = check["money"] - 10000
                    collection.update_one({"_id": ctx.message.author.id}, {"$set": {"money": new_money}})
                    inventory.update_one({"_id": ctx.message.author.id}, {"$set": {"rod": True}})

                    embed = discord.Embed(description=f'> {emojis.true} You **purchased** a **Rod**', color=color.success)
                    await ctx.send(embed=embed)
                else:
                    embed = discord.Embed(description=f'> {emojis.false} You cant buy a **Rod**, because it costs ``10,000💵`` and you have ``{check["money"]:,}💵``', color=color.fail)
                    await ctx.send(embed=embed)
            else:
                embed = discord.Embed(description=f'> {emojis.false} You **already** have a **Rod**', color=color.fail)
                await ctx.send(embed=embed)

        elif item == 'gun':
            if check2["gun"] == False:
                if check["money"] > 15000:
                    new_money = check["money"] - 15000
                    collection.update_one({"_id": ctx.message.author.id}, {"$set": {"money": new_money}})
                    inventory.update_one({"_id": ctx.message.author.id}, {"$set": {"gun": True}})

                    embed = discord.Embed(description=f'> {emojis.true} You **purchased** a **Gun**', color=color.success)
                    await ctx.send(embed=embed)
                else:
                    embed = discord.Embed(description=f'> {emojis.false} You cant buy a **Gun**, because it costs ``15,000💵`` and you have ``{check["money"]:,}💵``', color=color.fail)
                    await ctx.send(embed=embed)
            else:
                embed = discord.Embed(description=f'> {emojis.false} You **already** have a **Gun**', color=color.fail)
                await ctx.send(embed=embed) 	    

        else:
            amount = None
            embed = discord.Embed(description=f'> {emojis.false} The **Item** ``{item}`` couldnt be found in the **Shop**', color=color.fail)
            await ctx.send(embed=embed)

    @commands.command(brief='sell items you caughed', description='economy')
    @blacklist_check()
    async def sell(self, ctx, item, amount):
        if not inventory.find_one({"_id": ctx.message.author.id}):
            inv = {"_id": ctx.message.author.id, "shovel": False, "gun": False, "rod": False, "worms": 0, "fish": 0, "rabbits": 0}
            inventory.insert_one(inv)
        if not collection.find_one({"_id": ctx.message.author.id}):
            economy = {"_id": ctx.message.author.id, "money": 0, "level": 0, "bank_bal": 100, "bank":0, "multiplier": 1, "daily": 'none', "daily_time": 0, "weekly": 'none', "weekly_time": 0, "gamble_won": 0, "gamble_loos": 0, "passive": False}
            collection.insert_one(economy)

        check = collection.find_one({"_id": ctx.message.author.id})
        check2 = inventory.find_one({"_id": ctx.message.author.id})

        if item == 'fish':
            if check2["fish"] != 0:
                if amount == 'max':
                    amount = check2["fish"]
                else:
                    amount = int(amount)

                if amount > check2["fish"]:
                    embed = discord.Embed(description=f'> {emojis.false} You only can sell ``{check2["fish"]}`` Fish', color=color.fail)
                    await ctx.send(embed=embed)

                else:
                    money = amount * 15
                    new_money = round(check["money"] + money)
                    fishs = check2["fish"] - amount

                    collection.update_one({"_id": ctx.message.author.id}, {"$set": {"money": new_money}})
                    inventory.update_one({"_id": ctx.message.author.id}, {"$set": {"fish": fishs}})

                    embed = discord.Embed(description=f'> {emojis.true} You **sold** ``{amount}`` Fish and got ``{money:,}💵``', color=color.success)
                    await ctx.send(embed=embed)
            else:
                embed = discord.Embed(description=f'> {emojis.false} You dont have any **Fish** to **sell**', color=color.fail)
                await ctx.send(embed=embed)

        elif item == 'worms':
            if check2["worms"] != 0:
                if amount == 'max':
                    amount = check2["worms"]
                else:
                    amount = int(amount)

                if amount > check2["worms"]:
                    embed = discord.Embed(description=f'> {emojis.false} You only can sell ``{check2["worms"]}`` Worms', color=color.fail)
                    await ctx.send(embed=embed)

                else:
                    money = amount * 10
                    new_money = round(check["money"] + money)
                    worms = check2["worms"] - amount

                    collection.update_one({"_id": ctx.message.author.id}, {"$set": {"money": new_money}})
                    inventory.update_one({"_id": ctx.message.author.id}, {"$set": {"worms": worms}})

                    embed = discord.Embed(description=f'> {emojis.true} You **sold** ``{amount}`` Worms and got ``{money:,}💵``', color=color.success)
                    await ctx.send(embed=embed)
            else:
                embed = discord.Embed(description=f'> {emojis.false} You dont have any **Worms** to **sell**', color=color.fail)
                await ctx.send(embed=embed)

        elif item == 'rabbits':
            if check2["rabbits"] != 0:
                if amount == 'max':
                    amount = check2["rabbits"]
                else:
                    amount = int(amount)

                if amount > check2["rabbits"]:
                    embed = discord.Embed(description=f'> {emojis.false} You only can sell ``{check2["rabbits"]}`` Rabbits', color=color.fail)
                    await ctx.send(embed=embed)

                else:
                    money = amount * 30
                    new_money = round(check["money"] + money)
                    rabbits = check2["rabbits"] - amount

                    collection.update_one({"_id": ctx.message.author.id}, {"$set": {"money": new_money}})
                    inventory.update_one({"_id": ctx.message.author.id}, {"$set": {"rabbits": rabbits}})

                    embed = discord.Embed(description=f'> {emojis.true} You **sold** ``{amount}`` Rabbits and got ``{money:,}💵``', color=color.success)
                    await ctx.send(embed=embed)
            else:
                embed = discord.Embed(description=f'> {emojis.false} You dont have any **Rabbits** to **sell**', color=color.fail)
                await ctx.send(embed=embed)

        else:
            embed = discord.Embed(description=f'> {emojis.false} You cant sell ``{item}``, because it doesnt exist')
            await ctx.send(embed=embed)

    @commands.command(brief='fish for fishes', description='economy')
    @commands.cooldown(1, 10, commands.BucketType.user)
    @blacklist_check()
    async def fish(self, ctx):
        if not inventory.find_one({"_id": ctx.message.author.id}):
            inv = {"_id": ctx.message.author.id, "shovel": False, "gun": False, "rod": False, "worms": 0, "fish": 0, "rabbits": 0}
            inventory.insert_one(inv)
        if not collection.find_one({"_id": ctx.message.author.id}):
            economy = {"_id": ctx.message.author.id, "money": 0, "level": 0, "bank_bal": 100, "bank":0, "multiplier": 1, "daily": 'none', "daily_time": 0, "weekly": 'none', "weekly_time": 0, "gamble_won": 0, "gamble_loos": 0, "passive": False}

            collection.insert_one(economy)
        check = collection.find_one({"_id": ctx.message.author.id})
        check2 = inventory.find_one({"_id": ctx.message.author.id})

        if check2["rod"] == True:
            choice = random.choice(['good', "bad"])

            if choice == 'good':
                fishs = random.randint(1, 22)
                amount = check2["fish"] + fishs
                inventory.update_one({"_id": ctx.message.author.id}, {"$set": {"fish": amount}})

                embed = discord.Embed(description=f'> You went **Fishing** and **caught** ``{fishs}`` Fish', color=color.color)
                await ctx.send(embed=embed)

            if choice == 'bad':
                message = ['There where **no Fish** today in the **Sea** :(', 'To **Fish** in a **puddle** cant work.']

                embed = discord.Embed(description=f'> {random.choice(message)}', color=color.color)
                await ctx.send(embed=embed)

        else:
            embed = discord.Embed(description=f'{emojis.false} You cant **Fish**, you need to buy a **Rod** in the **Shop**', color=color.color)
            await ctx.send(embed=embed)

    @commands.command(brief='dig for worms', description='economy')
    @commands.cooldown(1, 3, commands.BucketType.user)
    @blacklist_check()
    async def dig(self, ctx):
        if not inventory.find_one({"_id": ctx.message.author.id}):
            inv = {"_id": ctx.message.author.id, "shovel": False, "gun": False, "rod": False, "worms": 0, "fish": 0, "rabbits": 0}
            inventory.insert_one(inv)
        if not collection.find_one({"_id": ctx.message.author.id}):
            economy = {"_id": ctx.message.author.id, "money": 0, "level": 0, "bank_bal": 100, "bank":0, "multiplier": 1, "daily": 'none', "daily_time": 0, "weekly": 'none', "weekly_time": 0, "gamble_won": 0, "gamble_loos": 0, "passive": False}

            collection.insert_one(economy)
        check = collection.find_one({"_id": ctx.message.author.id})
        check2 = inventory.find_one({"_id": ctx.message.author.id})

        if check2["shovel"] == True:
            choice = random.choice(['good', "bad"])

            if choice == 'good':
                worms = random.randint(1, 27)
                amount = check2["worms"] + worms
                inventory.update_one({"_id": ctx.message.author.id}, {"$set": {"worms": amount}})

                embed = discord.Embed(description=f'> You went **Digging** and **caught** ``{worms}`` Worms', color=color.color)
                await ctx.send(embed=embed)

            if choice == 'bad':
                message = ['You tried to **dig** at the **White house** smh.', 'You **digged** a really big **hole**, but found **nothing**']

                embed = discord.Embed(description=f'> {random.choice(message)}', color=color.color)
                await ctx.send(embed=embed)

        else:
            embed = discord.Embed(description=f'{emojis.false} You cant **Dig**, you need to buy a **Shovel** in the **Shop**', color=color.fail)
            await ctx.send(embed=embed)

    @commands.command(brief='hunt for rabbits', description='economy')
    @commands.cooldown(1, 30, commands.BucketType.user)
    @blacklist_check()
    async def hunt(self, ctx):
        if not inventory.find_one({"_id": ctx.message.author.id}):
            inv = {"_id": ctx.message.author.id, "shovel": False, "gun": False, "rod": False, "worms": 0, "fish": 0, "rabbits": 0}
            inventory.insert_one(inv)
        if not collection.find_one({"_id": ctx.message.author.id}):
            economy = {"_id": ctx.message.author.id, "money": 0, "level": 0, "bank_bal": 100, "bank":0, "multiplier": 1, "daily": 'none', "daily_time": 0, "weekly": 'none', "weekly_time": 0, "gamble_won": 0, "gamble_loos": 0, "passive": False}

            collection.insert_one(economy)
        check = collection.find_one({"_id": ctx.message.author.id})
        check2 = inventory.find_one({"_id": ctx.message.author.id})

        if check2["gun"] == True:
            choice = random.choice(['good', "bad"])

            if choice == 'good':
                rabbits = random.randint(1, 18)
                amount = check2["rabbits"] + rabbits
                inventory.update_one({"_id": ctx.message.author.id}, {"$set": {"rabbits": amount}})

                embed = discord.Embed(description=f'> You went **Hunting** and **caught** ``{rabbits}`` Rabbits', color=color.color)
                await ctx.send(embed=embed)

            if choice == 'bad':
                message = ['You went **Hunting** but there where **no Animals**', 'You wanted to **hunt**, instead you got a **Pet**']

                embed = discord.Embed(description=f'> {random.choice(message)}', color=color.color)
                await ctx.send(embed=embed)

        else:
            embed = discord.Embed(description=f'{emojis.false} You cant **Hunt**, you need to buy a **Gun** in the **Shop**', color=color.fail)
            await ctx.send(embed=embed)

    @commands.command(brief='work hard for your money', aliases=['w'], description='economy')
    @commands.cooldown(1, 3, commands.BucketType.user)
    @blacklist_check()
    async def work(self, ctx):
        if not collection.find_one({"_id": ctx.message.author.id}):
            economy = {"_id": ctx.message.author.id, "money": 0, "level": 0, "bank_bal": 100, "bank":0, "multiplier": 1, "daily": 'none', "daily_time": 0, "weekly": 'none', "weekly_time": 0, "gamble_won": 0, "gamble_loos": 0, "passive": False}
            collection.insert_one(economy)
        check = collection.find_one({"_id": ctx.message.author.id})

        money = random.randint(1, 250) * check["multiplier"]
        new_money = check["money"] + money
        new_money = round(new_money)
        collection.update_one({"_id": ctx.message.author.id}, {"$set": {"money": new_money}})

        new_bank_bal = check["bank_bal"] + 15
        collection.update_one({"_id": ctx.message.author.id}, {"$set": {"bank_bal": new_bank_bal}})


        work = ["You worked as a **Stripper**", "You sold your **Fortnite account**", "Someone bought your **Onlyfans**", "You worked as a **Cashier**", "Someone bought your **Art**", "You help in the **homeless kitchen**", "You sold **Feet pics**", "You worked as a **Pizzer delivery man**", "You worked at **McDonals**", "You worked at **Burger King**", "You helped **Older People**", "You sold your **Orgins**"]

        embed = discord.Embed(description=f"> {random.choice(work)}, you got ``{int(money):,}💵`` added to your Wallet!", color=color.color)
        await ctx.send(embed=embed)

    @commands.command(brief='beg on the streets for some change', description='economy')
    @commands.cooldown(1, 12, commands.BucketType.user)
    @blacklist_check()
    async def beg(self, ctx):
        if not collection.find_one({"_id": ctx.message.author.id}):
            economy = {"_id": ctx.message.author.id, "money": 0, "level": 0, "bank_bal": 100, "bank":0, "multiplier": 1, "daily": 'none', "daily_time": 0, "weekly": 'none', "weekly_time": 0, "gamble_won": 0, "gamble_loos": 0, "passive": False}
            collection.insert_one(economy)
        check = collection.find_one({"_id": ctx.message.author.id})

        rating = ["good", "bad", "really good", "really bad"]
        rate = random.choice(rating)

        if rate == "good":
            beg = ["Bart Simpson", "Helmut", "a Butler", "a Child", "your Grandma"]

            money = random.randint(1, 250) * check["multiplier"]
            new_money = check["money"] + money
            new_money = round(new_money)
            collection.update_one({"_id": ctx.message.author.id}, {"$set": {"money": new_money}})

            new_bank_bal = check["bank_bal"] + 15
            collection.update_one({"_id": ctx.message.author.id}, {"$set": {"bank_bal": new_bank_bal}})

            embed = discord.Embed(description=f"> You begged **{random.choice(beg)}**, and got ``{int(money):,}💵``", color=color.color)
            await ctx.send(embed=embed)

        if rate == "really good":
            beg = ["liar", "Kylie Jenner", "Travis Scott", "Will Smith", "Jahseh", "Carti", "lone", "Billie Eilish"]

            money = random.randint(50, 500) * check["multiplier"]
            new_money = check["money"] + money
            new_money = round(new_money)
            collection.update_one({"_id": ctx.message.author.id}, {"$set": {"money": new_money}})

            new_bank_bal = check["bank_bal"] + 15
            collection.update_one({"_id": ctx.message.author.id}, {"$set": {"bank_bal": new_bank_bal}})

            embed = discord.Embed(description=f"> You begged **{random.choice(beg)}**, and got ``{int(money):,}💵``", color=color.color)
            await ctx.send(embed=embed)

        if rate == "bad":
            beg = ["You begged a **Homeless** Person and got **nothing**", "u really asked a **Duck** for money?", "You begged on the **Street** and someone threw a **Rock** on you"]

            embed = discord.Embed(description=f"> {random.choice(beg)}", color=color.color)
            await ctx.send(embed=embed)

        if rate == "really bad":
            beg = ["You **begged** at the **Police Department**"]

            money = random.randint(1, 125)
            new_money = check["money"] - money
            new_money = round(new_money)
            collection.update_one({"_id": ctx.message.author.id}, {"$set": {"money": new_money}})

            embed = discord.Embed(description=f"> {random.choice(beg)}, and you had to pay ``{int(money):,}💵``", color=color.color)
            await ctx.send(embed=embed)

    @commands.command(brief='try to rob the bank', description='economy')
    @commands.cooldown(1, 33, commands.BucketType.user)
    @blacklist_check()
    async def rob(self, ctx):
        if not collection.find_one({"_id": ctx.message.author.id}):
            economy = {"_id": ctx.message.author.id, "money": 0, "level": 0, "bank_bal": 100, "bank":0, "multiplier": 1, "daily": 'none', "daily_time": 0, "weekly": 'none', "weekly_time": 0, "gamble_won": 0, "gamble_loos": 0, "passive": False}
            collection.insert_one(economy)
        check = collection.find_one({"_id": ctx.message.author.id})

        rating = ['good', 'bad']
        rate = random.choice(rating)

        if rate == "good":
            money = round(random.randint(15, 2000) * check["multiplier"])
            add_money = check["money"] + money
            add_money = round(add_money)

            collection.update_one({"_id": ctx.message.author.id}, {"$set": {"money": add_money}})

            new_bank_bal = check["bank_bal"] + money
            collection.update_one({"_id": ctx.message.author.id}, {"$set": {"bank_bal": new_bank_bal}})

            embed = discord.Embed(description=f'> You **Robbed** a Bank and it was **Successfull**, you stole ``{int(money):,}💵``', color=color.color)
            await ctx.send(embed=embed)

        if rate == "bad":
            message = ['You tried to Rob the Bank, but it was already **Empty**', 'The bank you tried to Rob, got already **Robbed**', 'You tried to Rob a Bank, but got shy because of the **Police**']
            embed = discord.Embed(description=f'> {random.choice(message)}', color=color.color)
            await ctx.send(embed=embed)

    @commands.command(brief='steal money from other users', description='economy')
    @commands.cooldown(1, 33, commands.BucketType.user)
    @blacklist_check()
    async def steal(self, ctx, user: discord.Member):
        if not collection.find_one({"_id": ctx.message.author.id}):
            economy = {"_id": ctx.message.author.id, "money": 0, "level": 0, "bank_bal": 100, "bank":0, "multiplier": 1, "daily": 'none', "daily_time": 0, "weekly": 'none', "weekly_time": 0, "gamble_won": 0, "gamble_loos": 0, "passive": False}
            collection.insert_one(economy)
        check = collection.find_one({"_id": user.id})
        add_check = collection.find_one({"_id": ctx.message.author.id})

        if add_check['passive'] == True:
            embed = discord.Embed(description=f'> {emojis.false} You cant **Steal**, you have **Passive** mode on', color=color.color)
            await ctx.send(embed=embed)

        else:
            if user == ctx.message.author or user.id == ctx.message.author.id:
                embed = discord.Embed(description=f'> You cant **Steal** money from Yourself', color=color.color)
                await ctx.send(embed=embed)

            if collection.find_one({"_id": user.id, "passive": True}):
                embed = discord.Embed(description=f'> {emojis.false} You cant **Steal** from {user.mention}, because they have **Passive** mode on', color=color.color)
                await ctx.send(embed=embed)

            else:
                rating = ["good", "bad"]
                rate = random.choice(rating)

                if rate == "good":
                    if collection.find_one({"_id": user.id}):
                        if check["money"] == 0:
                            embed = discord.Embed(description=f'> You tried to Steal from {user.mention}, but they doesnt even have Money', color=color.color)
                            await ctx.send(embed=embed)
                        else:
                            money = random.randint(0, int(check["money"])) / 100 * 5
                            money = round(money)
                            add_money = add_check["money"] + money
                            remove_money = check["money"] - money

                            collection.update_one({"_id": ctx.message.author.id}, {"$set": {"money": add_money}})
                            collection.update_one({"_id": user.id}, {"$set": {"money": remove_money}})
                            embed = discord.Embed(description=f'> You stole Money from {user.mention} and got ``{int(money):,}💵`` out of it.', color=color.color)
                            await ctx.send(embed=embed)
                    else:
                        embed = discord.Embed(description=f'> {emojis.false} The user {user.mention} has no **Profile**', color=color.fail)
                        await ctx.send(embed=embed)

                if rate == "bad":
                    embed = discord.Embed(description=f'> You tried to Steal from {user.mention}, but they Caugh you', color=color.color)
                    await ctx.send(embed=embed)

    @commands.command(brief='deposit money to your bank', aliases=["dep"], description='economy')
    @commands.cooldown(1, 2, commands.BucketType.user)
    @blacklist_check()
    async def deposit(self, ctx, *, money):
        if not collection.find_one({"_id": ctx.message.author.id}):
            economy = {"_id": ctx.message.author.id, "money": 0, "level": 0, "bank_bal": 100, "bank":0, "multiplier": 1, "daily": 'none', "daily_time": 0, "weekly": 'none', "weekly_time": 0, "gamble_won": 0, "gamble_loos": 0, "passive": False}
            collection.insert_one(economy)
        check = collection.find_one({"_id": ctx.message.author.id})

        if '-' in money or '+' in money or '*'in money or '/' in money:
            embed = discord.Embed(description=f'> {emojis.false} wtf, what do you try to do?', color=color.fail)
            await ctx.send(embed=embed)
            return

        if money == 'max' or money == 'all':
            if check["bank_bal"] == check["bank"]:
                embed = discord.Embed(description=f'> You have not enough **Money** to do that, your **Balance** is: ``{check["bank_bal"]:,}💵``', color=color.color)
                await ctx.send(embed=embed)

            if check["bank"] == 0:
                if check["money"] > check["bank_bal"]:
                    money_add = check["bank_bal"]
                    money_remove = check["money"] - check["bank_bal"]

                    collection.update_one({"_id": ctx.message.author.id}, {"$set": {"bank": money_add}})
                    collection.update_one({"_id": ctx.message.author.id}, {"$set": {"money": money_remove}})

                    embed = discord.Embed(description=f"> You deposited ``{money_add:,}💵`` in your **Bank**", color=color.color)
                    await ctx.send(embed=embed)

            if check["bank"] > 0:
                money_bal = check["bank_bal"] - check["bank"]

                if money_bal > check["money"]:
                    money_add = check["bank_bal"] + check["bank"]
                    money_remove = check["money"] - money_add

                    money_msg = check["bank_bal"] - check["bank"]

                    collection.update_one({"_id": ctx.message.author.id}, {"$set": {"bank": money_add}})
                    collection.update_one({"_id": ctx.message.author.id}, {"$set": {"money": money_remove}})

                    embed = discord.Embed(description=f"> You deposited ``{money_msg:,}💵`` in your **Bank**", color=color.color)
                    await ctx.send(embed=embed)

                if check["money"] > money_bal:
                    money_remove = check["money"] - money_bal
                    money_add = check["bank"] + money_bal

                    money_msg = check["bank_bal"] - check["bank"]

                    collection.update_one({"_id": ctx.message.author.id}, {"$set": {"bank": money_add}})
                    collection.update_one({"_id": ctx.message.author.id}, {"$set": {"money": money_remove}})

                    embed = discord.Embed(description=f"> You deposited ``{money_msg:,}💵`` in your **Bank**", color=color.color)
                    await ctx.send(embed=embed)

        elif int(money) > check["money"]:
            embed = discord.Embed(description=f'> You dont have enough **Space** in your **Bank**, you only have Space for ``{check["bank_bal"]:,}💵``', color=color.color)
            await ctx.send(embed=embed)

        elif int(money) == 0:
            embed = discord.Embed(description=f'> You dont have any **Money** to Deposit', color=color.color)
            await ctx.send(embed=embed)

        elif int(money) == check["money"] or int(money) < check["money"]:
            if int(money) > check["bank_bal"]:
                embed = discord.Embed(description=f'> You dont have enough **Space** in your **Bank**, you only have Space for ``{check["bank_bal"]:,}💵``', color=color.color)
                await ctx.send(embed=embed)

            else:
                if check["bank"] == check["bank_bal"]:
                    embed = discord.Embed(description=f'> You already have your **limit** reached in your **bank** from ``{check["bank_bal"]:,}💵``', color=color.color)
                    await ctx.send(embed=embed)
                    return
                elif int(money) + check["bank"] > check["bank_bal"]:
                    embed = discord.Embed(description=f'> You cant deposit ``{int(money):,}💵`` in your **Bank**, you can only have ``{check["bank_bal"]:,}💵`` in your **Bank** and you already got ``{check["bank"]:,}💵``', color=color.color)
                    await ctx.send(embed=embed)
                else:
                    add_money = check["bank"] + int(money)
                    remove_money = check["money"] - int(money)
                    collection.update_one({"_id": ctx.message.author.id}, {"$set": {"money": remove_money}})
                    collection.update_one({"_id": ctx.message.author.id}, {"$set": {"bank": add_money}})
                    embed = discord.Embed(description=f"> You deposited ``{int(money):,}💵`` in your **Bank**", color=color.color)
                    await ctx.send(embed=embed)

    @commands.command(brief='withdraw money from your bank', aliases=["wd"], description='economy')
    @commands.cooldown(1, 2, commands.BucketType.user)
    @blacklist_check()
    async def withdraw(self, ctx, *, money):
        if not collection.find_one({"_id": ctx.message.author.id}):
            economy = {"_id": ctx.message.author.id, "money": 0, "level": 0, "bank_bal": 100, "bank":0, "multiplier": 1, "daily": 'none', "daily_time": 0, "weekly": 'none', "weekly_time": 0, "gamble_won": 0, "gamble_loos": 0, "passive": False}
            collection.insert_one(economy)
        check = collection.find_one({"_id": ctx.message.author.id})

        if '-' in money or '+' in money or '*'in money or '/' in money:
            embed = discord.Embed(description=f'> {emojis.false} wtf, what do you try to do?', color=color.fail)
            await ctx.send(embed=embed)
            return

        if money == 'max' or money == 'all':
            if check["money"] == 0:
                embed = discord.Embed(description=f'> You have nothing to Withdraw.', color=color.color)
                await ctx.send(embed=embed)
            else:
                add_money = check["money"] + check["bank"]
                remove_money = check["bank"] - check["bank"]

                collection.update_one({"_id": ctx.message.author.id}, {"$set": {"money": add_money}})
                collection.update_one({"_id": ctx.message.author.id}, {"$set": {"bank": remove_money}})

                embed = discord.Embed(description=f'> You withdrawn ``{check["bank"]:,}💵`` from your **Bank**', color=color.color)
                await ctx.send(embed=embed)

        if int(money) > check["bank"]:
            embed = discord.Embed(description=f"> You can't withdraw ``{int(money):,}💵``, you only have ``{check['bank']:,}💵`` in your **Bank**", color=color.color)
            await ctx.send(embed=embed)
        else:
            if check["bank"] == 0:
                embed = discord.Embed(description=f'> You cant withdraw, you have nothing in your **Bank**', color=color.color)
                await ctx.send(embed=embed)
            elif check["bank"] - int(money) < 0 :
                embed = discord.Embed(description=f'> You cant withdraw ``{int(money):,}💵`` from your **Bank**, you can only withdraw ``{check["bank"]:,}💵``', color=color.color)
                await ctx.send(embed=embed)
            else:
                add_money = check["money"] + int(money)
                remove_money = check["bank"] - int(money)
                collection.update_one({"_id": ctx.message.author.id}, {"$set": {"money": add_money}})
                collection.update_one({"_id": ctx.message.author.id}, {"$set": {"bank": remove_money}})
                embed = discord.Embed(description=f"> You've withdrawn ``{int(money):,}💵`` from your **Bank**", color=color.color)
                await ctx.send(embed=embed)

    @commands.command(brief='pay a user money', aliases=["gift", "give"], description='economy')
    @commands.cooldown(1, 2, commands.BucketType.user)
    @blacklist_check()
    async def pay(self, ctx, user: discord.User, money):
        if not collection.find_one({"_id": ctx.message.author.id}):
            economy = {"_id": ctx.message.author.id, "money": 0, "level": 0, "bank_bal": 100, "bank":0, "multiplier": 1, "daily": 'none', "daily_time": 0, "weekly": 'none', "weekly_time": 0, "gamble_won": 0, "gamble_loos": 0, "passive": False}
            collection.insert_one(economy)

        if not collection.find_one({"_id": user.id}):
            embed = discord.Embed(description=f'> {emojis.false} The user {user.mention} has no **Profile**', color=color.fail)
            await ctx.send(embed=embed)

        if user == ctx.message.author:
            embed = discord.Embed(description=f'> {emojis.false} You cant **Pay** yourself Money', color=color.fail)
            await ctx.send(embed=embed)

        if '-' in money or '+' in money or '*'in money or '/' in money:
            embed = discord.Embed(description=f'> {emojis.false} wtf, what do you try to do?', color=color.fail)
            await ctx.send(embed=embed)
            return

        else:
            check = collection.find_one({"_id": ctx.message.author.id})

            if money == 'max' or money == 'all':
                money = check["money"]

            if check['money'] == 0:
                embed = discord.Embed(description=f'> You dont have enough **Money**, you only have ``{check["money"]:,}💵``', color=color.color)
                await ctx.send(embed=embed)

            elif int(money) > check['money']:
                embed = discord.Embed(description=f'> You dont have enough **Money**, you only have ``{check["money"]:,}💵``', color=color.color)
                await ctx.send(embed=embed)

            else:
                if int(money) > check["money"]:
                    money_bal = check["money"]
                    embed = discord.Embed(description=f'> You have not enough **Money** to do that, your **Balance** is: ``{money_bal:,}💵``', color=color.color)
                    await ctx.send(embed=embed)
                else:

                    payer = collection.find_one({"_id": ctx.message.author.id})
                    payed_money = round(payer["money"] - int(money))
                    collection.update_one({"_id": ctx.message.author.id}, {"$set": {"money": payed_money}})

                    get = collection.find_one({"_id": user.id})
                    send_money = round(get["money"] + int(money))
                    collection.update_one({"_id": user.id}, {"$set": {"money": send_money}})

                    embed = discord.Embed(description=f'> Sucessfully **sent** ``{int(money):,}💵`` to {user.mention}', color=color.success)
                    await ctx.send(embed=embed)

    @commands.command(brief='prestige to level up', description='economy')
    @commands.cooldown(1, 2, commands.BucketType.user)
    @blacklist_check()
    async def prestige(self, ctx):
        if not collection.find_one({"_id": ctx.message.author.id}):
            economy = {"_id": ctx.message.author.id, "money": 0, "level": 0, "bank_bal": 100, "bank":0, "multiplier": 1, "daily": 'none', "daily_time": 0, "weekly": 'none', "weekly_time": 0, "gamble_won": 0, "gamble_loos": 0, "passive": False}
            collection.insert_one(economy)
        check = collection.find_one({"_id": ctx.message.author.id})

        level = check['level']
        money = 100000 + (50000 * level)

        accept = discord.ui.Button(style=discord.ButtonStyle.green, label="accept", emoji=emojis.true)
        decline = discord.ui.Button(style=discord.ButtonStyle.red, label="decline", emoji=emojis.false)

        if check['money'] > money:
            async def accept_callback(interaction):
                accept = discord.ui.Button(style=discord.ButtonStyle.green, label="accept", emoji=emojis.true, disabled = True)
                decline = discord.ui.Button(style=discord.ButtonStyle.red, label="decline", emoji=emojis.false, disabled = True)

                accept.callback = accept_callback
                decline.callback = decline_callback

                view = discord.ui.View()
                view.add_item(item=accept)
                view.add_item(item=decline)

                if interaction.user != ctx.author:
                    embed = discord.Embed(description=f"> {emojis.false} This is not your message")
                    await interaction.response.send_message(embed=embed, view=None, ephemeral=True)
                    return
                else:
                    check = collection.find_one({"_id": ctx.message.author.id})
                    level = check["level"] + 1
                    multiplier = check["multiplier"] + 0.5
                    collection.update_one({"_id": ctx.message.author.id}, {"$set": {"money": 0}})
                    collection.update_one({"_id": ctx.message.author.id}, {"$set": {"level": level}})
                    collection.update_one({"_id": ctx.message.author.id}, {"$set": {"multiplier": multiplier}})

                    new_bank_bal = check["bank_bal"] + 1000
                    collection.update_one({"_id": ctx.message.author.id}, {"$set": {"bank_bal": new_bank_bal}})

                    embed = discord.Embed(description=f'> {emojis.true} You **Prestiged** to **Level**: ``{level}``, you got a multiplier to: ``{multiplier}``', color=color.success)
                    await interaction.response.edit_message(embed=embed, view=view)

            async def decline_callback(interaction):
                accept = discord.ui.Button(style=discord.ButtonStyle.green, label="accept", emoji=emojis.true, disabled = True)
                decline = discord.ui.Button(style=discord.ButtonStyle.red, label="decline", emoji=emojis.false, disabled = True)

                accept.callback = accept_callback
                decline.callback = decline_callback

                view = discord.ui.View()
                view.add_item(item=accept)
                view.add_item(item=decline)

                if interaction.user != ctx.author:
                    embed = discord.Embed(description=f"> {emojis.false} This is not your **Message**", color=color.fail)
                    await interaction.response.send_message(embed=embed, view=None, ephemeral=True)
                    return
                else:
                    embed = discord.Embed(description=f'> {emojis.false} You **declined** your **Prestige**', color=color.color)
                    await interaction.response.edit_message(embed=embed, view=view)

            accept.callback = accept_callback
            decline.callback = decline_callback

            view = discord.ui.View()
            view.add_item(item=accept)
            view.add_item(item=decline)

            embed = discord.Embed(description=f'> Are you sure to **Prestige** to **Level** ``{check["level"] + 1}`` for ``{int(money):,}💵`` ?', color=color.color)
            await ctx.send(embed=embed, view=view)
        else:
            embed = discord.Embed(description=f'> {emojis.false} You dont have enough **Money**, you need ``{int(money):,}💵`` to **Prestige** to **Level** ``{check["level"] + 1}``', color=color.fail)
            await ctx.send(embed=embed)

    @commands.command(brief='gamble against blade and hope for higher strikes', description='economy')
    @commands.cooldown(1, 22, commands.BucketType.user)
    @blacklist_check()
    async def gamble(self, ctx, money):
        if not collection.find_one({"_id": ctx.message.author.id}):
            economy = {"_id": ctx.message.author.id, "money": 0, "level": 0, "bank_bal": 100, "bank":0, "multiplier": 1, "daily": 'none', "daily_time": 0, "weekly": 'none', "weekly_time": 0, "gamble_won": 0, "gamble_loos": 0, "passive": False}
            collection.insert_one(economy)
        check = collection.find_one({"_id": ctx.message.author.id})

        if money == 'max' or money == 'all':
            money = check["money"]

        if check['money'] == 0:
            embed = discord.Embed(description=f'> You dont have enough **Money**, you only have ``{check["money"]:,}💵``', color=color.color)
            await ctx.send(embed=embed)

        elif int(money) > check['money']:
            embed = discord.Embed(description=f'> You dont have enough **Money**, you only have ``{check["money"]:,}💵``', color=color.color)
            await ctx.send(embed=embed)

        else:
            if int(money) < 10:
                embed = discord.Embed(description=f'> You have to **Gamble** with atleast ``10💵``', color=color.color)
                await ctx.send(embed=embed)
                return

            userstrikes = random.randint(1, 26)
            botstrikes = random.randint(13, 42)

            if userstrikes > botstrikes:
                embed = discord.Embed(title=f'{emojis.blade} Gamble', color=color.color,
                description=f'{emojis.reply} You gamble with ``{int(money):,}💵``')
                message = await ctx.send(embed=embed)

                await asyncio.sleep(2)

                percent = random.randint(50, 100)
                new_money = int(money) * percent / 100
                new_money = round(new_money)
                add_money = check["money"] + new_money
                collection.update_one({"_id": ctx.message.author.id}, {"$set": {"money": add_money}})

                gamble_set = check['gamble_won'] + int(money) * percent / 100
                collection.update_one({"_id": ctx.message.author.id}, {"$set": {"gamble_won": gamble_set}})

                embed = discord.Embed(title=f'{emojis.blade} Gamble', color=color.color,
                description=f'{emojis.reply2} You **WON** ``{int(new_money):,}💵``\n{emojis.reply} Percent won: ``{percent}%``')
                embed.add_field(name=f'{ctx.author.name}', value=f'> Strikes ``{userstrikes}``', inline=True)
                embed.add_field(name=f'{self.client.user.name}', value=f'> Strikes ``{botstrikes}``', inline=True)
                await message.edit(embed=embed)

            elif userstrikes < botstrikes:
                embed = discord.Embed(title=f'{emojis.blade} Gamble', color=color.color,
                description=f'{emojis.reply} You gamble with ``{int(money):,}💵``')
                message = await ctx.send(embed=embed)

                await asyncio.sleep(2)

                percent = random.randint(0, 80)
                new_money = int(money) * percent / 100
                new_money = round(new_money)
                add_money = check["money"] - new_money
                collection.update_one({"_id": ctx.message.author.id}, {"$set": {"money": add_money}})
                gamble_set = check['gamble_loos'] + int(money)
                collection.update_one({"_id": ctx.message.author.id}, {"$set": {"gamble_loos": gamble_set}})

                embed = discord.Embed(title=f'{emojis.blade} Gamble', color=color.color,
                description=f'{emojis.reply2} You **lost** ``{int(new_money):,}💵`` \n{emojis.reply} Percent lost: ``{percent}%``')
                embed.add_field(name=f'{ctx.author.name}', value=f'> Strikes ``{userstrikes}``', inline=True)
                embed.add_field(name=f'{self.client.user.name}', value=f'> Strikes ``{botstrikes}``', inline=True)
                await message.edit(embed=embed)

            else:
                embed = discord.Embed(title=f'{emojis.blade} Gamble', color=color.color,
                description=f'{emojis.reply} You gamble with ``{int(money):,}💵``')
                message = await ctx.send(embed=embed)

                await asyncio.sleep(2)

                embed = discord.Embed(title=f'{emojis.blade} Gamble', color=color.color,
                description=f'{emojis.reply} It was a **Tie**')
                embed.add_field(name=f'{ctx.author.name}', value=f'> Strikes ``{userstrikes}``', inline=True)
                embed.add_field(name=f'{self.client.user.name}', value=f'> Strikes ``{botstrikes}``', inline=True)
                await message.edit(embed=embed)

    @commands.command(aliases=['cf'], brief='bet money and try win with a coinflip', description='economy')
    @commands.cooldown(1, 10, commands.BucketType.user)
    @blacklist_check()
    async def coinflip(self, ctx, money, bet):
        if not collection.find_one({"_id": ctx.message.author.id}):
            economy = {"_id": ctx.message.author.id, "money": 0, "level": 0, "bank_bal": 100, "bank":0, "multiplier": 1, "daily": 'none', "daily_time": 0, "weekly": 'none', "weekly_time": 0, "gamble_won": 0, "gamble_loos": 0, "passive": False}
            collection.insert_one(economy)
        check = collection.find_one({"_id": ctx.message.author.id})

        if money == 'max' or money == 'all':
            money = check["money"]

        if check['money'] == 0:
            embed = discord.Embed(description=f'> You dont have enough **Money**, you only have ``{check["money"]:,}💵``', color=color.color)
            await ctx.send(embed=embed)

        elif int(money) > check['money']:
            embed = discord.Embed(description=f'> You dont have enough **Money**, you only have ``{check["money"]:,}💵``', color=color.color)
            await ctx.send(embed=embed)

        else:
            if int(money) < 10:
                embed = discord.Embed(description=f'> You have to **Gamble** with atleast ``10💵``', color=color.color)
                await ctx.send(embed=embed)
                return

            if bet == 'head' or 'tails':
                embed = discord.Embed(description=f'> <a:coinspin:1032345937848311838> You flip the **Coin** with ``{int(money):,}💵`` betting on **{bet}**', color=color.color)
                message = await ctx.send(embed=embed)

                await asyncio.sleep(4)

                coin = ['head', 'tails']
                coinflip = random.choice(coin)

                if bet == 'head':
                    if coinflip == 'head':
                        set_money = int(money) / 100 * 15
                        new_money = round(set_money)
                        add_money = check['money'] + int(new_money)
                        collection.update_one({"_id": ctx.message.author.id}, {"$set": {"money": add_money}})

                        gamble_set = check['gamble_won'] + int(money)
                        collection.update_one({"_id": ctx.message.author.id}, {"$set": {"gamble_won": gamble_set}})

                        embed = discord.Embed(description=f'> :coin: The Coin landed on **Head**, you **WON** ``{new_money:,}💵``', color=color.color)
                        await message.edit(embed=embed)

                    if coinflip == 'tails':
                        add_money = check['money'] - int(money)
                        collection.update_one({"_id": ctx.message.author.id}, {"$set": {"money": add_money}})

                        gamble_set = check['gamble_loos'] + int(money)
                        collection.update_one({"_id": ctx.message.author.id}, {"$set": {"gamble_loos": gamble_set}})

                        embed = discord.Embed(description=f'> :coin: The Coin landed on **Tails**, you **lost** ``{int(money):,}💵``', color=color.color)
                        await message.edit(embed=embed)

                if bet == 'tails':
                    if coinflip == 'tails':
                        set_money = int(money) / 100 * 15
                        new_money = round(set_money)
                        add_money = check['money'] + int(new_money)
                        collection.update_one({"_id": ctx.message.author.id}, {"$set": {"money": add_money}})

                        gamble_set = check['gamble_won'] + int(money)
                        collection.update_one({"_id": ctx.message.author.id}, {"$set": {"gamble_won": gamble_set}})

                        embed = discord.Embed(description=f'> :coin: The Coin landed on **Tails**, you **WON** ``{int(new_money):,}💵``', color=color.color)
                        await message.edit(embed=embed)

                    if coinflip == 'head':
                        add_money = check['money'] - int(money)
                        collection.update_one({"_id": ctx.message.author.id}, {"$set": {"money": add_money}})

                        gamble_set = check['gamble_loos'] + int(money)
                        collection.update_one({"_id": ctx.message.author.id}, {"$set": {"gamble_loos": gamble_set}})

                        embed = discord.Embed(description=f'> :coin: The Coin landed on **Head**, you **lost** ``{int(money):,}💵``', color=color.color)
                        await message.edit(embed=embed)

            else:
                embed = discord.Embed(description=f'> **{bet}** doesnt exist in Coinflip, only ``head`` or ``tails``', color=color.color)
                await ctx.send(embed=embed)


    @commands.command(brief=f'try to win some money', aliases=['slot', 'bet'], description='economy')
    @commands.cooldown(1, 8, commands.BucketType.user)
    @commands.max_concurrency(1,per=commands.BucketType.default,wait=False)
    @blacklist_check()
    async def slots(self, ctx, money):
        if not collection.find_one({"_id": ctx.message.author.id}):
            economy = {"_id": ctx.message.author.id, "money": 0, "level": 0, "bank_bal": 100, "bank":0, "multiplier": 1, "daily": 'none', "daily_time": 0, "weekly": 'none', "weekly_time": 0, "gamble_won": 0, "gamble_loos": 0, "passive": False}
            collection.insert_one(economy)
        check = collection.find_one({"_id": ctx.message.author.id})

        if money == 'max' or money == 'all':
            money = check["money"]

        if check['money'] == 0:
            embed = discord.Embed(description=f'> You dont have enough **Money**, you only have ``{check["money"]:,}💵``', color=color.color)
            await ctx.send(embed=embed)

        elif int(money) > check['money']:
            embed = discord.Embed(description=f'> You dont have enough **Money**, you only have ``{check["money"]:,}💵``', color=color.color)
            await ctx.send(embed=embed)

        else:
            if int(money) < 10:
                embed = discord.Embed(description=f'> You have to **Gamble** with atleast ``10💵``', color=color.color)
                await ctx.send(embed=embed)
                return

            outcomes = []

            for i in range(3):
                outcome = random.choice(['🍑', '🌍', '🌔'])
                outcomes.append(outcome)

            slots = f"{random.choice(['🍑', '🌍', '🌔'])} | {random.choice(['🍑', '🌍', '🌔'])} | {random.choice(['🍑', '🌍', '🌔'])}"
            slots2 = f"{random.choice(['🍑', '🌍', '🌔'])} | {random.choice(['🍑', '🌍', '🌔'])} | {random.choice(['🍑', '🌍', '🌔'])}"
            slots3 = f"{random.choice(['🍑', '🌍', '🌔'])} | {random.choice(['🍑', '🌍', '🌔'])} | {random.choice(['🍑', '🌍', '🌔'])}"
            slots4 = f"{random.choice(['🍑', '🌍', '🌔'])} | {random.choice(['🍑', '🌍', '🌔'])} | {random.choice(['🍑', '🌍', '🌔'])}"
            slots5 = f"{random.choice(['🍑', '🌍', '🌔'])} | {random.choice(['🍑', '🌍', '🌔'])} | {random.choice(['🍑', '🌍', '🌔'])}"
            slots6 = f"{random.choice(['🍑', '🌍', '🌔'])} | {random.choice(['🍑', '🌍', '🌔'])} | {random.choice(['🍑', '🌍', '🌔'])}"
            slots7 = f"{random.choice(['🍑', '🌍', '🌔'])} | {random.choice(['🍑', '🌍', '🌔'])} | {random.choice(['🍑', '🌍', '🌔'])}"
            slots8 = f"{random.choice(['🍑', '🌍', '🌔'])} | {random.choice(['🍑', '🌍', '🌔'])} | {random.choice(['🍑', '🌍', '🌔'])}"

            slot = f'{outcomes[0]} | {outcomes[1]} | {outcomes[2]}'

            if outcomes[0] == outcomes[1] == outcomes[2]:
                embed = discord.Embed(title=f'{emojis.blade} Slots',
                description=f'{emojis.reply} you **gamble** with ``{int(money):,}💵`` \n \n```{slots} \n{slots2} <<\n{slots3}```', color=color.color)
                message = await ctx.send(embed=embed)

                await asyncio.sleep(1)

                embed = discord.Embed(title=f'{emojis.blade} Slots',
                description=f'{emojis.reply} you **gamble** with ``{int(money):,}💵`` \n \n```{slots2} \n{slots3} <<\n{slots4}```', color=color.color)
                await message.edit(embed=embed)

                await asyncio.sleep(1)

                embed = discord.Embed(title=f'{emojis.blade} Slots',
                description=f'{emojis.reply} you **gamble** with ``{int(money):,}💵`` \n \n```{slots3} \n{slots4} <<\n{slots5}```', color=color.color)
                await message.edit(embed=embed)

                await asyncio.sleep(1)

                embed = discord.Embed(title=f'{emojis.blade} Slots',
                description=f'{emojis.reply} you **gamble** with ``{int(money):,}💵`` \n \n```{slots4} \n{slots5} <<\n{slots6}```', color=color.color)
                await message.edit(embed=embed)

                await asyncio.sleep(1)

                embed = discord.Embed(title=f'{emojis.blade} Slots',
                description=f'{emojis.reply} you **gamble** with ``{int(money):,}💵`` \n \n```{slots5} \n{slots6} <<\n{slots7}```', color=color.color)
                await message.edit(embed=embed)

                await asyncio.sleep(1)

                embed = discord.Embed(title=f'{emojis.blade} Slots',
                description=f'{emojis.reply} you **gamble** with ``{int(money):,}💵`` \n \n```{slots6} \n{slots7} <<\n{slot}```', color=color.color)
                await message.edit(embed=embed)

                await asyncio.sleep(1)

                embed = discord.Embed(title=f'{emojis.blade} Slots',
                description=f'{emojis.reply} you **gamble** with ``{int(money):,}💵`` \n \n```{slots7} \n{slot} <<\n{slots8}```', color=color.color)
                await message.edit(embed=embed)

                await asyncio.sleep(2)

                new_money = int(money) * 10
                new_money = round(new_money)
                add_money = check["money"] + new_money
                collection.update_one({"_id": ctx.message.author.id}, {"$set": {"money": add_money}})

                if outcomes[0] == '🍑':
                    gamble_set = check['gamble_won'] + (int(money) * 5)
                    collection.update_one({"_id": ctx.message.author.id}, {"$set": {"gamble_won": gamble_set}})
                
                if outcomes[0] == '🌍':
                    gamble_set = check['gamble_won'] + (int(money) * 10)
                    collection.update_one({"_id": ctx.message.author.id}, {"$set": {"gamble_won": gamble_set}})

                if outcomes[0] == '🌔':
                    gamble_set = check['gamble_won'] + (int(money) * 15)
                    collection.update_one({"_id": ctx.message.author.id}, {"$set": {"gamble_won": gamble_set}})

                embed = discord.Embed(description=f'> You **WON**, it got ``{int(new_money):,}💵`` money **deposit** in your balance.', color=color.color)
                await message.edit(embed=embed)

            else:
                embed = discord.Embed(title=f'{emojis.blade} Slots',
                description=f'{emojis.reply} you **gamble** with ``{int(money):,}💵`` \n \n```{slots} \n{slots2} <<\n{slots3}```', color=color.color)
                message = await ctx.send(embed=embed)

                await asyncio.sleep(1)

                embed = discord.Embed(title=f'{emojis.blade} Slots',
                description=f'{emojis.reply} you **gamble** with ``{int(money):,}💵`` \n \n```{slots2} \n{slots3} <<\n{slots4}```', color=color.color)
                await message.edit(embed=embed)

                await asyncio.sleep(1)

                embed = discord.Embed(title=f'{emojis.blade} Slots',
                description=f'{emojis.reply} you **gamble** with ``{int(money):,}💵`` \n \n```{slots3} \n{slots4} <<\n{slots5}```', color=color.color)
                await message.edit(embed=embed)

                await asyncio.sleep(1)

                embed = discord.Embed(title=f'{emojis.blade} Slots',
                description=f'{emojis.reply} you **gamble** with ``{int(money):,}💵`` \n \n```{slots4} \n{slots5} <<\n{slots6}```', color=color.color)
                await message.edit(embed=embed)

                await asyncio.sleep(1)

                embed = discord.Embed(title=f'{emojis.blade} Slots',
                description=f'{emojis.reply} you **gamble** with ``{int(money):,}💵`` \n \n```{slots5} \n{slots6} <<\n{slots7}```', color=color.color)
                await message.edit(embed=embed)

                await asyncio.sleep(1)

                embed = discord.Embed(title=f'{emojis.blade} Slots',
                description=f'{emojis.reply} you **gamble** with ``{int(money):,}💵`` \n \n```{slots6} \n{slots7} <<\n{slot}```', color=color.color)
                await message.edit(embed=embed)

                await asyncio.sleep(1)

                embed = discord.Embed(title=f'{emojis.blade} Slots',
                description=f'{emojis.reply} you **gamble** with ``{int(money):,}💵`` \n \n```{slots7} \n{slot} <<\n{slots8}```', color=color.color)
                await message.edit(embed=embed)

                await asyncio.sleep(2)

                new_money = check["money"] - round(int(money))
                collection.update_one({"_id": ctx.message.author.id}, {"$set": {"money": new_money}})

                gamble_set = check['gamble_loos'] + int(money)
                collection.update_one({"_id": ctx.message.author.id}, {"$set": {"gamble_loos": gamble_set}})

                embed = discord.Embed(description=f'> You **lost**, it got ``{int(money):,}💵`` **withdrawn** from you balance.', color=color.color)
                await message.edit(embed=embed)

    @commands.command(brief='set money and guess a number from 1-6', description='economy')
    async def craps(self, ctx, money, number:int):
        if not collection.find_one({"_id": ctx.message.author.id}):
            economy = {"_id": ctx.message.author.id, "money": 0, "level": 0, "bank_bal": 100, "bank":0, "multiplier": 1, "daily": 'none', "daily_time": 0, "weekly": 'none', "weekly_time": 0, "gamble_won": 0, "gamble_loos": 0, "passive": False}
            collection.insert_one(economy)
        check = collection.find_one({"_id": ctx.message.author.id})

        if money == 'max' or money == 'all':
            money = check["money"]

        if check['money'] == 0:
            embed = discord.Embed(description=f'> You dont have enough **Money**, you only have ``{check["money"]:,}💵``', color=color.color)
            await ctx.send(embed=embed)

        elif int(money) > check['money']:
            embed = discord.Embed(description=f'> You dont have enough **Money**, you only have ``{check["money"]:,}💵``', color=color.color)
            await ctx.send(embed=embed)

        else:
            if int(money) < 10:
                embed = discord.Embed(description=f'> You have to **Gamble** with atleast ``10💵``', color=color.color)
                await ctx.send(embed=embed)

            else:
                if number > 6:
                    embed = discord.Embed(description=f'> {emojis.false} You need to use a **Number** between ``1`` - ``6``', color=color.fail)
                    await ctx.send(embed=embed)

                else:
                    bot_numer = random.randint(1,6)

                    embed = discord.Embed(description=f'> :game_die: Blade is rolling the **Dice**', color=color.color)
                    message = await ctx.send(embed=embed)

                    await asyncio.sleep(2)

                    if bot_numer == number:
                        new_money = round((int(money) * 2) + check['money'])
                        gamble_new = check["gamble_won"] + new_money

                        collection.update_one({"_id": ctx.message.author.id}, {"$set": {"gamble_won": gamble_new}})
                        collection.update_one({"_id": ctx.message.author.id}, {"$set": {"money": new_money}})

                        embed = discord.Embed(title=f'{emojis.blade} Craps', color=color.color,
                        description=f'{emojis.reply} You **guessed** the right **Number**, you won ``{round(number * 2)}💵``')
                        embed.add_field(name=f'Dice', value=f'> ``{bot_numer}``', inline=True)
                        embed.add_field(name=f'{ctx.message.author.name}', value=f'> ``{number}``', inline=True)
                        await message.edit(embed=embed)

                    else:
                        gamble_new = check["gamble_loos"] + number
                        new_money = round(check['money'] - (int(money) * 2))

                        if new_money < 1:
                            new_money = 0

                        collection.update_one({"_id": ctx.message.author.id}, {"$set": {"gamble_loos": gamble_new }})
                        collection.update_one({"_id": ctx.message.author.id}, {"$set": {"money": new_money}})

                        embed = discord.Embed(title=f'{emojis.blade} Craps', color=color.color,
                        description=f'{emojis.reply} You **guessed** the wrong **Number**')
                        embed.add_field(name=f'Dice', value=f'> ``{bot_numer}``', inline=True)
                        embed.add_field(name=f'{ctx.message.author.name}', value=f'> ``{number}``', inline=True)
                        await message.edit(embed=embed)

    @commands.command(brief='try your luck to win', aliases=['wof'], description='economy')
    @commands.cooldown(1, 60, commands.BucketType.user)
    async def wheeloffortune(self, ctx):
        if not collection.find_one({"_id": ctx.message.author.id}):
            economy = {"_id": ctx.message.author.id, "money": 0, "level": 0, "bank_bal": 100, "bank":0, "multiplier": 1, "daily": 'none', "daily_time": 0, "weekly": 'none', "weekly_time": 0, "gamble_won": 0, "gamble_loos": 0, "passive": False}
            collection.insert_one(economy)
        check = collection.find_one({"_id": ctx.message.author.id})

        if check['money'] == 0:
            embed = discord.Embed(description=f'> You dont have enough **Money**, you only have ``{check["money"]:,}💵``', color=color.color)
            await ctx.send(embed=embed)

        elif 500 > check['money']:
            embed = discord.Embed(description=f'> You dont have enough **Money**, you only have ``{check["money"]:,}💵``', color=color.color)
            await ctx.send(embed=embed)

        else:
            if int(check['money']) > 500:
                embed = discord.Embed(description=f'> You bought a **Wheel** for ``500💵``', color=color.color)
                message = await ctx.send(embed=embed)

                await asyncio.sleep(1)
            
                new_money = check["money"] - 500
                new_money = round(new_money)

                collection.update_one({"_id": ctx.message.author.id}, {"$set": {"money": new_money}})

                embed = discord.Embed(title=f'{emojis.blade} Wheel of Fortune', color=color.color)
                embed.set_image(url='https://images-wixmp-ed30a86b8c4ca887773594c2.wixmp.com/f/a913725d-8ece-4a32-881d-0c60d37e47e0/decn0ke-9eec36f3-0c52-4fa1-a314-5d534ff92a79.gif?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ1cm46YXBwOjdlMGQxODg5ODIyNjQzNzNhNWYwZDQxNWVhMGQyNmUwIiwiaXNzIjoidXJuOmFwcDo3ZTBkMTg4OTgyMjY0MzczYTVmMGQ0MTVlYTBkMjZlMCIsIm9iaiI6W1t7InBhdGgiOiJcL2ZcL2E5MTM3MjVkLThlY2UtNGEzMi04ODFkLTBjNjBkMzdlNDdlMFwvZGVjbjBrZS05ZWVjMzZmMy0wYzUyLTRmYTEtYTMxNC01ZDUzNGZmOTJhNzkuZ2lmIn1dXSwiYXVkIjpbInVybjpzZXJ2aWNlOmZpbGUuZG93bmxvYWQiXX0.jiPrNbKOO_EYO_1iezKfvdu6y2a_GDQgSXnyxpQCTv4')
                await message.edit(embed=embed)

                await asyncio.sleep(random.randint(2, 10))

                win = random.choice([300, 0, 500, 600, 0, 5000, 650, 0, 300, 500, 0, 450, 350, 0, 800, 400, 100000, 0, 750, 0, 650, 0, 900, 300, 500, 0, 550])

                if win == 0:
                    embed = discord.Embed(title=f'{emojis.blade} Wheel of Fortune', color=color.color,
                                          description=f'{emojis.reply} You **lost**, try again')
                    await message.edit(embed=embed)
                    
                else:
                    collection.update_one({"_id": ctx.message.author.id}, {"$set": {"gamble_won": check["gamble_won"] + win }})

                    new_money = check["money"] + win
                    new_money = round(new_money)

                    collection.update_one({"_id": ctx.message.author.id}, {"$set": {"money": new_money}})
                    embed = discord.Embed(title=f'{emojis.blade} Wheel of Fortune', color=color.color,
                                          description=f'{emojis.reply} You **WON** ``{win}💵``, they got deposited to your **Wallet**')
                    await message.edit(embed=embed)

            else:
                embed = discord.Embed(description=f'> {emojis.false} You dont have enough **Money**, you only have ``{check["money"]}💵``', color=color.fail)


    @commands.command(brief='get your daily money', description='economy')
    @commands.cooldown(1, 2, commands.BucketType.user)
    @blacklist_check()
    async def daily(self, ctx):
        if not collection.find_one({"_id": ctx.message.author.id}):
            economy = {"_id": ctx.message.author.id, "money": 0, "level": 0, "bank_bal": 100, "bank":0, "multiplier": 1, "daily": 'none', "daily_time": 0, "weekly": 'none', "weekly_time": 0, "gamble_won": 0, "gamble_loos": 0, "passive": False}
            collection.insert_one(economy)
        check = collection.find_one({"_id": ctx.message.author.id})

        today = datetime.datetime.now()
        today = today.strftime("%m%d%H%M%S")

        if check["daily"] == 'none' or today > check["daily"]:
            money = 2500
            new_money = check["money"] + money * check["multiplier"]
            new_money = round(new_money)

            today_time = datetime.datetime.now() + datetime.timedelta(days=1)
            date_time = today_time.strftime("%m%d%H%M%S")
            timestamp = round(datetime.datetime.timestamp(today_time))
            collection.update_one({"_id": ctx.message.author.id}, {"$set": {"money": new_money}})
            collection.update_one({"_id": ctx.message.author.id}, {"$set": {"daily": date_time}})
            collection.update_one({"_id": ctx.message.author.id}, {"$set": {"daily_time": timestamp}})

            embed = discord.Embed(description=f"> {emojis.true} You claimed your **Daily** and got ``{int(money):,}💵`` added to your Wallet!", color=color.success)
            await ctx.send(embed=embed)
        else:
            daily = check["daily"]
            embed = discord.Embed(description=f'> {emojis.false} You already claimed your **Daily**, you can do it again <t:{check["daily_time"]}:R>', color=color.color)
            await ctx.send(embed=embed)

    @commands.command(brief='get your weekly money', description='economy')
    @commands.cooldown(1, 2, commands.BucketType.user)
    @blacklist_check()
    async def weekly(self, ctx):
        if not collection.find_one({"_id": ctx.message.author.id}):
            economy = {"_id": ctx.message.author.id, "money": 0, "level": 0, "bank_bal": 100, "bank":0, "multiplier": 1, "daily": 'none', "daily_time": 0, "weekly": 'none', "weekly_time": 0, "gamble_won": 0, "gamble_loos": 0, "passive": False}
            collection.insert_one(economy)

        check = collection.find_one({"_id": ctx.message.author.id})
        today = datetime.datetime.now()
        today = today.strftime("%m%d%H%M%S")

        if premium.find_one({"_id": ctx.message.author.id}):
            if check["weekly"] == 'none' or today > check["weekly"]:
                money = 20000
                new_money = check["money"] + money * check["multiplier"]
                new_money = round(new_money)

                today_time = datetime.datetime.now() + datetime.timedelta(days=7)
                date_time = today_time.strftime("%m%d%H%M%S")
                timestamp = round(datetime.datetime.timestamp(today_time))
                collection.update_one({"_id": ctx.message.author.id}, {"$set": {"money": new_money}})
                collection.update_one({"_id": ctx.message.author.id}, {"$set": {"weekly": date_time}})
                collection.update_one({"_id": ctx.message.author.id}, {"$set": {"weekly_time": timestamp}})

                embed = discord.Embed(description=f"> {emojis.true} You claimed your **Weekly** and got ``{int(money):,}💵`` added to your Wallet!", color=color.success)
                await ctx.send(embed=embed)
            else:
                daily = check["daily"]
                embed = discord.Embed(description=f'> {emojis.false} You already claimed your **Weekly**, you can do it again <t:{check["weekly_time"]}:R>', color=color.color)
                await ctx.send(embed=embed)
        else:
            px = functions.get_prefix(ctx)
            embed = discord.Embed(description=f'> {emojis.false} This Command is for **Premium** only, find more information [here](https://discord.gg/MVnhjYqfYu)', color=color.color)
            await ctx.send(embed=embed)

async def setup(client):
    await client.add_cog(economy(client))
