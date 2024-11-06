import discord
import asyncio
import orjson
import aiohttp
import datetime
import button_paginator as pg
import pymongo
from pymongo import MongoClient
from io import BytesIO
from typing import Union
from datetime import timedelta
from discord import Embed
from discord.ext import commands
from discord.ext.commands.core import has_guild_permissions
from discord.utils import get
from utils import functions
from utils.emojis import emojis
from utils.color import color

cluster = MongoClient('no')
db = cluster["blade"]
silence = db["silence"]
forcenick = db["forcenick"]
automutedb = db["automute"]
imgmutedb = db["imgmute"]
collection = db["blacklist"]

def blacklist_check():
    def predicate(ctx):
        if collection.find_one({'_id': ctx.author.id}):
            return False
        return True
    return commands.check(predicate)

class moderation(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(brief='forcenick members', aliases=['fn'], description='moderation')
    @commands.has_guild_permissions(manage_nicknames=True)
    @commands.cooldown(1, 3, commands.BucketType.user)
    @blacklist_check()
    async def forcenick(self, ctx, member: discord.Member, *, nick):
        if forcenick.find_one({"server": ctx.message.guild.id, "member": member.id}):
            embed = discord.Embed(description=f'> {emojis.true} {member.mention} gets already **Force Nicked**', color=color.fail)
            await ctx.send(embed=embed)

        else:
            try:
                await member.edit(nick=nick)

                nicked_member = {"server": ctx.message.guild.id, "member": member.id, "nick": nick}
                forcenick.insert_one(nicked_member)

                embed = discord.Embed(description=f'> {emojis.true} **Successfully** force nicked {member.mention} with the nick ``{nick}``', color=color.success)
                await ctx.send(embed=embed)
            except:
                embed = discord.Embed(description=f"> {emojis.false} Coudlnt **Forcenick** {member.mention}")
                await ctx.send(embed=embed)

    @commands.command(brief='forcenick members', aliases=['ufn'], description='moderation')
    @commands.has_guild_permissions(manage_nicknames=True)
    @commands.cooldown(1, 3, commands.BucketType.user)
    @blacklist_check()
    async def unforcenick(self, ctx, member: discord.Member):
        if forcenick.find_one({"server": ctx.message.guild.id, "member": member.id}):
            forcenick.delete_one({"server": ctx.message.guild.id, "member": member.id})
            await member.edit(nick=member.global_name)
            embed = discord.Embed(description=f'> {emojis.true} **Succesfully** removed {member.mention} force nick', color=color.success)
            await ctx.send(embed=embed)

        else:
            embed = discord.Embed(description=f'> {emojis.false} {member.mention} is not being **Force Nicked**', color=color.fail)
            await ctx.send(embed=embed)

    @commands.command(brief='silence a member', aliases=['stfu'], description='moderation')
    @commands.has_guild_permissions(mute_members=True)
    @commands.cooldown(1, 3, commands.BucketType.user)
    @blacklist_check()
    async def silence(self, ctx, member: discord.Member):
        if not silence.find_one({"_id": ctx.message.guild.id}):
                server_silence = {"_id": ctx.message.guild.id, "silenced": []}
                silence.insert_one(server_silence)

        check = silence.find_one({"_id": ctx.message.guild.id})

        if member.id in check['silenced']: 
            embed = discord.Embed(description=f'> {emojis.false} {member.mention} is already **Silenced**', color=color.fail)
            await ctx.send(embed=embed)

        else:
            silence.update_one({"_id": ctx.message.guild.id}, {"$push": {"silenced": member.id}})
            embed = discord.Embed(description=f'> {emojis.true} {member.mention} will be **Silenced** for now on', color=color.success)
            await ctx.send(embed=embed)

    @commands.command(brief='unsilence a member', description='moderation')
    @commands.has_guild_permissions(mute_members=True)
    @commands.cooldown(1, 3, commands.BucketType.user)
    @blacklist_check()
    async def unsilence(self, ctx, member: discord.Member):
        if not silence.find_one({"_id": ctx.message.guild.id}):
                server_silence = {"_id": ctx.message.guild.id, "silenced": []}
                silence.insert_one(server_silence)

        check = silence.find_one({"_id": ctx.message.guild.id})

        if member.id in check['silenced']: 
            silence.update_one({"_id": ctx.message.guild.id}, {"$pull": {"silenced": member.id}})
            embed = discord.Embed(description=f'> {emojis.true} {member.mention} is now **unsilenced**', color=color.success)
            await ctx.send(embed=embed)

        else:
            embed = discord.Embed(description=f'> {emojis.false} {member.mention} is not **Silenced**', color=color.fail)
            await ctx.send(embed=embed)

    @commands.command(brief='nuke the current channel', description='moderation')
    @commands.has_guild_permissions(administrator=True)
    @commands.cooldown(1, 4, commands.BucketType.user)
    @blacklist_check()
    async def nuke(self, ctx):
        accept = discord.ui.Button(style=discord.ButtonStyle.green, label="accept", emoji=emojis.true)
        decline = discord.ui.Button(style=discord.ButtonStyle.red, label="decline", emoji=emojis.false)

        async def accept_callback(interaction):
            if interaction.user != ctx.author:
                embed = discord.Embed(description=f"> {emojis.false} This is not your message", color=color.fail)
                await interaction.response.send_message(embed=embed, view=None, ephemeral=True)
                return
            else:
                nuke_channel = discord.utils.get(ctx.guild.channels, name=ctx.message.channel.name)
                new_channel = await nuke_channel.clone(reason="Has been Nuked!")
                await nuke_channel.delete()
                embed = discord.Embed(description=f'> {emojis.true} {new_channel.mention} has been **Nuked**!', color=color.success)
                await new_channel.send(embed=embed)

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
                embed = discord.Embed(description=f'> {emojis.true} This **Nuke** got ``declined``', color=color.success)
                await interaction.response.edit_message(embed=embed, view=None)

        accept.callback = accept_callback
        decline.callback = decline_callback

        view = discord.ui.View()
        view.add_item(item=accept)
        view.add_item(item=decline)

        embed = discord.Embed(description=f'> Are you sure to **Nuke** {ctx.message.channel.mention}?', color=color.color)
        await ctx.send(embed=embed, view=view)

    @commands.command(brief='make the bot say something', description='moderation')
    @commands.has_guild_permissions(manage_guild=True)
    @blacklist_check()
    async def say(self, ctx, *, message):
        await ctx.message.delete()
        await ctx.send(message)

    @commands.command(brief='change the guilds banner', aliases=['gb'], description='moderation')
    @commands.has_guild_permissions(manage_guild=True)
    @commands.cooldown(1, 4, commands.BucketType.user)
    @blacklist_check()
    async def guildbanner(self, ctx, image=None):
        ext = ['.jpg','.png','.jpeg', '.webp', '.gif']

        if image == None:
            if len(ctx.message.attachments) > 0:
                for file in ctx.message.attachments:
                    url = ctx.message.attachments[0].url
                    async with aiohttp.ClientSession() as ses:
                        async with ses.get(url) as r:
                            img = BytesIO(await r.read())
                            bytes = img.getvalue()

                    embed = discord.Embed(description=f'> {emojis.true} Succesfully changed the **Server Banner** to', color=color.success)
                    embed.set_image(url=ctx.message.attachments[0].url)
                    await ctx.guild.edit(banner=bytes)
                    await ctx.send(embed=embed)

            else:
                command = ctx.command
                pre = functions.get_prefix(ctx)
                if not command.aliases == []:
                  aliases = ", ".join(str(alias) for alias in command.aliases)
                else:
                  aliases = "None"
                params = []
                for key, value in command.params.items():
                    if key not in ("self", "ctx"):
                        params.append(f"<{key}>" if "NoneType" in
                                      str(value) else f"[{key}]")
                if params == []:
                    params = ""
                else:
                    params = " ".join(params)
                    param = params.replace("[", "")
                    param = param.replace("]", "")
                    param = param.replace(" ", ", ")
                    param_desc = "".join(param)
                embed = discord.Embed(title=f"{emojis.blade} {pre}{command.name}", color=color.color,
                                      description=f"{emojis.reply} ``description`` {command.brief} \n{emojis.reply} ``arguements`` {param_desc}")
                embed.add_field(name=f'{emojis.commands} ``Usage:``',
                                value=f'{emojis.reply} {pre}{command.name} {params}',
                                inline=False)
                embed.add_field(name=f'{emojis.alias} ``Aliases:``',
                                value=f'{emojis.reply} {aliases}',
                                inline=False)
                embed.set_thumbnail(url=self.client.user.display_avatar)
                await ctx.send(embed=embed)

        else:
            url = image
            async with aiohttp.ClientSession() as ses:
                async with ses.get(url) as r:
                    img = BytesIO(await r.read())
                    bytes = img.getvalue()

            embed = discord.Embed(description=f'> {emojis.true} Succesfully changed the **Server Banner** to', color=color.success)
            embed.set_image(url=image)
            await ctx.guild.edit(banner=bytes)
            await ctx.send(embed=embed)

    @commands.command(brief='change the guilds icon', aliases=['gi'], description='moderation')
    @commands.has_guild_permissions(manage_guild=True)
    @commands.cooldown(1, 4, commands.BucketType.user)
    @blacklist_check()
    async def guildicon(self, ctx, image=None):
        ext = ['.jpg','.png','.jpeg', '.webp', '.gif']

        if image == None:
            if len(ctx.message.attachments) > 0:
                for file in ctx.message.attachments:
                    url = ctx.message.attachments[0].url
                    async with aiohttp.ClientSession() as ses:
                        async with ses.get(url) as r:
                            img = BytesIO(await r.read())
                            bytes = img.getvalue()

                    embed = discord.Embed(description=f'> {emojis.true} Succesfully changed the **Server Icon** to', color=color.success)
                    embed.set_image(url=ctx.message.attachments[0].url)
                    await ctx.guild.edit(icon=bytes)
                    await ctx.send(embed=embed)

            else:
                command = ctx.command
                pre = functions.get_prefix(ctx)
                if not command.aliases == []:
                  aliases = ", ".join(str(alias) for alias in command.aliases)
                else:
                  aliases = "None"
                params = []
                for key, value in command.params.items():
                    if key not in ("self", "ctx"):
                        params.append(f"<{key}>" if "NoneType" in
                                      str(value) else f"[{key}]")
                if params == []:
                    params = ""
                else:
                    params = " ".join(params)
                    param = params.replace("[", "")
                    param = param.replace("]", "")
                    param = param.replace(" ", ", ")
                    param_desc = "".join(param)
                embed = discord.Embed(title=f"{emojis.blade} {pre}{command.name}", color=color.color,
                                      description=f"{emojis.reply} ``description`` {command.brief} \n{emojis.reply} ``arguements`` {param_desc}")
                embed.add_field(name=f'{emojis.commands} ``Usage:``',
                                value=f'{emojis.reply} {pre}{command.name} {params}',
                                inline=False)
                embed.add_field(name=f'{emojis.alias} ``Aliases:``',
                                value=f'{emojis.reply} {aliases}',
                                inline=False)
                embed.set_thumbnail(url=self.client.user.display_avatar)
                await ctx.send(embed=embed)

        else:
            url = image
            async with aiohttp.ClientSession() as ses:
                async with ses.get(url) as r:
                    img = BytesIO(await r.read())
                    bytes = img.getvalue()

            embed = discord.Embed(description=f'> {emojis.true} Succesfully changed the **Server Icon** to', color=color.success)
            embed.set_image(url=image)
            await ctx.guild.edit(icon=bytes)
            await ctx.send(embed=embed)

    @commands.command(brief='rename the server name', description='moderation')
    @commands.has_guild_permissions(manage_guild=True)
    @commands.cooldown(1, 4, commands.BucketType.user)
    @blacklist_check()
    async def rename(self, ctx, *, name):
        if len(name) < 1 or len(name)> 100:
            embed = discord.Embed(description=f'> {emojis.false} The Name can only be between ``1`` and ``100`` Characters', color=color.fail)
            await ctx.send(embed=embed)

        else:
            embed = discord.Embed(description=f'> {emojis.true} Succesfully changed the **Server Name** to ``{name}``', color=color.success)
            await ctx.guild.edit(name=f'{name}')
            await ctx.send(embed=embed)

    @commands.command(brief='lock the current channel', description='moderation')
    @commands.has_guild_permissions(manage_channels=True)
    @blacklist_check()
    async def lock(self, ctx):
        channel = ctx.message.channel
        overwrite = channel.overwrites_for(ctx.guild.default_role)
        overwrite.send_messages = False

        if overwrite.send_messages == True:
            embed = discord.Embed(description=f'> {emojis.lock} {ctx.message.channel.mention} is already **locked**', color=color.fail)
            await ctx.send(embed=embed)

        else:
            embed = discord.Embed(description=f'> {emojis.lock} **Successfully** **locked** {ctx.message.channel.mention}', color=color.success)
            await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
            await ctx.send(embed=embed)

    @commands.command(brief='unlock the current channel', description='moderation')
    @commands.has_guild_permissions(manage_channels=True)
    @blacklist_check()
    async def unlock(self, ctx):
        channel = ctx.message.channel
        overwrite = channel.overwrites_for(ctx.guild.default_role)
        overwrite.send_messages = True

        if overwrite.send_messages == False:
            embed = discord.Embed(description=f'> {emojis.unlock} {ctx.message.channel.mention} is not **locked**', color=color.fail)
            await ctx.send(embed=embed)

        else:
            embed = discord.Embed(description=f'> {emojis.unlock} {ctx.message.channel.mention} is now **unlocked**', color=color.success)
            await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
            await ctx.send(embed=embed)

    @commands.command(brief='sets the slowmode in your channel', description='moderation')
    @commands.has_guild_permissions(manage_channels=True)
    @blacklist_check()
    async def slowmode(self, ctx, seconds: int):
        if seconds > 21600:
            embed = discord.Embed(description=f'> {emojis.false} You cant set the **Slowmode** to ``{seconds}``, the max is ``21600``', color=color.fail)
            await ctx.send(embed=embed)

        else:
            embed = discord.Embed(description=f'> {emojis.true} **Successfully** set **Slowmode** to ``{seconds}`` seconds!', color=color.success)
            await ctx.channel.edit(slowmode_delay=seconds)
            await ctx.send(embed=embed)

    @commands.group(pass_context=True, invoke_without_command=True, brief='add, remove, etc emojis', description='moderation')
    @commands.has_guild_permissions(manage_emojis=True)
    @blacklist_check()
    async def emoji(self, ctx):
        await ctx.invoke()

    @emoji.command(brief="manage emojis")
    @commands.has_guild_permissions(manage_emojis=True)
    async def addmultiple(self, ctx: commands.Context, *emoji: Union[discord.Emoji, discord.PartialEmoji]): 
        if len(emoji) == 0: 
            embed = discord.Embed(description=f"{emojis.false} Please provide some emojis to add", color=color.fail)
            return await ctx.send(embed=embed)      
        
        if len(emoji) > 20: 
            embed = discord.Embed(description=f"> {emojis.false} You cant add more than ``20`` **Emojis** at the same time", color=color.fail)
            return await ctx.send(embed=embed)    

        embed = discord.Embed(description=f'> <a:loading:1217810364469739541> Adding multiple **Emojis**', color=color.color)
        message = await ctx.send(embed=embed)

        worked_emojis = []
        notworked_emojis = []
        for emo in emoji:
            try:
                emoj = await ctx.guild.create_custom_emoji(image=await emo.read(), name=emo.name)
                worked_emojis.append(f"{emoj}")
                await asyncio.sleep(.5)
            except discord.HTTPException as e:
                notworked_emojis.append(f"{emoj}")

        embed = discord.Embed(description=f'> {emojis.true} **Successfully** added multiple **Emojis**', color=color.success)

        if notworked_emojis != []:
            embed.description += f"\n{emojis.reply} {notworked_emojis} didnt work !"

        await message.edit(embed=embed)

    @emoji.command(brief='delete a emoji', description='moderation')
    @blacklist_check()
    async def delete(self, ctx, emoji: discord.Emoji):
        try:
            await emoji.delete()
            embed = discord.Embed(description=f'> {emojis.true} Succesfully **deleted** the Emoji', color=color.success)
            await ctx.send(embed=embed)

        except:
            embed = discord.Embed(description=f'> {emojis.false} Couldnt **delete** this Emoji', color=color.fail)
            await ctx.send(embed=embed)

    @commands.command(brief=f'take emojis from other servers', description='moderation')
    @commands.has_guild_permissions(manage_emojis=True)
    @blacklist_check()
    async def take(self, ctx, emoji: discord.PartialEmoji, name=None):
        if name == None:
            name = emoji.name
        url = emoji.url
        async with aiohttp.ClientSession() as ses:
            async with ses.get(url) as r:
                img = BytesIO(await r.read())
                bytes = img.getvalue()

        try:
            emoji = await ctx.guild.create_custom_emoji(name=name, image=bytes)
            embed = discord.Embed(description=f'> {emojis.true} **Successfully** added {emoji} with the name ``{name}`` to your Server', color=color.success)
            await ctx.send(embed=embed)

        except:
            embed = discord.Embed(description=f'> {emojis.false} You reached your **Maximum number** of **Emojis** in your **Server**', color=color.fail)
            await ctx.send(embed=embed)

    @commands.command(brief='bings coding command | not useable')
    async def add(self, ctx, member: discord.Member, *, role):
        for i in ctx.guild.roles:
            await ctx.send(i)
            if "role" == i.name.lower():
                await ctx.send('found')

    @commands.group(pass_context=True, invoke_without_command=True, brief='add or remove members role', description='moderation')
    @commands.has_guild_permissions(manage_roles=True)
    @blacklist_check()
    async def role(self, ctx, member: discord.Member, *, role: discord.Role):
        if role not in member.roles:
            if role >= ctx.author.top_role:
                if ctx.author == ctx.guild.owner:
                    await member.add_roles(role)
                    embed = discord.Embed(description=f"> {emojis.true} **Successfully** added ``{role}`` to {member.mention}.", color=color.success)
                    await ctx.send(embed=embed)

                else:
                    embed = discord.Embed(description=f'> {emojis.false} The role ``{role}`` is **Higher** than your **Role**', color=color.fail)
                    await ctx.send(embed=embed)

            else:
                await member.add_roles(role)
                embed = discord.Embed(description=f"> {emojis.true} **Successfully** added ``{role}`` to {member.mention}", color=color.success)
                await ctx.send(embed=embed)

        elif role in member.roles:
            if role >= ctx.author.top_role:
                if ctx.author == ctx.guild.owner:
                    await member.remove_roles(role)
                    embed = discord.Embed(description=f"> {emojis.true} **Successfully** removed ``{role}`` from {member.mention}.", color=color.success)
                    await ctx.send(embed=embed)

                else:
                    embed = discord.Embed(description=f'> {emojis.false} The role ``{role}`` is **Higher** than your **Role**', color=color.fail)
                    await ctx.send(embed=embed)

            else:
                await member.remove_roles(role)
                embed = discord.Embed(description=f"> {emojis.true} **Successfully** removed ``{role}`` from {member.mention}", color=color.success)
                await ctx.send(embed=embed)

    @role.command(brief='create a role')
    @commands.has_guild_permissions(manage_roles=True)
    @blacklist_check()
    async def create(self, ctx, *, name):
        role = await ctx.guild.create_role(name=name)
        embed = discord.Embed(description=f'> {emojis.true} **Successfully** created the Role {role.mention}', color=color.success)
        await ctx.send(embed=embed)

    @role.command(brief='delete a role')
    @commands.has_guild_permissions(manage_roles=True)
    @blacklist_check()
    async def delete(self, ctx, *, role: discord.Role):
        if role >= ctx.author.top_role:
            embed = discord.Embed(description=f'> {emojis.false} The role **{role}** is **Higher** than your **Role**', color=color.fail)
            await ctx.send(embed=embed)
        else:
            await role.delete()
            embed = discord.Embed(description=f'> {emojis.true} **Successfully** deleted the Role **{role.name}**', color=color.success)
            await ctx.send(embed=embed)

    @role.command(brief='give all members a role')
    @commands.has_guild_permissions(manage_roles=True)
    @blacklist_check()
    async def members(self, ctx, *, role: discord.Role):
        if role >= ctx.author.top_role:
            embed = discord.Embed(description=f'> {emojis.false} The role **{role}** is **Higher** than your **Role**', color=color.fail)
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(description=f'> <a:loading:1217810364469739541> Adding all **Members** the role **{role}**', color=color.color)
            message = await ctx.send(embed=embed)

            for i in ctx.guild.members:
                if role in i.roles:
                    pass

                try:
                    await i.add_roles(role)
                    await asyncio.sleep(1)
                except:
                    pass
            embed = discord.Embed(description=f"> {emojis.true} **Successfully** added the Role ``{role}`` to all **Members**", color=color.success)
            await message.edit(embed=embed)

    @role.command(brief='give all humans a role')
    @commands.has_guild_permissions(manage_roles=True)
    @blacklist_check()
    async def humans(self, ctx, *, role: discord.Role):
        if role >= ctx.author.top_role:
            embed = discord.Embed(description=f'> {emojis.false} The role **{role}** is **Higher** than your **Role**', color=color.fail)
            await ctx.send(embed=embed)

        else:
            embed = discord.Embed(description=f'> <a:loading:1217810364469739541> Adding all **Humans** the role **{role}**', color=color.color)
            message = await ctx.send(embed=embed)

            for i in list(filter(lambda m: not m.bot, ctx.guild.members)):
                if role in i.roles:
                    pass
                
                try:
                    await i.add_roles(role)
                    await asyncio.sleep(1)
                except:
                    pass
            embed = discord.Embed(description=f"> {emojis.true} **Successfully** added the Role ``{role}`` to all **Humans**", color=color.success)
            await message.edit(embed=embed)

    @role.command(brief='give all bots a role')
    @commands.has_guild_permissions(manage_roles=True)
    @blacklist_check()
    async def bots(self, ctx, *, role: discord.Role):
        if role >= ctx.author.top_role:
            embed = discord.Embed(description=f'> {emojis.false} The role **{role}** is **Higher** than your **Role**', color=color.fail)
            await ctx.send(embed=embed)

        else:
            embed = discord.Embed(description=f'> <a:loading:1217810364469739541> Adding all **Bots** the role **{role}**', color=color.color)
            message = await ctx.send(embed=embed)
            
            for i in list(filter(lambda m: m.bot, ctx.guild.members)):
                if role in i.roles:
                    pass
            
                try:
                    await i.add_roles(role)
                    await asyncio.sleep(1)
                except:
                    pass

            embed = discord.Embed(description=f"> {emojis.true} **Successfully** added the Role ``{role}`` to all **Bots**", color=color.success)
            await message.edit(embed=embed)

    @commands.command(aliases=['uc'], brief='delete messages from a member in your server', description='moderation')
    @commands.has_guild_permissions(manage_messages=True)
    @commands.cooldown(1, 3, commands.BucketType.user)
    @blacklist_check()
    async def userclear(self, ctx, member: discord.Member, amount: int):
        if amount > 250:
                embed = discord.Embed(description=f'> {emojis.false} You cant **Clear** more than ``250`` messages', color=color.fail)
                await ctx.send(embed=embed)

        else:
            async for msg in ctx.message.channel.history(limit=amount+10):
                if msg.author.id == member.id:
                    try:
                        await msg.delete()
                    except:
                        pass

            embed = discord.Embed(description=f"> {emojis.true} ``{amount}`` Messages got **deleted** from {member.mention}", color=color.success)
            message = await ctx.send(embed=embed)

            await asyncio.sleep(5)

            await message.delete()

    @commands.command(brief='delete messages from bots in your server', description='moderation')
    @commands.has_guild_permissions(manage_messages=True)
    @commands.cooldown(1, 3, commands.BucketType.user)
    @blacklist_check()
    async def botclear(self, ctx, amount: int):
        if amount > 250:
                embed = discord.Embed(description=f'> {emojis.false} You cant **Clear** more than ``250`` messages', color=color.fail)
                await ctx.send(embed=embed)

        else:
            async for msg in ctx.message.channel.history(limit=amount + 20):
                if msg.author.bot:
                    try:
                        await msg.delete()
                    except:
                        pass

            embed = discord.Embed(description=f"> {emojis.true} ``{amount}`` Messages got **deleted** from **Bots**", color=color.success)
            message = await ctx.send(embed=embed)

            await asyncio.sleep(5)

            await message.delete()
            await ctx.message.delete()

    @commands.command(aliases=['purge'], brief='delete messages in your server', description='moderation')
    @commands.has_guild_permissions(manage_messages=True)
    @commands.cooldown(1, 3, commands.BucketType.user)
    @blacklist_check()
    async def clear(self, ctx, amount: int):
        try:
            px = functions.get_prefix(ctx)
            if amount > 250:
                embed = discord.Embed(description=f'> {emojis.false} You cant **Clear** more than ``250`` messages. Use ``{px}nuke`` to clear all channel messages', color=color.fail)
                await ctx.send(embed=embed)

            else:
                await ctx.channel.purge(limit=amount+1)
                embed = discord.Embed(description=f"> {emojis.true} ``{amount}`` Messages got **deleted**. ", color=color.success)
                message = await ctx.send(embed=embed)

                await asyncio.sleep(5)

                await message.delete()
        except:
            embed = discord.Embed(description=f'> {emojis.fail} Couldnt **Clear** messages', color=color.fail)
            await ctx.send(embed=embed)

    @commands.command(brief='mute a user from your server', description='moderation')
    @commands.has_guild_permissions(mute_members=True)
    @commands.cooldown(1, 3, commands.BucketType.user)
    @blacklist_check()
    async def mute(self, ctx, member : discord.Member, *, reason=None):
        if member.top_role >= ctx.author.top_role:
            embed = discord.Embed(description=f'> {emojis.false} You cant **mute** {member.mention} because they has a **higher Role**', color=color.fail)
            await ctx.send(embed=embed)

        if member.is_timed_out():
            embed = discord.Embed(description=f'> {emojis.false} {member.mention} is already **muted**', color=color.fail)
            await ctx.send(embed=embed)

        else:
            await member.timeout(timedelta(days = 7), reason=reason)
            embed = discord.Embed(description=f"> {emojis.punishment} **Successfully** **muted** ``{member}`` ``({member.id})`` for: {reason}", color=color.color)
            embed.set_author(name=f"{ctx.message.author}", icon_url=ctx.author.display_avatar)
            await ctx.send(embed=embed)

    @commands.command(brief="auto mutes someone", description="moderation")
    @commands.has_guild_permissions(administrator=True)
    @commands.cooldown(1, 3, commands.BucketType.user)
    @blacklist_check()
    async def automute(self, ctx, user: discord.Member):
        if not automutedb.find_one({"server": ctx.guild.id ,"user": user.id}):
            await user.timeout(timedelta(days = 7), reason="blade ; automute")
            automutedb.insert_one({"_id": user.id})
            
            embed = discord.Embed(description=f"> {emojis.true} **Succesfully** automuted {user.mention}")
            await ctx.send(embed=embed)

        else:
            automutedb.delete_one({"server": ctx.guild.id ,"user": user.id})
            await user.edit(timed_out_until=None, reason='blade ; automute')

            embed = discord.Embed(description=f"> {emojis.true} **Succesfully** removed automute from {user.mention}")
            await ctx.send(embed=embed)

    @commands.command(brief='unmute the user', description='moderation')
    @commands.has_guild_permissions(mute_members=True)
    @commands.cooldown(1, 3, commands.BucketType.user)
    @blacklist_check()
    async def unmute(self, ctx, member : discord.Member):
        if not member.is_timed_out():
            embed = discord.Embed(description=f'> {emojis.false} {member.mention} is not **muted**', color=color.fail)
            await ctx.send(embed=embed)

        else:
            await member.edit(timed_out_until=None, reason='unmute')
            embed = discord.Embed(description=f"> {emojis.true} {member.mention} has been **unmuted**", color=color.color)
            embed.set_author(name=f"{ctx.message.author}", icon_url=ctx.author.display_avatar)
            await ctx.send(embed=embed)

    @commands.command(brief="image mute members", description="moderation", aliases=["imute"])
    @commands.has_guild_permissions(mute_members=True)
    @commands.cooldown(1, 3, commands.BucketType.user)
    @blacklist_check()
    async def imgmute(self, ctx, member : discord.Member):
        if imgmutedb.find_one({"server": ctx.guild.id, "member": member.id}):
            embed = discord.Embed(description=f"> {emojis.false} {member.mention} is already **image** muted", color=color.fail)
            await ctx.send(embed=embed)

        else:
            imgmutedb.insert_one({"server": ctx.guild.id, "member": member.id})
            embed = discord.Embed(description=f"> {emojis.true} **Successfully** image muted {member.mention}", color=color.success)
            await ctx.send(embed=embed)

    @commands.command(brief="image mute members", description="moderation", aliases=["uimute"])
    @commands.has_guild_permissions(mute_members=True)
    @commands.cooldown(1, 3, commands.BucketType.user)
    @blacklist_check()
    async def unimgmute(self, ctx, member : discord.Member):
        if not imgmutedb.find_one({"server": ctx.guild.id, "member": member.id}):
            embed = discord.Embed(description=f"> {emojis.false} {member.mention} is not **image** muted", color=color.fail)
            await ctx.send(embed=embed)

        else:
            imgmutedb.delete_one({"server": ctx.guild.id, "member": member.id})
            embed = discord.Embed(description=f"> {emojis.true} **Successfully** removed image mute from {member.mention}", color=color.success)
            await ctx.send(embed=embed)


    @commands.command(brief='kick a user from your server', description='moderation')
    @commands.has_guild_permissions(kick_members=True)
    @commands.cooldown(1, 3, commands.BucketType.user)
    @blacklist_check()
    async def kick(self, ctx, member : discord.Member, *, reason=None):
        if member.id == 432110614341746689:
            await ctx.send('tf you mean you wanna kick the bot owner, u so retardet, be fr :skull:')
            return

        if member.id == ctx.guild.owner.id:
            embed = discord.Embed(description=f'> {emojis.false} You cant **kick** {member.mention}, they are the **Owner**', color=color.fail)
            await ctx.send(embed=embed)

        elif member.top_role >= ctx.author.top_role:
            if ctx.message.author.id == ctx.guild.owner.id:
                try:
                    member_embed = discord.Embed(description=f'> {emojis.punishment} You have been **Kicked** in ``{ctx.message.guild.name}`` by ``{ctx.message.author.name}`` for: {reason}', color=color.color)
                    await member.send(embed=member_embed)
                except:
                    pass

                await member.kick(reason=reason)
                embed = discord.Embed(description=f"> {emojis.punishment} **Successfully** **kicked** ``{member}`` ``({member.id})`` for: {reason}", color=color.color)
                embed.set_author(name=f"{ctx.message.author}", icon_url=ctx.author.display_avatar)
                await ctx.send(embed=embed)
            else:
                embed = discord.Embed(description=f'> {emojis.false} Cant **kick** {member.mention}, they have a **higher Role**', color=color.fail)
                await ctx.send(embed=embed)

        else:
            try:
                member_embed = discord.Embed(description=f'> {emojis.punishment} You have been **Kicked** in ``{ctx.message.guild.name}`` by ``{ctx.message.author.name}`` for: {reason}', color=color.color)
                await member.send(embed=member_embed)
            except:
                pass

            await member.kick(reason=reason)
            embed = discord.Embed(description=f"> {emojis.punishment} **Successfully** **kicked** ``{member}`` ``({member.id})`` for: {reason}", color=color.color)
            embed.set_author(name=f"{ctx.message.author}", icon_url=ctx.author.display_avatar)
            await ctx.send(embed=embed)

    @commands.command(brief='ban a user from your server', description='moderation')
    @commands.has_guild_permissions(ban_members=True)
    @commands.cooldown(1, 3, commands.BucketType.user)
    @blacklist_check()
    async def ban(self, ctx, member : discord.Member, *, reason=None):
        member_embed = discord.Embed(description=f'> {emojis.punishment} You have been **Banned** in ``{ctx.message.guild.name}`` by ``{ctx.message.author.name}`` for: {reason}', color=color.color)
        error_embed = discord.Embed(description=f"{emojis.false} Couldnt **ban** {member.mention}")
        embed = discord.Embed(description=f"> {emojis.punishment} **Successfully** **banned** ``{member}`` ``({member.id})`` for: {reason}", color=color.color)
        embed.set_author(name=f"{ctx.message.author}", icon_url=ctx.author.display_avatar)

        if member.id == ctx.guild.owner.id:
            embed = discord.Embed(description=f'> {emojis.false} You cant **ban** {member.mention}, they are the **Owner**', color=color.fail)
            await ctx.send(embed=embed)

        elif member.top_role >= ctx.author.top_role:
            if ctx.message.author.id == ctx.guild.owner.id:
                try: 
                    await member.ban(reason=reason)
                    await ctx.send(embed=embed)
                    try: await member.send(embed=member_embed)
                    except: pass
                except:
                    await ctx.send(embed=error_embed)

            else:
                embed = discord.Embed(description=f'> {emojis.false} Couldnt **ban** {member.mention}, cuz they have a **higher Role**', color=color.fail)
                await ctx.send(embed=embed)

        else:
            try: 
                await member.ban(reason=reason)
                await ctx.send(embed=embed)
                try: await member.send(embed=member_embed)
                except: pass
            except:
                await ctx.send(embed=error_embed)

    @commands.command(brief='unban a user from your server', description='moderation')
    @commands.has_guild_permissions(ban_members=True)
    @commands.cooldown(1, 3, commands.BucketType.user)
    @blacklist_check()
    async def unban(self, ctx, member: discord.User):
        try:
            await ctx.guild.unban(member)
            embed = discord.Embed(description=f'> {emojis.true} ``{str(member)}`` got unbanned', color=color.color)
            embed.set_author(name=f"{ctx.message.author}", icon_url=ctx.author.display_avatar)
            await ctx.send(embed=embed)
            return

        except:
            embed = discord.Embed(description=f'> {emojis.false} Ether the **User** hasnt be Found or you didnt used the **User ID**', color=color.fail)
            await ctx.send(embed=embed)

    @commands.command(brief="see all banned members", description='moderation')
    @commands.has_guild_permissions(manage_guild=True)
    @commands.cooldown(1, 3, commands.BucketType.user)
    @blacklist_check()
    async def bans(self, ctx): 
        banned = [m async for m in ctx.guild.bans()]
        if len(banned) == 0: 
            await ctx.send("> There are no banned people in this server")  
            return
    
        i=0
        k=1
        l=0
        mes = ""
        number = []
        messages = []
        for m in banned: 
            mes = f"{mes}`{k}.` **{m.user}** - `{m.reason or 'No reason provided'}` \n"
            k+=1
            l+=1
            if l == 10:
                messages.append(mes)
                number.append(Embed(title=f"banned ({len(banned)})", description=messages[i], color=color.color))
                i+=1
                mes = ""
                l=0
    
        messages.append(mes)
        embed = Embed(title=f"{emojis.blade} Banned ({len(banned)})", description=messages[i], color=color.color)
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
    await client.add_cog(moderation(client))
