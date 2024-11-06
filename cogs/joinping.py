import discord
import pymongo
from pymongo import MongoClient
from discord.utils import get
from discord.ext import commands
from utils import functions
from utils.emojis import emojis
from utils.color import color

cluster = MongoClient('no')
db = cluster["blade"]
collection = db["joinping"]
premium = db["premium"]
blacklist = db["blacklist"]

def blacklist_check():
    def predicate(ctx):
        if blacklist.find_one({'_id': ctx.author.id}):
            return False
        return True
    return commands.check(predicate)

class joinping(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.group(pass_context=True, invoke_without_command=True, brief='pings when a member joins', description='config')
    @commands.has_guild_permissions(manage_guild=True)
    @blacklist_check()
    async def joinping(self, ctx):
        await ctx.invoke()

    @joinping.command(brief='clear the joinping config')
    @commands.has_guild_permissions(manage_guild=True)
    @blacklist_check()
    async def clear(self, ctx):
        if not collection.find_one({"_id": ctx.message.guild.id}):
            joinpings = {"_id": ctx.message.guild.id, "turn": False, "channels": [], "count": 0}
            collection.insert_one(joinpings)

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
                embed = discord.Embed(description=f'> {emojis.true} You cleared the **JoinPing** config', color=color.success)
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
                embed = discord.Embed(description=f'> {emojis.true} Your **JoinPing** hasnt been **Cleared**', color=color.success)
                await interaction.response.edit_message(embed=embed, view=view)

        accept.callback = accept_callback
        decline.callback = decline_callback

        view = discord.ui.View()
        view.add_item(item=accept)
        view.add_item(item=decline)

        embed = discord.Embed(description=f'> Are you sure to clear your **JoinPing** config?', color=color.color)
        await ctx.send(embed=embed, view=view)

    @joinping.command(brief='set joinping on or off')
    @blacklist_check()
    @commands.has_guild_permissions(manage_guild=True)
    async def set(self, ctx, turn=None):
        check = collection.find_one({"_id": ctx.message.guild.id})

        if turn == 'on':
            if check['turn'] == False:
                collection.update_one({"_id": ctx.message.guild.id}, {"$set": {"turn": True}})
                embed = discord.Embed(description=f'> {emojis.true} You **activated** JoinPing', color=color.success)
                await ctx.send(embed=embed)

            if check['turn'] == True:
                embed = discord.Embed(description=f'> {emojis.false} **JoinPing*+ is already **activated**', color=color.fail)
                await ctx.send(embed=embed)

        elif turn == 'off':
            if check['turn'] == True:
                collection.update_one({"_id": ctx.message.guild.id}, {"$set": {"turn": False}})
                embed = discord.Embed(description=f'> {emojis.true} You **deactivated** JoinPing', color=color.success)
                await ctx.send(embed=embed)

            if check['turn'] == False:
                embed = discord.Embed(description=f'> {emojis.false} **JoinPing** is already **deactivated**', color=color.fail)
                await ctx.send(embed=embed)

        else:
            embed = discord.Embed(description=f'> {emojis.false} You cant set **JoinPing** to ``{turn}``', color=color.fail)

    @joinping.command(brief='see all set channels')
    @blacklist_check()
    @commands.has_guild_permissions(manage_guild=True)
    async def channels(self, ctx):
        if not collection.find_one({"_id": ctx.message.guild.id}):
            joinpings = {"_id": ctx.message.guild.id, "turn": False, "channels": [], "count": 0}
            collection.insert_one(joinpings)

        data = collection.find_one({"_id": ctx.message.guild.id })['channels']
        embed = discord.Embed(description=f'> **JoinPing** Channels: \n', color=color.color)

        num = 0
        for i in data:
            num = num + 1
            channel = self.client.get_channel(i)
            embed.description += f'``{num}`` **{channel.mention}** | ``{channel.id}``\n'

        await ctx.send(embed=embed)

    @joinping.command(brief='add a channel to the list')
    @blacklist_check()
    @commands.has_guild_permissions(manage_guild=True)
    async def add(self, ctx, channel: discord.TextChannel=None):
        if not collection.find_one({"_id": ctx.message.guild.id}):
            joinpings = {"_id": ctx.message.guild.id, "turn": False, "channels": [], "count": 0}
            collection.insert_one(joinpings)
        check = collection.find_one({"_id": ctx.message.guild.id})
        px = functions.get_prefix(ctx)

        if channel == None:
            embed = discord.Embed(title=f'{emojis.blade} JoinPing', color=color.color,
            description=f'{emojis.reply} *add channels to the joinping*')
            embed.add_field(name=f"{emojis.commands} Command:", value=f"> ``{px}joinping add [#channel]`` add channels to the joinping", inline=False)
            embed.add_field(name=f"{emojis.commands} Status:", value=f"> ``Channels`` **{check['count']}**", inline=False)
            await ctx.send(embed=embed)

        else:
            if check["count"] == 3:
                if not premium.find_one({"server": ctx.guild.id}):
                    embed = discord.Embed(description=f'> {emojis.false} To have more than ``3`` Channels is a **Premium** only feature, to learn more about it, join our [``Support Server``](https://discord.gg/snore)', color=color.color)
                    await ctx.send(embed=embed)
                else:
                    count = check['count'] + 1
                    collection.update_one({"_id": ctx.message.guild.id}, {"$set": {"count": count}})
                    collection.update_one({"_id": ctx.message.guild.id}, {"$push": {"channels": channel.id}})
                    embed = discord.Embed(description=f'> {emojis.true} You added {channel.mention} to the **JoinPing**', color=color.success)
                    await ctx.send(embed=embed)

            elif check["count"] == 6:
                embed = discord.Embed(description=f'> {emojis.false} You cant have more than `6` **Channels**', color=color.fail)
                await ctx.send(embed=embed)

            else:
                count = check['count'] + 1
                collection.update_one({"_id": ctx.message.guild.id}, {"$set": {"count": count}})
                collection.update_one({"_id": ctx.message.guild.id}, {"$push": {"channels": channel.id}})
                embed = discord.Embed(description=f'> {emojis.true} You Added {channel.mention} to the **JoinPing**', color=color.success)
                await ctx.send(embed=embed)

    @joinping.command(brief='remove a channel from the list')
    @blacklist_check()
    @commands.has_guild_permissions(manage_guild=True)
    async def remove(self, ctx, channel: discord.TextChannel=None):
        if not collection.find_one({"_id": ctx.message.guild.id}):
            joinpings = {"_id": ctx.message.guild.id, "turn": False, "channels": [], "count": 0}
            collection.insert_one(joinpings)
        check = collection.find_one({"_id": ctx.message.guild.id})
        px = functions.get_prefix(ctx)

        if channel == None:
            embed = discord.Embed(title=f'{emojis.blade} JoinPing', color=color.color,
            description=f'{emojis.reply} *remove channels from the joinping*')
            embed.add_field(name=f"{emojis.commands} Command:", value=f"> ``{px}joinping remove [#channel]`` remove channels from the joinping", inline=False)
            embed.add_field(name=f"{emojis.commands} Status:", value=f"> ``Channels`` **{check['count']}**", inline=False)
            await ctx.send(embed=embed)

        else:
            count = check['count'] - 1
            collection.update_one({"_id": ctx.message.guild.id}, {"$set": {"count": count}})
            collection.update_one({"_id": ctx.message.guild.id}, {"$pull": {"channels": channel.id}})
            embed = discord.Embed(description=f'> {emojis.true} You removed {channel.mention} from the **JoinPing**', color=color.success)
            await ctx.send(embed=embed)

async def setup(client):
    await client.add_cog(joinping(client))
