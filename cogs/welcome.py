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

cluster = MongoClient('mongodb+srv://blade:lolidkbruh12333333333@cluster0.wbxaj.mongodb.net/myFirstDatabase?retryWrites=true&w=majority')
db = cluster["blade"]
collection = db["welcome"]

class welcome(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.group(pass_context=True, invoke_without_command=True, aliases=['welc'], brief='welcome new members', description='config')
    @commands.has_guild_permissions(manage_guild=True)
    async def welcome(self, ctx):
        if not collection.find_one({"_id": ctx.message.guild.id}):
            welcomer = {"_id": ctx.message.guild.id, "welcome": False, "channel": 0, "message": ''}
            collection.insert_one(welcomer)
            
        await ctx.invoke()

    @welcome.command(brief='clear welcome')
    @commands.has_guild_permissions(manage_guild=True)
    async def clear(self, ctx):
        if not collection.find_one({"_id": ctx.message.guild.id}):
            welcomer = {"_id": ctx.message.guild.id, "welcome": False, "channel": 0, "message": ''}
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
                embed = discord.Embed(description=f'> {emojis.true} **Successfully** cleared **Welcome**', color=color.success)
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
                embed = discord.Embed(description=f'> {emojis.true} Your **Welcome** hasnt been **Cleared**', color=color.success)
                await interaction.response.edit_message(embed=embed, view=view)

        accept.callback = accept_callback
        decline.callback = decline_callback

        view = discord.ui.View()
        view.add_item(item=accept)
        view.add_item(item=decline)

        embed = discord.Embed(description=f'> Are you sure to clear your **Welcome** config?', color=color.color)
        await ctx.send(embed=embed, view=view)

    @welcome.command(brief='turn welcome on or off')
    @commands.has_guild_permissions(manage_guild=True)
    async def set(self, ctx, turn):
        if not collection.find_one({"_id": ctx.message.guild.id}):
            welcomer = {"_id": ctx.message.guild.id, "welcome": False, "channel": 0, "message": ''}
            collection.insert_one(welcomer)

        check = collection.find_one({"_id": ctx.message.guild.id})
        px = functions.get_prefix(ctx)

        if turn == None:
            embed = discord.Embed(title=f'{emojis.blade} Welcome', color=color.color,
            description=f'{emojis.reply} *turn welcome on or off*')
            embed.add_field(name=f"{emojis.commands} Command:", value=f"> ``{px}welcome set [on/off]`` set welcome on or off", inline=False)
            await ctx.send(embed=embed)

        if turn == 'on' or turn == 'true':
            if check['welcome'] == True:
                embed = discord.Embed(description=f'> {emojis.false} **Welcome** is already **activated**', color=color.fail)
                await ctx.send(embed=embed)
            else:
                collection.update_one({"_id": ctx.message.guild.id}, {"$set": {"welcome": True}})
                embed = discord.Embed(description=f'> {emojis.true} **Successfully** activated **Welcome**', color=color.success)
                await ctx.send(embed=embed)

        elif turn == 'off' or turn == 'false':
            if check['welcome'] == False:
                embed = discord.Embed(description=f'> {emojis.false} **Welcome** is **deactivated**', color=color.fail)
                await ctx.send(embed=embed)
            else:
                collection.update_one({"_id": ctx.message.guild.id}, {"$set": {"welcome": False}})
                embed = discord.Embed(description=f'> {emojis.true} **Succesfully** deactivated **Welcome**', color=color.success)
                await ctx.send(embed=embed)

        else:
            embed = discord.Embed(description=f'> {emojis.false} You cant set **Welcome** to ``{turn}``', color=color.fail)
            await ctx.send(embed=embed)

    @welcome.command(brief='set the channel for the welcome message')
    @commands.has_guild_permissions(manage_guild=True)
    async def channel(self, ctx, channel: discord.TextChannel=None):
        if not collection.find_one({"_id": ctx.message.guild.id}):
            welcomer = {"_id": ctx.message.guild.id, "welcome": False, "channel": 0, "message": ''}
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

            embed = discord.Embed(title=f' Welcome', color=color.color,
            description=f'{emojis.reply} *set the welcome channel*')
            embed.add_field(name=f"{emojis.commands} Command:", value=f"> ``{px}welcome channel [#channel]`` set the welcome channel", inline=False)
            embed.add_field(name=f"{emojis.config} Config:", value=f"> ``Status`` {status}", inline=False)
            embed.add_field(name=f"{emojis.config} Channel:", value=f"> {channel}", inline=False)
            embed.set_footer(text=f'for help, use our Tutorial: {px}welcome tutorial')
            await ctx.send(embed=embed)

        else:
            if check['channel'] == 0:
                collection.update_one({"_id": ctx.message.guild.id}, {"$set": {"channel": channel.id}})
                embed = discord.Embed(description=f'> {emojis.true} You set {channel.mention} as **Welcome Channel**', color=color.success)
                await ctx.send(embed=embed)
            elif check['channel']:
                collection.update_one({"_id": ctx.message.guild.id}, {"$set": {"channel": channel.id}})
                embed = discord.Embed(description=f'> {emojis.true} You changed the **Welcome Channel** to {channel.mention}', color=color.success)
                await ctx.send(embed=embed)
            elif check['channel'] == channel.id:
                embed = discord.Embed(description=f'> {emojis.false} {channel.mention} is already the **Welcome Channel**', color=color.fail)
                await ctx.send(embed=embed)

    @welcome.command(brief='set welcome message')
    @commands.has_guild_permissions(manage_guild=True)
    async def message(self, ctx, *, json=None):
        if not collection.find_one({"_id": ctx.message.guild.id}):
            welcomer = {"_id": ctx.message.guild.id, "welcome": False, "channel": 0, "message": ''}
            collection.insert_one(welcomer)
        px = functions.get_prefix(ctx)

        check = collection.find_one({"_id": ctx.message.guild.id})

        if json == None:
            embed = discord.Embed(title=f' Welcome', color=color.color,
            description=f'{emojis.reply} *set the welcome message with json*')
            embed.add_field(name=f"{emojis.commands} Command:", value=f"> ``{px}welcome message [json]`` set the welcome message with json \n> ``{px}welcome json`` look at your set welcome message", inline=False)
            embed.add_field(name=f"{emojis.config} How To:", value=f"> Visit our [``Embed Builder``](https://bladebot.org/embed) and Create your Message", inline=False)
            embed.add_field(name=f"{emojis.config} Variables:", value="> ``{member.mention}`` mentions the joined member \n> ``{member.name}`` shows the joined members name \n> ``{member.tag}`` shows the members tag \n> ``{member.id}`` shows joined members id \n> ``{server.name}`` shows the name of the server \n> ``{server.id}`` shows the id of the server \n> ``{server.membercount}`` shows the member count of the server \n> ``{member.avatar}`` sets the joined members avatar as image \n> ``{server.icon}`` sets the server icon as image", inline=False)
            embed.set_footer(text=f'for help, use our Tutorial: {px}welcome tutorial')
            await ctx.send(embed=embed)

        else:
            if "'" in json:
                json = json.replace("'", '"')

            collection.update_one({"_id": ctx.message.guild.id}, {"$set": {"message": json}})

            success_embed = discord.Embed(description=f'> {emojis.true} Set the **Welcome Message** to:', color=color.success)

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

            try:
                if "embed" in json and "content" in json:
                    data = orjson.loads(json)
                    json_embed = data["embed"]
                    embed = discord.Embed.from_dict(json_embed)

                    json_message = data["content"]
                    message = (json_message)

                    await ctx.send(embed=success_embed)
                    await ctx.send(message, embed=embed)

                if "embed" in json and not "content" in json:
                    data = orjson.loads(json)
                    json_embed = data["embed"]
                    embed = discord.Embed.from_dict(json_embed)

                    await ctx.send(embed=success_embed)
                    await ctx.send(embed=embed)

                if "content" in json and not "embed" in json:
                    data = orjson.loads(json)
                    json_message = data["content"]
                    message = (json_message)
                    
                    await ctx.send(embed=success_embed)
                    await ctx.send(message)
                

            except:
                embed = discord.Embed(description=f"> {emojis.false} Invalid **Json** format, use blade's [**Embed Builder**](https://bladebot.org/embed) to create a **Embed**", color=color.fail)
                await ctx.send(embed=embed)

    @welcome.command(brief='see the welcome json')
    @commands.has_guild_permissions(manage_guild=True)
    async def json(self, ctx):
        if not collection.find_one({"_id": ctx.message.guild.id}):
            welcomer = {"_id": ctx.message.guild.id, "welcome": False, "channel": 0, "message": ''}
            collection.insert_one(welcomer)
        px = functions.get_prefix(ctx)

        check = collection.find_one({"_id": ctx.message.guild.id})

        if check["message"] != "":
            if len(check["message"]) > 1024:
                embed = discord.Embed(description=f"> {emojis.false} The **JSON** is to long to **Display**", color=color.fail)
                await ctx.send(embed=embed)
            else:
                embed = discord.Embed(title=f' Welcome', color=color.color,
                                    description=f'{emojis.reply} *look at your welcome json*')
                embed.add_field(name=f"{emojis.commands} Json", value=f"``` {check['message']} ```", inline=False)
                await ctx.send(embed=embed)
        
        else:
            embed = discord.Embed(description=f"> {emojis.false} Invalid **Json** format, use blade's [**Embed Builder**](https://bladebot.org/embed) to create a **Embed**", color=color.fail)
            await ctx.send(embed=embed)

    @welcome.command(brief='test your welcome message')
    @commands.has_guild_permissions(manage_guild=True)
    async def test(self, ctx):
        if not collection.find_one({"_id": ctx.message.guild.id}):
            welcomer = {"_id": ctx.message.guild.id, "welcome": False, "channel": 0, "message": ''}
            collection.insert_one(welcomer)
        px = functions.get_prefix(ctx)
        check = collection.find_one({"_id": ctx.message.guild.id})

        if check['message'] == '':
            embed = discord.Embed(description=f'> {emojis.false} There is no **Message** set up', color=color.fail)
            await ctx.send(embed=embed)

        else:
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

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        if not collection.find_one({"_id": member.guild.id}):
            return
        else:
            check = collection.find_one({"_id": member.guild.id})
            if member.guild.id == check["_id"]:
                channel = self.client.get_channel(check["channel"])

                json = check['message']

                if "{member.id}" in json:
                    json = json.replace("{member.id}", "%s" % (member.id))
                if "{member.mention}" in json:
                    json = json.replace("{member.mention}", "%s" % (member.mention))
                if "{member.tag}" in json:
                    json = json.replace("{member.tag}", "%s" % (member.discriminator))
                if "{member.name}" in json:
                    json = json.replace("{member.name}", "%s" % (member.name))
                if "{server.name}" in json:
                    json = json.replace("{server.name}", "%s" % (member.guild.name))
                if "{server.id}" in json:
                    json = json.replace("{server.id}", "%s" % (member.guild.id))
                if "{server.membercount}" in json:
                    json = json.replace("{server.membercount}", "%s" % (member.guild.member_count))

                if "{server.icon}" in json:
                    json = json.replace("{server.icon}", "%s" % (member.guild.icon))
                if "{member.avatar}" in json:
                    json = json.replace("{member.avatar}", "%s" % (member.display_avatar))

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

        await asyncio.sleep(2)

async def setup(client):
    await client.add_cog(welcome(client))
