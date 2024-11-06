import discord
import datetime
import pymongo
import asyncio
from datetime import datetime
from pymongo import MongoClient
from datetime import timedelta
from discord.ext import commands
from utils import functions
from utils.emojis import emojis
from utils.color import color 

cluster = MongoClient('mongodb+srv://blade:lolidkbruh12333333333@cluster0.wbxaj.mongodb.net/myFirstDatabase?retryWrites=true&w=majority')
db = cluster["blade"]
collection = db["whitelist"]
blacklist = db["blacklist"]

def blacklist_check():
    def predicate(ctx):
        if blacklist.find_one({'_id': ctx.author.id}):
            return False
        return True
    return commands.check(predicate)

class whitelist(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        try:
            if collection.find_one({"_id": member.guild.id}):
                check = collection.find_one({"_id": member.guild.id})
                
                if check["whitelist"] == True:

                    if member.id in check["whitelisted"]:
                        return

                    await member.kick(reason='Whitelist ; Member not on the Whitelist')

        except:
            pass

    @commands.group(pass_context=True, invoke_without_command=True, brief='add whitelist', description='config')
    @commands.has_guild_permissions(manage_messages=True)
    @blacklist_check()
    async def whitelist(self, ctx):
        if not collection.find_one({"_id": ctx.message.guild.id}):
            whitelistdb = {"_id": ctx.message.guild.id, "whitelist": False,  "whitelisted": []}
            collection.insert_one(whitelistdb)
        await ctx.invoke()

    @whitelist.command(brief='turn it on or off')
    @commands.has_guild_permissions(manage_messages=True)
    @blacklist_check()
    async def set(self, ctx, turn=None):
        if not collection.find_one({"_id": ctx.message.guild.id}):
            whitelistdb = {"_id": ctx.message.guild.id, "whitelist": False,  "whitelisted": []}
            collection.insert_one(whitelistdb)

        check = collection.find_one({"_id": ctx.message.guild.id})
        px = functions.get_prefix(ctx)

        if turn == None:
            embed = discord.Embed(title=f'{emojis.blade} Whitelist', color=color.success,
            description=f'{emojis.reply} *turn the whitelist on or off*')
            embed.add_field(name=f"{emojis.commands} Command:", value=f"> ``{px}whitelist set [on/off]`` set whitelist on or off", inline=False)
            await ctx.send(embed=embed)

        if turn == 'on' or turn == 'true':
            if check['whitelist'] == True:
                embed = discord.Embed(description=f'> {emojis.false} **Whitelist** is already **activated**', color=color.fail)
                await ctx.send(embed=embed)
            else:
                collection.update_one({"_id": ctx.message.guild.id}, {"$set": {"whitelist": True}})
                embed = discord.Embed(description=f'> {emojis.true} **Succesfully** activated **Whitelist**', color=color.success)
                await ctx.send(embed=embed)

        elif turn == 'off' or turn == 'false':
            if check['whitelist'] == False:
                embed = discord.Embed(description=f'> {emojis.false} **Whitelist** is not **activated**', color=color.fail)
                await ctx.send(embed=embed)
            else:
                collection.update_one({"_id": ctx.message.guild.id}, {"$set": {"whitelist": False}})
                embed = discord.Embed(description=f'> {emojis.true} **Succesfully** deactivated **Whitelist**', color=color.success)
                await ctx.send(embed=embed)

        else:
            embed = discord.Embed(description=f'> {emojis.false} Cant set **Whitelist** to ``{turn}``', color=color.fail)
            await ctx.send(embed=embed)

    @whitelist.command(brief='whitelisted members')
    @commands.has_guild_permissions(manage_messages=True)
    @blacklist_check()
    async def whitelisted(self, ctx, user: discord.Member=None):
        if not collection.find_one({"_id": ctx.message.guild.id}):
            whitelistdb = {"_id": ctx.message.guild.id, "whitelist": False,  "whitelisted": []}
            collection.insert_one(whitelistdb)
        check = collection.find_one({"_id": ctx.message.guild.id})

        if user == None:
            data = collection.find_one({"_id": ctx.guild.id })['whitelisted']
            embed = discord.Embed(title=f"{emojis.blade} AntiSpam", description=f"{emojis.reply} whitelist whitelisted: \n", color=color.color)
            if check["whitelisted"] == []:
                embed.description += f"> {emojis.false} there are no users in **whitelisted**!"
            else:
                for i in data:
                    if ctx.bot.get_user(i) != None:
                        if ctx.bot.get_user(i) == ctx.guild.owner:
                            embed.description += f"``Owner`` <@{i}> | `{i}`\n"
                        if ctx.bot.get_user(i) != ctx.guild.owner:
                            if ctx.bot.get_user(i).bot:
                                embed.description += f"``Bot`` <@{i}> | `{i}`\n"
                            else:
                                 embed.description += f"``User`` <@{i}> | `{i}`\n"
            await ctx.send(embed=embed)
        else:
            if user.id not in check["whitelisted"]:
                collection.update_one({"_id": ctx.message.guild.id}, {"$push": {"whitelisted": user.id}})
                embed = discord.Embed(description=f'> {emojis.true} {user.mention} has been added to **Whitelist**', color=color.success)
                await ctx.send(embed=embed)
            else:
                embed = discord.Embed(description=f'> {emojis.false} {user.mention} is already **Whitelisted**', color=color.fail)
                await ctx.send(embed=embed)

    @whitelist.command(brief='unwhitelisted members')
    @commands.has_guild_permissions(manage_messages=True)
    @blacklist_check()
    async def unwhitelisted(self, ctx, user: discord.Member=None):
        if not collection.find_one({"_id": ctx.message.guild.id}):
            whitelistdb = {"_id": ctx.message.guild.id, "whitelist": False,  "whitelisted": []}
            collection.insert_one(whitelistdb)

        check = collection.find_one({"_id": ctx.message.guild.id})

        if user == None:
            embed = discord.Embed(description=f'> {emojis.false} Tag a user to Remove him from the **Whitelist**', color=color.fail)
            await ctx.send(embed=embed)
        else:
            if user.id in check["whitelisted"]:
                collection.update_one({"_id": ctx.message.guild.id}, {"$pull": {"whitelisted": user.id}})
                embed = discord.Embed(description=f'> {emojis.true} {user.mention} has been **Unwhitelisteded**', color=color.success)
                await ctx.send(embed=embed)
            else:
                embed = discord.Embed(description=f'> {emojis.false} {user.mention} is not **Whitelisted**', color=color.fail)
                await ctx.send(embed=embed)

    @whitelist.command(brief='clear whitelist')
    @commands.has_guild_permissions(manage_messages=True)
    @blacklist_check()
    async def clear(self, ctx):
        if not collection.find_one({"_id": ctx.message.guild.id}):
            whitelistdb = {"_id": ctx.message.guild.id, "whitelist": False,  "whitelisted": []}
            collection.insert_one(whitelistdb)

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
                embed = discord.Embed(description=f'> {emojis.false} You cleared the **AntiSpam** config', color=color.success)
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
                embed = discord.Embed(description=f'> {emojis.true} The **AntiSpam** hasnt been **Cleared**', color=color.success)
                await interaction.response.edit_message(embed=embed, view=view)

        accept.callback = accept_callback
        decline.callback = decline_callback

        view = discord.ui.View()
        view.add_item(item=accept)
        view.add_item(item=decline)

        embed = discord.Embed(description=f'> Are you sure to clear your **AntiSpam** config?', color=color.color)
        await ctx.send(embed=embed, view=view)

async def setup(client):
    await client.add_cog(whitelist(client))


async def setup(client):
    await client.add_cog(whitelist(client))
