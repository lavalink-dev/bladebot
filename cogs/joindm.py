import discord
import discord
import asyncio
import orjson
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
collection = db["joindm"]
blacklist = db["blacklist"]

def blacklist_check():
    def predicate(ctx):
        if blacklist.find_one({'_id': ctx.author.id}):
            return False
        return True
    return commands.check(predicate)


class joindm(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.group(pass_context=True, invoke_without_command=True, description='config', brief='dm new members')
    @commands.has_guild_permissions(manage_guild=True)
    @blacklist_check()
    async def joindm(self, ctx):
        if not collection.find_one({"_id": ctx.message.guild.id}):
            joindmr = {"_id": ctx.message.guild.id, "joindm": False, "message": ''}
            collection.insert_one(joindmr)

        await ctx.invoke()

    @joindm.command(brief='clear the joindm config')
    @commands.has_guild_permissions(manage_guild=True)
    @blacklist_check()
    async def clear(self, ctx):
        if not collection.find_one({"_id": ctx.message.guild.id}):
            joindmr = {"_id": ctx.message.guild.id, "joindm": False, "channel": 0, "message": ''}
            collection.insert_one(joindmr)

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
                embed = discord.Embed(description=f'> {emojis.true} You cleared the **joindm** config', color=color.success)
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
                embed = discord.Embed(description=f'> {emojis.true} Your **joindm** hasnt been **Cleared**', color=color.success)
                await interaction.response.edit_message(embed=embed, view=view)

        accept.callback = accept_callback
        decline.callback = decline_callback

        view = discord.ui.View()
        view.add_item(item=accept)
        view.add_item(item=decline)

        embed = discord.Embed(description=f'> Are you sure to clear your **joindm** config?', color=color.color)
        await ctx.send(embed=embed, view=view)

    @joindm.command(brief='activate or deactivate')
    @commands.has_guild_permissions(manage_guild=True)
    @blacklist_check()
    async def set(self, ctx, turn=None):
        if not collection.find_one({"_id": ctx.message.guild.id}):
            joindmr = {"_id": ctx.message.guild.id, "joindm": False, "channel": 0, "message": ''}
            collection.insert_one(joindmr)

        check = collection.find_one({"_id": ctx.message.guild.id})
        px = functions.get_prefix(ctx)

        if turn == None:
            embed = discord.Embed(title=f'JoinDM', color=color.color,
            description=f'{emojis.reply} *turn joindm on or off*')
            embed.add_field(name=f"{emojis.commands} Command:", value=f"{emojis.reply} ``{px}joindm set [on/off]`` set joindm on or off", inline=False)
            await ctx.send(embed=embed)

        if turn == 'on' or turn == 'true':
            if check['joindm'] == True:
                embed = discord.Embed(description=f'> {emojis.false} **joindm** is already **activated**', color=color.fail)
                await ctx.send(embed=embed)
            else:
                collection.update_one({"_id": ctx.message.guild.id}, {"$set": {"joindm": True}})
                embed = discord.Embed(description=f'> {emojis.true} **Succesfully** **activated** **joindm**', color=color.success)
                await ctx.send(embed=embed)

        elif turn == 'off' or turn == 'false':
            if check['joindm'] == False:
                embed = discord.Embed(description=f'> {emojis.false} **joindm** is not **activated**', color=color.fail)
                await ctx.send(embed=embed)
            else:
                collection.update_one({"_id": ctx.message.guild.id}, {"$set": {"joindm": False}})
                embed = discord.Embed(description=f'> {emojis.true} **Succesfully** **deactivated** **joindm**', color=color.success)
                await ctx.send(embed=embed)

        else:
            embed = discord.Embed(description=f'> {emojis.false} Cant set **joindm** to ``{turn}``', color=color.fail)
            await ctx.send(embed=embed)

    @joindm.command(brief='set joindm message')
    @commands.has_guild_permissions(manage_guild=True)
    @blacklist_check()
    async def message(self, ctx, *, json=None):
        if not collection.find_one({"_id": ctx.message.guild.id}):
            joindmr = {"_id": ctx.message.guild.id, "joindm": False, "channel": 0, "message": ''}
            collection.insert_one(joindmr)
        px = functions.get_prefix(ctx)

        check = collection.find_one({"_id": ctx.message.guild.id})

        if json == None:
            embed = discord.Embed(title=f'JoinDM', color=color.color,
            description=f'{emojis.reply} *set the joindm message with json*')
            embed.add_field(name=f"{emojis.commands} Command:", value=f"{emojis.reply2} ``{px}joindm message [json]`` set the joindm message with json \n{emojis.reply} ``{px}joindm json`` look at your set joindm message", inline=False)
            embed.add_field(name=f"{emojis.config} Variables:", value="> ``{member.mention}`` mentions the joined member \n> ``{member.name}`` shows the joined members name \n> ``{member.tag}`` shows the members tag \n> ``{member.id}`` shows joined members id \n> ``{server.name}`` shows the name of the server \n> ``{server.id}`` shows the id of the server \n> ``{server.membercount}`` shows the member count of the server \n> ``{member.avatar}`` sets the joined members avatar as image \n> ``{server.icon}`` sets the server icon as image", inline=False)
            embed.set_footer(text=f'for help, use our Tutorial: {px}joindm tutorial')
            await ctx.send(embed=embed)

        else:
            if "'" in json:
                json = json.replace("'", '"')
            try:
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
                    await ctx.send(message)

                if "content" in json and not "embed" in json:
                    data = orjson.loads(json)
                    json_message = data["content"]
                    message = (json_message)
                    
                    await ctx.send(embed=success_embed)
                    await ctx.send(message)

            except:
                embed = discord.Embed(description=f"> {emojis.false} Invalid **Json** format", color=color.fail)
                await ctx.send(embed=embed)

    @joindm.command(brief='see the joindm json')
    @commands.has_guild_permissions(manage_guild=True)
    @blacklist_check()
    async def json(self, ctx, *, json=None):
        if not collection.find_one({"_id": ctx.message.guild.id}):
            joindmr = {"_id": ctx.message.guild.id, "joindm": False, "channel": 0, "message": ''}
            collection.insert_one(joindmr)
        px = functions.get_prefix(ctx)

        check = collection.find_one({"_id": ctx.message.guild.id})

        try:
            embed = discord.Embed(title=f'JoinDM', color=color.color,
                                description=f'{emojis.reply} *look at your joindm json*')
            embed.add_field(name=f"{emojis.commands} Json", value=f"``` {check['message']} ```", inline=False)
            await ctx.send(embed=embed)
        
        except:
            embed = discord.Embed(description=f"> {emojis.false} Invalid **Json** format", color=color.fail)
            await ctx.send(embed=embed)

    @joindm.command(brief='test the joindm message')
    @commands.has_guild_permissions(manage_guild=True)
    @blacklist_check()
    async def test(self, ctx):
        if not collection.find_one({"_id": ctx.message.guild.id}):
            joindmr = {"_id": ctx.message.guild.id, "joindm": False, "channel": 0, "message": ''}
            collection.insert_one(joindmr)
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
            embed = discord.Embed(description=f"> {emojis.false} Invalid **Json** format", color=color.fail)
            await ctx.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        if collection.find_one({"_id": member.guild.id}):
            check = collection.find_one({"_id": member.guild.id})
            if member.guild.id == check["_id"]:

                buttons = discord.ui.View()
                style = discord.ButtonStyle.gray
                button = discord.ui.Button(style=style, label=f"sent from: {member.guild.name}", disabled = True)
                buttons.add_item(item=button)

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
                    await member.send(message, embed=embed, view=buttons)

                if "embed" in json and not "content" in json:
                    data = orjson.loads(json)
                    json_embed = data["embed"]
                    embed = discord.Embed.from_dict(json_embed)
                    await member.send(embed=embed, view=buttons)

                if "content" in json and not "embed" in json:
                    data = orjson.loads(json)
                    json_message = data["content"]
                    message = (json_message)
                    await member.send(message, view=buttons)

        await asyncio.sleep(2)

async def setup(client):
    await client.add_cog(joindm(client))
