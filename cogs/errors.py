import discord
import pymongo
import asyncio
import json
import os
import secrets
from pymongo import MongoClient
from discord.ext import commands, tasks
from discord.ext.commands import MissingPermissions
from discord.ext.commands.core import command
from discord.utils import get
from utils import functions
from utils.emojis import emojis
from utils.color import color

cluster = MongoClient('no')
db = cluster["blade"]
collection = db["blacklist"]
errored = db["error"]

class errors(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        try:
            if isinstance(error, commands.MissingRequiredArgument) or isinstance(error, commands.CommandInvokeError):
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
                    param_desc = "None"
                    param = ""
                else:
                    params = " ".join(params)
                    param = params.replace("[", "")
                    param = param.replace("]", "")
                    param = param.replace(" ", ", ")
                    param_desc = "".join(param)
                embed = discord.Embed(title=f"{emojis.blade} {pre}{command.name}", color=color.color,
                                    description=f"{emojis.reply2} ``category`` {command.description} \n{emojis.reply2} ``description`` {command.brief} \n{emojis.reply} ``arguements`` {param_desc}")
                if isinstance(command, discord.ext.commands.Group):
                    subcommands = []
                    for subcommand in command.commands:
                        subparams = []
                        for key, value in subcommand.params.items():
                            if key not in ("self", "ctx"):
                                subparams.append(f"<{key}>" if "NoneType" in
                                                str(value) else f"[{key}]")
                        if subparams == []:
                            subparam = ""
                        else:
                            subparam = " " + ", ".join(subparams)
                            subparam = subparam.replace(",", "")

                        message = f'> ``{pre}{command.name} {subcommand.name}{subparam}`` {subcommand.brief}'
                        subcommands.append(message)

                    embed.add_field(name=f'{emojis.commands} ``Usage:``', 
                                    value="\n".join(subcommands), 
                                    inline=False)
                else:
                    embed.add_field(name=f'{emojis.commands} ``Usage:``',
                                    value=f'{emojis.reply} {pre}{command.name} {params}',
                                    inline=False)
                embed.add_field(name=f'{emojis.alias} ``Aliases:``',
                                value=f'{emojis.reply} {aliases}',
                                inline=False)

                embed.set_thumbnail(url=self.client.user.display_avatar)

                try:

                    if command.description != '':
                        await ctx.send(embed=embed)

                    else:
                        if ctx.message.author.id == 432110614341746689:
                            await ctx.send(embed=embed)
                        else:
                            return

                except:
                    pass

            elif isinstance(error, commands.MissingPermissions):
                error = format(error.missing_permissions).replace('[', '').replace("'", '').replace(']', '').replace('_', ' ')

                embed = discord.Embed(description=f'> {emojis.false} You are missing ``{error}`` permissions', color=color.fail)
                await ctx.send(embed=embed)

            elif isinstance(error, commands.CheckFailure):
                if collection.find_one({"_id": ctx.author.id}):
                    embed = discord.Embed(description=f'> {emojis.false} You are **Blacklisted** from Blade \n{emojis.reply} **Reason**: **{collection.find_one({"_id": ctx.author.id})["reason"]}**', color=color.fail)
                    await ctx.send(embed=embed)
                else:
                    pass

            elif isinstance(error, commands.CommandOnCooldown):
                command = ctx.command
                embed = discord.Embed(description=f'> {emojis.false} **{command.name}** is on cooldown, try again in ``{format(error.retry_after)[:3]}s``', color=color.fail)
                await ctx.send(embed=embed)

            elif isinstance(error, discord.HTTPException):
                print(f'blade is ratelimited \n - possible guild: {ctx.guild.id} | possible member: {ctx.message.author} \n')

            elif isinstance(error, commands.UserNotFound):
                embed = discord.Embed(description=f'> {emojis.false} Couldnt find the User **{format(error.argument)}**', color=color.fail)
                await ctx.send(embed=embed)

            elif isinstance(error, commands.MemberNotFound):
                embed = discord.Embed(description=f'> {emojis.false} Couldnt find the Member **{format(error.argument)}**', color=color.fail)
                await ctx.send(embed=embed)

            elif isinstance(error, commands.BadArgument):
                embed = discord.Embed(description=f'> {emojis.false} The wrong **Argument** has been used: **{format(error.argument)}**', color=color.fail)
                await ctx.send(embed=embed)

            elif isinstance(error, commands.MaxConcurrencyReached):
                embed = discord.Embed(description=f'> {emojis.false} **{command.name}** is already been used to often at this moment', color=color.fail)
                await ctx.send(embed=embed)

            else:
                try:
                    print(f'{error} | guild: {ctx.guild.id} | member: {ctx.message.author.id}')
                except:
                    print(error)

                try:
                    code = secrets.token_urlsafe(5)

                    error_code = {"_id": f'{code}', "command": f'{ctx.command.name}', "message": f'{ctx.message.content}', "error": f'{error}', "member": ctx.author.id, "server": ctx.guild.id}
                    errored.insert_one(error_code)

                    embed = discord.Embed(description=f'> {emojis.false} An Error occured trying to use **{ctx.command.name}**\n {emojis.reply} Report this Error [``here``](https://discord.gg/losing) with the **Error** code ``{code}``', color=color.fail)
                    await ctx.send(embed=embed)

                    channel = self.client.get_channel(1213479327816097853)
                    error_embed = discord.Embed(title=f'{emojis.blade} Error', description=f'{emojis.reply} Code: ``{code}`` | Command: ``{ctx.command.name}`` | ``({ctx.message.content})`` \n ```{error}```')
                    error_embed.set_footer(text=f'{ctx.guild.id} | {ctx.author.name} ({ctx.author.id})')
                    await channel.send(embed=error_embed)
                except:
                    pass
        except:
            pass

        await asyncio.sleep(1)

async def setup(client):
    await client.add_cog(errors(client))
