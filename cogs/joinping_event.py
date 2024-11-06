import discord
import pymongo
import asyncio
from pymongo import MongoClient
from discord.utils import get
from discord.ext import commands

cluster = MongoClient('mongodb+srv://blade:lolidkbruh12333333333@cluster0.wbxaj.mongodb.net/myFirstDatabase?retryWrites=true&w=majority')
db = cluster["blade"]
collection = db["joinping"]

class joinping_event(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        guild = member.guild.id
        if not collection.find_one({"_id": guild}):
            return
        
        else:
            try:
                check = collection.find_one({"_id": guild})
                server = check["_id"]

                if member.guild.id == server:
                    try:
                        data = collection.find_one({"_id": guild})['channels']

                        if check['turn'] == True:
                            for i in data:
                                channel = self.client.get_channel(i)
                                message = await channel.send(f'{member.mention}')
                                await message.delete()

                                await asyncio.sleep(1)
                    except:
                        pass
            except:
                pass

        await asyncio.sleep(2)

async def setup(client):
    await client.add_cog(joinping_event(client))
