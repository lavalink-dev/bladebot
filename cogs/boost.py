import discord
import asyncio
import pymongo
import asyncio
import pymongo
import orjson
import json
from pymongo import MongoClient
from discord.ext import commands
from utils import functions
from utils.emojis import emojis
from utils.color import color

cluster = MongoClient('no')
db = cluster["blade"]
collection = db["boost"]
boostroledb = db["boostrole"]
blacklist = db["blacklist"]

def blacklist_check():
    def predicate(ctx):
        if blacklist.find_one({'_id': ctx.author.id}):
            return False
        return True
    return commands.check(predicate)

class boost(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_member_update(self, before: discord.Member, after: discord.Member): 
        guild = before.guild

        if collection.find_one({"_id": guild.id}):
            check = collection.find_one({"_id": guild.id})
            if before.guild.id == check["_id"]:
                guild = before.guild
                if guild.premium_subscriber_role in after.roles and not guild.premium_subscriber_role in before.roles: 
                    channel = self.client.get_channel(check["channel"])
                    
                    json = check["message"]

                    if "'" in json:
                        json = json.replace("'", '"')
                    try:
                        if "{member.id}" in json:
                            json = json.replace("{member.id}", "%s" % (before.id))
                        if "{member.mention}" in json:
                            json = json.replace("{member.mention}", "%s" % (before.mention))
                        if "{member.tag}" in json:
                            json = json.replace("{member.tag}", "%s" % (before.discriminator))
                        if "{member.name}" in json:
                            json = json.replace("{member.name}", "%s" % (before.name))
                        if "{server.name}" in json:
                            json = json.replace("{server.name}", "%s" % (guild.name))
                        if "{server.id}" in json:
                            json = json.replace("{server.id}", "%s" % (guild.id))
                        if "{server.membercount}" in json:
                            json = json.replace("{server.membercount}", "%s" % (guild.member_count))

                        if "{server.icon}" in json:
                            json = json.replace("{server.icon}", "%s" % (guild.icon))
                        if "{member.avatar}" in json:
                            json = json.replace("{member.avatar}", "%s" % (before.display_avatar))

                        if '"url": "https://{' in json:
                            json = json.replace('"url": "https://{', '"url": "{')

                        if "embed" in json and "content" in json:
                            data = orjson.loads(json)
                            json_embed = data["embed"]
                            embed = discord.Embed.from_dict(json_embed)

                            json_message = data["content"]
                            message = (json_message)
                            await channel.send(message, embed=embed)

                        if "embed" in json and not "content" in json:
                            data = orjson.loads(json)
                            json_embed = data["embed"]
                            embed = discord.Embed.from_dict(json_embed)
                            await channel.send(embed=embed)

                        if "content" in json and not "embed" in json:
                            data = orjson.loads(json)
                            json_message = data["content"]
                            message = (json_message)
                            await channel.send(message)

                    except:
                        pass


    @commands.group(pass_context=True, invoke_without_command=True, aliases=["br"], description="utility", brief="create a booster role")
    @blacklist_check()
    async def boostrole(self, ctx, *, name):
        if ctx.guild.premium_subscriber_role in ctx.author.roles:
            if not boostroledb.find_one({"user": ctx.author.id, "server": ctx.guild.id}):
                role = await ctx.guild.create_role(name=name)

                booster = {"server": ctx.message.guild.id, "user": ctx.author.id, "role": role.id}
                boostroledb.insert_one(booster)     

                await ctx.author.add_roles(role)
                embed = discord.Embed(description=f'> {emojis.true} **Succesfully** created your **Booster** Role with the name ``{name}``', color=color.success)
                await ctx.send(embed=embed)

            else:
                embed = discord.Embed(description=f"> {emojis.false} You already created your own **Booster** Role", color=color.fail)
                await ctx.send(embed=embed)
        else:
            embed = discord.Embed(description=f'> {emojis.false} Cant create **Booster** Role, due no Boost in ``{ctx.guild.name}``')
            await ctx.send(embed=embed)

    @boostrole.command()
    @blacklist_check()
    async def delete(self, ctx):
        if ctx.guild.premium_subscriber_role in ctx.author.roles:
            if boostroledb.find_one({"user": ctx.author.id, "server": ctx.guild.id}):
                check = boostroledb.find_one({"user": ctx.author.id, "server": ctx.guild.id})
                boostroledb.delete_one({"user": ctx.author.id, "server": ctx.guild.id})

                role = self.client.get_role(check["role"])
                await role.delete()

                embed = discord.Embed(description=f'> {emojis.true} **Succesfully** deleted your **Booster** Role', color=color.success)
                await ctx.send(embed=embed)

            else:
                embed = discord.Embed(description=f"> {emojis.false} You dont own a **Booster** Role")
                await ctx.send(embed=embed)
        else:
            embed = discord.Embed(description=f'> {emojis.false} Cant delete **Booster** Role, due no Booster Role in ``{ctx.guild.name}``')
            await ctx.send(embed=embed)

    @boostrole.command()
    @blacklist_check()
    async def rename(self, ctx, *, name):
        if ctx.guild.premium_subscriber_role in ctx.author.roles:
            if boostroledb.find_one({"user": ctx.author.id, "server": ctx.guild.id}):
                check = boostroledb.find_one({"user": ctx.author.id, "server": ctx.guild.id})

                role = self.client.get_role(check["role"])
                await role.edit(name=name)

                embed = discord.Embed(description=f'> {emojis.true} **Succesfully** renamed your **Booster** Role with the name ``{name}``', color=color.success)
                await ctx.send(embed=embed)

            else:
                embed = discord.Embed(description=f"> {emojis.false} You dont own a **Booster** Role", color=color.fail)
                await ctx.send(embed=embed)
        else:
            embed = discord.Embed(description=f'> {emojis.false} Cant create **Booster** Role, due no Boost in ``{ctx.guild.name}``')
            await ctx.send(embed=embed)

    @boostrole.command()
    @blacklist_check()
    async def icon(self, ctx, icon):
        if ctx.guild.premium_subscriber_role in ctx.author.roles:
            if boostroledb.find_one({"user": ctx.author.id, "server": ctx.guild.id}):
                check = boostroledb.find_one({"user": ctx.author.id, "server": ctx.guild.id})

                try:
                    await ctx.message.add_reaction(icon)

                    role = self.client.get_role(check["role"])
                    await role.edit(display_icon=icon)

                    embed = discord.Embed(description=f'> {emojis.true} **Succesfully** changed the **Boosters** Role icon to ``{icon}``', color=color.success)
                    await ctx.send(embed=embed)
                except:
                    embed = discord.Embed(description=f"> {emojis.false} Couldnt find the **Emoji** for the **Icon**", color=color.fail)
                    await ctx.send(embed=embed)

            else:
                embed = discord.Embed(description=f"> {emojis.false} You dont own a **Booster** Role", color=color.fail)
                await ctx.send(embed=embed)
        else:
            embed = discord.Embed(description=f'> {emojis.false} Cant create **Booster** Role, due no Boost in ``{ctx.guild.name}``')
            await ctx.send(embed=embed)

    @commands.group(pass_context=True, invoke_without_command=True, brief='gives a booster message', description='config')
    @blacklist_check()
    async def boost(self, ctx):
        if not collection.find_one({"_id": ctx.message.guild.id}):
            booster = {"_id": ctx.message.guild.id, "boost": False, "channel": 0, "message": ''}
            collection.insert_one(booster)            
        await ctx.invoke()

    @boost.command(brief='test your boost message')
    @commands.has_guild_permissions(manage_guild=True)
    async def test(self, ctx):
        if not collection.find_one({"_id": ctx.message.guild.id}):
            welcomer = {"_id": ctx.message.guild.id, "boost": False, "channel": 0, "message": ''}
            collection.insert_one(welcomer)
        px = functions.get_prefix(ctx)
        check = collection.find_one({"_id": ctx.message.guild.id})

        json = check['message']

        if "{member.id}" in json:
            json = json.replace("{member.id}", "%s" % (ctx.author.id))
        if "{member.mention}" in json:
            json = json.replace("{member.mention}", "%s" % (ctx.author.mention))
        if "{member.tag}" in json:
            json = json.replace("{member.tag}", "%s" % (ctx.author.discriminator))
        if "{member.name}" in json:
            json = json.replace("{member.name}", "%s" % (ctx.author.name))
        if "{server.name}" in json:
            json = json.replace("{server.name}", "%s" % (ctx.guild.name))
        if "{server.id}" in json:
            json = json.replace("{server.id}", "%s" % (ctx.guild.id))
        if "{server.membercount}" in json:
            json = json.replace("{server.membercount}", "%s" % (ctx.guild.member_count))

        if "{server.icon}" in json:
            json = json.replace("{server.icon}", "%s" % (ctx.guild.icon))
        if "{member.avatar}" in json:
            json = json.replace("{member.avatar}", "%s" % (ctx.author.display_avatar))

        try:
            if "embed" in json and "content" in json:
                data = orjson.loads(json)
                json_embed = data["embed"]
                embed = discord.Embed.from_dict(json_embed)

                json_message = data["content"]
                message = (json_message)
                await ctx.send(message, embed=embed)

            if "embed" in json and not "content" in json:
                data = orjson.loads(json)
                json_embed = data["embed"]
                embed = discord.Embed.from_dict(json_embed)
                await ctx.send(embed=embed)

            if "content" in json and not "embed" in json:
                data = orjson.loads(json)
                json_message = data["content"]
                message = (json_message)
                await ctx.send(message)
        except:
            embed = discord.Embed(description=f"> {emojis.false} Invalid **Json** format, use blade's [**Embed Builder**](https://bladebot.org/embed) to create a **Embed**", color=color.fail)
            await ctx.send(embed=embed)

    @boost.command(brief='see the boost message json')
    @commands.has_guild_permissions(manage_guild=True)
    async def json(self, ctx):
        if not collection.find_one({"_id": ctx.message.guild.id}):
            welcomer = {"_id": ctx.message.guild.id, "boost": False, "channel": 0, "message": ''}
            collection.insert_one(welcomer)
        px = functions.get_prefix(ctx)

        check = collection.find_one({"_id": ctx.message.guild.id})

        try:
            embed = discord.Embed(title=f'{emojis.blade} Boost', color=color.color,
                                description=f'{emojis.reply} *look at your boost message json*')
            embed.add_field(name=f"{emojis.commands} Json", value=f"``` {check['message']} ```", inline=False)
            await ctx.send(embed=embed)
        
        except:
            embed = discord.Embed(description=f"> {emojis.false} Invalid **Json** format, use blade's [**Embed Builder**](https://bladebot.org/embed) to create a **Embed**", color=color.fail)
            await ctx.send(embed=embed)

    @boost.command(brief='turn boost message on or off')
    @commands.has_guild_permissions(manage_guild=True)
    async def set(self, ctx, turn=None):
        if not collection.find_one({"_id": ctx.message.guild.id}):
            welcomer = {"_id": ctx.message.guild.id, "welcome": False, "channel": 0, "message": ''}
            collection.insert_one(welcomer)

        check = collection.find_one({"_id": ctx.message.guild.id})
        px = functions.get_prefix(ctx)

        if turn == None:
            embed = discord.Embed(title=f'{emojis.blade} Boost', color=color.color,
            description=f'{emojis.reply} *turn boost message on or off*')
            embed.add_field(name=f"{emojis.commands} Command:", value=f"> ``{px}boost set [on/off]`` set boost message on or off", inline=False)
            await ctx.send(embed=embed)

        if turn == 'on' or turn == 'true':
            if check['boost'] == True:
                embed = discord.Embed(description=f'> {emojis.false} **Boost** is already **activated**', color=color.fail)
                await ctx.send(embed=embed)
            else:
                collection.update_one({"_id": ctx.message.guild.id}, {"$set": {"welcome": True}})
                embed = discord.Embed(description=f'> {emojis.true} **Sucessfully** activated **Boost**', color=color.success)
                await ctx.send(embed=embed)

        elif turn == 'off' or turn == 'false':
            if check['boost'] == False:
                embed = discord.Embed(description=f'> {emojis.false} **Welcome** is not **activated**', color=color.fail)
                await ctx.send(embed=embed)
            else:
                collection.update_one({"_id": ctx.message.guild.id}, {"$set": {"welcome": False}})
                embed = discord.Embed(description=f'> {emojis.true} **Sucessfully** deactivated **Boost**', color=color.success)
                await ctx.send(embed=embed)

        else:
            embed = discord.Embed(description=f'> {emojis.false} You cant set **Welcome** to ``{turn}``', color=color.fail)
            await ctx.send(embed=embed)

    @boost.command(brief='set the channel for the boost message')
    @commands.has_guild_permissions(manage_guild=True)
    async def channel(self, ctx, channel: discord.TextChannel=None):
        if not collection.find_one({"_id": ctx.message.guild.id}):
            welcomer = {"_id": ctx.message.guild.id, "boost": False, "channel": 0, "message": ''}
            collection.insert_one(welcomer)
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

            embed = discord.Embed(title=f'{emojis.blade} Boost', color=color.color,
            description=f'{emojis.reply} *set the boost channel*')
            embed.add_field(name=f"{emojis.commands} Command:", value=f"> ``{px}boost channel [#channel]`` set the boost channel", inline=False)
            embed.add_field(name=f"{emojis.config} Config:", value=f"> ``Status`` {status}", inline=False)
            embed.add_field(name=f"{emojis.config} Channel:", value=f"> {channel}", inline=False)
            await ctx.send(embed=embed)

        else:
            if check['channel'] == 0:
                collection.update_one({"_id": ctx.message.guild.id}, {"$set": {"channel": channel.id}})
                embed = discord.Embed(description=f'> {emojis.true} **Succesfully** set {channel.mention} as **Boost Channel**', color=color.success)
                await ctx.send(embed=embed)
            elif check['channel']:
                collection.update_one({"_id": ctx.message.guild.id}, {"$set": {"channel": channel.id}})
                embed = discord.Embed(description=f'> {emojis.true} **Succesfully** changed the **Boost Channel** to {channel.mention}', color=color.success)
                await ctx.send(embed=embed)
            elif check['channel'] == channel.id:
                embed = discord.Embed(description=f'> {emojis.false} {channel.mention} is already the **Boost Channel**', color=color.fail)
                await ctx.send(embed=embed)

    @boost.command(brief='clear the boost config')
    @commands.has_guild_permissions(manage_guild=True)
    @blacklist_check()
    async def clear(self, ctx):
        if not collection.find_one({"_id": ctx.message.guild.id}):
            welcomer = {"_id": ctx.message.guild.id, "boost": False, "channel": 0, "message": ''}
            collection.insert_one(welcomer)

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
                embed = discord.Embed(description=f'> {emojis.true} You cleared the **Boost** config', color=color.success)
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
                embed = discord.Embed(description=f'> {emojis.true} The **Boost** Config hasnt been **Cleared**', color=color.success)
                await interaction.response.edit_message(embed=embed, view=view)

        accept.callback = accept_callback
        decline.callback = decline_callback

        view = discord.ui.View()
        view.add_item(item=accept)
        view.add_item(item=decline)

        embed = discord.Embed(description=f'> Are you sure to clear your **Boost** config?', color=color.color)
        await ctx.send(embed=embed, view=view)

    @boost.command(brief='set boost message')
    @commands.has_guild_permissions(manage_guild=True)
    async def message(self, ctx, *, json=None):
        if not collection.find_one({"_id": ctx.message.guild.id}):
            welcomer = {"_id": ctx.message.guild.id, "boost": False, "channel": 0, "message": ''}
            collection.insert_one(welcomer)
        px = functions.get_prefix(ctx)

        check = collection.find_one({"_id": ctx.message.guild.id})

        if json == None:
            embed = discord.Embed(title=f'{emojis.blade} Boost', color=color.color,
            description=f'{emojis.reply} *set the boost message with json*')
            embed.add_field(name=f"{emojis.commands} Command:", value=f"> ``{px}boost message [json]`` set the boost message with json \n> ``{px}boost json`` look at your set boost message", inline=False)
            embed.add_field(name=f"{emojis.config} How To:", value=f"> Visit our [``Embed Builder``](https://bladebot.org/) and Create your Message", inline=False)
            embed.add_field(name=f"{emojis.config} Variables:", value="> ``{member.mention}`` mentions the member \n> ``{member.name}`` shows the members name \n> ``{member.tag}`` shows the members tag \n> ``{member.id}`` shows joined members id \n> ``{server.name}`` shows the name of the server \n> ``{server.id}`` shows the id of the server \n> ``{server.membercount}`` shows the member count of the server \n> ``{member.avatar}`` sets the joined members avatar as image \n> ``{server.icon}`` sets the server icon as image", inline=False)
            await ctx.send(embed=embed)

        else:
            if "'" in json:
                json = json.replace("'", '"')
            try:
                collection.update_one({"_id": ctx.message.guild.id}, {"$set": {"message": json}})
                embed = discord.Embed(description=f'> {emojis.true} Set the **Boost Message** to:', color=color.success)

                if "{member.id}" in json:
                    json = json.replace("{member.id}", "%s" % (ctx.author.id))
                if "{member.mention}" in json:
                    json = json.replace("{member.mention}", "%s" % (ctx.author.mention))
                if "{member.tag}" in json:
                    json = json.replace("{member.tag}", "%s" % (ctx.author.discriminator))
                if "{member.name}" in json:
                    json = json.replace("{member.name}", "%s" % (ctx.author.name))
                if "{server.name}" in json:
                    json = json.replace("{server.name}", "%s" % (ctx.guild.name))
                if "{server.id}" in json:
                    json = json.replace("{server.id}", "%s" % (ctx.guild.id))
                if "{server.membercount}" in json:
                    json = json.replace("{server.membercount}", "%s" % (ctx.guild.member_count))

                if "{server.icon}" in json:
                    json = json.replace("{server.icon}", "%s" % (ctx.guild.icon))
                if "{member.avatar}" in json:
                    json = json.replace("{member.avatar}", "%s" % (ctx.author.display_avatar))

                if '"url": "https://{' in json:
                    json = json.replace('"url": "https://{', '"url": "{')

                if "embed" in json and "content" in json:
                    await ctx.send(embed=embed)

                    data = orjson.loads(json)
                    json_embed = data["embed"]
                    embed = discord.Embed.from_dict(json_embed)

                    json_message = data["content"]
                    message = (json_message)
                    await ctx.send(message, embed=embed)

                if "embed" in json and not "content" in json:
                    await ctx.send(embed=embed)

                    data = orjson.loads(json)
                    json_embed = data["embed"]
                    embed = discord.Embed.from_dict(json_embed)
                    await ctx.send(embed=embed)

                if "content" in json and not "embed" in json:
                    await ctx.send(embed=embed)

                    data = orjson.loads(json)
                    json_message = data["content"]
                    message = (json_message)
                    await ctx.send(message)

            except:
                embed = discord.Embed(description=f"> {emojis.false} Invalid **Json** format, use blade's [**Embed Builder**](https://bladebot.org/embed) to create a **Embed**", color=color.fail)
                await ctx.send(embed=embed)
        
async def setup(client):
    await client.add_cog(boost(client))
