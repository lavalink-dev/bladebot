import discord
import asyncio
import pymongo
import pymongo
from pymongo import MongoClient
from pymongo import MongoClient
from discord.ext import commands
from utils import functions
from utils.emojis import emojis
from asyncio import TimeoutError
from utils.color import color

cluster = MongoClient('no')
db = cluster["blade"]
collection = db["blacklist"]

def blacklist_check():
    def predicate(ctx):
        if collection.find_one({'_id': ctx.author.id}):
            return False
        return True
    return commands.check(predicate)

class help(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['h'], brief='see the help page', description='utility')
    @blacklist_check()
    async def help(self, ctx, help=None):
        px = functions.get_prefix(ctx)

        if help == None:
            options = [
                discord.SelectOption(label="home", description="go back to the home menu", emoji=emojis.home),
                discord.SelectOption(label="utility", description="invite, afk, snipe", emoji=emojis.utility),
                discord.SelectOption(label="info", description="botinfo, userinfo, serverinfo", emoji=emojis.info),
                discord.SelectOption(label="moderation", description="ban, kick, mute", emoji=emojis.moderation),
                discord.SelectOption(label="config", description="antinuke, welcomer, level", emoji=emojis.config),
                discord.SelectOption(label="economy", description="profile, work, shop", emoji=emojis.economy),
                discord.SelectOption(label="image", description="sadcat, wanted, drip", emoji=emojis.image),
                discord.SelectOption(label="fun", description="memes, rates, actions", emoji=emojis.fun),
                discord.SelectOption(label="interactions", description="kiss, slap, hug", emoji=emojis.fun),
                discord.SelectOption(label="lastfm", description="lastfm, nowplaying, toptracks", emoji='<:lastfm:1113901596498206810>'),
                discord.SelectOption(label="premium", description="see all premium commands", emoji='⭐'),
                discord.SelectOption(label="pets", description="pet, play, feed", emoji='🐶'),
                discord.SelectOption(label="clans", description="create, invite, leave", emoji='<:clans:1149369663206199418>')
            ]       

            embed = discord.Embed(title=f'{emojis.blade} **blade**', color=color.color,
            description=f'{emojis.reply}{emojis.home} **help** \n \n {emojis.badge} [Support Server](https://discord.gg/MVnhjYqfYu) ・ {emojis.link} [Invite the Bot](https://discord.com/api/oauth2/authorize?client_id=1212465954408370297&permissions=8&scope=bot) \n {emojis.info} For more Info on a **Command** use ``{px}help [command]`` \n \n> Select a **Category** in the **Menu** to view its Commands')
            embed.set_thumbnail(url=self.client.user.display_avatar)
            embed.set_footer(text=f'{len(self.client.commands)} command(s)')
            select = discord.ui.Select(placeholder="Select a Category", options=options)

            async def select_callback(interaction: discord.Interaction):
                if interaction.user != ctx.author:
                    embed = discord.Embed(description=f"> {emojis.false} This is not your message", color=color.fail)
                    await interaction.response.send_message(embed=embed, view=None, ephemeral=True)
                    return
                
                if select.values[0] == "home":
                    embed = discord.Embed(title=f'{emojis.blade} **blade**', color=color.color,
                    description=f'{emojis.reply}{emojis.home} **help** \n \n {emojis.badge} [Support Server](https://discord.gg/MVnhjYqfYu) ・ {emojis.link} [Invite the Bot](https://discord.com/api/oauth2/authorize?client_id=1212465954408370297&permissions=8&scope=bot) \n {emojis.info} For more Info on a **Command** use ``{px}help [command]`` \n \n> Select a **Category** in the **Menu** to view its Commands')
                    embed.set_thumbnail(url=self.client.user.display_avatar)
                    embed.set_footer(text=f'{len(self.client.commands)} command(s)')
                    await interaction.response.edit_message(embed=embed)

                if select.values[0] == "utility":
                    embed = discord.Embed(title=f'{emojis.blade} **blade**', color=color.color)
                    
                    command_list = ""
                    command_list2 = ""

                    for command in self.client.commands:
                        if command.description == "utility":
                            if command.aliases != []:
                                aliases = " | " + " | ".join(str(alias) for alias in command.aliases)
                            else:
                                aliases = ""

                            if len(command_list) < 950:
                                command_list += f'> ``{px}{command.name}{aliases}`` {command.brief} \n'
                            else:
                                command_list2 += f'> ``{px}{command.name}{aliases}`` {command.brief} \n'

                    embed.add_field(name=f'{emojis.reply}{emojis.utility} utility', value=command_list)
                    if len(command_list2) != "":
                        embed.add_field(name=f'{emojis.dash}{emojis.utility} utility', value=command_list2)

                    embed.set_footer(text=f'{len(self.client.commands)} command(s)')
                    await interaction.response.edit_message(embed=embed)

                if select.values[0] == "info":
                    embed = discord.Embed(title=f'{emojis.blade} **blade**', color=color.color)
                    
                    command_list = ""

                    for command in self.client.commands:
                        if command.description == 'info':
                            if not command.aliases == []:
                                aliases = " | " + " | ".join(str(alias) for alias in command.aliases)
                            else:
                                aliases = ""
                            command_list += f'> ``{px}{command.name}{aliases}`` {command.brief} \n'

                    embed.add_field(name=f'{emojis.reply}{emojis.info} info', value=command_list)

                    embed.set_footer(text=f'{len(self.client.commands)} command(s)')
                    await interaction.response.edit_message(embed=embed)

                if select.values[0] == "moderation":
                    embed = discord.Embed(title=f'{emojis.blade} **blade**', color=color.color)
                    
                    command_list = ""
                    command_list2 = ""

                    for command in self.client.commands:
                        if command.description == 'moderation':
                            if not command.aliases == []:
                                aliases = " | " + " | ".join(str(alias) for alias in command.aliases)
                            else:
                                aliases = ""

                            if len(command_list) < 900:
                                command_list += f'> ``{px}{command.name}{aliases}`` {command.brief} \n'
                            else:
                                command_list2 += f'> ``{px}{command.name}{aliases}`` {command.brief} \n'

                    embed.add_field(name=f'{emojis.reply}{emojis.moderation} moderation', value=command_list)

                    if len(command_list2) != "":
                        embed.add_field(name=f'{emojis.dash}{emojis.moderation} moderation', value=command_list2)

                    embed.set_footer(text=f'{len(self.client.commands)} command(s)')
                    await interaction.response.edit_message(embed=embed)

                if select.values[0] == "config":
                    embed = discord.Embed(title=f'{emojis.blade} **blade**', color=color.color)
                    
                    command_list = ""
                    command_list2 = ""

                    for command in self.client.commands:
                        if command.description == 'config':
                            if not command.aliases == []:
                                aliases = " | " + " | ".join(str(alias) for alias in command.aliases)
                            else:
                                aliases = ""

                            if len(command_list) < 900:
                                command_list += f'> ``{px}{command.name}{aliases}`` {command.brief} \n'
                            else:
                                command_list2 += f'> ``{px}{command.name}{aliases}`` {command.brief} \n'

                    embed.add_field(name=f'{emojis.reply}{emojis.config} config', value=command_list)
                    if len(command_list2) != "":
                        embed.add_field(name=f'{emojis.dash}{emojis.config} config', value=command_list2)

                    embed.set_footer(text=f'{len(self.client.commands)} command(s)')
                    await interaction.response.edit_message(embed=embed)

                if select.values[0] == "economy":
                    embed = discord.Embed(title=f'{emojis.blade} **blade**', color=color.color)
                    
                    command_list = ""
                    command_list2 = ""

                    for command in self.client.commands:
                        if command.description == 'economy':
                            if not command.aliases == []:
                                aliases = " | " + " | ".join(str(alias) for alias in command.aliases)
                            else:
                                aliases = ""

                            if len(command_list) < 900:
                                command_list += f'> ``{px}{command.name}{aliases}`` {command.brief} \n'
                            else:
                                command_list2 += f'> ``{px}{command.name}{aliases}`` {command.brief} \n'

                    embed.add_field(name=f'{emojis.reply}{emojis.economy} economy', value=command_list)
                    if len(command_list2) != "":
                        embed.add_field(name=f'{emojis.dash}{emojis.economy} economy', value=command_list2)

                    embed.set_footer(text=f'{len(self.client.commands)} command(s)')
                    await interaction.response.edit_message(embed=embed)

                if select.values[0] == "image":
                    embed = discord.Embed(title=f'{emojis.blade} **blade**', color=color.color)
                    
                    command_list = ""

                    for command in self.client.commands:
                        if command.description == 'image':
                            if not command.aliases == []:
                                aliases = " | " + " | ".join(str(alias) for alias in command.aliases)
                            else:
                                aliases = ""
                            command_list += f'> ``{px}{command.name}{aliases}`` {command.brief} \n'

                    embed.add_field(name=f'{emojis.reply}{emojis.image} image', value=command_list)

                    embed.set_footer(text=f'{len(self.client.commands)} command(s)')
                    await interaction.response.edit_message(embed=embed)

                if select.values[0] == "fun":
                    embed = discord.Embed(title=f'{emojis.blade} **blade**', color=color.color)
                    
                    command_list = ""
                    command_list2 = ""

                    for command in self.client.commands:
                        if command.description == 'fun':
                            if not command.aliases == []:
                                aliases = " | " + " | ".join(str(alias) for alias in command.aliases)
                            else:
                                aliases = ""

                            if len(command_list) < 900:
                                command_list += f'> ``{px}{command.name}{aliases}`` {command.brief} \n'
                            else:
                                command_list2 += f'> ``{px}{command.name}{aliases}`` {command.brief} \n'

                    embed.add_field(name=f'{emojis.reply}{emojis.fun} fun', value=command_list)
                    if len(command_list2) != "":
                        embed.add_field(name=f'{emojis.dash}{emojis.fun} fun', value=command_list2)

                    embed.set_footer(text=f'{len(self.client.commands)} command(s)')
                    await interaction.response.edit_message(embed=embed)

                if select.values[0] == "interactions":
                    embed = discord.Embed(title=f'{emojis.blade} **blade**', color=color.color)
                    
                    command_list = ""

                    for command in self.client.commands:
                        if command.description == 'interactions':
                            if not command.aliases == []:
                                aliases = " | " + " | ".join(str(alias) for alias in command.aliases)
                            else:
                                aliases = ""
                            command_list += f'> ``{px}{command.name}{aliases}`` {command.brief} \n'

                    embed.add_field(name=f'{emojis.reply}{emojis.fun} interactions', value=command_list)

                    embed.set_footer(text=f'{len(self.client.commands)} command(s)')
                    await interaction.response.edit_message(embed=embed)

                if select.values[0] == "lastfm":
                    embed = discord.Embed(title=f'{emojis.blade} **blade**', color=color.color)
                    
                    command_list = ""

                    for command in self.client.commands:
                        if command.description == 'lastfm':
                            if not command.aliases == []:
                                aliases = " | " + " | ".join(str(alias) for alias in command.aliases)
                            else:
                                aliases = ""
                            command_list += f'> ``{px}{command.name}{aliases}`` {command.brief} \n'

                    embed.add_field(name=f'{emojis.reply}<:lastfm:1113901596498206810> lastfm', value=command_list)

                    embed.set_footer(text=f'{len(self.client.commands)} command(s)')
                    await interaction.response.edit_message(embed=embed)

                if select.values[0] == "premium":
                    embed = discord.Embed(title=f'{emojis.blade} **blade**', color=color.color)
                    
                    command_list = ""

                    for command in self.client.commands:
                        if command.description == 'premium':
                            if not command.aliases == []:
                                aliases = " | " + " | ".join(str(alias) for alias in command.aliases)
                            else:
                                aliases = ""
                            command_list += f'> ``{px}{command.name}{aliases}`` {command.brief} \n'

                    embed.add_field(name=f'{emojis.reply}:star: premium', value=command_list)

                    embed.set_footer(text=f'{len(self.client.commands)} command(s)')
                    await interaction.response.edit_message(embed=embed)

                if select.values[0] == "pets":
                    embed = discord.Embed(title=f'{emojis.blade} **blade**', color=color.color)
                    
                    command_list = ""

                    for command in self.client.commands:
                        if command.description == 'pets':
                            if not command.aliases == []:
                                aliases = " | " + " | ".join(str(alias) for alias in command.aliases)
                            else:
                                aliases = ""
                            command_list += f'> ``{px}{command.name}{aliases}`` {command.brief} \n'

                    embed.add_field(name=f'{emojis.reply}:dog: pets', value=command_list)

                    embed.set_footer(text=f'{len(self.client.commands)} command(s)')
                    await interaction.response.edit_message(embed=embed)

                if select.values[0] == "clans":
                    embed = discord.Embed(title=f'{emojis.blade} **blade**', color=color.color)
                    
                    command_list = ""
                    command_list2 = ""

                    for command in self.client.commands:
                        if command.description == 'clans':
                            if not command.aliases == []:
                                aliases = " | " + " | ".join(str(alias) for alias in command.aliases)
                            else:
                                aliases = ""
                            command_list += f'> ``{px}{command.name}{aliases}`` {command.brief} \n'

                    command_clan = self.client.get_command("clan")

                    if isinstance(command_clan, discord.ext.commands.Group):
                        for subcommand in command_clan.commands:
                            if len(command_list) < 900:
                                command_list += f'> ``{px}clan {subcommand.name}`` {subcommand.brief} \n'
                            else:
                                command_list2 += f'> ``{px}clan {subcommand.name}`` {subcommand.brief} \n'

                    embed.add_field(name=f'{emojis.reply} <:clans:1149369663206199418> clans', value=command_list)

                    embed.set_footer(text=f'{len(self.client.commands)} command(s)')
                    await interaction.response.edit_message(embed=embed)

            select.callback = select_callback

            view = discord.ui.View()
            invite = discord.ui.Button(style=discord.ButtonStyle.gray, label="Invite", url="https://discord.com/api/oauth2/authorize?client_id=1212465954408370297&permissions=8&scope=bot")
            support = discord.ui.Button(style=discord.ButtonStyle.gray, label="Support", url="https://discord.gg/MVnhjYqfYu")
            website = discord.ui.Button(style=discord.ButtonStyle.gray, label="Website", url="https://bladebot.net/")
            vote = discord.ui.Button(style=discord.ButtonStyle.gray, label="Vote", url="https://top.gg/bot/1212465954408370297/vote")
            view.add_item(select)
            view.add_item(item=invite)
            view.add_item(item=support)
            view.add_item(item=website)
            view.add_item(item=vote)
            await ctx.send(embed=embed, view=view)

        else:
            try:
                command = self.client.get_command(help)
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
                    param = ""
                    param_desc = "none"
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

                if command.description != '':
                    await ctx.send(embed=embed)

                else:
                    if ctx.message.author.id == 432110614341746689:
                        await ctx.send(embed=embed)

                    else:
                        embed = discord.Embed(description=f'> {emojis.false} The Command ``{help}`` dosnt Exist', color=color.fail)
                        await ctx.send(embed=embed)
            except:
                embed = discord.Embed(description=f'> {emojis.false} The Command ``{help}`` dosnt Exist', color=color.fail)
                await ctx.send(embed=embed)

async def setup(client):
    await client.add_cog(help(client))
