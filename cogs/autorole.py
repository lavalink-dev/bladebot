import discord
import asyncio
import pymongo
from pymongo import MongoClient
from discord.ext import commands
from utils import functions
from utils.emojis import emojis
from utils.color import color

cluster = MongoClient('no')
db = cluster["blade"]
collection = db["autorole"]
premium = db["premium"]
blacklist = db["blacklist"]

def blacklist_check():
    def predicate(ctx):
        if blacklist.find_one({'_id': ctx.author.id}):
            return False
        return True
    return commands.check(predicate)

class autorole(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.group(pass_context=True, invoke_without_command=True, aliases=['ar'], description='config', brief='gives automatic roles to new members')
    @commands.has_guild_permissions(manage_guild=True)
    @blacklist_check()
    async def autorole(self, ctx):
        await ctx.invoke()

    @autorole.command(brief='see all roles set')
    @commands.has_guild_permissions(manage_guild=True)
    @blacklist_check()
    async def list(self, ctx, role: discord.Role=None):
        if not collection.find_one({"_id": ctx.message.guild.id}):
            autoroler = {"_id": ctx.message.guild.id, "switch": False, "roles": [], "count": 0}
            collection.insert_one(autoroler)

        px = functions.get_prefix(ctx)
        check = collection.find_one({"_id": ctx.message.guild.id})

        embed = discord.Embed(title=f'{emojis.blade} AutoRole', color=color.color,
        description=f'{emojis.reply} **Role list** \n \n')

        if check['roles'] != []:
            for i in check['roles']:
                role = ctx.guild.get_role(i)
                embed.description += f"> {role.mention} | `{i}`\n"
        else:
            embed.description += f"> {emojis.false} *no roles set*"

        await ctx.send(embed=embed)

    @autorole.command(brief='set autorole on or off')
    @commands.has_guild_permissions(manage_guild=True)
    @blacklist_check()
    async def set(self, ctx, turn=None):
        if not collection.find_one({"_id": ctx.message.guild.id}):
            autoroler = {"_id": ctx.message.guild.id, "switch": False, "roles": [], "count": 0}
            collection.insert_one(autoroler)

        check = collection.find_one({"_id": ctx.message.guild.id})

        if turn == None:
            px = functions.get_prefix(ctx)
            embed = discord.Embed(title=f'{emojis.blade} AutoRole', color=color.color,
            description=f'{emojis.reply} *activate or deactivate autorole*')
            embed.add_field(name=f"{emojis.commands} Command:", value=f"> ``{px}autorole set [on/off]`` activate or deactive autorole", inline=False)
            await ctx.send(embed=embed)

        if turn == 'on':
            if check["switch"] == False:
                if check["roles"] == []:
                    embed = discord.Embed(description=f'> {emojis.false} You cant turn the **AutoRole** on, cuz they are no **Roles** added', color=color.fail)
                    await ctx.send(embed=embed)

                else:
                    collection.update_one({"_id": ctx.message.guild.id}, {"$set": {"switch": True}})
                    embed = discord.Embed(description=f'> {emojis.true} You turned the **AutoRole** on', color=color.success)
                    await ctx.send(embed=embed)

            else:
                embed = discord.Embed(description=f'> {emojis.false} **AutoRole** is already **activated**', color=color.fail)
                await ctx.send(embed=embed)

        elif turn == 'off':
            if check["switch"] == True:
                collection.update_one({"_id": ctx.message.guild.id}, {"$set": {"switch": False}})
                embed = discord.Embed(description=f'> {emojis.true} You turned the **AutoRole** off', color=color.success)
                await ctx.send(embed=embed)

            else:
                embed = discord.Embed(description=f'> {emojis.false} **AutoRole** is not **activated**', color=color.fail)
                await ctx.send(embed=embed)

        else:
            embed = discord.Embed(description=f'> {emojis.false} **AutoRole** is already **deactivated**', color=color.fail)
            await ctx.send(embed=embed)

    @autorole.command(brief='add a role the autorole')
    @commands.has_guild_permissions(manage_guild=True)
    @blacklist_check()
    async def add(self, ctx, role: discord.Role=None):
        if not collection.find_one({"_id": ctx.message.guild.id}):
            autoroler = {"_id": ctx.message.guild.id, "switch": False, "roles": [], "count": 0}
            collection.insert_one(autoroler)

        px = functions.get_prefix(ctx)
        check = collection.find_one({"_id": ctx.message.guild.id})
        blade = ctx.guild.get_member(self.client.user.id)

        if role == None:
            embed = discord.Embed(title=f'{emojis.blade} AutoRole', color=color.color,
            description=f'{emojis.reply} *add a role to your autorole*')
            embed.add_field(name=f"{emojis.commands} Command:", value=f"> ``{px}autorole add [@role]`` add a role to your autorole", inline=False)
            await ctx.send(embed=embed)

        else:
            if role.id in check['roles']:
                embed = discord.Embed(description=f'> {emojis.false} {role.mention} is already added to the **AutoRole**', color=color.fail)
                await ctx.send(embed=embed)

            elif role >= ctx.author.top_role and ctx.author.id != ctx.guild.owner.id:
                embed = discord.Embed(description=f'> {emojis.false} The Role {role.mention} is too **high**', color=color.fail)
                await ctx.send(embed=embed)

            else:
                if check['count'] == 6:
                    if not premium.find_one({"server": ctx.guild.id}):
                        embed = discord.Embed(description=f'> {emojis.false} To have more than ``6`` Roles is a **Premium** only feature, to learn more about it, join our [``Support Server``](https://discord.gg/snore)', color=color.color)
                        await ctx.send(embed=embed)
                    else:
                        collection.update_one({"_id": ctx.message.guild.id}, {"$set": {"count": check['count'] + 1}})
                        collection.update_one({"_id": ctx.message.guild.id}, {"$push": {"roles": role.id}})
                        embed = discord.Embed(description=f'> {emojis.true} Added {role.mention} in the **AutoRole**', color=color.success)
                        await ctx.send(embed=embed)

                elif check["count"] == 8:
                    embed = discord.Embed(description=f'> {emojis.false} You cant add more than `6` **Roles**', color=color.fail)
                    await ctx.send(embed=embed)
                else:
                    collection.update_one({"_id": ctx.message.guild.id}, {"$set": {"count": check['count'] + 1}})
                    collection.update_one({"_id": ctx.message.guild.id}, {"$push": {"roles": role.id}})
                    embed = discord.Embed(description=f'> {emojis.true} Added {role.mention} ``({role.id})`` to the **AutoRole**', color=color.success)
                    await ctx.send(embed=embed)

    @autorole.command(brief='remove a role the autorole')
    @commands.has_guild_permissions(manage_guild=True)
    @blacklist_check()
    async def remove(self, ctx, role: discord.Role=None):
        if not collection.find_one({"_id": ctx.message.guild.id}):
            autoroler = {"_id": ctx.message.guild.id, "switch": False, "roles": [], "count": 0}
            collection.insert_one(autoroler)

        px = functions.get_prefix(ctx)
        check = collection.find_one({"_id": ctx.message.guild.id})
        blade = ctx.guild.get_member(self.client.user.id)

        if role == None:
            embed = discord.Embed(title=f'{emojis.blade} AutoRole', color=color.color,
            description=f'{emojis.reply} *remove a role from your autorole*')
            embed.add_field(name=f"{emojis.commands} Command:", value=f"> ``{px}autorole remove [@role]`` remove a role from your autorole", inline=False)
            await ctx.send(embed=embed)

        else:
            if role.id not in check['roles']:
                embed = discord.Embed(description=f'> {emojis.false} {role.mention} is not added to the **AutoRole**', color=color.fail)
                await ctx.send(embed=embed)
            else:
                collection.update_one({"_id": ctx.message.guild.id}, {"$set": {"count": check['count'] - 1}})
                collection.update_one({"_id": ctx.message.guild.id}, {"$pull": {"roles": role.id}})
                embed = discord.Embed(description=f'> {emojis.true} Removed {role.mention} ``({role.id})`` to the **AutoRole**', color=color.success)
                await ctx.send(embed=embed)

    @autorole.command(brief='clear the autorole config')
    @commands.has_guild_permissions(manage_guild=True)
    @blacklist_check()
    async def clear(self, ctx):
        if not collection.find_one({"_id": ctx.message.guild.id}):
            autoroler = {"_id": ctx.message.guild.id, "switch": False, "roles": [], "count": 0}
            collection.insert_one(autoroler)

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
                embed = discord.Embed(description=f'> {emojis.true} You cleared the **AutoRole** config', color=color.success)
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
                embed = discord.Embed(description=f'> {emojis.true} Your **AutoRole** hasnt been **Cleared**', color=color.success)
                await interaction.response.edit_message(embed=embed, view=view)

        accept.callback = accept_callback
        decline.callback = decline_callback

        view = discord.ui.View()
        view.add_item(item=accept)
        view.add_item(item=decline)

        embed = discord.Embed(description=f'> Are you sure to clear your **AutoRole** config?', color=color.color)
        await ctx.send(embed=embed, view=view)

    @commands.Cog.listener()
    @blacklist_check()
    async def on_member_join(self, member: discord.Member):
        guild = member.guild.id

        if collection.find_one({"_id": guild}):
            check = collection.find_one({"_id": guild})

            if check["switch"] == True:
                if check["roles"] != []:
                    for i in check["roles"]:
                        role = member.guild.get_role(i)
                        await member.add_roles(role)
            else:
                return
            
        else:
            pass

        await asyncio.sleep(2)

async def setup(client):
    await client.add_cog(autorole(client))
