import discord
import pymongo
from pymongo import MongoClient
from utils import functions
from utils.emojis import emojis
from discord.ext import commands
from utils.color import color

cluster = MongoClient('no')
db = cluster["blade"]
collection = db["autopfp"]
blacklist = db["blacklist"]
premium = db["premium"]

def blacklist_check():
    def predicate(ctx):
        if blacklist.find_one({'_id': ctx.author.id}):
            return False
        return True
    return commands.check(predicate)

class autopfp(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.group(pass_context=True, invoke_without_command=True, aliases=['ap'], brief='sends automatic profile pictures', description='premium')
    @commands.has_guild_permissions(manage_guild=True)
    @blacklist_check()
    async def autopfp(self, ctx):
        await ctx.invoke()

    @autopfp.command(brief='see the autopfp categories', aliases=["category"])
    @commands.has_guild_permissions(manage_guild=True)
    @blacklist_check()
    async def categories(self, ctx):
        if not premium.find_one({"server": ctx.guild.id}):
            embed = discord.Embed(description=f'> {emojis.false} This command is a **Premium** only feature, to learn more about it, join our [``Support Server``](https://discord.gg/snore)', color=color.color)
            await ctx.send(embed=embed)
        else:
            if not collection.find_one({"_id": ctx.message.guild.id}):
                autopfps = {"_id": ctx.message.guild.id, "autopfp": False, "female": 0, "female_gifs": 0, "male": 0, "male_gifs": 0, "anime": 0, "banner": 0, "cartoon": 0, "drill": 0, "smoking": 0, "soft": 0, "jewellry": 0, "faceless": 0, "random": 0}
                collection.insert_one(autopfps)
            check = collection.find_one({"_id": ctx.message.guild.id})

            if check['female'] != 0:
                channel = self.client.get_channel(check['female'])
                female = f'{emojis.true} *(set)* | {channel.mention}'
            else:
                female = f'{emojis.false} *(not set)*'

            if check['female_gifs'] != 0:
                channel = self.client.get_channel(check['female_gifs'])
                female_gifs = f'{emojis.true} *(set)* | {channel.mention}'
            else:
                female_gifs = f'{emojis.false} *(not set)*'

            if check['male'] != 0:
                channel = self.client.get_channel(check['male'])
                male = f'{emojis.true} *(set)* | {channel.mention}'
            else:
                male = f'{emojis.false} *(not set)*'

            if check['male_gifs'] != 0:
                channel = self.client.get_channel(check['male_gifs'])
                male_gifs = f'{emojis.true} *(set)* | {channel.mention}'
            else:
                male_gifs = f'{emojis.false} *(not set)*'

            if check['anime'] != 0:
                channel = self.client.get_channel(check['anime'])
                anime = f'{emojis.true} *(set)* | {channel.mention}'
            else:
                anime = f'{emojis.false} *(not set)*'

            if check['banner'] != 0:
                channel = self.client.get_channel(check['banner'])
                banner = f'{emojis.true} *(set)* | {channel.mention}'
            else:
                banner = f'{emojis.false} *(not set)*'

            if check['cartoon'] != 0:
                channel = self.client.get_channel(check['cartoon'])
                cartoon = f'{emojis.true} *(set)* | {channel.mention}'
            else:
                cartoon = f'{emojis.false} *(not set)*'

            if check['drill'] != 0:
                channel = self.client.get_channel(check['drill'])
                drill = f'{emojis.true} *(set)* | {channel.mention}'
            else:
                drill = f'{emojis.false} *(not set)*'

            if check['smoking'] != 0:
                channel = self.client.get_channel(check['smoking'])
                smoking = f'{emojis.true} *(set)* | {channel.mention}'
            else:
                smoking = f'{emojis.false} *(not set)*'

            if check['soft'] != 0:
                channel = self.client.get_channel(check['soft'])
                soft = f'{emojis.true} *(set)* | {channel.mention}'
            else:
                soft = f'{emojis.false} *(not set)*'

            if check['jewellry'] != 0:
                channel = self.client.get_channel(check['jewellry'])
                jewellry = f'{emojis.true} *(set)* | {channel.mention}'
            else:
                jewellry = f'{emojis.false} *(not set)*'

            if check['faceless'] != 0:
                channel = self.client.get_channel(check['faceless'])
                faceless = f'{emojis.true} *(set)* | {channel.mention}'
            else:
                faceless = f'{emojis.false} *(not set)*'

            if check['random'] != 0:
                channel = self.client.get_channel(check['random'])
                random = f'{emojis.true} *(set)* | {channel.mention}'
            else:
                random = f'{emojis.false} *(not set)*'

            embed = discord.Embed(title=f'{emojis.blade} AutoPFP', color=color.color,
            description=f'{emojis.reply} *all channel config* \n \n> ``female`` {female} \n> ``female_gifs`` {female_gifs} \n> ``male`` {male} \n> ``male_gifs`` {male_gifs} \n> ``anime`` {anime} \n> ``banner`` {banner} \n> ``cartoon`` {cartoon} \n> ``drill`` {drill} \n> ``smoking`` {smoking} \n> ``soft`` {soft} \n> ``jewellry`` {jewellry} \n> ``faceless`` {faceless} \n> ``random`` {random}')
            await ctx.send(embed=embed)


    @autopfp.command(brief='clear the autopfp config')
    @commands.has_guild_permissions(manage_guild=True)
    @blacklist_check()
    async def clear(self, ctx):
        if not premium.find_one({"server": ctx.guild.id}):
            embed = discord.Embed(description=f'> {emojis.false} This command is a **Premium** only feature, to learn more about it, join our [``Support Server``](https://discord.gg/snore)', color=color.color)
            await ctx.send(embed=embed)
            return
        
        if not collection.find_one({"_id": ctx.message.guild.id}):
                autopfps = {"_id": ctx.message.guild.id, "autopfp": False, "female": 0, "female_gifs": 0, "male": 0, "male_gifs": 0, "anime": 0, "banner": 0, "cartoon": 0, "drill": 0, "smoking": 0, "soft": 0, "jewellry": 0, "faceless": 0, "random": 0}
                collection.insert_one(autopfps)

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
                embed = discord.Embed(description=f'> {emojis.true} You cleared the **AutoPfp** config', color=color.success)
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
                embed = discord.Embed(description=f'> {emojis.true} Your **AutoPfp** hasnt been **Cleared**', color=color.success)
                await interaction.response.edit_message(embed=embed, view=view)

        accept.callback = accept_callback
        decline.callback = decline_callback

        view = discord.ui.View()
        view.add_item(item=accept)
        view.add_item(item=decline)

        embed = discord.Embed(description=f'> Are you sure to clear your **AutoPfp** config?', color=color.color)
        await ctx.send(embed=embed, view=view)

    @autopfp.command(brief='turn autopfp on or off')
    @commands.has_guild_permissions(manage_guild=True)
    @blacklist_check()
    async def set(self, ctx, turn=None):
        if not premium.find_one({"server": ctx.guild.id}):
            embed = discord.Embed(description=f'> The **Server** dosnt have **Premium**, find more information [``here``](https://discord.gg/MVnhjYqfYu)', color=color.color)
            await ctx.send(embed=embed)
        else:
            if not collection.find_one({"_id": ctx.message.guild.id}):
                autopfps = {"_id": ctx.message.guild.id, "autopfp": False, "female": 0, "female_gifs": 0, "male": 0, "male_gifs": 0, "anime": 0, "banner": 0, "cartoon": 0, "drill": 0, "smoking": 0, "soft": 0, "jewellry": 0, "faceless": 0, "random": 0}
                collection.insert_one(autopfps)

            check = collection.find_one({"_id": ctx.message.guild.id})

            if turn == None:
                px = functions.get_prefix(ctx)
                embed = discord.Embed(title=f'{emojis.blade} AutoPFP',
                description=f'{emojis.reply} *set autopfp on or off*', color=color.color)
                embed.add_field(name=f"{emojis.commands} Command:", value=f"> ``{px}autopfp set [on/off]`` set auto pfp on or off", inline=False)
                await ctx.send(embed=embed)

            elif turn == 'on':
                if check["autopfp"] == False:
                    collection.update_one({"_id": ctx.message.guild.id}, {"$set": {"autopfp": True}})
                    embed = discord.Embed(description=f'> {emojis.true} **Successfully** activated **AutoPFP**', color=color.success)
                    await ctx.send(embed=embed)
                if check["autopfp"] == True:
                    embed = discord.Embed(description=f'> {emojis.false} **AutoPFP** is already **activated**', color=color.fail)
                    await ctx.send(embed=embed)

            elif turn == 'off':
                if check["autopfp"] == True:
                    collection.update_one({"_id": ctx.message.guild.id}, {"$set": {"autopfp": False}})
                    embed = discord.Embed(description=f'> {emojis.true} **Successfully** deactivated **AutoPFP**', color=color.success)
                    await ctx.send(embed=embed)
                if check["autopfp"] == False:
                    embed = discord.Embed(description=f'> {emojis.false} **AutoPFP** is not **activated**', color=color.fail)
                    await ctx.send(embed=embed)
            else:
                embed = discord.Embed(description=f'> {emojis.false} Cant set **AutoPFP** to ``{turn}``', color=color.fail)
                await ctx.send(embed=embed)

    @autopfp.command(brief='add a categorie to a channel')
    @commands.has_guild_permissions(manage_guild=True)
    @blacklist_check()
    async def add(self, ctx, channel: discord.TextChannel=None, categorie=None):
        if not premium.find_one({"server": ctx.guild.id}):
            embed = discord.Embed(description=f'> The **Server** dosnt have **Premium**, find more information [``here``](https://discord.gg/MVnhjYqfYu)', color=color.color)
            await ctx.send(embed=embed)
        else:
            if not collection.find_one({"_id": ctx.message.guild.id}):
                autopfps = {"_id": ctx.message.guild.id, "autopfp": False, "female": 0, "female_gifs": 0, "male": 0, "male_gifs": 0, "anime": 0, "banner": 0, "cartoon": 0, "drill": 0, "smoking": 0, "soft": 0, "jewellry": 0, "faceless": 0, "random": 0}
                collection.insert_one(autopfps)

            if categorie == None and channel == None:
                embed = discord.Embed(title=f'{emojis.blade} AutoPFP', color=color.success,
                description=f'{emojis.reply} *add a category to a channel to send automaticly pfps*')
                embed.add_field(name=f"{emojis.commands} Command:", value=f"> ``{px}autopfp add [category] [#channel]`` add a category to a channel to send automaticly pfps", inline=False)
                await ctx.send(embed=embed)
            else:
                if categorie == 'female':
                    if channel == None:
                        embed = discord.Embed(description=f'> {emojis.false} Tag a **Channel** to set the **autopfp**', color=color.fail)
                        await ctx.send(embed=embed)
                    else:
                        collection.update_one({"_id": ctx.message.guild.id}, {"$set": {"female": channel.id}})
                        embed = discord.Embed(description=f'> {emojis.true} You added the **Female** AutoPFP to {channel.mention}', color=color.success)
                        await ctx.send(embed=embed)
                elif categorie == 'female_gifs':
                    if channel == None:
                        embed = discord.Embed(description=f'> {emojis.false} Tag a **Channel** to set the **autopfp**', color=color.color)
                        await ctx.send(embed=embed)
                    else:
                        collection.update_one({"_id": ctx.message.guild.id}, {"$set": {"female_gifs": channel.id}})
                        embed = discord.Embed(description=f'> {emojis.true} You added the **Female Gifs** AutoPFP to {channel.mention}', color=color.success)
                        await ctx.send(embed=embed)
                elif categorie == 'male':
                    if channel == None:
                        embed = discord.Embed(description=f'> {emojis.false} Tag a **Channel** to set the **autopfp**', color=color.fail)
                        await ctx.send(embed=embed)
                    else:
                        collection.update_one({"_id": ctx.message.guild.id}, {"$set": {"male": channel.id}})
                        embed = discord.Embed(description=f'> {emojis.true} You added the **Male** AutoPFP to {channel.mention}', color=color.success)
                        await ctx.send(embed=embed)
                elif categorie == 'male_gifs':
                    if channel == None:
                        embed = discord.Embed(description=f'> {emojis.false} Tag a **Channel** to set the **autopfp**', color=color.fail)
                        await ctx.send(embed=embed)
                    else:
                        collection.update_one({"_id": ctx.message.guild.id}, {"$set": {"male_gifs": channel.id}})
                        embed = discord.Embed(description=f'> {emojis.true} You added the **Male Gifs** AutoPFP to {channel.mention}', color=color.success)
                        await ctx.send(embed=embed)
                elif categorie == 'anime':
                    if channel == None:
                        embed = discord.Embed(description=f'> {emojis.false} Tag a **Channel** to set the **autopfp**', color=color.fail)
                        await ctx.send(embed=embed)
                    else:
                        collection.update_one({"_id": ctx.message.guild.id}, {"$set": {"anime": channel.id}})
                        embed = discord.Embed(description=f'> {emojis.true} You added the **Anime** AutoPFP to {channel.mention}', color=color.success)
                        await ctx.send(embed=embed)
                elif categorie == 'banner':
                    if channel == None:
                        embed = discord.Embed(description=f'> {emojis.false} Tag a **Channel** to set the **autopfp**', color=color.fail)
                        await ctx.send(embed=embed)
                    else:
                        collection.update_one({"_id": ctx.message.guild.id}, {"$set": {"banner": channel.id}})
                        embed = discord.Embed(description=f'> {emojis.true} You added the **Banner** AutoPFP to {channel.mention}', color=color.success)
                        await ctx.send(embed=embed)
                elif categorie == 'cartoon':
                    if channel == None:
                        embed = discord.Embed(description=f'> {emojis.false} Tag a **Channel** to set the **autopfp**', color=color.fail)
                        await ctx.send(embed=embed)
                    else:
                        collection.update_one({"_id": ctx.message.guild.id}, {"$set": {"cartoon": channel.id}})
                        embed = discord.Embed(description=f'> {emojis.true} You added the **Cartoon** AutoPFP to {channel.mention}', color=color.success)
                        await ctx.send(embed=embed)
                elif categorie == 'drill':
                    if channel == None:
                        embed = discord.Embed(description=f'> {emojis.false} Tag a **Channel** to set the **autopfp**', color=color.fail)
                        await ctx.send(embed=embed)
                    else:
                        collection.update_one({"_id": ctx.message.guild.id}, {"$set": {"drill": channel.id}})
                        embed = discord.Embed(description=f'> {emojis.true} You added the **Drill** AutoPFP to {channel.mention}', color=color.success)
                        await ctx.send(embed=embed)
                elif categorie == 'smoking':
                    if channel == None:
                        embed = discord.Embed(description=f'> {emojis.false} Tag a **Channel** to set the **autopfp**', color=color.fail)
                        await ctx.send(embed=embed)
                    else:
                        collection.update_one({"_id": ctx.message.guild.id}, {"$set": {"smoking": channel.id}})
                        embed = discord.Embed(description=f'> {emojis.true} You added the **Smoking** AutoPFP to {channel.mention}', color=color.success)
                        await ctx.send(embed=embed)      
                elif categorie == 'soft':
                    if channel == None:
                        embed = discord.Embed(description=f'> {emojis.false} Tag a **Channel** to set the **autopfp**', color=color.fail)
                        await ctx.send(embed=embed)
                    else:
                        collection.update_one({"_id": ctx.message.guild.id}, {"$set": {"soft": channel.id}})
                        embed = discord.Embed(description=f'> {emojis.true} You added the **Soft** AutoPFP to {channel.mention}', color=color.success)
                        await ctx.send(embed=embed)     
                elif categorie == 'jewellry':
                    if channel == None:
                        embed = discord.Embed(description=f'> {emojis.false} Tag a **Channel** to set the **autopfp**', color=color.fail)
                        await ctx.send(embed=embed)
                    else:
                        collection.update_one({"_id": ctx.message.guild.id}, {"$set": {"jewellry": channel.id}})
                        embed = discord.Embed(description=f'> {emojis.true} You added the **Jewellry** AutoPFP to {channel.mention}', color=color.success)
                        await ctx.send(embed=embed)
                elif categorie == 'faceless':
                    if channel == None:
                        embed = discord.Embed(description=f'> {emojis.false} Tag a **Channel** to set the **autopfp**', color=color.fail)
                        await ctx.send(embed=embed)
                    else:
                        collection.update_one({"_id": ctx.message.guild.id}, {"$set": {"faceless": channel.id}})
                        embed = discord.Embed(description=f'> {emojis.true} You added the **Faceless** AutoPFP to {channel.mention}', color=color.success)
                        await ctx.send(embed=embed)

                elif categorie == 'random':
                    if channel == None:
                        embed = discord.Embed(description=f'> {emojis.false} Tag a **Channel** to set the **autopfp**', color=color.fail)
                        await ctx.send(embed=embed)
                    else:
                        collection.update_one({"_id": ctx.message.guild.id}, {"$set": {"random": channel.id}})
                        embed = discord.Embed(description=f'> {emojis.true} You added the **Random** AutoPFP to {channel.mention}', color=color.success)
                        await ctx.send(embed=embed)

                else:
                    px = functions.get_prefix(ctx)
                    embed = discord.Embed(description=f'> {emojis.false} The categorie ``{categorie}`` dosnt exist, choose a **Categorie** from ``{px}autopfp categories``', color=color.fail)
                    await ctx.send(embed=embed)

async def setup(client):
    await client.add_cog(autopfp(client))
