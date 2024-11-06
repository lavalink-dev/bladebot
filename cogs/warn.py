import discord
import pymongo
from pymongo import MongoClient
from discord.ext import commands
from utils import functions
from utils.emojis import emojis
from utils.color import color

cluster = MongoClient('mongodb+srv://blade:lolidkbruh12333333333@cluster0.wbxaj.mongodb.net/myFirstDatabase?retryWrites=true&w=majority')
db = cluster["blade"]
collection = db["warn"]
blacklist = db["blacklist"]

class warn(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(brief='warn a member', description='moderation')
    @commands.has_guild_permissions(mute_members=True)
    async def warn(self, ctx, member: discord.Member, *, reason=None):
        if member.id == ctx.guild.owner.id:
            embed = discord.Embed(description=f'> {emojis.false} Trying to **WARN** the **Owner** is crazy', color=color.fail)
            await ctx.send(embed=embed)
            return
        
        else:

            if not collection.find_one({"member": member.id, "server": ctx.guild.id}):
                warning = {"member": member.id, "server": ctx.guild.id, "warn1": '', "warn2": '', "warn3": ''}
                collection.insert_one(warning)

            check = collection.find_one({"member": member.id, "server": ctx.guild.id})

            if check['warn1'] == '':
                collection.update_one({"member": member.id, "server": ctx.guild.id}, {"$set": {"warn1": f'{reason} ¦ {ctx.message.author.id}'}})

                embed = discord.Embed(description=f'> {emojis.punishment} {member.mention} has been **warned** for: {reason} \n {emojis.reply} this is their **1** Warning', color=color.color)
                embed.set_author(name=f"{ctx.message.author}", icon_url=ctx.author.display_avatar)
                await ctx.send(embed=embed)

            elif check['warn2'] == '':
                collection.update_one({"member": member.id, "server": ctx.guild.id}, {"$set": {"warn2": f'{reason} ¦ {ctx.message.author.id}'}})
                
                embed = discord.Embed(description=f'> {emojis.punishment} {member.mention} has been **warned** for: {reason} \n {emojis.reply} this is their **2** Warning', color=color.color)
                embed.set_author(name=f"{ctx.message.author}", icon_url=ctx.author.display_avatar)
                await ctx.send(embed=embed)

            elif check['warn3'] == '':
                collection.update_one({"member": member.id, "server": ctx.guild.id}, {"$set": {"warn3": f'{reason} ¦ {ctx.message.author.id}'}})

                embed = discord.Embed(description=f'> {emojis.punishment} {member.mention} has been **warned** for: {reason} \n {emojis.reply} this is their **3** Warning', color=color.color)
                embed.set_author(name=f"{ctx.message.author}", icon_url=ctx.author.display_avatar)
                await ctx.send(embed=embed)

            else:
                collection.delete_one({"member": member.id, "server": ctx.guild.id})

                await member.ban(reason=f'Warn ; to many Warns')

                embed = discord.Embed(description=f'> {emojis.punishment} {member.mention} has been banned due to many **Warns**', color=color.color)
                embed.set_author(name=f"{ctx.message.author}", icon_url=ctx.author.display_avatar)
                await ctx.send(embed=embed)

    @commands.command(brief='see a members warns', description='moderation')
    @commands.has_guild_permissions(mute_members=True)
    async def warns(self, ctx, member: discord.Member):
        if not collection.find_one({"member": member.id, "server": ctx.guild.id}):
            embed = discord.Embed(description=f'> {emojis.false} {member.mention} has no **warns**', color=color.fail)
            await ctx.send(embed=embed)
        
        else:
            check = collection.find_one({"member": member.id, "server": ctx.guild.id})

            embed = discord.Embed(title=f'{emojis.blade} Warns', color=color.color,
                                  description=f'{emojis.reply} {member.mention} warnings \n \n')
            
            if check['warn1'] != '':
                warn1 = check['warn1']
                reason, person = warn1.split('¦')
                person = self.client.get_user(int(person))

                embed.description += f'``1.`` Warn | **Reason**: {reason} \n {emojis.reply} by: {person.mention} | ``({person.id})`` \n'

            if check['warn2'] != '':
                warn2 = check['warn2']
                reason, person = warn2.split('¦')
                person = self.client.get_user(int(person))

                embed.description += f'\n``2.`` Warn | **Reason**: {reason} \n {emojis.reply} by: {person.mention} | ``({person.id})`` \n'

            if check['warn3'] != '':
                warn3 = check['warn3']
                reason, person = warn3.split('¦')
                person = self.client.get_user(int(person))

                embed.description += f'\n``3.`` Warn | **Reason**: {reason} \n {emojis.reply} by: {person.mention} | ``({person.id})``'
            await ctx.send(embed=embed)

    @commands.command(brief='clear a members warns', description='moderation')
    @commands.has_guild_permissions(administrator=True)
    async def warnsclear(self, ctx, member: discord.Member):
        if not collection.find_one({"member": member.id, "server": ctx.guild.id}):
            embed = discord.Embed(description=f'> {emojis.false} {member.mention} has no **warns**', color=color.fail)
            await ctx.send(embed=embed)
        
        else:
            collection.delete_one({"member": member.id, "server": ctx.guild.id})
            embed = discord.Embed(description=f'> {emojis.true} {member.mention} **warns** has been **cleared**', color=color.success)
            await ctx.send(embed=embed)

async def setup(client):
    await client.add_cog(warn(client))