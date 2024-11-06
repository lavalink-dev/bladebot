import discord
from discord.ext import commands
from utils.emojis import emojis
import pymongo
from pymongo import MongoClient
from utils.emojis import emojis
from utils.color import color

cluster = MongoClient('mongodb+srv://blade:lolidkbruh12333333333@cluster0.wbxaj.mongodb.net/myFirstDatabase?retryWrites=true&w=majority')
db = cluster["blade"]
collection = db["staff"]
blacklist = db["blacklist"]

def blacklist_check():
    def predicate(ctx):
        if blacklist.find_one({'_id': ctx.author.id}):
            return False
        return True
    return commands.check(predicate)

class staff(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(brief='gives roles in blade')
    @commands.is_owner()
    async def staff(self, ctx, user: discord.User, role):
        if collection.find_one({"_id": user.id}):
            embed = discord.Embed(description=f'> {emojis.false} {user.mention} has already a Role', color=color.fail)
            await ctx.send(embed=embed)

        else:
            if role == 'moderator' or role == 'mod':
                role = 'Moderator'
                staff = {"_id": user.id, "role": "moderator"}
                collection.insert_one(staff)

            if role == 'developer' or role == 'dev':
                role = 'Developer'
                staff = {"_id": user.id, "role": "developer"}
                collection.insert_one(staff)

            if role == 'owner' or role == 'own':
                role = 'Owner'
                staff = {"_id": user.id, "role": "developer"}
                collection.insert_one(staff)

            embed = discord.Embed(description=f'> {emojis.true} **Succesfully** added the Role **{role}** to {user.mention}', color=color.success)
            await ctx.send(embed=embed)

    @commands.command(brief='gives roles away in blade')
    @commands.is_owner()
    async def unstaff(self, ctx, user: discord.User):
        if collection.find_one({"_id": user.id}):
            collection.delete_one({"_id": user.id})
            embed = discord.Embed(description=f'> {emojis.true} **Sucessfully** unstaffed {user.mention}', color=color.success)
            await ctx.send(embed=embed)

        else:
            embed = discord.Embed(description=f'> {emojis.false} {user.mention} is no **Staff**', color=color.fail)
            await ctx.send(embed=embed)

async def setup(client):
    await client.add_cog(staff(client))
