import discord
import sys
import os
import pymongo
import button_paginator as pg
from pymongo import MongoClient
from discord.ext import commands
from utils import functions
from utils.emojis import emojis
from utils.color import color

cluster = MongoClient('mongodb+srv://blade:lolidkbruh12333333333@cluster0.wbxaj.mongodb.net/myFirstDatabase?retryWrites=true&w=majority')
db = cluster["blade"]
collection = db["clans"]
collections = db["clan_members"]
economy = db["economy"]

class clans(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_message(self, message):
        if not collections.find_one({"_id": message.author.id}):
            return
        
        else:
            data = collections.find_one({"_id": message.author.id})
            check = collection.find_one({"_id": data["clan"]})
            collections.update_one({"_id": message.author.id}, {"$set": {"points": data["points"] + 1}})
            collection.update_one({"_id": data["clan"]}, {"$set": {"points": check["points"] + 1}})
            
    @commands.group(pass_context=True, invoke_without_command=True, brief='look at a clan', description='clans')
    async def clan(self, ctx, clan=None):
        if clan == None:
            if not collections.find_one({"_id": ctx.message.author.id}):
                embed = discord.Embed(description=f'> {emojis.false} You are not in a **Clan**', color=color.fail)
                await ctx.send(embed=embed)

            else:
                data = collections.find_one({"_id": ctx.message.author.id})
                check = collection.find_one({"_id": data["clan"]})
                owner = self.client.get_user(check["owner"])

                if check["public"] == False:
                    badge = f'{emojis.lock}'
                else:
                    badge = f'<:globe:1152946124718620672>'

                embed = discord.Embed(title=f'{emojis.blade} Clan | {check["_id"]} {badge}', color=color.color,
                                    description=f'{emojis.reply} **Description**: {check["description"]}')
                embed.add_field(name='<:stats:1149447552526205019> Stats', value=f'{emojis.reply2} **Owner**: ``{owner.name}`` \n{emojis.reply2} **Members**: ``{check["member_count"]} Members`` \n{emojis.reply} **Points**: ``{check["points"]} Points``', inline=False)

                if check['icon'] == 'none':
                    embed.set_thumbnail(url=owner.display_avatar)
                else:
                    try:
                        embed.set_thumbnail(url=check['icon'])
                    except:
                        embed.set_thumbnail(url=owner.display_avatar)

                await ctx.send(embed=embed)
        else:
            if collection.find_one({"_id": clan}):
                check = collection.find_one({"_id": clan})
                owner = self.client.get_user(check["owner"])

                if check["public"] == False:
                    badge = f'{emojis.lock}'
                else:
                    badge = f'<:globe:1152946124718620672>'

                embed = discord.Embed(title=f'{emojis.blade} Clan | {check["_id"]} {badge}', color=color.color,
                                    description=f'{emojis.reply} **Description**: {check["description"]}')
                embed.add_field(name='<:stats:1149447552526205019> Stats', value=f'{emojis.reply2} **Owner**: ``{owner.name}`` \n{emojis.reply2} **Members**: ``{check["member_count"]} Members`` \n{emojis.reply} **Points**: ``{check["points"]} Points``', inline=False)

                if check['icon'] == 'none':
                    embed.set_thumbnail(url=owner.display_avatar)
                else:
                    try:
                        embed.set_thumbnail(url=check['icon'])
                    except:
                        embed.set_thumbnail(url=owner.display_avatar)
                await ctx.send(embed=embed)

            else:
                embed = discord.Embed(description=f'> {emojis.false} The Clan ``{clan}`` dosnt **exist**', color=color.fail)
                await ctx.send(embed=embed)

    @commands.command(brief='see all clans', description='clans')
    async def clans(self, ctx):
        count = collection.count_documents({})

        banned = [m async for m in ctx.guild.bans()]
        if len(banned) == 0: 
            await ctx.send("> There are no banned people in this server")  
            return
    
        i=0
        k=1
        l=0
        mes = ""
        number = []
        messages = []
        for x in collection.find({}): 

            if x["public"] == False:
                badge = f'{emojis.lock}'
            else:
                badge = f'<:globe:1152946124718620672>'

            mes = f"{mes}`{k}.` **{x['_id']}** - `{x['points']} Points` {badge} \n"
            k+=1
            l+=1
            if l == 10:
                messages.append(mes)
                number.append(discord.Embed(title=f"{emojis.blade} Clans | {count}", description=messages[i], color=color.color))
                i+=1
                mes = ""
                l=0
    
        messages.append(mes)
        embed = discord.Embed(title=f"{emojis.blade} Clans | {count}", description=messages[i], color=color.color)
        number.append(embed)

        if len(number) > 1:
            paginator = pg.Paginator(self.client, number, ctx, invoker=ctx.author.id)
            paginator.add_button('prev', emoji= "<:left_arrow:1111012825511493764>")
            paginator.add_button('delete', emoji = "<:fail:963149868698837062>")
            paginator.add_button('next', emoji="<:right_arrow:1111012858071875594>")
            await paginator.start()  
        else:
            await ctx.send(embed=embed)

    @clan.command(brief='create a clan', description='clans')
    async def create(self, ctx, name: str=None):
        if collections.find_one({"_id": ctx.message.author.id}):
            embed = discord.Embed(description=f'> {emojis.false} You are already inside a **Clan**', color=color.fail)
            await ctx.send(embed=embed)

        else:
            if economy.find_one({"_id": ctx.message.author.id}):
                check = economy.find_one({"_id": ctx.message.author.id})

                if check["money"] < 5000:
                    embed = discord.Embed(description=f'> {emojis.false} You dont have enough **Money** to create a **Clan** you need at least ``5,000💵`` ', color=color.fail)
                    await ctx.send(embed=embed)

                else:
                    if name == None:
                        embed = discord.Embed(description=f'> {emojis.false} You need to type a **Name** for your Clan', color=color.fail)
                        await ctx.send(embed=embed)
                        
                    else:
                        if len(name)> 16:
                            embed = discord.Embed(description=f'> {emojis.false} The Name ``{name}`` is to **long**', color=color.fail)
                            await ctx.send(embed=embed)

                        if len(name)< 3:
                            embed = discord.Embed(description=f'> {emojis.false} The Name ``{name}`` is to **short**', color=color.fail)
                            await ctx.send(embed=embed)

                        else:
                            for i in collection.find({}):
                                if name.lower() in i["_id"].lower():
                                    embed = discord.Embed(description=f'> {emojis.false} A Clan with the Name **{name}** already exist', color=color.fail)
                                    await ctx.send(embed=embed)
                                    return
                            
                            else:
                                clan = {"_id": name, "owner": ctx.message.author.id, "points": 0, "member_count": 1, "members": [], "icon": 'none', "description": 'none', "public": False}
                                collection.insert_one(clan)

                                clan_owner = {"_id": ctx.message.author.id, "clan": name, "points": 0}
                                collections.insert_one(clan_owner)

                                #economy.update_one({"_id": ctx.message.author.id}, {"$set": {"money": check["money"] - 5000}})

                                embed = discord.Embed(description=f'> {emojis.true} Created your Clan named **{name}**', color=color.success)
                                await ctx.send(embed=embed)

            else:
                embed = discord.Embed(description=f'> {emojis.false} You dont have a **Economy Profile**', color=color.fail)
                await ctx.send(embed=embed)

    @commands.command(aliases=['clanlb', 'clb'], brief='look at the leaderboard', description='clans')
    async def clanleaderboard(self, ctx):
        rankings = collection.find().sort("points",-1)
        i = 1
        embed = discord.Embed(title=f"{emojis.blade} Clans Leaderboard", description=f'{emojis.reply} Top 10 best Clans \n \n', color=color.color)
        for x in rankings:
            try:
                name = x["_id"]
                points = x["points"]
                members = x["member_count"]
                embed.description += f"``{i}.`` **{name}**: ``{points} Points`` \n"
                i += 1
            except:
                pass
            if i == 11:
                break
        await ctx.send(embed=embed)

    @clan.command(brief='set the clan public', description='clans')
    async def public(self, ctx):
        if collection.find_one({"owner": ctx.message.author.id}):
            check = collection.find_one({"owner": ctx.message.author.id})
            if check["public"] == False:
                collection.update_one({"owner": ctx.message.author.id}, {"$set": {"public": True}})
                embed = discord.Embed(description=f'> {emojis.true} **Successfully** made the **Clan** Public', color=color.success)
                await ctx.send(embed=embed)

            else:
                embed = discord.Embed(description=f'> {emojis.false} The **Clan** is already Public', color=color.fail)
                await ctx.send(embed=embed)
                
        else:
            embed = discord.Embed(description=f'> {emojis.false} You dont own a **Clan**', color=color.fail)
            await ctx.send(embed=embed)

    @clan.command(brief='set the clan private', description='clans')
    async def private(self, ctx):
        if collection.find_one({"owner": ctx.message.author.id}):
            check = collection.find_one({"owner": ctx.message.author.id})

            if check["public"] == True:
                collection.update_one({"owner": ctx.message.author.id}, {"$set": {"public": False}})
                embed = discord.Embed(description=f'> {emojis.true} **Successfully** made the **Clan** Private', color=color.success)
                await ctx.send(embed=embed)

            else:
                embed = discord.Embed(description=f'> {emojis.false} The **Clan** is already Private', color=color.fail)
                await ctx.send(embed=embed)
                
        else:
            embed = discord.Embed(description=f'> {emojis.false} You dont own a **Clan**', color=color.fail)
            await ctx.send(embed=embed)

    @clan.command(brief='join a public clan', description='clans')
    async def join(self, ctx, clan=None):
        if collections.find_one({"_id": ctx.message.author.id}):
            embed = discord.Embed(description=f'> {emojis.false} You are already inside a **Clan**', color=color.fail)
            await ctx.send(embed=embed)

        else:
            if clan == None:
                embed = discord.Embed(description=f'> {emojis.false} Which **Clan** do you want to **Join**?', color=color.fail)
                await ctx.send(embed=embed)

            else:
                if collection.find_one({"_id": clan}):
                    check = collection.find_one({"_id": clan})

                    if check["public"] == True:
                        clan_member = {"_id": ctx.message.author.id, "clan": check["_id"], "points": 0}
                        collections.insert_one(clan_member)

                        collection.update_one({"_id": check["_id"]}, {"$push": {"members": ctx.message.author.id}})
                        collection.update_one({"_id": check["_id"]}, {"$set": {"member_count": check["member_count"]+ 1}})

                        embed = discord.Embed(description=f'> {emojis.true} You joined the clan **{clan}**', color=color.success)
                        await ctx.send(embed=embed)

                    else:
                        embed = discord.Embed(description=f'> {emojis.false} The Clan **{clan}** is not **Public**', color=color.fail)
                        await ctx.send(embed=embed)
                else:
                    embed = discord.Embed(description=f'> {emojis.false} There is no Clan with the Name **{clan}**', color=color.fail)
                    await ctx.send(embed=embed)

    @clan.command(brief='leave a clan', description='clans')
    async def leave(self, ctx):
        if collections.find_one({"_id": ctx.message.author.id}):
            px = functions.get_prefix(ctx)

            if collection.find_one({"owner": ctx.message.author.id}):
                embed = discord.Embed(description=f'> {emojis.false} You cant **Leave** your own Clan, delete it with ``{px}clan delete``', color=color.fail)
                await ctx.send(embed=embed)

            else:
                data = collections.find_one({"_id": ctx.message.author.id})
                check = collection.find_one({"_id": data["clan"]})

                collection.update_one({"_id": check["_id"]}, {"$pull": {"members": ctx.message.author.id}})
                collection.update_one({"_id": check["_id"]}, {"$set": {"member_count": check["member_count"] - 1}})
                collection.update_one({"_id": check["_id"]}, {"$set": {"points": check["points"] - data["points"]}})

                collections.delete_one({"_id": ctx.message.author.id})

                embed = discord.Embed(description=f'> {emojis.true} You left your **Clan**', color=color.success)
                await ctx.send(embed=embed)
        
        else:
            embed = discord.Embed(description=f'> {emojis.false} You are not in a **Clan**', color=color.fail)
            await ctx.send(embed=embed)

    @clan.command(brief='change the clans icon', description='clans')
    async def icon(self, ctx, image=None):
        if collection.find_one({"owner": ctx.message.author.id}):
            check = collection.find_one({"owner": ctx.message.author.id})
            if image == None:
                embed = discord.Embed(description=f'{emojis.false} You need to **Provide** a Image-Link', color=color.fail)
                await ctx.send(embed=embed)
            
            else:
                try:
                    embed = discord.Embed(description=f'> {emojis.true} Successfully set you clan **Icon** to:', color=color.success)
                    embed.set_image(url=image)
                    collection.update_one({"owner": ctx.message.author.id}, {"$set": {"icon": image}})
                    await ctx.send(embed=embed)
                except:
                    embed = discord.Embed(description=f'{emojis.false} The **Image-Link** didnt work', color=color.fail)
                    await ctx.send(embed=embed)
        
        else:
            embed = discord.Embed(description=f'{emojis.false} You dont own a **Clan**', color=color.fail)
            await ctx.send(embed=embed)

    @clan.command(aliases=['desc'], brief='change the clan description', description='clans')
    async def description(self, ctx, *, message=None):
        if collection.find_one({"owner": ctx.message.author.id}):
            check = collection.find_one({"owner": ctx.message.author.id})
            if message == None:
                embed = discord.Embed(description=f'{emojis.false} You need to **Provide** a message', color=color.fail)
                await ctx.send(embed=embed)
            
            else:
                embed = discord.Embed(description=f'> {emojis.true} Successfully set the Clan **description** to:  \n ``{message}``', color=color.success)
                collection.update_one({"owner": ctx.message.author.id}, {"$set": {"description": message}})
                await ctx.send(embed=embed)
        
        else:
            embed = discord.Embed(description=f'{emojis.false} You dont own a **Clan**', color=color.fail)
            await ctx.send(embed=embed)

    @clan.command(brief='kick a clan member', description='clans')
    async def kick(self, ctx, user: discord.User = None):
        if collection.find_one({"owner": ctx.message.author.id}):
            check = collection.find_one({"owner": ctx.message.author.id})
            if user == None:
                embed = discord.Embed(description=f'{emojis.false} Who do you want to **Kick** ?', color=color.fail)
                await ctx.send(embed=embed)
            
            else:
                if user.id in check["members"]:
                    data = collections.find_one({"_id": user.id})

                    collection.update_one({"owner": ctx.message.author.id}, {"$pull": {"members": user.id}})
                    collection.update_one({"owner": ctx.message.author.id}, {"$set": {"member_count": check["member_count"] - 1}})
                    collection.update_one({"owner": ctx.message.author.id}, {"$set": {"points": check["points"] - data["points"]}})

                    collections.delete_one({"_id": user.id})

                    embed = discord.Embed(description=f'{emojis.true} **Succesfully** kicked {user.mention} from your **Clan**', color=color.success)
                    await ctx.send(embed=embed)

                else:
                    embed = discord.Embed(description=f'{emojis.false} {user.mention} is not in your Clan', color=color.fail)
                    await ctx.send(embed=embed)
        
        else:
            embed = discord.Embed(description=f'{emojis.false} You dont own a **Clan**', color=color.fail)
            await ctx.send(embed=embed)

    @clan.command(brief='look at your clan points', description='clans')
    @commands.cooldown(1, 4, commands.BucketType.user)
    async def points(self, ctx):
        if not collections.find_one({"_id": ctx.message.author.id}):
            embed = discord.Embed(description=f'> {emojis.false} You are not in a **Clan**', color=color.fail)
            await ctx.send(embed=embed)

        else:
            data = collections.find_one({"_id": ctx.message.author.id})

            embed = discord.Embed(description=f'> You got ``{data["points"]} Points``', color=color.color)
            await ctx.send(embed=embed)

    @clan.command(brief='look at all the clan members', description='clans')
    @commands.cooldown(1, 4, commands.BucketType.user)
    async def members(self, ctx):
        if collections.find_one({"_id": ctx.message.author.id}):
            data = collections.find_one({"_id": ctx.message.author.id})
            check = collection.find_one({"_id": data["clan"]})
            check2 = collections.find_one({"_id": check["owner"]})
            if check['members'] == []: 
                embed = discord.Embed(description=f'> {emojis.false} There are no **Members** in this **Clan**', color=color.fail)
                await ctx.send(embed=embed)  
                return

            owner = self.client.get_user(check['owner'])

            i=0
            k=2
            l=0
            mes = ""
            number = []
            messages = []

            #owner = self.client.get_user(check['owner'])
            #msg = f'{mes} `👑.` **{owner.mention}** | ``{check2["points"]} Points``'
            for m in check['members']: 
                member = self.client.get_user(m)
                check = collections.find_one({"_id": m})
                mes = f"{mes}`{k}.` **{member.mention}** | ``{check['points']} Points`` \n"
                k+=1
                l+=1
                if l == 10:
                    messages.append(mes)
                    number.append(discord.Embed(title=f"{emojis.blade} Clan Members", description=f'`👑.` **{owner.mention}** | ``{check2["points"]} Points``\n' + messages[i], color=color.color))
                    i+=1
                    mes = ""
                    l=0
        
            messages.append(mes)
            embed = discord.Embed(title=f"{emojis.blade} Clan Members", description=f'``👑.`` **{owner.mention}** | ``{check2["points"]} Points`` \n' + messages[i], color=color.color)
            number.append(embed)

            if len(number) > 1:
                paginator = pg.Paginator(self.client, number, ctx, invoker=ctx.author.id)
                paginator.add_button('prev', emoji= "<:left_arrow:1111012825511493764>")
                paginator.add_button('delete', emoji = "<:fail:963149868698837062>")
                paginator.add_button('next', emoji="<:right_arrow:1111012858071875594>")
                await paginator.start()  
            else:
                await ctx.send(embed=embed)

        else:
            embed = discord.Embed(description=f'> {emojis.false} You are not in a **Clan**', color=color.fail)
            await ctx.send(embed=embed)

    @clan.command(brief='invite a member to your clan', description='clans')
    @commands.cooldown(1, 4, commands.BucketType.user)
    async def invite(self, ctx, user: discord.Member):
        if collection.find_one({"owner": ctx.message.author.id}):
            if collections.find_one({"_id": user.id}):
                embed = discord.Embed(description=f'> {emojis.false} {user.mention} is already in a **Clan**', color=color.fail)
                await ctx.send(embed=embed)

            else:
                check = collection.find_one({"owner": ctx.message.author.id})

                accept = discord.ui.Button(style=discord.ButtonStyle.green, label="accept", emoji=emojis.true)
                decline = discord.ui.Button(style=discord.ButtonStyle.red, label="decline", emoji=emojis.false)

                async def accept_callback(interaction):
                    if interaction.user.id != user.id:
                        embed = discord.Embed(description=f"> {emojis.false} This is not your message", color=color.fail)
                        await interaction.response.send_message(embed=embed, view=None, ephemeral=True)
                        return
                    else:
                        clan_member = {"_id": user.id, "clan": check["_id"], "points": 0}
                        collections.insert_one(clan_member)

                        collection.update_one({"_id": check["_id"]}, {"$push": {"members": user.id}})
                        collection.update_one({"_id": check["_id"]}, {"$set": {"member_count": check["member_count"]+ 1}})

                        embed = discord.Embed(description=f'> {emojis.true} Successfully **Joined** the **Clan**', color=color.success)
                        await interaction.response.edit_message(embed=embed, view=None)

                async def decline_callback(interaction):
                    accept = discord.ui.Button(style=discord.ButtonStyle.green, label="accept", emoji=emojis.true, disabled = True)
                    decline = discord.ui.Button(style=discord.ButtonStyle.red, label="decline", emoji=emojis.false, disabled = True)

                    accept.callback = accept_callback
                    decline.callback = decline_callback

                    view = discord.ui.View()
                    view.add_item(item=accept)
                    view.add_item(item=decline)

                    if interaction.user.id != user.id:
                        embed = discord.Embed(description=f"> {emojis.false} This is not your message", color=color.fail)
                        await interaction.response.send_message(embed=embed, view=None, ephemeral=True)
                        return
                    else:
                        embed = discord.Embed(description=f'> {emojis.true} {user.mention} **declined** to Join the **Clan**', color=color.success)
                        await interaction.response.edit_message(embed=embed, view=None)

                accept.callback = accept_callback
                decline.callback = decline_callback

                view = discord.ui.View()
                view.add_item(item=accept)
                view.add_item(item=decline)

                embed = discord.Embed(description=f'> {user.mention} has been **Invited** to join the ``{check["_id"]}`` Clan, do you want to Join?', color=color.color)
                await ctx.send(embed=embed, view=view)

        else:
            embed = discord.Embed(description=f'> {emojis.false} You dont own a **Clan**', color=color.fail)
            await ctx.send(embed=embed)

    @clan.command(brief='delete your clan', description='clans')
    @commands.cooldown(1, 4, commands.BucketType.user)
    async def delete(self, ctx):
        if collection.find_one({"owner": ctx.message.author.id}):
            accept = discord.ui.Button(style=discord.ButtonStyle.green, label="accept", emoji=emojis.true)
            decline = discord.ui.Button(style=discord.ButtonStyle.red, label="decline", emoji=emojis.false)

            async def accept_callback(interaction):
                if interaction.user != ctx.author:
                    embed = discord.Embed(description=f"> {emojis.false} This is not your message", color=color.fail)
                    await interaction.response.send_message(embed=embed, view=None, ephemeral=True)
                    return
                else:

                    check = collection.find_one({"owner": ctx.message.author.id})

                    for x in check["members"]:
                        collections.delete_one({"_id": x})

                    collection.delete_one({"owner": ctx.message.author.id})
                    collections.delete_one({"_id": ctx.message.author.id})

                    embed = discord.Embed(description=f'> {emojis.true} Successfully **deleted** your **Clan**', color=color.success)
                    await interaction.response.edit_message(embed=embed, view=None)

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
                    embed = discord.Embed(description=f'> {emojis.true} You **declined** to delete your **Clan**', color=color.success)
                    await interaction.response.edit_message(embed=embed, view=None)

            accept.callback = accept_callback
            decline.callback = decline_callback

            view = discord.ui.View()
            view.add_item(item=accept)
            view.add_item(item=decline)

            embed = discord.Embed(description=f'> Are you sure to delete your **Clan** ?', color=color.color)
            await ctx.send(embed=embed, view=view)

        else:
            embed = discord.Embed(description=f'> {emojis.false} You dont own a **Clan**', color=color.fail)
            await ctx.send(embed=embed)

async def setup(client):
    await client.add_cog(clans(client))
