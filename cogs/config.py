import discord
import asyncio
import json
import pymongo
from pymongo import MongoClient
from discord.ext import commands
from utils import functions
from utils.emojis import emojis
from utils.color import color

cluster = MongoClient('mongodb+srv://blade:lolidkbruh12333333333@cluster0.wbxaj.mongodb.net/myFirstDatabase?retryWrites=true&w=majority')
db = cluster["blade"]
collection = db["blacklist"]
welcome = db["welcome"]
leave = db["leave"]
joindm = db["joindm"]
joinping = db["joinping"]
autorole = db["autorole"]
antinuke = db["antinuke"]
antispam = db["antispam"]
reaction = db["reaction"]
responder = db["responder"]
filter = db["filter"]
level = db["level"]
levelconfig = db["levelconfig"]
antilink = db["antilink"]
ticket = db["ticket"]
logger = db["logger"]
voicemaster = db["voicemaster"]
boost = db["boost"]

autopfp = db["autopfp"]
tags = db["tags"]
tracker = db["tracker"]
onlyimg = db["onlyimg"]
silence = db["silence"]

blacklist = db["blacklist"]

def blacklist_check():
    def predicate(ctx):
        if collection.find_one({'_id': ctx.author.id}):
            return False
        return True
    return commands.check(predicate)

class config(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(brief='set the server prefix', aliases=['px'], description='config')
    @commands.has_permissions(administrator = True)
    @blacklist_check()
    async def prefix(self, ctx, prefix=None):
        if prefix == None:
            px = functions.get_prefix(ctx)
            embed = discord.Embed(title=f'{emojis.blade} Prefix', color=color.color,
            description=f'{emojis.reply} *change the bots server prefix*')
            embed.add_field(name=f"{emojis.commands} Command:", value=f"> ``{px}prefix [preifx]`` change the bots server prefix", inline=False)
            embed.add_field(name=f"{emojis.config} Current Prefix:", value=f"``{px}``", inline=False)
            await ctx.send(embed=embed)


        elif len(prefix) > 1:
            await ctx.send('nuh uh, to long :3')

        else:
            with open("data/prefixes.json", "r") as f:
                prefixes = json.load(f)

            prefixes[str(ctx.guild.id)] = prefix

            with open("data/prefixes.json", "w") as f:
                json.dump(prefixes,f)

            embed = discord.Embed(description=f'> {emojis.true} Changed the **Server Prefix** to ``{prefix}``', color=color.success)
            await ctx.send(embed=embed)

    @commands.command()
    async def toggle(self, ctx, feature):
        if feature == 'antinuke':
            if antinuke.find_one({"_id": ctx.guild.id}):
                if antinuke.find_one({"_id": ctx.guild.id})["antinuke"] == True:
                    antinuke.update_one({"_id": ctx.message.guild.id}, {"$set": {"antinuke": False}})
                    embed = discord.Embed(description=f"> {emojis.true} **Successfully** deactivated **AntiNuke**", color=color.success)
                    await ctx.send(embed=embed)

                elif antinuke.find_one({"_id": ctx.guild.id})["antinuke"] == False:
                    antinuke.update_one({"_id": ctx.message.guild.id}, {"$set": {"antinuke": True}})
                    embed = discord.Embed(description=f"> {emojis.true} **Successfully** activated **AntiNuke**", color=color.success)
                    await ctx.send(embed=embed)
            if not antinuke.find_one({"_id": ctx.guild.id}):
                embed = discord.Embed(description=f'> {emojis.false} **AntiNuke** is not Configured', color=color.fail)
                await ctx.send(embed=embed)

        elif feature == 'welcome':
            if welcome.find_one({"_id": ctx.guild.id}):
                if welcome.find_one({"_id": ctx.guild.id})["welcome"] == True:
                    welcome.update_one({"_id": ctx.message.guild.id}, {"$set": {"welcome": False}})
                    embed = discord.Embed(description=f"> {emojis.true} **Successfully** deactivated **Welcome**", color=color.success)
                    await ctx.send(embed=embed)

                elif welcome.find_one({"_id": ctx.guild.id})["welcome"] == False:
                    welcome.update_one({"_id": ctx.message.guild.id}, {"$set": {"welcome": True}})
                    embed = discord.Embed(description=f"> {emojis.true} **Successfully** activated **Welcome**", color=color.success)
                    await ctx.send(embed=embed)
            if not welcome.find_one({"_id": ctx.guild.id}):
                embed = discord.Embed(description=f'> {emojis.false} **Welcome** is not Configured', color=color.fail)
                await ctx.send(embed=embed)

        elif feature == 'leave':
            if leave.find_one({"_id": ctx.guild.id}):
                if leave.find_one({"_id": ctx.guild.id})["leave"] == True:
                    leave.update_one({"_id": ctx.message.guild.id}, {"$set": {"leave": False}})
                    embed = discord.Embed(description=f"> {emojis.true} **Successfully** deactivated **Leave**", color=color.success)
                    await ctx.send(embed=embed)

                elif leave.find_one({"_id": ctx.guild.id})["leave"] == False:
                    leave.update_one({"_id": ctx.message.guild.id}, {"$set": {"leave": True}})
                    embed = discord.Embed(description=f"> {emojis.true} **Successfully** activated **Leave**", color=color.success)
                    await ctx.send(embed=embed)
            if not leave.find_one({"_id": ctx.guild.id}):
                embed = discord.Embed(description=f'> {emojis.false} **Leave** is not Configured', color=color.fail)
                await ctx.send(embed=embed)

        elif feature == 'voicemaster':
            if voicemaster.find_one({"_id": ctx.guild.id}):
                voicemaster.delete_one({"_id": ctx.guild.id})
                embed = discord.Embed(description=f"> {emojis.true} **Successfully** deleted **VoiceMaster**", color=color.success)
                await ctx.send(embed=embed)
            if not voicemaster.find_one({"_id": ctx.guild.id}):
                embed = discord.Embed(description=f'> {emojis.false} **VoiceMaster** is not Configured', color=color.fail)
                await ctx.send(embed=embed)

        else:
            embed = discord.Embed(description=f"> {emojis.true} Couldnt find **{feature}**", color=color.fail)
            embed.set_footer(text='NOT EVERY FEATURE IS IN HERE YET !')
            await ctx.send(embed=embed)

    @commands.command(brief='every config settings', description='config')
    @commands.has_permissions(administrator = True)
    @blacklist_check()
    async def settings(self, ctx):
        px = functions.get_prefix(ctx)

        embed = discord.Embed(title=f"{emojis.blade} **{ctx.guild.name}** Server Settings", color=color.color)
        embed.set_thumbnail(url=ctx.guild.icon)
        embed.set_footer(text=f'{px}toggle [feature] - to toggle/reset a feature')

        if antinuke.find_one({"_id": ctx.guild.id}):
            embed.add_field(name=f"{emojis.dash} AntiNuke", value=f"{emojis.reply2} {emojis.true} Configurated \n{emojis.reply2} Turn: **{antinuke.find_one({'_id': ctx.guild.id})['antinuke']}** \n{emojis.reply} logs: <#{antinuke.find_one({'_id': ctx.guild.id})['logs']}>")
        else:
            embed.add_field(name=f"{emojis.dash} AntiNuke", value=f"{emojis.reply} {emojis.false} None")

        if welcome.find_one({"_id": ctx.guild.id}):
            embed.add_field(name=f"{emojis.dash} Welcome", value=f"{emojis.reply2} {emojis.true} Configurated \n{emojis.reply2} Turn: **{welcome.find_one({'_id': ctx.guild.id})['welcome']}** \n{emojis.reply} Channel: <#{welcome.find_one({'_id': ctx.guild.id})['channel']}>")
        else:
            embed.add_field(name=f"{emojis.dash} Welcome", value=f"{emojis.reply} {emojis.false} None")

        if autorole.find_one({"_id": ctx.guild.id}):
            embed.add_field(name=f"{emojis.dash} AutoRole", value=f"{emojis.reply2} {emojis.true} Configurated \n{emojis.reply2} Turn: **{autorole.find_one({'_id': ctx.guild.id})['switch']}** \n{emojis.reply} Roles: ``{autorole.find_one({'_id': ctx.guild.id})['count']}``")
        else:
            embed.add_field(name=f"{emojis.dash} AutoRole", value=f"{emojis.reply} {emojis.false} None")

        if leave.find_one({"_id": ctx.guild.id}):
            embed.add_field(name=f"{emojis.dash} Leave", value=f"{emojis.reply2} {emojis.true} Configurated \n{emojis.reply2} Turn: **{leave.find_one({'_id': ctx.guild.id})['leave']}** \n{emojis.reply} Channel: <#{leave.find_one({'_id': ctx.guild.id})['channel']}>")
        else:
            embed.add_field(name=f"{emojis.dash} Leave", value=f"{emojis.reply} {emojis.false} None")

        if levelconfig.find_one({"_id": ctx.guild.id}):
            embed.add_field(name=f"{emojis.dash} Level", value=f"{emojis.reply2} {emojis.true} Configurated \n{emojis.reply2} Turn: **{levelconfig.find_one({'_id': ctx.guild.id})['level']}** \n{emojis.reply} Mention: **{levelconfig.find_one({'_id': ctx.guild.id})['mention']}**")
        else:
            embed.add_field(name=f"{emojis.dash} Level", value=f"{emojis.reply} {emojis.false} None")

        if antilink.find_one({"_id": ctx.guild.id}):
            embed.add_field(name=f"{emojis.dash} AntiLink", value=f"{emojis.reply2} {emojis.true} Configurated \n{emojis.reply2} Turn: **{antilink.find_one({'_id': ctx.guild.id})['antilink']}** \n{emojis.reply} Punishment: **{antilink.find_one({'_id': ctx.guild.id})['punishment']}**")
        else:
            embed.add_field(name=f"{emojis.dash} AntiLink", value=f"{emojis.reply} {emojis.false} None")

        if filter.find_one({"_id": ctx.guild.id}):
            embed.add_field(name=f"{emojis.dash} Filter", value=f"{emojis.reply2} {emojis.true} Configurated \n{emojis.reply2} Turn: **{filter.find_one({'_id': ctx.guild.id})['filter']}** \n{emojis.reply} Punishment: **{filter.find_one({'_id': ctx.guild.id})['punishment']}**")
        else:
            embed.add_field(name=f"{emojis.dash} Filter", value=f"{emojis.reply} {emojis.false} None")

        if antispam.find_one({"_id": ctx.guild.id}):
            embed.add_field(name=f"{emojis.dash} AntiSpam", value=f"{emojis.reply2} {emojis.true} Configurated \n{emojis.reply2} Turn: **{filter.find_one({'_id': ctx.guild.id})['filter']}** \n{emojis.reply} Punishment: **{filter.find_one({'_id': ctx.guild.id})['punishment']}**")
        else:
            embed.add_field(name=f"{emojis.dash} AntiSpam", value=f"{emojis.reply} {emojis.false} None")

        if logger.find_one({"_id": ctx.guild.id}):
            embed.add_field(name=f"{emojis.dash} Logger", value=f"{emojis.reply2} {emojis.true} Configurated \n{emojis.reply2} Turn: **{logger.find_one({'_id': ctx.guild.id})['logger']}** \n{emojis.reply} Channel: <#{logger.find_one({'_id': ctx.guild.id})['channel']}>")
        else:
            embed.add_field(name=f"{emojis.dash} Logger", value=f"{emojis.reply} {emojis.false} None")

        if ticket.find_one({"_id": ctx.guild.id}):
            embed.add_field(name=f"{emojis.dash} Ticket", value=f"{emojis.reply2} {emojis.true} Configurated \n{emojis.reply} Channel: <#{ticket.find_one({'_id': ctx.guild.id})['channel']}>")
        else:
            embed.add_field(name=f"{emojis.dash} Ticket", value=f"{emojis.reply} {emojis.false} None")

        if responder.find_one({"_id": ctx.guild.id}):
            embed.add_field(name=f"{emojis.dash} AutoResponder", value=f"{emojis.reply2} {emojis.true} Configurated \n{emojis.reply} Responds: **{responder.find_one({'_id': ctx.guild.id})['count']}**")
        else:
            embed.add_field(name=f"{emojis.dash} AutoResponder", value=f"{emojis.reply} {emojis.false} None")

        if reaction.find_one({"_id": ctx.guild.id}):
            embed.add_field(name=f"{emojis.dash} AutoReaction", value=f"{emojis.reply2} {emojis.true} Configurated \n{emojis.reply} Responds: **{reaction.find_one({'_id': ctx.guild.id})['count']}**")
        else:
            embed.add_field(name=f"{emojis.dash} AutoReaction", value=f"{emojis.reply} {emojis.false} None")

        if joindm.find_one({"_id": ctx.guild.id}):
            embed.add_field(name=f"{emojis.dash} JoinDM", value=f"{emojis.reply2} {emojis.true} Configurated \n{emojis.reply} Turn: **{joindm.find_one({'_id': ctx.guild.id})['joindm']}**")
        else:
            embed.add_field(name=f"{emojis.dash} JoinDM", value=f"{emojis.reply} {emojis.false} None")

        if joinping.find_one({"_id": ctx.guild.id}):
            embed.add_field(name=f"{emojis.dash} JoinPing", value=f"{emojis.reply} {emojis.true} Configurated \n{emojis.reply2} Turn: **{joinping.find_one({'_id': ctx.guild.id})['joinping']}** \n{emojis.reply} Channels: **{joinping.find_one({'_id': ctx.guild.id})['count']}**")
        else:
            embed.add_field(name=f"{emojis.dash} JoinPing", value=f"{emojis.reply} {emojis.false} None")

        if voicemaster.find_one({"_id": ctx.guild.id}):
            embed.add_field(name=f"{emojis.dash} VoiceMaster", value=f"{emojis.reply2} {emojis.true} Configurated \n{emojis.reply2} Panel: <#{voicemaster.find_one({'_id': ctx.guild.id})['panel']}> \n{emojis.reply} Create: <#{voicemaster.find_one({'_id': ctx.guild.id})['channel']}>")
        else:
            embed.add_field(name=f"{emojis.dash} VoiceMaster", value=f"{emojis.reply} {emojis.false} None")

        if boost.find_one({"_id": ctx.guild.id}):
            embed.add_field(name=f"{emojis.dash} Boost", value=f"{emojis.reply2} {emojis.true} Configurated \n{emojis.reply2} Turn: **{boost.find_one({'_id': ctx.guild.id})['boost']}** \n{emojis.reply} Channel: <#{boost.find_one({'_id': ctx.guild.id})['channel']}>")
        else:
            embed.add_field(name=f"{emojis.dash} Boost", value=f"{emojis.reply} {emojis.false} None")

        await ctx.send(embed=embed)

async def setup(client):
    await client.add_cog(config(client))
