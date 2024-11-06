import discord
import pymongo
import datetime
import asyncio
from utils import functions
from pymongo import MongoClient
from datetime import timedelta
from discord.ext import commands
from utils.emojis import emojis
from utils.color import color

cluster = MongoClient('mongodb+srv://blade:lolidkbruh12333333333@cluster0.wbxaj.mongodb.net/myFirstDatabase?retryWrites=true&w=majority')
db = cluster["blade"]
collection = db["antilink"]
warn_collection = db["warn"]

links = ['.gg/', 'gg/', '.com', 'https://', 'http', '.org', '.rock', '.vip', '.bot', "www.", ".rip", ".lol", ".wtf", "discord.gg/"]

class antilink_event(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_message(self, message):
        if not collection.find_one({"_id": message.guild.id}):
            return

        else:
            try:
                check = collection.find_one({"_id": message.guild.id})
                if message.guild.id == check["_id"] and check["antilink"] == True:
                    if message.author.id in check["whitelist"] or message.author.bot:
                        return

                    mssg = (message.content.lower())
                    mssg = mssg.replace("°", "").replace("²", '').replace("³", '').replace("{", '').replace("[", '').replace("]", '').replace("}", '').replace("^", "").replace("!", "").replace("?", "").replace('"', "").replace("§", "").replace("$", "").replace("%", "").replace("&", "").replace("/", "").replace("(", "").replace(")", "").replace("=", "").replace("`", "").replace("{", "").replace("}", "").replace("[", "").replace("]", "").replace("+", "").replace("#", "").replace("-", "").replace("'", "").replace(",", "").replace(";", "").replace(":", "").replace("-", "").replace("_", "").replace("~", "").replace("<", "").replace(">", "").replace("|", "").replace('*', "").replace(' ', "").replace('´', "").replace('`', "").replace('á', "a").replace('é', "e").replace('í', "i").replace('ó', "o").replace('à', "a").replace('è', "e").replace('ì', "i").replace('ò', "o")

                    for link in links:
                        if link in mssg:
                            await message.delete()
                            filter_message = check["message"]
                            if "{member.id}" in filter_message:
                                filter_message = filter_message.replace("{member.mention}","%s" % (message.author.id))
                            if "{member.mention}" in filter_message:
                                filter_message = filter_message.replace("{member.mention}", "%s" % (message.author.mention))
                            if "{member.tag}" in filter_message:
                                filter_message = filter_message.replace("{member.tag}", "%s" % (message.author.discriminator))
                            if "{member.name}" in filter_message:
                                filter_message = filter_message.replace("{member.name}", "%s" % (message.author.name))
                            if "{server.name}" in filter_message:
                                filter_message = filter_message.replace("{server.name}", "%s" % (message.guild.name))
                            if "{server.id}" in filter_message:
                                filter_message = filter_message.replace("{server.id}", "%s" % (message.guild.id))

                            embed = discord.Embed(description=filter_message, color=color.fail)
                            bot_message = await message.channel.send(embed=embed)
                            await asyncio.sleep(2)
                            await bot_message.delete()
            except:
                pass

        await asyncio.sleep(1)
    
async def setup(client):
    await client.add_cog(antilink_event(client))
