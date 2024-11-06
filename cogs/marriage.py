import discord
import pymongo
import asyncio
import datetime
from discord import File
from datetime import date
from pymongo import MongoClient
from discord.utils import get
from discord.ext import commands
from utils import functions
from utils.emojis import emojis
from utils.color import color
from easy_pil import Editor, Canvas, load_image_async, Font

cluster = MongoClient('mongodb+srv://blade:lolidkbruh12333333333@cluster0.wbxaj.mongodb.net/myFirstDatabase?retryWrites=true&w=majority')
db = cluster["blade"]
collection = db["marriage"]
blacklist = db["blacklist"]

def blacklist_check():
    def predicate(ctx):
        if blacklist.find_one({'_id': ctx.author.id}):
            return False
        return True
    return commands.check(predicate)

class marriage(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(brief='shows your marriage', description='fun')
    @blacklist_check()
    async def marriage(self, ctx, member: discord.User=None):
        if member == None:
            if not collection.find_one({"_id": ctx.message.author.id}):
                embed = discord.Embed(title=f'{emojis.blade} Marriage', color=color.color,
                description=f'> You are not **Married** :cry:')
                await ctx.send(embed=embed)

            else:
                check = collection.find_one({"_id": ctx.message.author.id})
                if check["married"] != 0:
                    user = self.client.get_user(check['married'])
                    embed = discord.Embed(title=f'{emojis.blade} Marriage', color=color.color,
                    description=f'{emojis.reply} You are happily **Married** with {user.mention} since ``{check["date"]}``')
                    embed.set_image(url=check["certificate"])
                    await ctx.send(embed=embed)

                if check["married"] == 0:
                    collection.delete_one({"_id": ctx.message.author.id})
                    embed = discord.Embed(title=f'{emojis.blade} Marriage', color=color.color,
                    description=f'> The **Profile** of {ctx.message.author.mention} bugs, its now fixed')
                    await ctx.send(embed=embed)

        else:
            if not collection.find_one({"_id": member.id}):
                embed = discord.Embed(title=f'{emojis.blade} Marriage', color=color.color,
                description=f'> {member.mention} is not **Married** :cry:')
                await ctx.send(embed=embed)

            else:
                check = collection.find_one({"_id": member.id})
                if check["married"] != 0:
                    user = self.client.get_user(check['married'])
                    embed = discord.Embed(title=f'{emojis.blade} Marriage', color=color.color,
                    description=f'> {member.mention} is **happily Married** with {user.mention}')
                    await ctx.send(embed=embed)
                    
                if check["married"] == 0:
                    collection.delete_one({"_id": member.id})
                    embed = discord.Embed(title=f'{emojis.blade} Marriage', color=color.color,
                    description=f'> The **Profile** of {member.mention} bugs, its now fixed')
                    await ctx.send(embed=embed)

    @commands.command(brief='propose to a member to marry them', aliases=['marry'], description='fun')
    @blacklist_check()
    async def propose(self, ctx, member: discord.User):
        if collection.find_one({"_id": ctx.message.author.id}):
            embed = discord.Embed(description=f'> You are already **Married** 🤨', color=color.color)
            await ctx.send(embed=embed)


        elif collection.find_one({"_id": member.id}):
            embed = discord.Embed(description=f'> {member.mention} is already **Married** :pensive:', color=color.color)
            await ctx.send(embed=embed)


        else:
            if member.id == 896550468128505877:
                embed = discord.Embed(description=f'> **Blade** is **Married** to <@432110614341746689>, as he is the sexiest Man alive', color=color.color)
                await ctx.send(embed=embed)
                return

            if member == ctx.message.author:
                embed = discord.Embed(description='> You cant **marry** yourself 🤨', color=color.color)
                await ctx.send(embed=embed)

            else:
                accept = discord.ui.Button(style=discord.ButtonStyle.green, label="yes")
                decline = discord.ui.Button(style=discord.ButtonStyle.red, label="no")

                embed = discord.Embed(description=f'> 💍 {member.mention} will you **Marry** {ctx.message.author.mention}? 💍', color=color.color)

                async def accept_callback(interaction):
                    if interaction.user != member:
                        embed = discord.Embed(description=f"> {emojis.false} They didnt asked you", color=color.f   )
                        await interaction.response.send_message(embed=embed, view=None, ephemeral=True)
                        return
                    else:
                        today = date.today()
                        today_date = today.strftime("%B %d, %Y")

                        collection.insert_one({"_id": ctx.message.author.id, "married": member.id, "date": today_date, "certificate": 'none'})
                        collection.insert_one({"_id": member.id, "married": ctx.message.author.id, "date": today_date, "certificate": 'none'})

                        embed = discord.Embed(description=f'> 🎉 {member.mention} and {ctx.message.author.mention} are now **Married** 🎉', color=color.color)
                        await interaction.response.edit_message(embed=embed, view=None)

                        channel = self.client.get_channel(1196058236143538236)

                        caveat = Font.caveat(size=45)
                        small_caveat = Font.caveat(size=40)

                        today = date.today()
                        today_date = today.strftime("%B %d, %Y")

                        background = Editor("./assets/marriage/certificate.png")
                        background.text(
                                        (329, 224),
                                        f"{ctx.message.author}",
                                        font=caveat,
                                        align="center",
                                        color=0x3C1C1F,)
                        
                        background.text(
                                        (329, 292),
                                        f"{member}",
                                        font=caveat,
                                        align="center",
                                        color=0x3C1C1F,)
                        
                        background.text(
                                        (254, 365),
                                        f"{today_date}",
                                        font=small_caveat,
                                        color=0x3C1C1F,)
                        
                        file = File(fp=background.image_bytes, filename="certificate.png")
                        message = await channel.send(file=file)
                        url = message.attachments[0].url
                        
                        collection.update_one({"_id": ctx.message.author.id}, {"$set": {"certificate": url}})
                        collection.update_one({"_id": member.id}, {"$set": {"certificate": url}})


                async def decline_callback(interaction):
                    channel = self.client.get_channel(1039221368291602532)

                    accept = discord.ui.Button(style=discord.ButtonStyle.green, label="yes", disabled = True)
                    decline = discord.ui.Button(style=discord.ButtonStyle.red, label="no", disabled = True)

                    accept.callback = accept_callback
                    decline.callback = decline_callback

                    view = discord.ui.View()
                    view.add_item(item=accept)
                    view.add_item(item=decline)

                    if interaction.user != member:
                        embed = discord.Embed(description=f"> {emojis.false} They didnt asked you", color=color.f)
                        await interaction.response.send_message(embed=embed, view=None, ephemeral=True)
                        return
                    else:
                        embed = discord.Embed(description=f'> {member.mention} said **no**... :sob:', color=color.color)
                        await interaction.response.edit_message(embed=embed, view=None)


                accept.callback = accept_callback
                decline.callback = decline_callback

                view = discord.ui.View()
                view.add_item(item=accept)
                view.add_item(item=decline)
                await ctx.send(embed=embed, view=view)


    @commands.command(brief='divorce from your marriage', description='fun')
    @blacklist_check()
    async def divorce(self, ctx):
        if not collection.find_one({"_id": ctx.message.author.id}):
            embed = discord.Embed(description=f'> You are not **Married** :cry:', color=color.color)
            await ctx.send(embed=embed)

        else:
            check = collection.find_one({"_id": ctx.message.author.id})
            member = self.client.get_user(check['married'])

            accept = discord.ui.Button(style=discord.ButtonStyle.green, label="yes")
            decline = discord.ui.Button(style=discord.ButtonStyle.red, label="no")

            embed = discord.Embed(description=f'> Do you really want to **Divorce** {member.mention}? :cry:', color=color.color)

            async def accept_callback(interaction):
                if interaction.user != ctx.author:
                    embed = discord.Embed(description=f"> {emojis.false} They didnt asked you", color=color.f)
                    await interaction.response.send_message(embed=embed, view=None, ephemeral=True)
                    return
                else:
                    check = collection.find_one({"_id": ctx.message.author.id})
                    member = self.client.get_user(check['married'])

                    collection.delete_one({"_id": ctx.message.author.id})
                    collection.delete_one({"_id": member.id})

                    embed = discord.Embed(description=f'> You **divorced** {member.mention} :sob:', color=color.color)
                    await interaction.response.edit_message(embed=embed, view=None)

            async def decline_callback(interaction):
                if interaction.user != ctx.author:
                    embed = discord.Embed(description=f"> {emojis.false} They didnt asked you", color=color.colofr)
                    await interaction.response.send_message(embed=embed, view=None, ephemeral=True)
                    return
                else:
                    check = collection.find_one({"_id": ctx.message.author.id})
                    member = self.client.get_user(check['married'])

                    embed = discord.Embed(description=f'> You didnt **divorced** {member.mention}, luckily 🥰', color=color.color)
                    await interaction.response.edit_message(embed=embed, view=None)

            accept.callback = accept_callback
            decline.callback = decline_callback

            view = discord.ui.View()
            view.add_item(item=accept)
            view.add_item(item=decline)
            await ctx.send(embed=embed, view=view)

async def setup(client):
    await client.add_cog(marriage(client))
