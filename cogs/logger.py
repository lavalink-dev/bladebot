import discord
import pymongo
import asyncio
from utils import functions
from pymongo import MongoClient
from discord.ext import commands
from utils.emojis import emojis
from utils.color import color

cluster = MongoClient('mongodb+srv://blade:lolidkbruh12333333333@cluster0.wbxaj.mongodb.net/myFirstDatabase?retryWrites=true&w=majority')
db = cluster["blade"]
collection = db["logger"]
blacklist = db["blacklist"]

def blacklist_check():
    def predicate(ctx):
        if blacklist.find_one({'_id': ctx.author.id}):
            return False
        return True
    return commands.check(predicate)

class logger(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.group(pass_context=True, invoke_without_command=True, aliases=["log", 'logs'], brief='logs everything in the server', description='config')
    @commands.has_guild_permissions(manage_guild=True)
    @blacklist_check()
    async def logger(self, ctx):
        if not collection.find_one({'_id': ctx.message.guild.id}):
            economy = {"_id": ctx.message.guild.id, "logger": False, "whitelist": [], "channel": 0}
            collection.insert_one(economy)

        await ctx.invoke()

    @logger.command(brief='clear logs config')
    @commands.has_guild_permissions(manage_guild=True)
    async def clear(self, ctx):
        if not collection.find_one({'_id': ctx.message.guild.id}):
            economy = {"_id": ctx.message.guild.id, "logger": False, "whitelist": [], "channel": 0}
            collection.insert_one(economy)

        accept = discord.ui.Button(style=discord.ButtonStyle.green, label="accept", emoji=emojis.true)
        decline = discord.ui.Button(style=discord.ButtonStyle.red, label="decline", emoji=emojis.false)

        async def accept_callback(interaction):
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
                collection.delete_one({"_id": ctx.message.guild.id})
                embed = discord.Embed(description=f'> {emojis.true} **Successfully** cleared **Logger**', color=color.success)
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
                embed = discord.Embed(description=f"> {emojis.false} This is not your message", color=color.fail)
                await interaction.response.send_message(embed=embed, view=None, ephemeral=True)
                return

            else:
                embed = discord.Embed(description=f'> {emojis.true} Your **Logger** hasnt been **Cleared**', color=color.success)
                await interaction.response.edit_message(embed=embed, view=view)

        accept.callback = accept_callback
        decline.callback = decline_callback

        view = discord.ui.View()
        view.add_item(item=accept)
        view.add_item(item=decline)

        embed = discord.Embed(description=f'> Are you sure to clear your **Logs** config?', color=color.color)
        await ctx.send(embed=embed, view=view)

    @logger.command(brief='whitelist a member')
    @commands.has_guild_permissions(manage_guild=True)
    @blacklist_check()
    async def whitelist(self, ctx, user: discord.Member=None):
        if not collection.find_one({'_id': ctx.message.guild.id}):
            economy = {"_id": ctx.message.guild.id, "logger": False, "whitelist": [], "channel": 0}
            collection.insert_one(economy)
        check = collection.find_one({"_id": ctx.message.guild.id})

        if user == None:
            data = collection.find_one({"_id": ctx.guild.id })['whitelist']
            embed = discord.Embed(title=f"{emojis.blade} Logger", color=color.color, description=f"{emojis.reply} logger whitelist: \n")
            if check["whitelist"] == []:
                embed.description += f"No user is **Whitelisted**!"
            else:
                for i in data:
                    if ctx.bot.get_user(i) != None:
                        if ctx.bot.get_user(i) == ctx.guild.owner:
                            embed.description += f"Owner **|** <@{i}> | `{i}`\n"
                        if ctx.bot.get_user(i) != ctx.guild.owner:
                            if ctx.bot.get_user(i).bot:
                                embed.description += f"Bot **|** <@{i}> | `{i}`\n"
                            else:
                                 embed.description += f"User **|** <@{i}> | `{i}`\n"
            await ctx.send(embed=embed)
        else:
            if user.id in check['whitelist']:
                embed = discord.Embed(description=f'> {emojis.false} {user.mention} is already **Whitelisted**', color=color.fail)
                await ctx.send(embed=embed)
            else:
                collection.update_one({"_id": ctx.message.guild.id}, {"$push": {"whitelist": user.id}})
                embed = discord.Embed(description=f'> {emojis.true} {user.mention} has been **Whitelisted**', color=color.success)
                await ctx.send(embed=embed)

    @logger.command(brief='unwhitelist a member')
    @commands.has_guild_permissions(manage_guild=True)
    @blacklist_check()
    async def unwhitelist(self, ctx, user: discord.Member=None):
        if not collection.find_one({'_id': ctx.message.guild.id}):
            economy = {"_id": ctx.message.guild.id, "logger": False, "whitelist": [], "channel": 0}
            collection.insert_one(economy)
        check = collection.find_one({"_id": ctx.message.guild.id})

        if user == None:
            data = collection.find_one({"_id": ctx.guild.id })['whitelist']
            embed = discord.Embed(title=f"{emojis.blade} Logger", color=color.color, description=f"{emojis.reply} logger whitelist: \n")
            if check["whitelist"] == []:
                embed.description += f"No user is **Whitelisted**!"
            else:
                for i in data:
                    if ctx.bot.get_user(i) != None:
                        if ctx.bot.get_user(i) == ctx.guild.owner:
                            embed.description += f"Owner **|** <@{i}> | `{i}`\n"
                        if ctx.bot.get_user(i) != ctx.guild.owner:
                            if ctx.bot.get_user(i).bot:
                                embed.description += f"Bot **|** <@{i}> | `{i}`\n"
                            else:
                                 embed.description += f"User **|** <@{i}> | `{i}`\n"
            await ctx.send(embed=embed)

        else:
            if user.id in check['whitelist']:
                collection.update_one({"_id": ctx.message.guild.id}, {"$pull": {"whitelist": user.id}})
                embed = discord.Embed(description=f'> {emojis.true} {user.mention} has been **Unwhitelisted**', color=color.success)
                await ctx.send(embed=embed)
            else:
                embed = discord.Embed(description=f'> {emojis.false} {user.mention} is not **Whitelisted**', color=color.fail)
                await ctx.send(embed=embed)

    @logger.command(brief='set logger on or off')
    @commands.has_guild_permissions(manage_guild=True)
    @blacklist_check()
    async def set(self, ctx, turn=None):
        if not collection.find_one({'_id': ctx.message.guild.id}):
            economy = {"_id": ctx.message.guild.id, "logger": False, "whitelist": [], "channel": 0}
            collection.insert_one(economy)

        px = functions.get_prefix(ctx)
        check = collection.find_one({"_id": ctx.message.guild.id})

        if check["logger"] == False:
            status = f'{emojis.false} *(deactivated)*'
        if check["logger"] == True:
            status = f'{emojis.true} *(activated)*'

        if turn == None:
            embed = discord.Embed(title=f"{emojis.blade} Logger", color=color.color,
            description=f'{emojis.reply} *set the status of the logger*')
            embed.add_field(name=f"{emojis.commands} Command:", value=f"> ``{px}logger set [on/off]`` turn logger on or off", inline=False)
            embed.add_field(name=f"{emojis.config} Config:", value=f"> ``Status`` {status}", inline=False)
            await ctx.send(embed=embed)

        if turn == 'on':
            if check["logger"] == False:
                if check["channel"] == 0:
                    embed = discord.Embed(description=f'> {emojis.false} You cant turn **Logger** on, you have to create the channel first', color=color.fail)
                    await ctx.send(embed=embed)
                    return
                else:
                    collection.update_one({"_id": ctx.message.guild.id}, {"$set": {"logger": True}})
                    embed = discord.Embed(description=f'> {emojis.true} **Succesfully** activated **Logger**', color=color.success)
                    await ctx.send(embed=embed)
                    return
            if check["logger"] == True:
                embed = discord.Embed(description=f'> {emojis.false} **Logger** is already **activate**', color=color.fail)
                await ctx.send(embed=embed)
        if turn == 'off':
            if check["logger"] == True:
                collection.update_one({"_id": ctx.message.guild.id}, {"$set": {"logger": False}})
                embed = discord.Embed(description=f'> {emojis.true} **Successfully** deactivated **Logger**', color=color.success)
                await ctx.send(embed=embed)
            if check["logger"] == False:
                embed = discord.Embed(description=f'> {emojis.false} **Logger** is not **activated**', color=color.fail)
                await ctx.send(embed=embed)
        else:
            embed = discord.Embed(description=f'> {emojis.false} You cant set **Logger** to **{turn}**', color=color.fail)
            await ctx.send(embed=embed)

    @logger.command(brief='create the logger channel')
    @commands.has_guild_permissions(manage_guild=True)
    @blacklist_check()
    async def create(self, ctx):
        if not collection.find_one({'_id': ctx.message.guild.id}):
            economy = {"_id": ctx.message.guild.id, "logger": False, "whitelist": [], "channel": 0}
            collection.insert_one(economy)

        px = functions.get_prefix(ctx)
        check = collection.find_one({"_id": ctx.message.guild.id})

        if check["channel"] == 0:
            creating = discord.Embed(title=f"{emojis.blade} Logger", color=color.color,
            description=f'{emojis.reply2} {emojis.false} creating **category** \n {emojis.reply} {emojis.false} creating **channel**')
            message = await ctx.send(embed=creating)

            category_channel = await ctx.guild.create_category('server logs')
            category = discord.Embed(title=f"{emojis.blade} Logger", color=color.color,
            description=f'{emojis.reply2} {emojis.false} **category** created, waiting for **overwrite** \n {emojis.reply} {emojis.false} creating **channel**')
            await message.edit(embed=category)

            overwrites = {ctx.guild.default_role: discord.PermissionOverwrite(read_messages=False, connect=False)}
            await category_channel.edit(overwrites=overwrites)
            overwrite = discord.Embed(title=f"{emojis.blade} Logger", color=color.color,
            description=f'{emojis.reply2} {emojis.true} **overwrite** successed \n {emojis.reply} {emojis.false} waiting for **channel**')
            await message.edit(embed=overwrite)

            channel_message = await ctx.guild.create_text_channel('logs', category=category_channel)
            channel = discord.Embed(title=f"{emojis.blade} Logger", color=color.color,
            description=f'{emojis.reply2} {emojis.true} **category** done \n {emojis.reply} {emojis.true} **channel** created')
            await message.edit(embed=channel)

            finished = discord.Embed(title=f"{emojis.blade} Logger", color=color.color,
            description=f'{emojis.reply2} {emojis.true} **category** done \n {emojis.reply2} {emojis.true} **channel** created \n {emojis.reply} {emojis.true} Succesfully created **logs channel**')
            await message.edit(embed=finished)

            collection.update_one({"_id": ctx.message.guild.id}, {"$set": {"channel": channel_message.id}})
            logs_channel = discord.Embed(title=f"{emojis.blade} Logger", color=color.success,
            description=f'{emojis.reply2} This is the **channel** for the **logger** \n{emojis.reply} every action gets send here.')
            await channel_message.send(embed=logs_channel)
        else:

            try:
                channel = self.client.get_channel(check["channel"])
                embed = discord.Embed(title=f"{emojis.blade} Logger", color=color.color,
                description=f'{emojis.reply} You already have a **logs channel**: {channel.mention}')
                await ctx.send(embed=embed)

            except:
                creating = discord.Embed(title=f"{emojis.blade} Logger", color=color.color,
                description=f'{emojis.reply2} {emojis.false} **category** created, waiting for **overwrite** \n {emojis.reply} {emojis.false} creating **channel**')
                message = await ctx.send(embed=creating)

                category_channel = await ctx.guild.create_category('logger')
                category = discord.Embed(title=f"{emojis.blade} Logger", color=color.color,
                description=f'{emojis.reply2} {emojis.true} **overwrite** successed \n {emojis.reply} {emojis.false} waiting for **channel**')
                await message.edit(embed=category)

                overwrites = {ctx.guild.default_role: discord.PermissionOverwrite(read_messages=False, connect=False)}
                await category_channel.edit(overwrites=overwrites)
                overwrite = discord.Embed(title=f"{emojis.blade} Logger", color=color.color,
                description=f'{emojis.reply2} {emojis.true} **category** done \n {emojis.reply} {emojis.true} **channel** created')
                await message.edit(embed=overwrite)

                channel_message = await ctx.guild.create_text_channel('logs', category=category_channel)
                channel = discord.Embed(title=f"{emojis.blade} Logger", color=color.color,
                description=f'{emojis.reply2} {emojis.true} **category** done \n {emojis.reply} {emojis.true} **channel** created')
                await message.edit(embed=channel)

                finished = discord.Embed(title=f"{emojis.blade} Logger", color=color.success,
                description=f'{emojis.reply2} {emojis.true} **category** done \n {emojis.reply2} {emojis.true} **channel** created \n {emojis.reply} {emojis.true} Succesfully created **logs channel**')
                await message.edit(embed=finished)

                collection.update_one({"_id": ctx.message.guild.id}, {"$set": {"channel": channel_message.id}})
                logs_channel = discord.Embed(title=f"{emojis.blade} Logger", color=color.color,
                description=f'{emojis.reply2} This is the **channel** for the **logger** \n{emojis.reply} every action gets send here.')
                await channel_message.send(embed=logs_channel)

async def setup(client):
    await client.add_cog(logger(client))
