import discord
import datetime
import pymongo
from pymongo import MongoClient
from datetime import timedelta
from discord.ext import commands
from utils import functions
from utils.emojis import emojis
from utils.color import color 

cluster = MongoClient('no')
db = cluster["blade"]
collection = db["antilink"]
warn_collection = db["warn"]
blacklist = db["blacklist"]

def blacklist_check():
    def predicate(ctx):
        if blacklist.find_one({'_id': ctx.author.id}):
            return False
        return True
    return commands.check(predicate)

class antilink(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.group(pass_context=True, invoke_without_command=True, aliases=['al'], brief='clean links out of your chat', description='config')
    @commands.has_guild_permissions(manage_messages=True)
    @blacklist_check()
    async def antilink(self, ctx):
        if not collection.find_one({"_id": ctx.message.guild.id}):
            antilinkdb = {"_id": ctx.message.guild.id, "antilink": False, "punishment": 'timeout', 'filter_invite': False, 'filter_links': False, "whitelist": []}
            collection.insert_one(antilinkdb)

        await ctx.invoke()
        
    @antilink.command(brief='set the punishment due link sending')
    @commands.has_guild_permissions(manage_messages=True)
    @blacklist_check()
    async def punishment(self, ctx, punishment=None):
        if not collection.find_one({"_id": ctx.message.guild.id}):
            antilinkdb = {"_id": ctx.message.guild.id, "antilink": False, "punishment": 'timeout', "message": '> You cant sent **Links** in {server.name}', "whitelist": []}
            collection.insert_one(antilinkdb)

        check = collection.find_one({"_id": ctx.message.guild.id})
        px = functions.get_prefix(ctx)

        if punishment == None:
            embed = discord.Embed(title=f'AntiLink', color=color.color,
            description=f'{emojis.reply} *set the antilink messages*')
            embed.add_field(name=f"{emojis.commands} Command:", value=f"> ``{px}antilinkconfig message [message]`` set your antilinking message", inline=False)
            embed.add_field(name=f"{emojis.config} Punishment:", value="> ``ban`` bans the member \n> ``kick`` kicks the member \n> ``timeout`` timeouts the member for 1 day", inline=False)
            embed.add_field(name=f"{emojis.config} Current Punishment:", value=f"> ``Punishment`` {check['punishment']}", inline=False)
            await ctx.send(embed=embed)

        else:
            if punishment == 'ban':
                collection.update_one({"_id": ctx.message.guild.id}, {"$set": {"punishment": 'ban'}})
                embed = discord.Embed(description=f'> {emojis.true} **Succesfully** set the **Punishment** to: ``ban``', color=color.success)
                await ctx.send(embed=embed)

            elif punishment == 'kick':
                collection.update_one({"_id": ctx.message.guild.id}, {"$set": {"punishment": 'kick'}})
                embed = discord.Embed(description=f'> {emojis.true} **Succesfully** set the **Punishment** to: ``kick``', color=color.success)
                await ctx.send(embed=embed)

            elif punishment == 'timeout':
                collection.update_one({"_id": ctx.message.guild.id}, {"$set": {"punishment": 'timeout'}})
                embed = discord.Embed(description=f'> {emojis.true} **Succesfully** set the **Punishment** to: ``timeout``', color=color.success)
                await ctx.send(embed=embed)

            elif punishment == 'warn':
                collection.update_one({"_id": ctx.message.guild.id}, {"$set": {"punishment": 'warn'}})
                embed = discord.Embed(description=f'> {emojis.true} **Succesfully** set the **Punishment** to: ``warn``', color=color.success)
                await ctx.send(embed=embed)
            
            else:
                embed = discord.Embed(description=f'> {emojis.false} Cant set the **Punishment** to ``{function}``', color=color.fail)
                await ctx.send(embed=embed)

    @antilink.command(brief='set the antilink message')
    @commands.has_guild_permissions(manage_guild=True)
    @blacklist_check()
    async def message(self, ctx, *, message=None):
        if not collection.find_one({"_id": ctx.message.guild.id}):
            antilinkdb = {"_id": ctx.message.guild.id, "antilink": False, "punishment": 'timeout', "message": '> You cant sent **Links** in {server.name}', "whitelist": []}
            collection.insert_one(antilinkdb)
        check = collection.find_one({"_id": ctx.message.guild.id})

        if message == None:
            px = functions.get_prefix(ctx)
            embed = discord.Embed(title=f'{emojis.blade} Filter', color=color.color,
            description=f'{emojis.reply} *set the filter message*')
            embed.add_field(name=f"{emojis.commands} Command:", value=f"> ``{px}antilink message [message]`` set your filter message", inline=False)
            embed.add_field(name=f"{emojis.config} Variables:", value="> ``{member.mention}`` mentions the member \n> ``{member.name}`` shows the members name \n> ``{member.tag}`` shows the members tag \n> ``{member.id}`` shows members id \n> ``{server.name}`` shows the name of the server \n> ``{server.id}`` shows the id of the server", inline=False)
            embed.add_field(name=f"{emojis.config} Current Message:", value=f"{check['message']}", inline=False)
            await ctx.send(embed=embed)
            
        else:
            collection.update_one({"_id": ctx.message.guild.id}, {"$set": {"message": message}})

            if "{member.id}" in message:
                message = message.replace("{member.mention}","%s" % (ctx.author.id))
            if "{member.mention}" in message:
                message = message.replace("{member.mention}", "%s" % (ctx.author.mention))
            if "{member.tag}" in message:
                message = message.replace("{member.tag}", "%s" % (ctx.author.discriminator))
            if "{member.name}" in message:
                message = message.replace("{member.name}", "%s" % (ctx.author.name))
            if "{server.name}" in message:
                message = message.replace("{server.name}", "%s" % (ctx.guild.name))
            if "{server.id}" in message:
                message = message.replace("{server.id}", "%s" % (ctx.guild.id))
            embed = discord.Embed(description=f'{emojis.true} Succesfully changed the **Warning** message to: \n{message}', color=color.success)
            await ctx.send(embed=embed)

    @antilink.command(brief='activate or deactivate antilink')
    @commands.has_guild_permissions(manage_messages=True)
    @blacklist_check()
    async def set(self, ctx, turn=None):
        if not collection.find_one({"_id": ctx.message.guild.id}):
            antilinkdb = {"_id": ctx.message.guild.id, "antilink": False, "punishment": 'timeout', "message": '> You cant sent **Links** in {server.name}', "whitelist": []}
            collection.insert_one(antilinkdb)

        check = collection.find_one({"_id": ctx.message.guild.id})
        px = functions.get_prefix(ctx)

        if turn == None:
            embed = discord.Embed(title=f'AntiLink', color=color.success,
            description=f'{emojis.reply} *turn the antilink on or off*')
            embed.add_field(name=f"{emojis.commands} Command:", value=f"> ``{px}antilink set [on/off]`` set antilink on or off", inline=False)
            await ctx.send(embed=embed)

        if turn == 'on' or turn == 'true':
            if check['antilink'] == True:
                embed = discord.Embed(description=f'> {emojis.false} **AntiLink** is already **activated**', color=color.fail)
                await ctx.send(embed=embed)
            else:
                collection.update_one({"_id": ctx.message.guild.id}, {"$set": {"antilink": True}})
                embed = discord.Embed(description=f'> {emojis.true} **Succesfully** activated **AntiLink**', color=color.success)
                await ctx.send(embed=embed)

        elif turn == 'off' or turn == 'false':
            if check['antilink'] == False:
                embed = discord.Embed(description=f'> {emojis.false} **AntiLink** is not **activated**', color=color.fail)
                await ctx.send(embed=embed)
            else:
                collection.update_one({"_id": ctx.message.guild.id}, {"$set": {"antilink": False}})
                embed = discord.Embed(description=f'> {emojis.true} **Succesfully** deactivated **AntiLink**', color=color.success)
                await ctx.send(embed=embed)

        else:
            embed = discord.Embed(description=f'> {emojis.false} Cant set **AntiLink** to ``{turn}``', color=color.fail)
            await ctx.send(embed=embed)

    @antilink.command(brief='whitelist members')
    @commands.has_guild_permissions(manage_messages=True)
    @blacklist_check()
    async def whitelist(self, ctx, user: discord.Member=None):
        if not collection.find_one({"_id": ctx.message.guild.id}):
            antilinkdb = {"_id": ctx.message.guild.id, "antilink": False, "punishment": 'timeout', "message": '> You cant sent **Links** in {server.name}', "whitelist": []}
            collection.insert_one(antilinkdb)
        check = collection.find_one({"_id": ctx.message.guild.id})

        if user == None:
            data = collection.find_one({"_id": ctx.guild.id })['whitelist']
            embed = discord.Embed(title=f"AntiLink", description=f"{emojis.reply} whitelisted members: \n \n", color=color.color)
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

    @antilink.command(brief='unwhitelist members')
    @commands.has_guild_permissions(manage_messages=True)
    @blacklist_check()
    async def unwhitelist(self, ctx, user: discord.Member=None):
        if not collection.find_one({"_id": ctx.message.guild.id}):
            antilinkdb = {"_id": ctx.message.guild.id, "antilink": False, "punishment": 'timeout', "message": '> You cant sent **Links** in {server.name}', "whitelist": []}
            collection.insert_one(antilinkdb)
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

    @antilink.command(brief='clear the antilink config')
    @commands.has_guild_permissions(manage_messages=True)
    @blacklist_check()
    async def clear(self, ctx):
        if not collection.find_one({"_id": ctx.message.guild.id}):
            antilinkdb = {"_id": ctx.message.guild.id, "antilink": False, "punishment": 'timeout', "message": '> You cant sent **Links** in {server.name}', "whitelist": []}
            collection.insert_one(antilinkdb)

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
                embed = discord.Embed(description=f'> {emojis.false} You cleared the **antilink** config', color=color.success)
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
                embed = discord.Embed(description=f'> {emojis.true} The **antilink** hasnt been **Cleared**', color=color.success)
                await interaction.response.edit_message(embed=embed, view=view)

        accept.callback = accept_callback
        decline.callback = decline_callback

        view = discord.ui.View()
        view.add_item(item=accept)
        view.add_item(item=decline)

        embed = discord.Embed(description=f'> Are you sure to clear your **antilink** config?', color=color.color)
        await ctx.send(embed=embed, view=view)

async def setup(client):
    await client.add_cog(antilink(client))
