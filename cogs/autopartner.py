import discord
import pymongo
import asyncio
from discord.utils import get
from pymongo import MongoClient
from discord.ext import commands
from utils import functions
from utils.emojis import emojis
from utils.color import color

cluster = MongoClient('no')
db = cluster["blade"]
collection = db["autopartner"]

class autopartner(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.group(pass_context=True, invoke_without_command=True, brief='automaticly partner with server', description='config')
    @commands.has_guild_permissions(manage_guild=True)
    async def autopartner(self, ctx):
        if not collection.find_one({"_id": ctx.message.guild.id}):
            autopartnerr = {"_id": ctx.message.guild.id, "autopartner": False, "channel": 0, "ad": ''}
            collection.insert_one(autopartnerr)
            
        await ctx.invoke()

    @autopartner.command(brief='clear autopartner')
    @commands.has_guild_permissions(manage_guild=True)
    async def clear(self, ctx):
        if not collection.find_one({"_id": ctx.message.guild.id}):
            autopartnerr = {"_id": ctx.message.guild.id, "autopartner": False, "channel": 0, "ad": ''}
            collection.insert_one(autopartnerr)

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
                embed = discord.Embed(description=f'> {emojis.true} **Successfully** cleared **AutoPartner**', color=color.success)
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
                embed = discord.Embed(description=f'> {emojis.true} Your **AutoPartner** hasnt been **Cleared**', color=color.success)
                await interaction.response.edit_message(embed=embed, view=view)

        accept.callback = accept_callback
        decline.callback = decline_callback

        view = discord.ui.View()
        view.add_item(item=accept)
        view.add_item(item=decline)

        embed = discord.Embed(description=f'> Are you sure to clear your **AutoPartner** config?', color=color.color)
        await ctx.send(embed=embed, view=view)

    @autopartner.command(brief='activate or deactivate autopartner')
    @commands.has_guild_permissions(manage_guild=True)
    async def set(self, ctx, turn):
        if not collection.find_one({"_id": ctx.message.guild.id}):
            autopartnerr = {"_id": ctx.message.guild.id, "autopartner": False, "channel": 0, "ad": ''}
            collection.insert_one(autopartnerr)

        check = collection.find_one({"_id": ctx.message.guild.id})
        px = functions.get_prefix(ctx)

        if turn == None:
            embed = discord.Embed(title=f'{emojis.blade} AutoPartner', color=color.color,
            description=f'{emojis.reply} *activate or deactivate autopartner*')
            embed.add_field(name=f"{emojis.commands} Command:", value=f"> ``{px}autopartner set [on/off]`` activate or deactivate autopartner", inline=False)
            await ctx.send(embed=embed)

        if check["channel"] == 0 or check["ad"] == None:
            embed = discord.Embed(description=f'> {emojis.false} Setup a **Channel** and the Server **AD** first.', color=color.fail)
            await ctx.send(embed=embed)
            return

        if turn == 'on' or turn == 'true':
            if check['autopartner'] == True:
                embed = discord.Embed(description=f'> {emojis.false} **AutoPartner** is already **activated**', color=color.fail)
                await ctx.send(embed=embed)
            else:
                collection.update_one({"_id": ctx.message.guild.id}, {"$set": {"autopartner": True}})
                embed = discord.Embed(description=f'> {emojis.true} **Successfully** activated **AutoPartner**', color=color.success)
                await ctx.send(embed=embed)

                for i in collection.find({}):
                    await asyncio.sleep(10)

                    if i["_id"] == ctx.guild.id or i["autopartner"] == False:
                        pass

                    else:
                        own_channel = self.client.get_channel(check["channel"])

                        them_message = i["ad"]
                        them_message = them_message.replace("@everyone", "").replace("@here", "")

                        await own_channel.send(them_message)
                        
                        await asyncio.sleep(2)

                        other_channel = self.client.get_channel(i["channel"])

                        own_message = check["ad"]
                        own_message = own_message.replace("@everyone", "").replace("@here", "")

                        await other_channel.send(own_message)

        elif turn == 'off' or turn == 'false':
            if check['autopartner'] == False:
                embed = discord.Embed(description=f'> {emojis.false} **AutoPartner** is **deactivated**', color=color.fail)
                await ctx.send(embed=embed)
            else:
                collection.update_one({"_id": ctx.message.guild.id}, {"$set": {"autopartner": False}})
                embed = discord.Embed(description=f'> {emojis.true} **Succesfully** deactivated **AutoPartner**', color=color.success)
                await ctx.send(embed=embed)

        else:
            embed = discord.Embed(description=f'> {emojis.false} You cant set **AutoPartner** to ``{turn}``', color=color.fail)
            await ctx.send(embed=embed)

    @autopartner.command(brief='set the channel for the server ads')
    @commands.has_guild_permissions(manage_guild=True)
    async def channel(self, ctx, channel: discord.TextChannel=None):
        if not collection.find_one({"_id": ctx.message.guild.id}):
            autopartnerr = {"_id": ctx.message.guild.id, "autopartner": False, "channel": 0, "ad": ''}
            collection.insert_one(autopartnerr)
        px = functions.get_prefix(ctx)

        check = collection.find_one({"_id": ctx.message.guild.id})

        if channel == None:
            channel = check["channel"]
            if channel == 0:
                status = f'{emojis.false} *(no channel set)*'
                channel = f'{emojis.false} *(no channel set)*'

            elif channel:
                channel = self.client.get_channel(channel)
                status  = f'{emojis.true} *(channel set)*'
                channel = f'{channel.mention} | ``{channel.id}``'

            embed = discord.Embed(title=f'{emojis.blade} AutoPartner', color=color.color,
            description=f'{emojis.reply} *set the autopartner channel*')
            embed.add_field(name=f"{emojis.commands} Command:", value=f"> ``{px}autopartner channel [#channel]`` set the channel for the server ads", inline=False)
            embed.add_field(name=f"{emojis.config} Config:", value=f"> ``Status`` {status}", inline=False)
            embed.add_field(name=f"{emojis.config} Channel:", value=f"> {channel}", inline=False)
            await ctx.send(embed=embed)

        else:
            if check['channel'] == 0:
                collection.update_one({"_id": ctx.message.guild.id}, {"$set": {"channel": channel.id}})
                embed = discord.Embed(description=f'> {emojis.true} **Succsessfully** set {channel.mention} as **AutoPartner Channel**', color=color.success)
                await ctx.send(embed=embed)

            elif check['channel']:
                collection.update_one({"_id": ctx.message.guild.id}, {"$set": {"channel": channel.id}})
                embed = discord.Embed(description=f'> {emojis.true} **Succsessfully** changed the **AutoPartner Channel** to {channel.mention}', color=color.success)
                await ctx.send(embed=embed)
            elif check['channel'] == channel.id:
                embed = discord.Embed(description=f'> {emojis.false} {channel.mention} is already the **AutoPartner Channel**', color=color.fail)
                await ctx.send(embed=embed)

    @autopartner.command(brief='set the server ad')
    @commands.has_guild_permissions(manage_guild=True)
    async def message(self, ctx, *, ad=None):
        if not collection.find_one({"_id": ctx.message.guild.id}):
            autopartnerr = {"_id": ctx.message.guild.id, "autopartner": False, "channel": 0, "ad": ''}
            collection.insert_one(autopartnerr)
        px = functions.get_prefix(ctx)

        check = collection.find_one({"_id": ctx.message.guild.id})

        if ad == None:
            embed = discord.Embed(title=f'{emojis.blade} AutoPartner', color=color.color,
            description=f'{emojis.reply} *set the autopartner message with json*')
            embed.add_field(name=f"{emojis.commands} Command:", value=f"> ``{px}autopartner message [json]`` set the server ad", inline=False)
            await ctx.send(embed=embed)

        else:
            collection.update_one({"_id": ctx.message.guild.id}, {"$set": {"ad": ad}})
            embed = discord.Embed(description=f'> {emojis.true} **Succsessfully** set the Server **AD** to:', color=color.success)
            await ctx.send(embed=embed)
            await ctx.send(ad)


async def setup(client):
    await client.add_cog(autopartner(client))
