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
collection = db["antialt"]
blacklist = db["blacklist"]

def blacklist_check():
    def predicate(ctx):
        if blacklist.find_one({'_id': ctx.author.id}):
            return False
        return True
    return commands.check(predicate)

class antialt(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        try:
            if collection.find_one({"_id": member.guild.id}):
                check = collection.find_one({"_id": member.guild.id})
                
                if check["antialt"] == True:

                    if member.id in check["whitelist"]:
                        return

                    now = datetime.now()
                    now = now.strftime("%Y%m%d")
                    
                    user = member.created_at
                    user = user.strftime("%Y%m%d")

                    math = int(now) - int(user)

                    if math < check["age"]:
                        await member.kick(reason='AntiAlt ; Alt Account detected')

                    if check["logs"] != 0:
                        channel = self.client.get_channel(check["logs"])
                        embed = discord.Embed(title=f'{emojis.blade} AntiAlt', color=color.color,
                        description=f'{emojis.reply} **Event**: alt detected')
                        embed.add_field(name=f"{emojis.dash} Member", value=f"{emojis.reply} {member.mention} ``{member.name}`` | ``{member.id}``", inline=False)
                        embed.add_field(name=f"{emojis.dash} Punishment:", value=f"{emojis.reply} ``kick``", inline=False)
                        await channel.send(embed=embed)

        except:
            pass

    @commands.group(pass_context=True, invoke_without_command=True, brief='kick alt accounts', description='config')
    @commands.has_guild_permissions(manage_messages=True)
    @blacklist_check()
    async def antialt(self, ctx):
        if not collection.find_one({"_id": ctx.message.guild.id}):
            antialtdb = {"_id": ctx.message.guild.id, "antialt": False, "age": 10, "logs": 0, "whitelist": []}
            collection.insert_one(antialtdb)
        await ctx.invoke()

    @antialt.command(brief='set the min. acc age in days')
    async def age(self, ctx, age: int):
        if not collection.find_one({"_id": ctx.message.guild.id}):
            antialtdb = {"_id": ctx.message.guild.id, "antialt": False, "age": 10, "logs": 0, "whitelist": []}
            collection.insert_one(antialtdb)

        embed = discord.Embed(description=f'> {emojis.true} **Succesfully** changed the Member min. Age to ``{age}``', color=color.success)
        await ctx.send(embed=embed)

    @antialt.command(brief='set the channel for the logs')
    @commands.has_guild_permissions(manage_guild=True)
    async def channel(self, ctx, channel: discord.TextChannel):
        if not collection.find_one({"_id": ctx.message.guild.id}):
            antialtdb = {"_id": ctx.message.guild.id, "antialt": False, "age": 10, "logs": 0, "whitelist": []}
            collection.insert_one(antialtdb)
        px = functions.get_prefix(ctx)

        check = collection.find_one({"_id": ctx.message.guild.id})

        if check['logs'] == 0:
            collection.update_one({"_id": ctx.message.guild.id}, {"$set": {"logs": channel.id}})
            embed = discord.Embed(description=f'> {emojis.true} **Succesfully** set {channel.mention} as **Logs** Channel', color=color.success)
            await ctx.send(embed=embed)

        elif check['logs']:
            collection.update_one({"_id": ctx.message.guild.id}, {"$set": {"logs": channel.id}})
            embed = discord.Embed(description=f'> {emojis.true} **Succesfully** changed the **Logs** Channel to {channel.mention}', color=color.success)
            await ctx.send(embed=embed)

        elif check['logs'] == channel.id:
            embed = discord.Embed(description=f'> {emojis.false} {channel.mention} is already the **Logs** channel', color=color.fail)
            await ctx.send(embed=embed)
   
    @antialt.command(brief='turn it on or off')
    @commands.has_guild_permissions(manage_messages=True)
    @blacklist_check()
    async def set(self, ctx, turn=None):
        if not collection.find_one({"_id": ctx.message.guild.id}):
            antialtdb = {"_id": ctx.message.guild.id, "antialt": False, "age": 10, "logs": 0, "whitelist": []}
            collection.insert_one(antialtdb)

        check = collection.find_one({"_id": ctx.message.guild.id})
        px = functions.get_prefix(ctx)

        if turn == None:
            embed = discord.Embed(title=f'{emojis.blade} AntiSpam', color=color.success,
            description=f'{emojis.reply} *turn the antialt on or off*')
            embed.add_field(name=f"{emojis.commands} Command:", value=f"> ``{px}antialt set [on/off]`` set antialt on or off", inline=False)
            await ctx.send(embed=embed)

        if turn == 'on' or turn == 'true':
            if check['antialt'] == True:
                embed = discord.Embed(description=f'> {emojis.false} **AntiAlt** is already **activated**', color=color.fail)
                await ctx.send(embed=embed)
            else:
                collection.update_one({"_id": ctx.message.guild.id}, {"$set": {"antialt": True}})
                embed = discord.Embed(description=f'> {emojis.true} **Succesfully** activated **AntiAlt**', color=color.success)
                await ctx.send(embed=embed)

        elif turn == 'off' or turn == 'false':
            if check['antialt'] == False:
                embed = discord.Embed(description=f'> {emojis.false} **AntiAlt** is not **activated**', color=color.fail)
                await ctx.send(embed=embed)
            else:
                collection.update_one({"_id": ctx.message.guild.id}, {"$set": {"antialt": False}})
                embed = discord.Embed(description=f'> {emojis.true} **Succesfully** deactivated **AntiAlt**', color=color.success)
                await ctx.send(embed=embed)

        else:
            embed = discord.Embed(description=f'> {emojis.false} Cant set **AntiAlt** to ``{turn}``', color=color.fail)
            await ctx.send(embed=embed)

    @antialt.command(brief='whitelist members')
    @commands.has_guild_permissions(manage_messages=True)
    @blacklist_check()
    async def whitelist(self, ctx, user: discord.Member=None):
        if not collection.find_one({"_id": ctx.message.guild.id}):
            antialtdb = {"_id": ctx.message.guild.id, "antialt": False, "age": 10, "logs": 0, "whitelist": []}
            collection.insert_one(antialtdb)
        check = collection.find_one({"_id": ctx.message.guild.id})

        if user == None:
            data = collection.find_one({"_id": ctx.guild.id })['whitelist']
            embed = discord.Embed(title=f"{emojis.blade} AntiSpam", description=f"{emojis.reply} antialt whitelist: \n", color=color.color)
            if check["whitelist"] == []:
                embed.description += f"> {emojis.false} there are no users in **whitelist**!"
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
            if user.id not in check["whitelist"]:
                collection.update_one({"_id": ctx.message.guild.id}, {"$push": {"whitelist": user.id}})
                embed = discord.Embed(description=f'> {emojis.true} {user.mention} has been added to **Whitelist**', color=color.success)
                await ctx.send(embed=embed)
            else:
                embed = discord.Embed(description=f'> {emojis.false} {user.mention} is already **Whitelisted**', color=color.fail)
                await ctx.send(embed=embed)

    @antialt.command(brief='unwhitelist members')
    @commands.has_guild_permissions(manage_messages=True)
    @blacklist_check()
    async def unwhitelist(self, ctx, user: discord.Member=None):
        if not collection.find_one({"_id": ctx.message.guild.id}):
            antialtdb = {"_id": ctx.message.guild.id, "antialt": False, "age": 10, "logs": 0, "whitelist": []}
            collection.insert_one(antialtdb)

        check = collection.find_one({"_id": ctx.message.guild.id})

        if user == None:
            embed = discord.Embed(description=f'> {emojis.false} Tag a user to Remove him from the **Whitelist**', color=color.fail)
            await ctx.send(embed=embed)
        else:
            if user.id in check["whitelist"]:
                collection.update_one({"_id": ctx.message.guild.id}, {"$pull": {"whitelist": user.id}})
                embed = discord.Embed(description=f'> {emojis.true} {user.mention} has been **Unwhitelisted**', color=color.success)
                await ctx.send(embed=embed)
            else:
                embed = discord.Embed(description=f'> {emojis.false} {user.mention} is not **Whitelisted**', color=color.fail)
                await ctx.send(embed=embed)

    @antialt.command(brief='clear antialt')
    @commands.has_guild_permissions(manage_messages=True)
    @blacklist_check()
    async def clear(self, ctx):
        if not collection.find_one({"_id": ctx.message.guild.id}):
            antialtdb = {"_id": ctx.message.guild.id, "antialt": False, "age": 10, "logs": 0, "whitelist": []}
            collection.insert_one(antialtdb)

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
    await client.add_cog(antialt(client))
