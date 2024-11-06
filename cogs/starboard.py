import discord
import pymongo
import datetime
import asyncio
from discord.ext import commands
from pymongo import MongoClient
from utils import functions
from utils.emojis import emojis
from utils.color import color

cluster = MongoClient('mongodb+srv://blade:lolidkbruh12333333333@cluster0.wbxaj.mongodb.net/myFirstDatabase?retryWrites=true&w=majority')
db = cluster["blade"]
collection = db["starboard"]
blacklist = db["blacklist"]

def blacklist_check():
    def predicate(ctx):
        if blacklist.find_one({'_id': ctx.author.id}):
            return False
        return True
    return commands.check(predicate)

class starboard(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        if collection.find_one({"_id": reaction.message.guild.id}):
            check = collection.find_one({"_id": reaction.message.guild.id})

            message = reaction.message

            if not check['star'] == True:
                return

            if message.guild.id == check['_id']:
                if reaction.emoji == f'{check["emoji"]}':
                    if reaction.count == check['count']:
                        channel = self.client.get_channel(check['channel'])

                        if message.embeds:
                            try:
                                if '.mp4' in message.embeds[0].url or '.mov' in message.embeds[0].url:
                                    embed = discord.Embed()
                                    embed.set_author(name=f'{message.author.name}', icon_url=message.author.display_avatar)
                                    embed.set_footer(text=datetime.date.today())
                                    
                                    view = discord.ui.View()
                                    invite = discord.ui.Button(style=discord.ButtonStyle.gray, label="message", url=message.jump_url)
                                    view.add_item(item=invite)
                                    await channel.send(f'#{reaction.count} {check["emoji"]}', embed=embed)
                                    msg = f'<:blank:1109912797770428426>||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||  \n{message.embeds[0].url}'
                                    await channel.send(f'{msg}', view=view)

                            except:
                                embed = discord.Embed()
                                embed.set_author(name=f'{message.author.name}', icon_url=message.author.display_avatar)
                                embed.set_footer(text=datetime.date.today())
                                
                                view = discord.ui.View()
                                invite = discord.ui.Button(style=discord.ButtonStyle.gray, label="message", url=message.jump_url)
                                view.add_item(item=invite)
                                await channel.send(f'#{reaction.count} {check["emoji"]}', embed=embed)
                                await channel.send(embed=message.embeds[0], view=view)

                        else:
                            embed = discord.Embed(description=f'{message.content}')
                            embed.set_author(name=f'{message.author.name}', icon_url=message.author.display_avatar)
                            embed.set_footer(text=f'{datetime.date.today()}')

                            try:
                                embed.set_image(url=message.attachments[0].url)
                            except:
                                pass

                            view = discord.ui.View()
                            invite = discord.ui.Button(style=discord.ButtonStyle.gray, label="message", url=message.jump_url)
                            view.add_item(item=invite)

                            await channel.send(f'#{reaction.count} {check["emoji"]}', embed=embed, view=view)
        else:
            pass

        await asyncio.sleep(2)

    @commands.group(pass_context=True, invoke_without_command=True, aliases=['sb'], description='config', brief='create a starboard')
    @commands.has_guild_permissions(manage_guild=True)
    @blacklist_check()
    async def starboard(self, ctx):
        if not collection.find_one({"_id": ctx.message.guild.id}):
            stars = {"_id": ctx.message.guild.id, "star": False, "channel": 0, "count": 1, "emoji": "⭐"}
            collection.insert_one(stars)

        check = collection.find_one({"_id": ctx.message.guild.id})
        px = functions.get_prefix(ctx)

        if check['star'] == True:
            status = f'{emojis.true} *(activated)*'
        else:
            status = f'{emojis.false} *(deactivated)*'

        if check['channel'] != 0:
            channel = self.client.get_channel(check['channel'])
            channel = f'{emojis.true} | {channel.mention}'
        else:
            channel = f'{emojis.false} *(no channel set)*'

        embed = discord.Embed(title=f'{emojis.blade} Starboard', color=color.color,
        description=f'{emojis.reply} *emojis with a star will be send on the board*')
        embed.add_field(name=f"{emojis.commands} Commands:", value=f"> ``{px}starboard set [on/off]`` set starboard on or off \n> ``{px}starboard channel [#channel]`` set the board channel \n> ``{px}starboard emoji [emoji]`` set the starboards emoji \n> ``{px}starboard count [number]`` set the amount of reactions \n> ``{px}starboard clear`` clear your tracker config", inline=False)
        embed.add_field(name=f"{emojis.config} Config:", value=f"> ``Status`` {status} \n> ``Channel`` {channel} \n> ``Emoji`` {check['emoji']} \n> ``Count`` {check['count']}", inline=False)
        embed.add_field(name=f"{emojis.alias} Aliases:", value=f"```sb```", inline=False)
        await ctx.send(embed=embed)

    @starboard.command(brief='set your own emoji')
    @commands.has_guild_permissions(manage_guild=True)
    @blacklist_check()
    async def emoji(self, ctx, emoji):
        if not collection.find_one({"_id": ctx.message.guild.id}):
            stars = {"_id": ctx.message.guild.id, "star": False, "channel": 0, "count": 1, "emoji": "⭐"}
            collection.insert_one(stars)

        check = collection.find_one({"_id": ctx.message.guild.id})
        px = functions.get_prefix(ctx)

        if emoji == None:
            embed = discord.Embed(title=f'{emojis.blade} Starboard', color=color.color,
            description=f'{emojis.reply} *set the starboards emoji*')
            embed.add_field(name=f"{emojis.commands} Command:", value=f"> ``{px}starboard emoji [emoji]`` set your starboards emoji", inline=False)
            await ctx.send(embed=embed)

        else:

            try:
                await ctx.message.add_reaction(emoji)

                collection.update_one({"_id": ctx.message.guild.id}, {"$set": {"emoji": emoji}})
                embed = discord.Embed(description=f'> {emojis.true} **Succesfully** set the **Starboard** emoji to {emoji}', color=color.success)
                await ctx.send(embed=embed)

            except:
                embed = discord.Embed(description=f'> {emojis.false} Cant set the **Star** emoji to ``{emoji}``', color=color.fail)
                await ctx.send(embed=embed)

    @starboard.command(brief='set how many reactions it needs')
    @commands.has_guild_permissions(manage_guild=True)
    @blacklist_check()
    async def count(self, ctx, number: int=None):
        if not collection.find_one({"_id": ctx.message.guild.id}):
            stars = {"_id": ctx.message.guild.id, "star": False, "channel": 0, "count": 1, "emoji": "⭐"}
            collection.insert_one(stars)

        check = collection.find_one({"_id": ctx.message.guild.id})
        px = functions.get_prefix(ctx)

        if number == None:
            embed = discord.Embed(title=f'{emojis.blade} Starboard', color=color.color,
            description=f'{emojis.reply} *set the board channel*')
            embed.add_field(name=f"{emojis.commands} Command:", value=f"> ``{px}starboard count [number]`` set your starboard count", inline=False)
            await ctx.send(embed=embed)

        else:
            if number < 1 or number > 15:
                embed = discord.Embed(description=f'> {emojis.false} You cant set the **Star** count to ``{number}``', color=color.fail)
                await ctx.send(embed=embed)

            else:
                collection.update_one({"_id": ctx.message.guild.id}, {"$set": {"count": number}})
                embed = discord.Embed(description=f'> {emojis.true} **Succesfully** set the **Star** count to ``{number}``', color=color.success)
                await ctx.send(embed=embed)

    @starboard.command(brief='set the channel for the board')
    @commands.has_guild_permissions(manage_guild=True)
    @blacklist_check()
    async def channel(self, ctx, channel: discord.TextChannel=None):
        if not collection.find_one({"_id": ctx.message.guild.id}):
            stars = {"_id": ctx.message.guild.id, "star": False, "channel": 0, "count": 1, "emoji": "⭐"}
            collection.insert_one(stars)

        check = collection.find_one({"_id": ctx.message.guild.id})
        px = functions.get_prefix(ctx)

        if channel == None:
            embed = discord.Embed(title=f'{emojis.blade} Starboard', color=color.color,
            description=f'{emojis.reply} *set the board channel*')
            embed.add_field(name=f"{emojis.commands} Command:", value=f"> ``{px}starboard channel [#channel]`` set your starboard channel", inline=False)
            await ctx.send(embed=embed)

        else:
            collection.update_one({"_id": ctx.message.guild.id}, {"$set": {"channel": channel.id}})
            embed = discord.Embed(description=f'> {emojis.true} **Succesfully** set the **Starboard** channel as {channel.mention}', color=color.success)
            await ctx.send(embed=embed)

    @starboard.command(brief='activate or deactivate starboard')
    @commands.has_guild_permissions(manage_guild=True)
    @blacklist_check()
    async def set(self, ctx, turn=None):
        if not collection.find_one({"_id": ctx.message.guild.id}):
            stars = {"_id": ctx.message.guild.id, "star": False, "channel": 0, "count": 1, "emoji": "⭐"}
            collection.insert_one(stars)

        check = collection.find_one({"_id": ctx.message.guild.id})
        px = functions.get_prefix(ctx)

        if turn == None:
            embed = discord.Embed(title=f'{emojis.blade} Starboard', color=color.color,
            description=f'{emojis.reply} *turn starboard on or off*')
            embed.add_field(name=f"{emojis.commands} Command:", value=f"> ``{px}starboard set [on/off]`` set starboard on or off", inline=False)
            await ctx.send(embed=embed)

        if turn == 'on' or turn == 'true':
            if check['star'] == True:
                embed = discord.Embed(description=f'> {emojis.false} The **Starboard** is already **activated**', color=color.fail)
                await ctx.send(embed=embed)
            else:
                collection.update_one({"_id": ctx.message.guild.id}, {"$set": {"star": True}})
                embed = discord.Embed(description=f'> {emojis.true} **Succesfully** activated **Starboard**', color=color.success)
                await ctx.send(embed=embed)

        elif turn == 'off' or turn == 'false':
            if check['star'] == False:
                embed = discord.Embed(description=f'> {emojis.false} The **Starboard** is not **activated**', color=color.fail)
                await ctx.send(embed=embed)
            else:
                collection.update_one({"_id": ctx.message.guild.id}, {"$set": {"star": False}})
                embed = discord.Embed(description=f'> {emojis.true} **Succesfully** deactivated **Starboard**', color=color.success)
                await ctx.send(embed=embed)

        else:
            embed = discord.Embed(description=f'> {emojis.false} Cant set the **Starboard** to ``{turn}``', color=color.fail)
            await ctx.send(embed=embed)

    @starboard.command(brief='clear starboards config')
    @commands.has_guild_permissions(manage_guild=True)
    @blacklist_check()
    async def clear(self, ctx):
        if not collection.find_one({"_id": ctx.message.guild.id}):
            stars = {"_id": ctx.message.guild.id, "star": False, "channel": 0, "count": 1, "emoji": "⭐"}
            collection.insert_one(stars)

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
                embed = discord.Embed(description=f'> {emojis.true} **Succesfully** cleared the **Starboard** config', color=color.success)
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
                embed = discord.Embed(description=f'> {emojis.true} **Starboard** hasnt been **Cleared**', color=color.success)
                await interaction.response.edit_message(embed=embed, view=view)

        accept.callback = accept_callback
        decline.callback = decline_callback

        view = discord.ui.View()
        view.add_item(item=accept)
        view.add_item(item=decline)

        embed = discord.Embed(description=f'> Are you sure to clear **Starboard**?', color=color.color)
        await ctx.send(embed=embed, view=view)

async def setup(client):
    await client.add_cog(starboard(client))
