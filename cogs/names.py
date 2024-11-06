import discord
import pymongo
import button_paginator as pg
from pymongo import MongoClient
from discord.ext import commands
from utils import functions
from utils.emojis import emojis
from utils.color import color

cluster = MongoClient('no')
db = cluster["blade"]
collection = db["names"]
blacklist = db["blacklist"]

def blacklist_check():
    def predicate(ctx):
        if blacklist.find_one({'_id': ctx.author.id}):
            return False
        return True
    return commands.check(predicate)

class names(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_user_update(self, before, after):
        if not collection.find_one({"_id": before.id}):
            names = {"_id": before.id, "names": []}
            collection.insert_one(names)

        if before.name == after.name:
            return
        else:
            user_name = f'{before.name}#{before.discriminator}'
            collection.update_one({"_id": before.id}, {"$push": {"names": user_name}})

    @commands.command()
    @blacklist_check()
    async def clearnames(self, ctx):
        collection.delete_one({"_id": ctx.message.author.id})
        embed = discord.Embed(description=f'> {emojis.true} You **cleared** your **logged** usernames', color=color.color)
        await ctx.send(embed=embed)

    @commands.command()
    @blacklist_check()
    async def names(self, ctx, member: discord.User=None): 
        if member == None:
            member = ctx.message.author

        check = collection.find_one({"_id": member.id})

        if not collection.find_one({"_id": member.id}):
            embed = discord.Embed(description=f'> {emojis.false} They have no logged **Usernames**', color=color.fail)
            embed.set_author(name=f"{member.name}'s logged usernames", icon_url=member.display_avatar)
            await ctx.send(embed=embed)

        elif check["names"] == [] or not collection.find_one({"_id": member.id}):
            embed = discord.Embed(description=f'> {emojis.false} They have no logged **Usernames**', color=color.fail)
            embed.set_author(name=f"{member.name}'s logged usernames", icon_url=member.display_avatar)
            await ctx.send(embed=embed)
        
        else:
            i=0
            k=1
            l=0
            mes = ""
            number = []
            messages = []
            for m in check['names']: 
                mes = f"{mes}> `{k}.` **{m}**\n"
                k+=1
                l+=1
                if l == 10:
                    messages.append(mes)
                    embed = discord.Embed(description=messages[i], color=color.color)
                    embed.set_author(name=f"{member.name}'s logged usernames", icon_url=member.display_avatar)
                    number.append(embed)
                    i+=1
                    mes = ""
                    l=0
        
            messages.append(mes)
            embed = discord.Embed(description=messages[i], color=color.color)
            embed.set_author(name=f"{member.name}'s logged usernames", icon_url=member.display_avatar)
            number.append(embed)

            if len(number) > 1:
                paginator = pg.Paginator(self.client, number, ctx, invoker=ctx.author.id)
                paginator.add_button('prev', emoji= "<:left_arrow:1111012825511493764>")
                paginator.add_button('delete', emoji = "<:fail:963149868698837062>")
                paginator.add_button('next', emoji="<:right_arrow:1111012858071875594>")
                await paginator.start()  
            else:
                await ctx.send(embed=embed)


async def setup(client):
    await client.add_cog(names(client))
