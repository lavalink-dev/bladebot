import discord
import pymongo
import platform
import button_paginator as pg
from pymongo import MongoClient
from discord.ext import commands
from discord.ui import Select, View
from utils import functions
from utils.emojis import emojis
from utils.color import color

cluster = MongoClient('mongodb+srv://blade:lolidkbruh12333333333@cluster0.wbxaj.mongodb.net/myFirstDatabase?retryWrites=true&w=majority')
db = cluster["blade"]
collection = db["blacklist"]

def blacklist_check():
    def predicate(ctx):
        if collection.find_one({'_id': ctx.author.id}):
            return False
        return True
    return commands.check(predicate)

class blacklist(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.group(pass_context=True, invoke_without_command=True, aliases=["bl"])
    @commands.is_owner()
    async def blacklist(self, ctx, user: discord.User=None, *, reason=None):
        px = functions.get_prefix(ctx)
        count = collection.count_documents({})

        if user == None:
            embed = discord.Embed(title=f"{emojis.blade} {px}blacklist", color=color.color,
            description=f'{emojis.reply} **description**: ``blacklist a user from blade``')
            embed.add_field(name=f"{emojis.commands} Command:", value=f"> ``{px}blacklist [user] [reason]``", inline=False)
            embed.add_field(name=f"{emojis.config} Infos:", value=f"> ``users`` **{count}**", inline=False)
            embed.add_field(name=f"{emojis.alias} Aliases:", value=f"```bl```", inline=False)
            await ctx.send(embed=embed)
        else:
            if not collection.find_one({"_id": user.id}):
                blacklist = {"_id": user.id, "reason": reason}
                collection.insert_one(blacklist)

                embed = discord.Embed(description=f'> {emojis.true} {user.mention} has been **Blacklisted** with the Reason: **{reason}**', color=color.success)
                await ctx.send(embed=embed)

                for guild in self.client.guilds:
                        if guild.owner.id == user.id:
                            await self.client.get_guild(int(guild.id)).leave()
            else:
                embed = discord.Embed(description=f'> {emojis.false} {user.mention} is already **Blacklisted**', color=color.fail)
                await ctx.send(embed=embed)

    @blacklist.command()
    @commands.is_owner()
    async def list(self, ctx):
        i=0
        k=1
        l=0
        mes = ""
        number = []
        messages = []
        for m in collection.find({}): 
            user = self.client.get_user(m["_id"])
            reason = m['reason']
            mes = f"{mes}`{k}.` **{user}** | ``{m['_id']}`` | reason: {reason} \n"
            k+=1
            l+=1
            if l == 10:
                messages.append(mes)
                number.append(discord.Embed(title=f"{emojis.blade} blacklist", description=messages[i], color=color.color))
                i+=1
                mes = ""
                l=0
    
        messages.append(mes)
        embed = discord.Embed(title=f"{emojis.blade} blacklist", description=messages[i], color=color.color)
        number.append(embed)

        if len(number) > 1:
            paginator = pg.Paginator(self.client, number, ctx, invoker=ctx.author.id)
            paginator.add_button('prev', emoji= "<:left_arrow:1111012825511493764>")
            paginator.add_button('delete', emoji = "<:fail:963149868698837062>")
            paginator.add_button('next', emoji="<:right_arrow:1111012858071875594>")
            await paginator.start()  
        else:
            await ctx.send(embed=embed)

    @commands.command(aliases=['ubl'])
    @commands.is_owner()
    async def unblacklist(self, ctx, user: discord.User=None):
        px = functions.get_prefix(ctx)
        count = collection.count_documents({})

        if user == None:
            embed = discord.Embed(title=f"{emojis.blade} {px}unblacklist", color=color.color,
            description=f'{emojis.reply} **description**: ``unblacklist a user from blade``')
            embed.add_field(name=f"{emojis.commands} Command:", value=f"> ``{px}unblacklist [user]``", inline=False)
            embed.add_field(name=f"{emojis.config} Infos:", value=f"> ``users`` **{count}**", inline=False)
            embed.add_field(name=f"{emojis.alias} Aliases:", value=f"```ubl```", inline=False)
        else:
            if collection.find_one({"_id": user.id}):
                collection.delete_one({"_id": user.id})

                embed = discord.Embed(description=f'> {emojis.true} {user.mention} has been **Unblacklisted**', color=color.success)
                await ctx.send(embed=embed)
            else:
                embed = discord.Embed(description=f'> {emojis.false} {user.mention} is not **Blacklisted**', color=color.f)
                await ctx.send(embed=embed)

async def setup(client):
    await client.add_cog(blacklist(client))
