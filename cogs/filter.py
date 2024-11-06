import discord
import pymongo
from pymongo import MongoClient
from discord import Embed
from utils import functions
from discord.ext import commands
from utils.emojis import emojis
from utils.color import color

cluster = MongoClient('no')
db = cluster["blade"]
collection = db["filter"]
blacklist = db["blacklist"]

def blacklist_check():
    def predicate(ctx):
        if blacklist.find_one({'_id': ctx.author.id}):
            return False
        return True
    return commands.check(predicate)

class filter(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.group(pass_context=True, invoke_without_command=True, brief='filter words out of the chat', description='config')
    @commands.has_guild_permissions(manage_guild=True)
    @blacklist_check()
    async def filter(self, ctx):
        await ctx.invoke()

    @filter.command(brief='set the filter message')
    @commands.has_guild_permissions(manage_guild=True)
    @blacklist_check()
    async def message(self, ctx, *, message=None):
        if not collection.find_one({"_id": ctx.message.guild.id}):
            filter = {"_id": ctx.message.guild.id, "filter": False, "links": False, "words": [], "whitelist": [], "message_switch": True, "message": '> {member.mention}, you cant type that in **{server.name}**', 'punishment_switch': False, "punishment": 'kick'}
            collection.insert_one(filter)
        check = collection.find_one({"_id": ctx.message.guild.id})

        if message == None:
            px = functions.get_prefix(ctx)
            embed = discord.Embed(title=f'{emojis.blade} Filter', color=color.color,
            description=f'{emojis.reply} *set the filter message*')
            embed.add_field(name=f"{emojis.commands} Command:", value=f"> ``{px}filter message [message]`` set your filter message", inline=False)
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

    @filter.command(brief='turn functions on or off')
    @commands.has_guild_permissions(manage_guild=True)
    @blacklist_check()
    async def set(self, ctx, turn=None):
        if not collection.find_one({"_id": ctx.message.guild.id}):
            filter = {"_id": ctx.message.guild.id, "filter": False, "links": False, "words": [], "whitelist": [], "message": '> {member.mention}, you cant type that in **{server.name}**', 'punishment_switch': False, "punishment": 'kick'}
            collection.insert_one(filter)
        check = collection.find_one({"_id": ctx.message.guild.id})

        if turn == None:
            px = functions.get_prefix(ctx)
            embed = discord.Embed(title=f'{emojis.blade} Filter', color=color.color,
            description=f'{emojis.reply} *set different functions on or off*')
            embed.add_field(name=f"{emojis.commands} Command:", value=f"> ``{px}filter set [on/off]`` set filter on or off", inline=False)
            await ctx.send(embed=embed)

        elif turn == 'on':
            if check["filter"] == False:
                collection.update_one({"_id": ctx.message.guild.id}, {"$set": {"filter": True}})
                embed = discord.Embed(description=f'> {emojis.true} **Successfully** activated **Filter**', color=color.success)
                await ctx.send(embed=embed)

            elif check["filter"] == True:
                embed = discord.Embed(description=f'> {emojis.false} Filter is already **activated**', color=color.fail)
                await ctx.send(embed=embed)
                return

        elif turn == 'off':
            if check["filter"] == True:
                collection.update_one({"_id": ctx.message.guild.id}, {"$set": {"filter": False}})
                embed = discord.Embed(description=f'> {emojis.true} **Successfully** deactivated **Filter**', color=color.success)
                await ctx.send(embed=embed)

            elif check["filter"] == False:
                embed = discord.Embed(description=f'> {emojis.false} **Filter** is not **deactivated**', color=color.fail)
                await ctx.send(embed=embed)

        else:
            embed = discord.Embed(description=f'> {emojis.false} Cant set **Filter** to **{turn}**', color=color.fail)
            await ctx.send(embed=embed)

    @filter.command(brief='set the filter punishment')
    @commands.has_guild_permissions(manage_guild=True)
    @blacklist_check()
    async def punishment(self, ctx, punishment=None):
        if not collection.find_one({"_id": ctx.message.guild.id}):
            filter = {"_id": ctx.message.guild.id, "filter": False, "links": False, "words": [], "whitelist": [], "message_switch": True, "message": '> {member.mention}, you cant type that in **{server.name}**', 'punishment_switch': False, "punishment": 'kick'}
            collection.insert_one(filter)
        check = collection.find_one({"_id": ctx.message.guild.id})

        if punishment == None:
            px = functions.get_prefix(ctx)

            px = functions.get_prefix(ctx)
            embed = discord.Embed(title=f'{emojis.blade} Filter',
            description=f'{emojis.reply} *set the filter punishment*', color=color.color)
            embed.add_field(name=f"{emojis.commands} Command:", value=f"> ``{px}filter punishment [punishment]`` punish the member", inline=False)
            embed.add_field(name=f"{emojis.config} Punishments:", value=f"> ``on`` turns punishment on \n> ``off`` turns punishment off \n> ``kick`` kicks the user \n> ``ban`` bans the user \n> ``timeout`` timesout the user for a day \n> ``warn`` add a warn to the user", inline=False)
            await ctx.send(embed=embed)

        elif punishment == 'kick':
            collection.update_one({"_id": ctx.message.guild.id}, {"$set": {"punishment": punishment}})
            embed = discord.Embed(description=f'> {emojis.true} **Successfully** set the **Punishment** to **Kick**', color=color.success)
            await ctx.send(embed=embed)

        elif punishment == 'ban':
            collection.update_one({"_id": ctx.message.guild.id}, {"$set": {"punishment": punishment}})
            embed = discord.Embed(description=f'> {emojis.true} **Successfully** set the **Punishment** to **Ban**', color=color.success)
            await ctx.send(embed=embed)

        elif punishment == 'timeout':
            collection.update_one({"_id": ctx.message.guild.id}, {"$set": {"punishment": punishment}})
            embed = discord.Embed(description=f'> {emojis.true} **Successfully** set the **Punishment** to **Timeout**', color=color.success)
            await ctx.send(embed=embed)

        elif punishment == 'warn':
            collection.update_one({"_id": ctx.message.guild.id}, {"$set": {"punishment": punishment}})
            embed = discord.Embed(description=f'> {emojis.true} **Successfully** set the **Punishment** to **Warn**', color=color.success)
            await ctx.send(embed=embed)

        elif punishment == 'on':
            collection.update_one({"_id": ctx.message.guild.id}, {"$set": {"punishment_switch": True}})
            embed = discord.Embed(description=f'> {emojis.true} **Successfully** activated **Punishment**', color=color.success)
            await ctx.send(embed=embed)

        elif punishment == 'off':
            collection.update_one({"_id": ctx.message.guild.id}, {"$set": {"punishment_switch": False}})
            embed = discord.Embed(description=f'> {emojis.true} **Successfully** deactivated **Punishment**', color=color.success)
            await ctx.send(embed=embed)

        else:
            embed = embed = discord.Embed(description=f'> {emojis.false} Cant set **Punishment** to **{punishment}**', color=color.fail)
            await ctx.send(embed=embed)


    @filter.command(brief='add a word to the filter list')
    @commands.has_guild_permissions(manage_guild=True)
    @blacklist_check()
    async def add(self, ctx, *, word=None):
        px = functions.get_prefix(ctx)
        if not collection.find_one({"_id": ctx.message.guild.id}):
            filter = {"_id": ctx.message.guild.id, "filter": False, "links": False, "words": [], "whitelist": [], "message_switch": True, "message": '> {member.mention}, you cant type that in **{server.name}**', 'punishment_switch': False, "punishment": 'kick'}
            collection.insert_one(filter)
        check = collection.find_one({"_id": ctx.message.guild.id})

        if word == None:
            embed = discord.Embed(title=f'{emojis.blade} Filter', color=color.color,
            description=f'{emojis.reply} *add words to the filter*')
            embed.add_field(name=f"{emojis.commands} Command:", value=f"> ``{px}filter add [word]`` add a word to the filter", inline=False)
            await ctx.send(embed=embed)

        else:
            if word in check["words"]:
                embed = discord.Embed(description=f'> {emojis.false} The word ``{word}`` is already in the **Filter**', color=color.color)
                await ctx.send(embed=embed)

            else:
                collection.update_one({"_id": ctx.message.guild.id}, {"$push": {"words": word}})
                embed = discord.Embed(description=f'> {emojis.true} **Succesfully** added ``{word}`` to the Filter, it will be **Filtered** out for now on', color=color.success)
                await ctx.send(embed=embed)

    @filter.command(brief='remove a word from the filter list')
    @commands.has_guild_permissions(manage_guild=True)
    @blacklist_check()
    async def remove(self, ctx, *, word=None):
        px = functions.get_prefix(ctx)
        if not collection.find_one({"_id": ctx.message.guild.id}):
            filter = {"_id": ctx.message.guild.id, "filter": False, "links": False, "words": [], "whitelist": [], "message_switch": True, "message": '> {member.mention}, you cant type that in **{server.name}**', 'punishment_switch': False, "punishment": 'kick'}
            collection.insert_one(filter)
        check = collection.find_one({"_id": ctx.message.guild.id})

        if word == None:
            embed = discord.Embed(title=f'{emojis.blade} Filter', color=color.color,
            description=f'{emojis.reply} *remove words to the filter*')
            embed.add_field(name=f"{emojis.commands} Command:", value=f"> ``{px}filter remove [word]`` remove a word to the filter", inline=False)
            await ctx.send(embed=embed)

        else:
            if word not in check["words"]:
                embed = discord.Embed(description=f'> {emojis.false} The word ``{word}`` is not in the **Filter**', color=color.fail)
                await ctx.send(embed=embed)

            else:
                collection.update_one({"_id": ctx.message.guild.id}, {"$pull": {"words": word}})
                embed = discord.Embed(description=f'> {emojis.true} **Succesfully** remove ``{word}`` from the **Filter**, it wont be **Filtered** anymore', color=color.success)
                await ctx.send(embed=embed)

    @filter.command(brief='clear the filter config')
    @commands.has_guild_permissions(manage_guild=True)
    @blacklist_check()
    async def clear(self, ctx):
        if not collection.find_one({"_id": ctx.message.guild.id}):
            filter = {"_id": ctx.message.guild.id, "filter": False, "links": False, "words": [], "whitelist": [], "message_switch": True, "message": '> {member.mention}, you cant type that in **{server.name}**', 'punishment_switch': False, "punishment": 'kick'}
            collection.insert_one(filter)

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
                embed = discord.Embed(description=f'> {emojis.true} You cleared the **Filter** config', color=color.success)
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
                embed = discord.Embed(description=f'> {emojis.true} The **Filter** hasnt been **Cleared**', color=color.success)
                await interaction.response.edit_message(embed=embed, view=view)

        accept.callback = accept_callback
        decline.callback = decline_callback

        view = discord.ui.View()
        view.add_item(item=accept)
        view.add_item(item=decline)

        embed = discord.Embed(description=f'> Are you sure to clear your **Filter** config?', color=color.color)
        await ctx.send(embed=embed, view=view)


    @filter.command(brief='see all filter words')
    @commands.has_guild_permissions(manage_guild=True)
    @blacklist_check()
    async def list(self, ctx):
        if not collection.find_one({"_id": ctx.message.guild.id}):
            filter = {"_id": ctx.message.guild.id, "filter": False, "links": False, "words": [], "whitelist": [], "message_switch": True, "message": '> {member.mention}, you cant type that in **{server.name}**', 'punishment_switch': False, "punishment": 'kick'}
            collection.insert_one(filter)
        check = collection.find_one({"_id": ctx.message.guild.id})

        embed = discord.Embed(title=f'{emojis.blade} Filter', color=color.color,
        description=f'{emojis.reply} filtered words: \n \n')
        i = 0

        if check["words"] == []:
            embed.description += f'> {emojis.false} there are no **Filtered Words**'
        elif check["words"]:
            for word in check["words"]:
                i = i + 1
                embed.description += f"> ``{i}.`` **{word}**\n"
        await ctx.send(embed=embed)

    @filter.command(brief='whitelist members')
    @commands.has_guild_permissions(manage_guild=True)
    @blacklist_check()
    async def whitelist(self, ctx, user: discord.Member=None):
        if not collection.find_one({"_id": ctx.message.guild.id}):
            filter = {"_id": ctx.message.guild.id, "filter": False, "links": False, "words": [], "whitelist": [], "message_switch": True, "message": '> {member.mention}, you cant type that in **{server.name}**', 'punishment_switch': False, "punishment": 'kick'}
            collection.insert_one(filter)
        check = collection.find_one({"_id": ctx.message.guild.id})

        if user == None:
            data = collection.find_one({"_id": ctx.guild.id })['whitelist']
            embed = discord.Embed(title=f"{emojis.blade} Filter", color=color.color,
                                description=f"{emojis.reply} filter whitelist: \n \n")
            if check["whitelist"] == []:
                embed.description += f"> {emojis.false} there are no users in **whitelist**!"
            else:
                for i in data:
                    if ctx.bot.get_user(i) != None:
                        if ctx.bot.get_user(i) == ctx.guild.owner:
                            embed.description += f"``Owner`` <@{i}> | ``{i}``\n"
                        if ctx.bot.get_user(i) != ctx.guild.owner:
                            if ctx.bot.get_user(i).bot:
                                embed.description += f"``Bot`` <@{i}> | ``{i}``\n"
                            else:
                                 embed.description += f"``Member`` <@{i}> | ``{i}``\n"
            await ctx.send(embed=embed)
        else:
            if user.id not in check["whitelist"]:
                collection.update_one({"_id": ctx.message.guild.id}, {"$push": {"whitelist": user.id}})
                embed = discord.Embed(description=f'> {emojis.true} {user.mention} has been added to **Whitelist**', color=color.success)
                await ctx.send(embed=embed)
            else:
                embed = discord.Embed(description=f'> {emojis.false} {user.mention} is already **Whitelisted**', color=color.fail)
                await ctx.send(embed=embed)

    @filter.command(brief='unwhitelist members')
    @commands.has_guild_permissions(manage_guild=True)
    @blacklist_check()
    async def unwhitelist(self, ctx, user: discord.Member=None):
        if not collection.find_one({"_id": ctx.message.guild.id}):
            filter = {"_id": ctx.message.guild.id, "filter": False, "links": False, "words": [], "whitelist": [], "message_switch": True, "message": '> {member.mention}, you cant type that in **{server.name}**', 'punishment_switch': False, "punishment": 'kick'}
            collection.insert_one(filter)
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

async def setup(client):
    await client.add_cog(filter(client))
