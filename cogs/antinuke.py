import discord
import asyncio
import pymongo
from discord.ext import commands
from pymongo import MongoClient
from utils import functions
from utils.emojis import emojis
from utils.color import color

cluster = MongoClient('no')
db = cluster["blade"]
collection = db["antinuke"]
blacklist = db["blacklist"]

def blacklist_check():
    def predicate(ctx):
        if blacklist.find_one({'_id': ctx.author.id}):
            return False
        return True
    return commands.check(predicate)

class antinuke(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.group(pass_context=True, invoke_without_command=True, aliases=['an'], description='config', brief='secures your server')
    @blacklist_check()
    async def antinuke(self, ctx):
        if ctx.message.author == ctx.guild.owner:
            if not collection.find_one({"_id": ctx.message.guild.id}):
                antinuker = {"_id": ctx.message.guild.id, "antinuke": False, "punishment": 'none', "logs": 0, "whitelisted": []}
                collection.insert_one(antinuker)
                collection.update_one({"_id": ctx.message.guild.id}, {"$push": {"whitelisted": ctx.guild.owner.id}})
                collection.update_one({"_id": ctx.message.guild.id}, {"$push": {"whitelisted": 896550468128505877}})

            px = functions.get_prefix(ctx)
            check = collection.find_one({"_id": ctx.message.guild.id})

            if check["antinuke"] == False:
                antinuke = f"{emojis.false} *(not activated)*"
            if check["antinuke"]:
                antinuke = f"{emojis.true} *(activated)*"

            if check["punishment"] == 'none':
                punishment = f"{emojis.false} *(not set)*"
            elif check["punishment"]:
                punishment = f'**{check["punishment"]}**'

            if check["logs"] == 0:
                logs = f"{emojis.false} *(not created)*"
            elif check["logs"]:
                try:
                    channel = self.client.get_channel(check["logs"])
                    logs = f'**{channel.mention}** | ``{channel.id}``'
                except:
                    collection.update_one({"_id": ctx.message.guild.id}, {"$set": {"antinuke": False}})
                    logs = f'{emojis.false} *(channel got deleted)*'

            embed = discord.Embed(title=f'{emojis.blade} AntiNuke', color=color.color,
            description=f'{emojis.reply} secure your server bozo.')
            embed.add_field(name=f"{emojis.commands} Commands:", value=f"> ``{px}antinuke set [on/off]`` set your antinuke on or off \n> ``{px}antinuke punishment [punishment]`` set the punishment for the antinuke \n> ``{px}antinuke whitelist [@member]`` whitelist trusted members \n> ``{px}antinuke whitelisted`` see who is whitelisted \n> ``{px}antinuke unwhitelist [@member]`` unwhitelist users \n> ``{px}antinuke logs`` create a antinuke logs channel \n> ``{px}antinuke clear`` clear your antinukes settings", inline=False)
            embed.add_field(name=f"{emojis.config} Config:", value=f"> ``status`` {antinuke} \n> ``punishment`` {punishment} \n> ``logs`` {logs}", inline=False)
            embed.add_field(name=f"{emojis.alias} Aliases:", value=f"```an```", inline=False)
            embed.set_footer(text='disclaimer: the AntiNuke works when the Bot has the highest role!')
            await ctx.send(embed=embed)

        else:
            embed = discord.Embed(title=f'{emojis.blade} AntiNuke', color=color.fail,
            description=f'{emojis.reply} only the **Server Owner** can use this **command**')
            await ctx.send(embed=embed)

    @antinuke.command()
    @blacklist_check()
    async def whitelisted(self, ctx):
        if ctx.message.author == ctx.guild.owner:
            data = collection.find_one({"_id": ctx.guild.id })['whitelisted']
            embed = discord.Embed(title=f"{emojis.blade} AntiNuke", description=f"{emojis.reply} AntiNuke whitelist \n \n", color=color.color)
            #embed.set_footer(text="all of a user's roles will be removed when a limit is hit")
            for i in data:
                if ctx.bot.get_user(i) != None:
                    if ctx.bot.get_user(i) == ctx.guild.owner:
                        embed.description += f"Owner **|** <@{i}> | `{i}`\n"
                    if ctx.bot.get_user(i) != ctx.guild.owner:
                        if ctx.bot.get_user(i).bot:
                            embed.description += f"Bot **|** <@{i}> | `{i}`\n"
                        else:
                             embed.description += f"User **|** <@{i}> | `{i}`\n"
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(title=f'{emojis.blade} AntiNuke', color=color.fail,
            description=f'{emojis.reply} only the **Server Owner** can use this **command**')
            await ctx.send(embed=embed)

    @antinuke.command()
    @blacklist_check()
    async def whitelist(self, ctx, member: discord.Member=None):
        if ctx.message.author == ctx.guild.owner:
            check = collection.find_one({"_id": ctx.message.guild.id})
            px = functions.get_prefix(ctx)

            if check["whitelisted"] == []:
                whitelisted = '*no one is whitelisted*'

            elif check["whitelisted"]:
                whitelisted = f"They're Persons **Whitelisted**, use ``{px}antinuke whitelisted`` to see who is whitelisted."

            if member == None:
                embed = discord.Embed(title=f'{emojis.blade} AntiNuke', color=color.color,
                description=f'{emojis.reply} AntiNuke whitelist')
                embed.add_field(name=f"> Description:", value=f"whitelist **users**, so they dont get detected from the **AntiNuke**", inline=False)
                embed.add_field(name=f"{emojis.commands} Command:", value=f"``{px}antinuke whitelist [@user]``", inline=False)
                embed.add_field(name=f"> **Example:**", value=f"**usage:** ``$antinuke whitelist @fin`` \n {emojis.reply} fin gets added to the whitelist and cant get detected from the AntiNuke", inline=False)
                embed.add_field(name=f"{emojis.config} Whitelisted:", value=f"{whitelisted}", inline=False)
                await ctx.send(embed=embed)

            else:
                collection.update_one({"_id": ctx.message.guild.id}, {"$push": {"whitelisted": member.id}})
                embed = discord.Embed(title=f'{emojis.blade} AntiNuke', color=color.color,
                description=f'{emojis.reply} {member.mention} got added to the **Whitelist**')
                await ctx.send(embed=embed)
        else:
            embed = discord.Embed(title=f'{emojis.blade} AntiNuke', color=color.fail,
            description=f'{emojis.reply} only the **Server Owner** can use this **command**')
            await ctx.send(embed=embed)

    @antinuke.command()
    @blacklist_check()
    async def unwhitelist(self, ctx, member: discord.Member=None):
        if ctx.message.author == ctx.guild.owner:
            check = collection.find_one({"_id": ctx.message.guild.id})
            px = functions.get_prefix(ctx)

            if check["whitelisted"] == []:
                whitelisted = '*no one is whitelisted*'

            elif check["whitelisted"]:
                whitelisted = f"They're Persons **Whitelisted**, use ``{px}antinuke whitelisted`` to see who is whitelisted."

            if member == None:
                embed = discord.Embed(title=f'{emojis.blade} AntiNuke', color=color.color,
                description=f'{emojis.reply} AntiNuke whitelist')
                embed.add_field(name=f"> Description:", value=f"unwhitelist **users**, so they get detected from the **AntiNuke**", inline=False)
                embed.add_field(name=f"{emojis.commands} Command:", value=f"``{px}antinuke unwhitelist [@user]``", inline=False)
                embed.add_field(name=f"> **Example:**", value=f"**usage:** ``$antinuke unwhitelist @fin`` \n {emojis.reply} fin gets removed from the whitelist and gets detected again", inline=False)
                embed.add_field(name=f"{emojis.config} Whitelisted:", value=f"{whitelisted}", inline=False)
                await ctx.send(embed=embed)

            else:
                collection.update_one({"_id": ctx.message.guild.id}, {"$pull": {"whitelisted": member.id}})
                embed = discord.Embed(title=f'{emojis.blade} AntiNuke', color=color.success,
                description=f'{emojis.reply} {member.mention} got removed from the **Whitelist**')
                await ctx.send(embed=embed)
        else:
            embed = discord.Embed(title=f'{emojis.blade} AntiNuke', color=color.fail,
            description=f'{emojis.reply} only the **Server Owner** can use this **command**')
            await ctx.send(embed=embed)

    @antinuke.command()
    @blacklist_check()
    async def clear(self, ctx):
        if ctx.message.author == ctx.guild.owner:
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
                    embed = discord.Embed(description=f"> {emojis.false} This is not your message", color=color.cf  )
                    await interaction.response.send_message(embed=embed, view=None, ephemeral=True)
                    return

                else:
                    collection.delete_one({"_id": ctx.message.guild.id})
                    embed = discord.Embed(description=f'> {emojis.true} **Successfully** cleared **AntiNuke**', color=color.success)
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
                    embed = discord.Embed(description=f'> {emojis.true} **AntiNuke** hasnt been **Cleared**', color=color.success)
                    await interaction.response.edit_message(embed=embed, view=view)

            accept.callback = accept_callback
            decline.callback = decline_callback

            view = discord.ui.View()
            view.add_item(item=accept)
            view.add_item(item=decline)

            embed = discord.Embed(description=f'> Are you sure to clear your **AntiNuke** config?', color=color.success)
            await ctx.send(embed=embed, view=view)
        else:
            embed = discord.Embed(title=f'{emojis.blade} AntiNuke',
            description=f'{emojis.reply} only the **Server Owner** can use this **command**', color=color.fail)
            await ctx.send(embed=embed)

    @antinuke.command()
    @blacklist_check()
    async def set(self, ctx, function=None):
        if ctx.message.author == ctx.guild.owner:
            px = functions.get_prefix(ctx)
            check = collection.find_one({"_id": ctx.message.guild.id})

            if function == None:
                embed = discord.Embed(title=f'{emojis.blade} AntiNuke', color=color.color,
                description=f'{emojis.reply} AntiNuke set')
                embed.add_field(name=f"> Description:", value=f"set your AntiNuke on or off", inline=False)
                embed.add_field(name=f"{emojis.commands} Command:", value=f"``{px}antinuke set [on/off]``", inline=False)
                embed.add_field(name=f"> **Example:**", value=f"**usage:** ``$antinuke set on`` \n {emojis.reply} your AntiNuke is now on and detects nukers", inline=False)
                await ctx.send(embed=embed)

            if function == 'on':
                if check["antinuke"] == True:
                    embed = discord.Embed(title=f'{emojis.blade} AntiNuke', color=color.fail,
                    description=f'{emojis.reply} your **AntiNuke** is already ``activated``')
                    await ctx.send(embed=embed)
                if check["antinuke"] == False:
                    if check["punishment"] == 'none' and check["logs"] == 0:
                        embed = discord.Embed(title=f'{emojis.blade} AntiNuke', color=color.fail,
                        description=f'{emojis.reply} your **AntiNuke** cant be ``activated`` because you didnt set a, **punishment** and created a **logs channel** \n> **use:** ``{px}antinuke punishment`` ``{px}antinuke logs``')
                        await ctx.send(embed=embed)
                    elif check["punishment"] == 'none':
                        embed = discord.Embed(title=f'{emojis.blade} AntiNuke', color=color.fail,
                        description=f'{emojis.reply} your **AntiNuke** cant be ``activated`` because you didnt set a **punishment** \n> **use:** ``{px}antinuke punishment``')
                        await ctx.send(embed=embed)
                    else:
                        collection.update_one({"_id": ctx.message.guild.id}, {"$set": {"antinuke": True}})
                        embed = discord.Embed(title=f'{emojis.blade} AntiNuke', color=color.success,
                        description=f'{emojis.reply} your **AntiNuke** is now ``activated``')
                        await ctx.send(embed=embed)

            if function == 'off':
                if check["antinuke"] == False:
                    embed = discord.Embed(title=f'{emojis.blade} AntiNuke', color=color.fail,
                    description=f'{emojis.reply} your **AntiNuke** is already ``deactivated``')
                    await ctx.send(embed=embed)
                if check["antinuke"] == True:
                    collection.update_one({"_id": ctx.message.guild.id}, {"$set": {"antinuke": False}})
                    embed = discord.Embed(title=f'{emojis.blade} AntiNuke', color=color.success,
                    description=f'{emojis.reply} your **AntiNuke** is now ``deactivated``')
                    await ctx.send(embed=embed)

        else:
            embed = discord.Embed(title=f'{emojis.blade} AntiNuke', color=color.fail,
            description=f'{emojis.reply} only the **Server Owner** can use this **command**')
            await ctx.send(embed=embed)

    @antinuke.command()
    @blacklist_check()
    async def logs(self, ctx):
        if ctx.message.author == ctx.guild.owner:
            px = functions.get_prefix(ctx)
            check = collection.find_one({"_id": ctx.message.guild.id})
            if check["logs"] == 0:
                creating = discord.Embed(title=f'{emojis.blade} AntiNuke', color=color.color,
                description=f'{emojis.reply} creating **category** and **channel**')
                message = await ctx.send(embed=creating)

                category_channel = await ctx.guild.create_category('antinuke-logs')
                category = discord.Embed(title=f'{emojis.blade} AntiNuke', color=color.color,
                description=f'{emojis.reply} **category** created, waiting for **overwrite**')
                await message.edit(embed=category)

                overwrites = {ctx.guild.default_role: discord.PermissionOverwrite(read_messages=False, connect=False)}
                await category_channel.edit(overwrites=overwrites)
                overwrite = discord.Embed(title=f'{emojis.blade} AntiNuke', color=color.color,
                description=f'{emojis.reply} **overwrite** successed, waiting for **channel**')
                await message.edit(embed=overwrite)

                channel_message = await ctx.guild.create_text_channel('logs', category=category_channel)
                channel = discord.Embed(title=f'{emojis.blade} AntiNuke', color=color.color,
                description=f'{emojis.reply} **channel** created')
                await message.edit(embed=channel)

                finished = discord.Embed(title=f'{emojis.blade} AntiNuke', color=color.color,
                description=f'{emojis.reply} {emojis.true} Succesfully created **AntiNuke Logs**')
                await message.edit(embed=finished)

                collection.update_one({"_id": ctx.message.guild.id}, {"$set": {"logs": channel_message.id}})
                logs_channel = discord.Embed(title=f'{emojis.blade} AntiNuke', color=color.success,
                description=f'{emojis.reply} This is the **logs** channel for the **AntiNuke** \n{emojis.reply} If the **AntiNuke** detects something, it send a message in here')
                await channel_message.send(embed=logs_channel)
            else:
                try:
                    channel = self.client.get_channel(check["logs"])
                    embed = discord.Embed(title=f'{emojis.blade} AnitNuke', color=color.color,
                    description=f'{emojis.reply} You already have a **logs channel**: {channel.mention}')
                    await ctx.send(embed=embed)
                except:
                    creating = discord.Embed(title=f'{emojis.blade} AntiNuke', color=color.color,
                    description=f'{emojis.reply} creating **category** and **channel**')
                    message = await ctx.send(embed=creating)

                    category_channel = await ctx.guild.create_category('antinuke-logs')
                    category = discord.Embed(title=f'{emojis.blade} AntiNuke', color=color.color,
                    description=f'{emojis.reply} **category** created, waiting for **overwrite**')
                    await message.edit(embed=category)

                    overwrites = {ctx.guild.default_role: discord.PermissionOverwrite(read_messages=False, connect=False)}
                    await category_channel.edit(overwrites=overwrites)
                    overwrite = discord.Embed(title=f'{emojis.blade} AntiNuke', color=color.color,
                    description=f'{emojis.reply} **overwrite** successed, waiting for **channel**')
                    await message.edit(embed=overwrite)

                    channel_message = await ctx.guild.create_text_channel('logs', category=category_channel)
                    channel = discord.Embed(title=f'{emojis.blade} AntiNuke', color=color.color,
                    description=f'{emojis.reply} **channel** created')
                    await message.edit(embed=channel)

                    finished = discord.Embed(title=f'{emojis.blade} AntiNuke', color=color.color,
                    description=f'{emojis.reply} {emojis.true} Succesfully created **AntiNuke Logs**')
                    await message.edit(embed=finished)

                    collection.update_one({"_id": ctx.message.guild.id}, {"$set": {"logs": channel_message.id}})
                    logs_channel = discord.Embed(title=f'{emojis.blade} AntiNuke', color=color.success,
                    description=f'{emojis.reply} This is the **logs** channel for the **AntiNuke** \n{emojis.reply} If the **AntiNuke** detects something, it send a message in here')
                    await channel_message.send(embed=logs_channel)

        else:
            embed = discord.Embed(title=f'{emojis.blade} AntiNuke', color=color.fail,
            description=f'{emojis.reply} only the **Server Owner** can use this **command**')
            await ctx.send(embed=embed)

    @antinuke.command()
    @blacklist_check()
    async def punishment(self, ctx, punishment=None):
        if ctx.message.author == ctx.guild.owner:
            px = functions.get_prefix(ctx)
            if punishment == None:
                embed = discord.Embed(title=f'{emojis.blade} AntiNuke', color=color.color,
                description=f'{emojis.reply} AntiNuke punishment')
                embed.add_field(name=f"> Description:", value=f"set the punishment for being detected from the AntiNuke", inline=False)
                embed.add_field(name=f"{emojis.commands} Command:", value=f"``{px}antinuke punishment [kick/ban]``", inline=False)
                embed.add_field(name=f"> **Example:**", value=f"**usage:** ``$antinuke punishment kick`` \n {emojis.reply} if a user/bot gets detected the AntiNuke, he direclty gets Kicked", inline=False)
                await ctx.send(embed=embed)

            elif punishment == 'kick':
                collection.update_one({"_id": ctx.message.guild.id}, {"$set": {"punishment": 'kick'}})
                embed = discord.Embed(title=f'{emojis.blade} AntiNuke', color=color.success,
                description=f'{emojis.reply} your **punishment** is set to ``kick``')
                await ctx.send(embed=embed)

            elif punishment == 'ban':
                collection.update_one({"_id": ctx.message.guild.id}, {"$set": {"punishment": 'ban'}})
                embed = discord.Embed(title=f'{emojis.blade} AntiNuke', color=color.success,
                description=f'{emojis.reply} your **punishment** is set to ``ban``')
                await ctx.send(embed=embed)

            else:
                embed = discord.Embed(title=f'{emojis.blade} AntiNuke', color=color.fail,
                description=f'{emojis.reply} ``{punishment}`` cant be used as **punishment**')
                await ctx.send(embed=embed)

        else:
            embed = discord.Embed(title=f'{emojis.blade} AntiNuke', color=color.fail,
            description=f'{emojis.reply} only the **Server Owner** can use this **command**')
            await ctx.send(embed=embed)

async def setup(client):
    await client.add_cog(antinuke(client))
