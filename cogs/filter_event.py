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
collection = db["filter"]
warn_collection = db["warn"]

class filter_event(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_message(self, message):
        if not collection.find_one({"_id": message.guild.id}):
            return
        else:
            try:
                check = collection.find_one({"_id": message.guild.id})
                if message.guild.id == check["_id"]:
                    if not message.author.bot:
                        if check["filter"] == True:
                            mssg = (message.content.lower())
                            mssg = mssg.replace("°", "").replace("²", '').replace("³", '').replace("{", '').replace("[", '').replace("]", '').replace("}", '').replace("^", "").replace("!", "").replace("?", "").replace('"', "").replace("§", "").replace("$", "").replace("%", "").replace("&", "").replace("/", "").replace("(", "").replace(")", "").replace("=", "").replace("`", "").replace("{", "").replace("}", "").replace("[", "").replace("]", "").replace("+", "").replace("#", "").replace("-", "").replace(".", "").replace(",", "").replace(";", "").replace(":", "").replace("-", "").replace("_", "").replace("~", "").replace("<", "").replace(">", "").replace("|", "").replace('*', "").replace(' ', "").replace('´', "").replace('`', "").replace('á', "a").replace('é', "e").replace('í', "i").replace('ó', "o").replace('à', "a").replace('è', "e").replace('ì', "i").replace('ò', "o")

                            if message.author.id in check["whitelist"]:
                                return
                            else:
                                for filter in check["words"]:
                                    if filter in mssg:
                                        if message.content.startswith('-filter'):
                                            return
                                        else:
                                            check = collection.find_one({"_id": message.guild.id})
                                            await message.delete()
                                            if check['message_switch'] == True:
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

                                                embed = discord.Embed(description=f'{filter_message}', color=color.fail)
                                                bot_message = await message.channel.send(embed=embed, delete_after=5)

                                            if check['punishment_switch'] == True:
                                                if check['punishment'] == 'kick':
                                                    await message.author.kick(reason='Filter ; wrote a Filtered Word')

                                                if check['punishment'] == 'ban':
                                                    await message.author.ban(reason='Filter ; wrote a Filtered Word')

                                                if check['punishment'] == 'timeout':
                                                    await message.author.timeout(timedelta(days = 7), reason='Filter ; wrote a Filtered Word')

                                                if check['punishment'] == 'warn':
                                                    if not warn_collection.find_one({"member": message.author.id, "server": message.guild.id}):
                                                        warning = {"member": message.author.id, "server": message.guild.id, "warn1": '', "warn2": '', "warn3": ''}
                                                        collection.insert_one(warning)

                                                    warn_check = warn_collection.find_one({"member": message.author.id, "server": message.guild.id})
                                                    if warn_check['warn1'] == '':
                                                        warn_collection.update_one({"member": message.author.id, "server": message.guild.id}, {"$set": {"warn1": f'Filter ; wrote a Filtered Word ¦ {self.client.user.id}'}})

                                                    elif warn_check['warn2'] == '':
                                                        warn_collection.update_one({"member": message.author.id, "server": message.guild.id}, {"$set": {"warn2": f'Filter ; wrote a Filtered Word ¦ {self.client.user.id}'}})

                                                    elif warn_check['warn3'] == '':
                                                        warn_collection.update_one({"member": message.author.id, "server": message.guild.id}, {"$set": {"warn3": f'Filter ; wrote a Filtered Word ¦ {self.client.user.id}'}})
                                                            
                                                    else:
                                                        await message.author.ban(reason='Warn ; To many Warns (banned due Filter)')

                else:
                    return
            except:
                pass

        await asyncio.sleep(1)
    
async def setup(client):
    await client.add_cog(filter_event(client))
