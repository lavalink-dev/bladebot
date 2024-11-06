import discord
import pymongo
import asyncio
from pymongo import MongoClient
from discord.ext import commands
from utils import functions
from utils.emojis import emojis
from utils.color import color

cluster = MongoClient('mongodb+srv://blade:lolidkbruh12333333333@cluster0.wbxaj.mongodb.net/myFirstDatabase?retryWrites=true&w=majority')
db = cluster["blade"]
collection = db["onlyimg"]
blacklist = db["blacklist"]
premium = db["premium"]

def blacklist_check():
    def predicate(ctx):
        if blacklist.find_one({'_id': ctx.author.id}):
            return False
        return True
    return commands.check(predicate)

class onlyimg(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_message(self, message):
        try:
            if collection.find_one({"_id": message.guild.id}):
                check = collection.find_one({"_id": message.guild.id})

                if check["onlyimg"] == False:
                    return

                else:
                    if message.channel.id in check['channels']:
                        if message.author.id in check['whitelist']:
                                return
                        
                        if message.author.bot:
                            await asyncio.sleep(5)
                            await message.delete()

                        elif len(message.attachments) > 0:
                            return
                        else:
                            await message.delete()
            else:
                pass
        except:
            pass

        await asyncio.sleep(1)

    @commands.group(pass_context=True, invoke_without_command=True, aliases=['oi'], brief='configurate onlyimg', description='config')
    @commands.has_guild_permissions(manage_guild=True)
    @blacklist_check()
    async def onlyimg(self, ctx):
        await ctx.invoke()

    @onlyimg.command(brief='clear the onlyimg config')
    @commands.has_guild_permissions(manage_guild=True)
    @blacklist_check()
    async def clear(self, ctx):
        if not collection.find_one({"_id": ctx.message.guild.id}):
            onlyimg = {"_id": ctx.message.guild.id, "onlyimg": False, "channels": [], "count": 0, "whitelist": []}
            collection.insert_one(onlyimg)

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
                embed = discord.Embed(description=f'> {emojis.true} You cleared the **OnlyImg** config', color=color.success)
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
                embed = discord.Embed(description=f'> {emojis.true} Your **OnlyImg** hasnt been **Cleared**', color=color.success)
                await interaction.response.edit_message(embed=embed, view=view)

        accept.callback = accept_callback
        decline.callback = decline_callback

        view = discord.ui.View()
        view.add_item(item=accept)
        view.add_item(item=decline)

        embed = discord.Embed(description=f'> Are you sure to clear your **OnlyImg** config?', color=color.color)
        await ctx.send(embed=embed, view=view)

    @onlyimg.command(brief='turn onlyimg on or off')
    @commands.has_guild_permissions(manage_guild=True)
    @blacklist_check()
    async def set(self, ctx, turn=None):
        if not collection.find_one({"_id": ctx.message.guild.id}):
            onlyimg = {"_id": ctx.message.guild.id, "onlyimg": False, "channels": [], "count": 0, "whitelist": []}
            collection.insert_one(onlyimg)

        check = collection.find_one({"_id": ctx.message.guild.id})
        px = functions.get_prefix(ctx)

        if turn == None:
            embed = discord.Embed(title=f'{emojis.blade} OnlyImg', color=color.color,
            description=f'{emojis.reply} *turn the onlyimg on or off*')
            embed.add_field(name=f"{emojis.commands} Command:", value=f"> ``{px}onlyimg set [on/off]`` set your onlyimg on or off", inline=False)
            await ctx.send(embed=embed)

        if turn == 'on' or turn == 'true':
            if check['onlyimg'] == True:
                embed = discord.Embed(description=f'> {emojis.false} **OnlyImg** is already **activated**', color=color.fail)
                await ctx.send(embed=embed)
            else:
                collection.update_one({"_id": ctx.message.guild.id}, {"$set": {"onlyimg": True}})
                embed = discord.Embed(description=f'> {emojis.true} You **activated** **OnlyImg**', color=color.success)
                await ctx.send(embed=embed)

        elif turn == 'off' or turn == 'false':
            if check['onlyimg'] == False:
                embed = discord.Embed(description=f'> {emojis.false} **OnlyImg** is not **activated**', color=color.fail)
                await ctx.send(embed=embed)
            else:
                collection.update_one({"_id": ctx.message.guild.id}, {"$set": {"onlyimg": False}})
                embed = discord.Embed(description=f'> {emojis.true} You **deactivated** **OnlyImg**', color=color.success)
                await ctx.send(embed=embed)

        else:
            embed = discord.Embed(description=f'> {emojis.false} You cant set **OnlyImg** to ``{turn}``', color=color.fail)
            await ctx.send(embed=embed)

    @onlyimg.command(brief='add a channel to the list')
    @commands.has_guild_permissions(manage_guild=True)
    @blacklist_check()
    async def add(self, ctx, channel: discord.TextChannel=None):
        if not collection.find_one({"_id": ctx.message.guild.id}):
            onlyimg = {"_id": ctx.message.guild.id, "onlyimg": False, "channels": [], "count": 0, "whitelist": []}
            collection.insert_one(onlyimg)

        px = functions.get_prefix(ctx)
        check = collection.find_one({"_id": ctx.message.guild.id})

        if channel == None:
            embed = discord.Embed(title=f'{emojis.blade} OnlyImg', color=color.color,
            description=f'{emojis.reply} *add a channel to onlyimg*')
            embed.add_field(name=f"{emojis.commands} Command:", value=f"> ``{px}onlyimg add [#channel]`` add a channel to the onlyimg", inline=False)
            await ctx.send(embed=embed)

        if channel.id in check['channels']:
            embed = discord.Embed(description=f'> {emojis.false} The Channel {channel.mention} is already in **OnlyImg**', color=color.fail)
            await ctx.send(embed=embed)

        else:
            if check['count'] == 3 and not premium.find_one({"server": ctx.guild.id}):
                embed = discord.Embed(description=f'> {emojis.false} You cant have more then ``3`` **Channels**', color=color.fail)
                await ctx.send(embed=embed)

            elif premium.find_one({"server": ctx.guild.id}) and check["count"] == 6:
                embed = discord.Embed(description=f'> {emojis.false} You cant have more then ``6`` **Channels**', color=color.fail)
                await ctx.send(embed=embed)

            else:
                collection.update_one({"_id": ctx.message.guild.id}, {"$push": {"channels": channel.id}})
                collection.update_one({"_id": ctx.message.guild.id}, {"$set": {"count": check['count']+1}})
                embed = discord.Embed(description=f'> {emojis.true} You added {channel.mention} to the **OnlyImg**', color=color.success)
                await ctx.send(embed=embed)

    @onlyimg.command(brief='remove a channel from the list')
    @commands.has_guild_permissions(manage_guild=True)
    @blacklist_check()
    async def remove(self, ctx, channel: discord.TextChannel=None):
        if not collection.find_one({"_id": ctx.message.guild.id}):
            onlyimg = {"_id": ctx.message.guild.id, "onlyimg": False, "channels": [], "count": 0, "whitelist": []}
            collection.insert_one(onlyimg)

        px = functions.get_prefix(ctx)
        check = collection.find_one({"_id": ctx.message.guild.id})
        if channel == None:
            embed = discord.Embed(title=f'{emojis.blade} OnlyImg', color=color.color,
            description=f'{emojis.reply} *remove a channel from onlyimg*')
            embed.add_field(name=f"{emojis.commands} Command:", value=f"> ``{px}onlyimg remove [#channel]`` remove a channel from the onlyimg", inline=False)
            await ctx.send(embed=embed)

        if channel.id not in check['channels']:
            embed = discord.Embed(description=f'> {emojis.false} The Channel {channel.mention} is not in **OnlyImg**', color=color.fail)
            await ctx.send(embed=embed)

        else:
            collection.update_one({"_id": ctx.message.guild.id}, {"$pull": {"channels": channel.id}})
            collection.update_one({"_id": ctx.message.guild.id}, {"$set": {"count": check['count']-1}})
            embed = discord.Embed(description=f'> {emojis.true} You removed {channel.mention} from the **OnlyImg**', color=color.success)
            await ctx.send(embed=embed)

    @onlyimg.command(brief='see all channels')
    @commands.has_guild_permissions(manage_guild=True)
    @blacklist_check()
    async def list(self, ctx):
        if not collection.find_one({"_id": ctx.message.guild.id}):
            onlyimg = {"_id": ctx.message.guild.id, "onlyimg": False, "channels": [], "count": 0, "whitelist": []}
            collection.insert_one(onlyimg)

        data = collection.find_one({"_id": ctx.message.guild.id })['channels']
        embed = discord.Embed(title=f'{emojis.blade} OnlyImg', color=color.color,
        description=f'{emojis.reply} *all onlyimg channels* \n \n')

        num = 0
        for i in data:
            num = num + 1
            channel = self.client.get_channel(i)
            embed.description += f'``{num}`` **{channel.mention}** | ``{channel.id}``\n'

        await ctx.send(embed=embed)

    @onlyimg.command(brief='whitelist a member')
    @commands.has_guild_permissions(manage_guild=True)
    @blacklist_check()
    async def whitelist(self, ctx, user: discord.Member=None):
        data = collection.find_one({"_id": ctx.guild.id })['whitelist']
        check = collection.find_one({"_id": ctx.message.guild.id})
        
        if user == None:
            embed = discord.Embed(title=f"{emojis.blade} OnlyImg", description=f"{emojis.reply} whitelisted people: \n")
            if check["whitelist"] == []:
                embed.description += f"No user is **Whitelisted**!"
            else:
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
            if user.id in check['whitelist']:
                embed = discord.Embed(description=f'> {emojis.false} {user.mention} is already **Whitelisted**', color=color.fail)
                await ctx.send(embed=embed)
            else:
                collection.update_one({"_id": ctx.message.guild.id}, {"$push": {"whitelist": user.id}})
                embed = discord.Embed(description=f'> {emojis.true} {user.mention} has been **Whitelisted**', color=color.success)
                await ctx.send(embed=embed)

    @onlyimg.command(brief='unwhitelist a member')
    @commands.has_guild_permissions(manage_guild=True)
    @blacklist_check()
    async def unwhitelist(self, ctx, user: discord.Member=None):
        data = collection.find_one({"_id": ctx.guild.id })['whitelist']
        check = collection.find_one({"_id": ctx.message.guild.id})
        
        if user == None:
            embed = discord.Embed(title=f"{emojis.blade} OnlyImg", color=color.color, description=f"{emojis.reply} whitelisted people: \n")
            if check["whitelist"] == []:
                embed.description += f"No user is **Whitelisted**!"
            else:
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
            if user.id in check['whitelist']:
                collection.update_one({"_id": ctx.message.guild.id}, {"$pull": {"whitelist": user.id}})
                embed = discord.Embed(description=f'> {emojis.true} {user.mention} has been **Unwhitelisted**', color=color.success)
                await ctx.send(embed=embed)
            else:
                embed = discord.Embed(description=f'> {emojis.false} {user.mention} isnts **Whitelisted**', color=color.fail)
                await ctx.send(embed=embed)

async def setup(client):
    await client.add_cog(onlyimg(client))
