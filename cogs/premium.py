import discord
import pymongo
import random
import aiohttp
from pymongo import MongoClient
from discord.ext import commands
from utils import functions
from utils.emojis import emojis
from utils.color import color

cluster = MongoClient('no')
db = cluster["blade"]
collection = db["premium"]
blacklist = db["blacklist"]

def blacklist_check():
    def predicate(ctx):
        if blacklist.find_one({'_id': ctx.author.id}):
            return False
        return True
    return commands.check(predicate)

class premium(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(brief='trasnfer your premium to a other server', description='premium')
    async def transfer(self, ctx, id=None):
        if collection.find_one({"_id": ctx.message.author.id}):
            check = collection.find_one({"_id": ctx.message.author.id})
            transfer = collection.find_one({"_id": ctx.message.author.id})['transfers']
            if id == None:
                id = ctx.message.guild.id

            if check['transfers'] == 0:
                embed = discord.Embed(description=f'> {emojis.false} You dont have any **Transfers**, get more transfers [``here``](https://discord.gg/MVnhjYqfYu)', color=color.color)
                await ctx.send(embed=embed)
            else:
                if collection.find_one({"server": ctx.message.guild.id}):
                    embed = discord.Embed(description=f'> {emojis.false} This Server has already **Premium**', color=color.fail)
                    await ctx.send(embed=embed)

                else:
                    accept = discord.ui.Button(style=discord.ButtonStyle.green, label="accept", emoji=emojis.true)
                    decline = discord.ui.Button(style=discord.ButtonStyle.red, label="decline", emoji=emojis.false)

                    async def accept_callback(interaction):
                        if interaction.user != ctx.author:
                            embed = discord.Embed(description=f"> {emojis.false} This is not your message", color=color.fail)
                            await interaction.response.send_message(embed=embed, view=None, ephemeral=True)
                            return
                        else:
                            collection.update_one({"_id": ctx.message.author.id}, {"$set": {"server": id}})
                            collection.update_one({"_id": ctx.message.author.id}, {"$set": {"transfers": transfer -1 }})

                            if id == ctx.guild.id:
                                text = f'{ctx.guild.name} | {id}'
                            else:
                                text = id

                            embed = discord.Embed(description=f'> {emojis.true} Transfered your Server **Premium** to ``{text}``', color=color.success)
                            await interaction.response.edit_message(embed=embed)

                    async def decline_callback(interaction):
                        accept = discord.ui.Button(style=discord.ButtonStyle.green, label="accept", emoji=emojis.true, disabled = True)
                        decline = discord.ui.Button(style=discord.ButtonStyle.red, label="decline", emoji=emojis.false, disabled = True)

                        accept.callback = accept_callback
                        decline.callback = decline_callback

                        view = discord.ui.View()
                        view.add_item(item=accept)
                        view.add_item(item=decline)

                        if interaction.user != ctx.author:
                            embed = discord.Embed(description=f"> {emojis.false} This is not your message", color=color.fail)
                            await interaction.response.send_message(embed=embed, view=None, ephemeral=True)
                            return
                        else:
                            embed = discord.Embed(description=f'> {emojis.true} You didnt added Server **Premium** to ``{ctx.guild.name}`` ``({ctx.guild.id})``', color=color.success)
                            await interaction.response.edit_message(embed=embed, view=None)

                    accept.callback = accept_callback
                    decline.callback = decline_callback

                    view = discord.ui.View()
                    view.add_item(item=accept)
                    view.add_item(item=decline)

                    embed = discord.Embed(description=f'> Are you sure to transfer your Server **Premium** to ``{ctx.guild.name}`` ``({ctx.guild.id})``?', color=color.color)
                    await ctx.send(embed=embed, view=view)

        else:
            px = functions.get_prefix(ctx)
            embed = discord.Embed(description=f'> {emojis.false} This Command is for **Premium** only, find more information [``here``](https://discord.gg/MVnhjYqfYu)', color=color.color)
            await ctx.send(embed=embed)

    @commands.command(aliases=['addprem'], brief='add premium to a server', description='premium')
    async def addpremium(self, ctx):
        if collection.find_one({"_id": ctx.message.author.id}):
            check = collection.find_one({"_id": ctx.message.author.id})
            if check['server'] == 0:
                if collection.find_one({"_id": ctx.message.author.guild.id}):
                    embed = discord.Embed(description=f'> {emojis.false} This **Server** already have **Premium**')
                    await ctx.send(embed=embed)

                else:
                    accept = discord.ui.Button(style=discord.ButtonStyle.green, label="accept", emoji=emojis.true)
                    decline = discord.ui.Button(style=discord.ButtonStyle.red, label="decline", emoji=emojis.false)

                    async def accept_callback(interaction):
                        if interaction.user != ctx.author:
                            embed = discord.Embed(description=f"> {emojis.false} This is not your message", color=color.fail)
                            await interaction.response.send_message(embed=embed, view=None, ephemeral=True)
                            return
                        else:
                            collection.update_one({"_id": ctx.message.author.id}, {"$set": {"server": ctx.guild.id}})
                            embed = discord.Embed(description=f'> {emojis.true} You added **Premium** to ``{ctx.guild.name}`` ``({ctx.guild.id})``', color=color.success)
                            await interaction.response.edit_message(embed=embed)

                    async def decline_callback(interaction):
                        accept = discord.ui.Button(style=discord.ButtonStyle.green, label="accept", emoji=emojis.true, disabled = True)
                        decline = discord.ui.Button(style=discord.ButtonStyle.red, label="decline", emoji=emojis.false, disabled = True)

                        accept.callback = accept_callback
                        decline.callback = decline_callback

                        view = discord.ui.View()
                        view.add_item(item=accept)
                        view.add_item(item=decline)

                        if interaction.user != ctx.author:
                            embed = discord.Embed(description=f"> {emojis.false} This is not your message", color=color.fail)
                            await interaction.response.send_message(embed=embed, view=None, ephemeral=True)
                            return
                        else:
                            embed = discord.Embed(description=f'> {emojis.true} You didnt added your Server **Premium** to ``{ctx.guild.name}`` ``({ctx.guild.id})``', color=color.success)
                            await interaction.response.edit_message(embed=embed, view=None)

                    accept.callback = accept_callback
                    decline.callback = decline_callback

                    view = discord.ui.View()
                    view.add_item(item=accept)
                    view.add_item(item=decline)

                    embed = discord.Embed(description=f'> Are you sure to add Server **Premium** to ``{ctx.guild.name}`` ``({ctx.guild.id})``?', color=color.color)
                    await ctx.send(embed=embed, view=view)

            else:
                embed = discord.Embed(description=f'> {emojis.false} You already gave ``{check["server"]}`` your Server **Premium**, get more information [``here``](https://discord.gg/MVnhjYqfYu)', color=color.color)
                await ctx.send(embed=embed)
        else:
            px = functions.get_prefix(ctx)
            embed = discord.Embed(description=f'> {emojis.false} This Command is for **Premium** only, find more information [``here``](https://discord.gg/MVnhjYqfYu)', color=color.color)
            await ctx.send(embed=embed)

    @commands.command(brief='claim your premium', description='premium')
    @blacklist_check()
    async def claim(self, ctx):
        if ctx.guild.id == 782275066020233236:
            role = discord.utils.get(ctx.guild.roles, name="prem")
            guild = ctx.guild

            if role in ctx.message.author.roles:
                if not collection.find_one({"_id": ctx.message.author.id}):
                    premium = {"_id": ctx.message.author.id, "reason": 'Membership', "server": 0, "transfers": 1}
                    collection.insert_one(premium)

                    embed = discord.Embed(description=f'> {emojis.true} You successfully **claimed** your **Premium**, have fun!', color=color.success)
                    await ctx.send(embed=embed)
                else:
                    embed = discord.Embed(description=f'> {emojis.false} You already **claimed** your **Premium**, have fun man', color=color.color)
                    await ctx.send(embed=embed)
            else:
                embed = discord.Embed(description=f'> {emojis.false} To **claim** your **Premium** you need to Purchase our [``Membership Here``](https://ko-fi.com/bladebot#tier16728358017680)', color=color.color)
                await ctx.send(embed=embed)
        else:
            embed = discord.Embed(description=f'> {emojis.false} Join the [``Support Server``](https://discord.gg/MVnhjYqfYu) to claim your **Premium**', color=color.color)
            await ctx.send(embed=embed)

    @commands.group(pass_context=True, invoke_without_command=True, aliases=["prem"])
    @commands.is_owner()
    @blacklist_check()
    async def premium(self, ctx):
        px = functions.get_prefix(ctx)
        count = collection.count_documents({})

        embed = discord.Embed(title=f"{emojis.blade} {px}premium", color=color.color,
        description=f'{emojis.reply} **description**: ``commands for blades premium management``')
        embed.add_field(name=f"{emojis.commands} Commands:", value=f"> ``{px}premium add [user] [reason]`` \n> ``{px}premium remove [user]`` \n> ``{px}premium transfers [user] [amount]``  \n> ``{px}premium list`` \n> ``{px}premium check [user]``", inline=False)
        embed.add_field(name=f"{emojis.config} Infos:", value=f"> ``users`` **{count}**", inline=False)
        embed.add_field(name=f"{emojis.alias} Aliases:", value=f"```prem```", inline=False)
        await ctx.send(embed=embed)

    @premium.command()
    @commands.is_owner()
    @blacklist_check()
    async def check(self, ctx, user: discord.User=None):
        px = functions.get_prefix(ctx)
        if user == None:
            embed = discord.Embed(title=f"{emojis.blade} {px}premium check", color=color.color,
            description=f'{emojis.reply} **description**: ``check a user`')
            embed.add_field(name=f'{emojis.commands} Commands:', value=f'{emojis.reply} ``{px}premium check [user]``', inline=False)
            embed.add_field(name=f'{emojis.alias} Aliases:', value=f'```none```', inline=False)
            await ctx.send(embed=embed)
        else:
            if collection.find_one({"_id": user.id}):
                check = collection.find_one({"_id": user.id})
                embed = discord.Embed(description=f'> {emojis.true} **{user.name}** has **Premium** with the Reason ``{check["reason"]}`` and got ``{check["transfers"]}`` Transfers \n {emojis.reply} **Premium Server**: ``{check["server"]}``', color=color.success)
                await ctx.send(embed=embed)
            else:
                embed = discord.Embed(description=f'> {emojis.false} **{user.name}** dosnt have **Premium**', color=color.fail)
                await ctx.send(embed=embed)

    @premium.command()
    @commands.is_owner()
    @blacklist_check()
    async def list(self, ctx, user: discord.User=None, *, reason=None):
        embed = discord.Embed(title=f'{emojis.blade} Premium', color=color.color,
        description=f'{emojis.reply} *all users with premium* \n \n')

        num = 0
        for i in collection.find({}):
            num = num + 1
            user = self.client.get_user(i["_id"])
            embed.description += f'``{num}.`` **{user}** | ``{i["_id"]}`` | reason: {i["reason"]} | transfers: {i["transfers"]} \n'

        await ctx.send(embed=embed)

    @premium.command(aliases=["allow", "auth"])
    @commands.is_owner()
    @blacklist_check()
    async def add(self, ctx, user: discord.User=None, *, reason=None):
        px = functions.get_prefix(ctx)
        if user == None:
            embed = discord.Embed(title=f"{emojis.blade} {px}premium add", color=color.color,
            description=f'{emojis.reply} **description**: ``grant a user premium``')
            embed.add_field(name=f'{emojis.commands} Commands:', value=f'{emojis.reply} ``{px}premium add [user] [reason]``', inline=False)
            embed.add_field(name=f'{emojis.alias} Aliases:', value=f'```allow, auth```', inline=False)
            await ctx.send(embed=embed)
        else:
            if collection.find_one({"_id": user.id}):
                embed = discord.Embed(description=f'> {emojis.false} **{user.name}** has already **Premium**', color=color.fail)
                await ctx.send(embed=embed)
                return
            else:
                premium = {"_id": user.id, "reason": reason, "server": 0, "transfers": 1}
                collection.insert_one(premium)
                embed = discord.Embed(description=f'> {emojis.true} **Premium** has been added to **{user.name}**, with reason: ``{reason}`` \n {emojis.reply} {emojis.false} Sending **Direct Message**...', color=color.success)
                message = await ctx.send(embed=embed)

                try:
                    dm = discord.Embed(description=f'> You have been granted **Premium**, by **{ctx.author.name}**, with reason: ``{reason}`` \n {emojis.reply} To add **Premium** write ``$addpremium | $addprem`` in the Server you want to add Premium', color=color.color)
                    await user.send(embed=dm)
                    dm_send = discord.Embed(description=f'> {emojis.true} **Premium** has been added to **{user.name}**, with reason: ``{reason}`` \n {emojis.reply} {emojis.true} **Direct Message** got sent', color=color.success)
                    await message.edit(embed=dm_send)
                except:
                    dm_send = discord.Embed(description=f'> {emojis.true} **Premium** has been added to **{user.name}**, with reason: ``{reason}`` \n {emojis.reply} {emojis.false} Couldnt send a **Direct Message**', color=color.fail)
                    await message.edit(embed=dm_send)

    @premium.command(aliases=["deny", "deauth"])
    @commands.is_owner()
    @blacklist_check()
    async def remove(self, ctx, user: discord.User=None):
        px = functions.get_prefix(ctx)
        if user == None:
            embed = discord.Embed(title=f"{emojis.blade} {px}premium remove", color=color.color,
            description=f'{emojis.reply} **description**: ``remove a user premium``')
            embed.add_field(name=f'{emojis.commands} Commands:', value=f'> ``{px}premium remove [user]``', inline=False)
            embed.add_field(name=f'{emojis.alias} Aliases:', value=f'```deny, deauth```', inline=False)
            await ctx.send(embed=embed)

        else:
            if collection.find_one({"_id": user.id}):
                collection.delete_one({"_id": user.id})
                embed = discord.Embed(description=f'> {emojis.true} **Premium** has been removed from **{user.name}** \n {emojis.reply} {emojis.false} Sending **Direct Message**...', color=color.success)
                message = await ctx.send(embed=embed)

                try:
                    dm = discord.Embed(description=f'> You have been removed from **Premium**, by **{ctx.author.name}**', color=color.color)
                    await user.send(embed=dm)
                    dm_send = discord.Embed(description=f'> {emojis.true} **Premium** has been removed from **{user.name}** \n {emojis.reply} {emojis.true} **Direct Message** got sent', color=color.success)
                    await message.edit(embed=dm_send)
                except:
                    dm_send = discord.Embed(description=f'> {emojis.true} **Premium** has been removed from **{user.name}** \n {emojis.reply} {emojis.false} Couldnt send a **Direct Message**', color=color.fail)
                    await message.edit(embed=dm_send)

            else:
                embed = discord.Embed(description=f'> {emojis.false} **{user.name}** dosnt have **Premium**', color=color.fail)
                await ctx.send(embed=embed)

    @premium.command(aliases=["transfer", "tf"])
    @commands.is_owner()
    @blacklist_check()
    async def transfers(self, ctx, user: discord.User=None, *, amount: int=None):
        px = functions.get_prefix(ctx)
        if user == None and amount == None:
            embed = discord.Embed(title=f"{emojis.blade} {px}premium add", color=color.color,
            description=f'{emojis.reply} **description**: ``grant a user premium``')
            embed.add_field(name=f'{emojis.commands} Commands:', value=f'{emojis.reply} ``{px}premium transfers [user] [amount]``', inline=False)
            embed.add_field(name=f'{emojis.alias} Aliases:', value=f'```transfer, tf```', inline=False)
            await ctx.send(embed=embed)
        else:
            if collection.find_one({"_id": user.id}):
                transfer = collection.find_one({"_id": user.id})['transfers']
                collection.update_one({"_id": user.id}, {"$set": {"transfers": transfer + amount }})
                embed = discord.Embed(description=f'> {emojis.true} Added **{user.name}** ``{amount}`` transfers', color=color.success)
                await ctx.send(embed=embed)
            else:
                embed = discord.Embed(description=f'> {emojis.false} **{user.name}** dosnt have **Premium**', color=color.fail)
                await ctx.send(embed=embed)

    @commands.command(brief='premium test command', description='premium')
    @blacklist_check()
    async def lol(self, ctx):
        if collection.find_one({"_id": ctx.message.author.id}):
            await ctx.send('lol')
        else:
            px = functions.get_prefix(ctx)
            embed = discord.Embed(description=f'> {emojis.false} how tf are you to broke to use this lil ass command u broke ass kid nah cmon nigga, get yo money up and use this command after u bought premium, its not that hard be fr', color=color.color)
            await ctx.send(embed=embed)

    @commands.command(brief='see feet ig', description='premium')
    @blacklist_check()
    async def feet(self, ctx):
        if collection.find_one({"_id": ctx.message.author.id}):
            if ctx.channel.is_nsfw():
                async with aiohttp.ClientSession() as cs:
                    async with cs.get('https://purrbot.site/api/img/nsfw/fuck/gif') as r:
                        res = await r.json()
                embed = discord.Embed(color=color.color,
                description=f"> Tasty Feet")
                embed.set_image(url=res["link"])
                await ctx.send(embed=embed)
            else:
                embed = discord.Embed(description=f"> {emojis.false} ``NSFW`` must be **enabled** to use this command", color=color.fail)
                await ctx.send(embed=embed)
        else:
            px = functions.get_prefix(ctx)
            embed = discord.Embed(description=f'> {emojis.false} This command is a **Premium** only feature, to learn more about it, join our [``Support Server``](https://discord.gg/snore)', color=color.color)
            await ctx.send(embed=embed)

    @commands.command(brief='fuck a member', description='premium')
    @blacklist_check()
    async def fuck(self, ctx, user2: discord.Member=None):
        if collection.find_one({"_id": ctx.message.author.id}):
            if ctx.channel.is_nsfw():
                if user2 == None:
                    embed = discord.Embed(description='> tag a other user.', color=color.color)
                    await ctx.send(embed=embed)
                    return
                if user2 == ctx.message.author:
                    self  = ['are you lonely or some?', 'it dosnt work like this', 'that is sad..', 'go find you someone', 'sad moment for the singles', 'if you have nobody, just say that', ':(', 'ask someone', 'go on tinder']
                    await ctx.send(f'{random.choice(self)}')
                else:
                    async with aiohttp.ClientSession() as cs:
                        async with cs.get('https://purrbot.site/api/img/nsfw/fuck/gif') as r:
                            res = await r.json()
                    embed = discord.Embed(color=color.color,
                    description=f"> **{ctx.message.author.mention}** fucks **{user2.mention}** ;).")
                    embed.set_image(url=res["link"])
                    await ctx.send(embed=embed)
            else:
                embed = discord.Embed(description=f"> {emojis.false} ``NSFW`` must be **enabled** to use this command", color=color.fail)
                await ctx.send(embed=embed)
        else:
            px = functions.get_prefix(ctx)
            embed = discord.Embed(description=f'> {emojis.false} This command is a **Premium** only feature, to learn more about it, join our [``Support Server``](https://discord.gg/snore)', color=color.color)
            await ctx.send(embed=embed)

    @commands.command(brief='masturbate', description='premium')
    @blacklist_check()
    async def masturbate(self, ctx):
        if collection.find_one({"_id": ctx.message.author.id}):
            if ctx.channel.is_nsfw():
                async with aiohttp.ClientSession() as cs:
                    async with cs.get('https://purrbot.site/api/img/nsfw/solo/gif') as r:
                        res = await r.json()
                embed = discord.Embed(color=color.color,
                description=f"> {ctx.message.author.mention} started to Masturbate")
                embed.set_image(url=res["link"])
                await ctx.send(embed=embed)
            else:
                embed = discord.Embed(description=f"> {emojis.false} ``NSFW`` must be **enabled** to use this command", color=color.fail)
                await ctx.send(embed=embed)
        else:
            px = functions.get_prefix(ctx)
            embed = discord.Embed(description=f'> {emojis.false} This command is a **Premium** only feature, to learn more about it, join our [``Support Server``](https://discord.gg/snore)', color=color.color)
            await ctx.send(embed=embed)

async def setup(client):
    await client.add_cog(premium(client))
