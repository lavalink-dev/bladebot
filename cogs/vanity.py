import discord
import pymongo
import asyncio
import button_paginator as pg
from pymongo import MongoClient
from discord.ext import commands
from utils import functions
from utils.emojis import emojis
from utils.color import color

cluster = MongoClient('mongodb+srv://blade:lolidkbruh12333333333@cluster0.wbxaj.mongodb.net/myFirstDatabase?retryWrites=true&w=majority')
db = cluster["blade"]
collection = db["vanity"]
blacklist = db["blacklist"]

def blacklist_check():
    def predicate(ctx):
        if blacklist.find_one({'_id': ctx.author.id}):
            return False
        return True
    return commands.check(predicate)

class vanity(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_guild_update(self, before: discord.Guild, after: discord.Guild):
        for i in collection.find({}):
            await asyncio.sleep(2)
            try:
                channel = self.client.get_channel(i['channel'])

                if str(before.vanity_url_code) != str(after.vanity_url_code) and str(before.vanity_url_code) != "None":
                    await asyncio.sleep(2)

                    embed = discord.Embed(description=f'> {emojis.true} The Vanity **{before.vanity_url_code}** is now available', color=color.color)
                    await channel.send(embed=embed)

                    await asyncio.sleep(2)
            except:
                pass

    @commands.group(pass_context=True, invoke_without_command=True, brief='sends automaticly available vanitys', description='config')
    @commands.has_guild_permissions(manage_guild=True)
    @blacklist_check()
    async def vanity(self, ctx):
        await ctx.invoke()

    @vanity.command(brief='set the vanity channel')
    @commands.has_guild_permissions(manage_guild=True)
    @blacklist_check()
    async def channel(self, ctx, channel: discord.TextChannel=None):
        if not collection.find_one({"_id": ctx.message.guild.id}):
            taggg = {"_id": ctx.message.guild.id, "vanity": False, "channel": 0}
            collection.insert_one(taggg)

        check = collection.find_one({"_id": ctx.message.guild.id})
        px = functions.get_prefix(ctx)

        if channel == None:
            embed = discord.Embed(title=f'{emojis.blade} Tracker', color=color.color,
            description=f'{emojis.reply} *set the vanity channel*')
            embed.add_field(name=f"{emojis.commands} Command:", value=f"> ``{px}vanity channel [#channel]`` set your vanity tracker channel", inline=False)
            await ctx.send(embed=embed)

        else:
            collection.update_one({"_id": ctx.message.guild.id}, {"$set": {"channel": channel.id}})
            embed = discord.Embed(description=f'> {emojis.true} **Succesfully** set the **Vanity** Tracker to {channel.mention}', color=color.success)
            await ctx.send(embed=embed)

    @vanity.command(brief='turn vanity on or off')
    @commands.has_guild_permissions(manage_guild=True)
    @blacklist_check()
    async def set(self, ctx, turn=None):
        if not collection.find_one({"_id": ctx.message.guild.id}):
            taggg = {"_id": ctx.message.guild.id, "vanity": False, "channel": 0}
            collection.insert_one(taggg)

        check = collection.find_one({"_id": ctx.message.guild.id})
        px = functions.get_prefix(ctx)

        if turn == None:
            embed = discord.Embed(title=f'{emojis.blade} Tracker', color=color.color,
            description=f'{emojis.reply} *turn the vanity on or off*')
            embed.add_field(name=f"{emojis.commands} Command:", value=f"> ``{px}vanity set [on/off]`` set the vanity tracker on or off", inline=False)
            await ctx.send(embed=embed)

        if turn == 'on' or turn == 'true':
            if check['vanity'] == True:
                embed = discord.Embed(description=f'> {emojis.false} **Vanity** Tracker is already **activated**', color=color.fail)
                await ctx.send(embed=embed)
            else:
                collection.update_one({"_id": ctx.message.guild.id}, {"$set": {"vanity": True}})
                embed = discord.Embed(description=f'> {emojis.true} **Successfully** **activated** the **Vanity**', color=color.success)
                await ctx.send(embed=embed)

        elif turn == 'off' or turn == 'false':
            if check['vanity'] == False:
                embed = discord.Embed(description=f'> {emojis.false} **Vanity** Tracker is not **activated**', color=color.fail)
                await ctx.send(embed=embed)
            else:
                collection.update_one({"_id": ctx.message.guild.id}, {"$set": {"vanity": False}})
                embed = discord.Embed(description=f'> {emojis.true} **Successfully** deactivated the **Vanity** Tracker', color=color.success)
                await ctx.send(embed=embed)

        else:
            embed = discord.Embed(description=f'> {emojis.false} You cant set the **Vanity** to ``{turn}``', color=color.fail)
            await ctx.send(embed=embed)

    @vanity.command(brief='clear the vanity config')
    @commands.has_guild_permissions(manage_guild=True)
    @blacklist_check()
    async def clear(self, ctx):
        if not collection.find_one({"_id": ctx.message.guild.id}):
            taggg = {"_id": ctx.message.guild.id, "vanity": False, "channel": 0}
            collection.insert_one(taggg)

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
                embed = discord.Embed(description=f'> {emojis.true} You cleared the **Vanity** config', color=color.success)
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
                embed = discord.Embed(description=f'> {emojis.true} Your **Vanity** hasnt been **Cleared**', color=color.success)
                await interaction.response.edit_message(embed=embed, view=view)

        accept.callback = accept_callback
        decline.callback = decline_callback

        view = discord.ui.View()
        view.add_item(item=accept)
        view.add_item(item=decline)

        embed = discord.Embed(description=f'> Are you sure to clear your **Vanity**?', color=color.color)
        await ctx.send(embed=embed, view=view)

async def setup(client):
    await client.add_cog(vanity(client))
