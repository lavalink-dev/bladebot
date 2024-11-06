import discord
import pymongo
import json
import asyncio
from pymongo import MongoClient
from discord.ext import commands
from utils import functions
from utils.emojis import emojis
from utils.color import color

cluster = MongoClient('mongodb+srv://rip:lolidkbruh12333333333@cluster0.urnkhuo.mongodb.net/?retryWrites=true&w=majority')
db = cluster["lone"]
collection = db["responder"]
premdb = db["premium"]
blacklist = db["blacklist"]

def blacklist_check():
    def predicate(ctx):
        if blacklist.find_one({'_id': ctx.author.id}):
            return False
        return True
    return commands.check(predicate)

class autoresponder(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        try:
            with open("data/prefixes.json", "r") as f:
                prefixes = json.load(f)
            px = prefixes[str(message.guild.id)]
        except:
            px = "$"

        if px in message.content:
            return

        try:
            if collection.find_one({"_id": message.guild.id}):
                check = collection.find_one({"_id": message.guild.id})
                for messages in check['responds']:
                    autorsp_message, autorsp_reaction = messages.split('¦')

                    if "{member.id}" in autorsp_reaction:
                        autorsp_reaction = autorsp_reaction.replace("{member.mention}","%s" % (message.author.id))

                    if "{member.mention}" in autorsp_reaction:
                        autorsp_reaction = autorsp_reaction.replace("{member.mention}", "%s" % (message.author.mention))

                    if "{member.tag}" in autorsp_reaction:
                        autorsp_reaction = autorsp_reaction.replace("{member.tag}", "%s" % (message.author.discriminator))

                    if "{member.name}" in autorsp_reaction:
                        autorsp_reaction = autorsp_reaction.replace("{member.name}", "%s" % (message.author.name))

                    if "{server.name}" in autorsp_reaction:
                        autorsp_reaction = autorsp_reaction.replace("{server.name}", "%s" % (message.guild.name))

                    if "{server.id}" in autorsp_reaction:
                        autorsp_reaction = autorsp_reaction.replace("{server.id}", "%s" % (message.guild.id))

                    if autorsp_message in message.content.lower():
                        await message.channel.send(f'{autorsp_reaction}')
        except:
            pass

        await asyncio.sleep(1)

    @commands.group(pass_context=True, invoke_without_command=True, aliases=['respond', "rs"], brief='responds to messages', description='config')
    @commands.has_guild_permissions(manage_guild=True)
    @blacklist_check()
    async def autoresponder(self, ctx):
        if not collection.find_one({"_id": ctx.message.guild.id}):
            autorsp = {"_id": ctx.message.guild.id, "responds": [], "count": 0}
            collection.insert_one(autorsp)

        await ctx.invoke()

    @autoresponder.command(brief='add a reaction', description='config')
    @commands.has_guild_permissions(manage_guild=True)
    @blacklist_check()
    async def add(self, ctx, message, *, respond):
        if not collection.find_one({"_id": ctx.message.guild.id}):
            autorsp = {"_id": ctx.message.guild.id, "responds": [], "count": 0}
            collection.insert_one(autorsp)

        check = collection.find_one({"_id": ctx.message.guild.id})

        if check["count"] != 6:
            autorsp = f'{message.lower()}¦{respond}'
            collection.update_one({"_id": ctx.message.guild.id}, {"$push": {"responds": autorsp}})

            embed = discord.Embed(description=f'> {emojis.true} **Succesfully** added ``{message}`` with the **Respond** ``{respond}``', color=color.success)
            await ctx.send(embed=embed)

        else:
            if premdb.find_one({"server": ctx.message.guild.id}):
                if check["count"] < 10:
                    autorsp = f'{message.lower()}¦{respond}'
                    collection.update_one({"_id": ctx.message.guild.id}, {"$push": {"responds": autorsp}})

                    embed = discord.Embed(description=f'> {emojis.true} **Succesfully** added ``{message}`` with the **Respond** ``{respond}``', color=color.success)
                    await ctx.send(embed=embed)
                
                else:
                    embed = discord.Embed(description=f'> {emojis.false} You cant set more than ``9`` **AutoResponders**')
                    await ctx.send(embed=embed)

            else:
                embed = discord.Embed(description=f'> {emojis.false} To have more than ``6`` Responds is a **Premium** only feature, to learn more about it, join our [``Support Server``](https://discord.gg/snore)', color=color.color)
                await ctx.send(embed=embed)

    @autoresponder.command(brief='see the list of autoreactions', description='config')
    @commands.has_guild_permissions(manage_guild=True)
    @blacklist_check()
    async def list(self, ctx):
        if not collection.find_one({"_id": ctx.message.guild.id}):
            autorsp = {"_id": ctx.message.guild.id, "responds": [], "count": 0}
            collection.insert_one(autorsp)

        if not collection.find_one({"_id": ctx.message.guild.id}):
            embed = discord.Embed(description=f'> {emojis.false} There are no **Responds**', color=color.fail)
            await ctx.send(embed=embed)

        else:
            px = functions.get_prefix(ctx)
            check = collection.find_one({"_id": ctx.message.guild.id})

            embed = discord.Embed(title=f'{emojis.blade} AutoResponder', color=color.color,
            description=f'{emojis.reply} *all autoresponders* \n \n')

            num = 1

            if check['responds'] == []:
                embed.description += f"> No **Responders** set"

            for messages in check['responds']:
                autorsp_message, autorsp_reaction = messages.split('¦')
                embed.description += f"``{num}.`` **Trigger**: **{autorsp_message}** \n{emojis.reply} **Respond**: ``{autorsp_reaction}`` \n \n"

                num += 1

            await ctx.send(embed=embed)

    @autoresponder.command(brief='remove a respond', description='config')
    @commands.has_guild_permissions(manage_guild=True)
    @blacklist_check()
    async def remove(self, ctx, message):
        if not collection.find_one({"_id": ctx.message.guild.id}):
            autorsp = {"_id": ctx.message.guild.id, "responds": [], "count": 0}
            collection.insert_one(autorsp)

        if not collection.find_one({"_id": ctx.message.guild.id}):
            embed = discord.Embed(description=f'> {emojis.false} There are no **Responds**', color=color.fail)
            await ctx.send(embed=embed)
        
        else:
            num = 0

            check = collection.find_one({"_id": ctx.message.guild.id})
            for i in check['responds']:
                autorsp_message, autorsp_reaction = i.split('¦')

                if autorsp_message in message:
                    num = num+1
                    collection.update_one({"_id": ctx.message.guild.id}, {"$set": {"count": check['count'] - 1}})
                    collection.update_one({"_id": ctx.message.guild.id}, {"$pull": {"responds": i}})
            
            embed = discord.Embed(description=f'> {emojis.true} **Successfully** removed ``{num}`` **Responders** with the Trigger ``{message}``', color=color.success)
            await ctx.send(embed=embed)

    @autoresponder.command(brief='clears autoresponder', description='config')
    @commands.has_guild_permissions(manage_guild=True)
    @blacklist_check()
    async def clear(self, ctx):
        if not collection.find_one({"_id": ctx.message.guild.id}):
            autorsp = {"_id": ctx.message.guild.id, "responds": [], "count": 0}
            collection.insert_one(autorsp)

        if not collection.find_one({"_id": ctx.message.guild.id}):
            embed = discord.Embed(description=f'> {emojis.false} There are no **Responds**', color=color.fail)
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
                    collection.delete_one({"_id": ctx.message.guild.id})
                    embed = discord.Embed(description=f'> {emojis.true} **Succesfully** cleared **AutoResponders** config', color=color.success)
                    await interaction.response.edit_message(embed=embed, view=None)

            async def decline_callback(interaction):
                if interaction.user != ctx.author:
                    embed = discord.Embed(description=f"> {emojis.false} This is not your message", color=color.fail)
                    await interaction.response.send_message(embed=embed, view=None, ephemeral=True)
                    return

                else:
                    embed = discord.Embed(description=f'> {emojis.true} **AutoResponder** hasnt been **Cleared**', color=color.success)
                    await interaction.response.edit_message(embed=embed, view=None)

            accept.callback = accept_callback
            decline.callback = decline_callback

            view = discord.ui.View()
            view.add_item(item=accept)
            view.add_item(item=decline)

            embed = discord.Embed(description=f'> Are you sure to clear **AutoResponder** config?', color=color.color)
            await ctx.send(embed=embed, view=view)

async def setup(client):
    await client.add_cog(autoresponder(client))
