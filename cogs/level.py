import discord
import pymongo
import asyncio
import aiohttp
import random
import button_paginator as pg
from io import BytesIO
from pymongo import MongoClient
from discord.ext import commands
from utils import functions
from utils.emojis import emojis
from utils.bar import bar
from utils.color import color

cluster = MongoClient('no')
db = cluster["blade"]
collection = db["level"]
config = db["levelconfig"]
premium = db["premium"]
silence = db["silence"]
rankcard = db["rankcard"]
blacklist = db["blacklist"]

def blacklist_check():
    def predicate(ctx):
        if blacklist.find_one({'_id': ctx.author.id}):
            return False
        return True
    return commands.check(predicate)

class level(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    @blacklist_check()
    async def on_member_remove(self, member: discord.Member):
        if config.find_one({"_id": member.guild.id}):
            if collection.find_one({"user": member.id, "server": member.guild.id}):
                collection.delete_one({"user": member.id, "server": member.guild.id})

    @commands.Cog.listener()
    async def on_message(self, message):
        try:
            if config.find_one({"_id": message.guild.id}):
                check = config.find_one({"_id": message.guild.id})
                if not message.author.bot and not blacklist.find_one({'_id': message.author.id}):
                    if check['level'] == True:
                        if not collection.find_one({"user": message.author.id, "server": message.guild.id}):
                            leveler = {"user": message.author.id, "server": message.guild.id, "level": 0, "xp": 10}
                            collection.insert_one(leveler)

                        if message.channel.id in check['blacklist']:
                            return
                        
                        if silence.find_one({"_id": message.guild.id}):
                            if message.author.id in silence.find_one({"_id": message.guild.id})["silenced"]:
                                return

                        check2 = collection.find_one({"user": message.author.id, "server": message.guild.id})
                        collection.update_one({"user": message.author.id, "server": message.guild.id}, {"$set": {"xp": check2["xp"] + 10 }})

                        level_up = 750 + (1050 * check2['level'])

                        if check2['xp'] == level_up or check2['xp'] > level_up:
                            level = check2['level'] + 1
                            collection.update_one({"user": message.author.id, "server": message.guild.id}, {"$set": {"level": level}})

                            level_message = check['level_message']
                            level_message = level_message.replace("{level}","%s" % (level))
                            level_message = level_message.replace("{xp}","%s" % (check2['xp']))
                            level_message = level_message.replace("{member.id}","%s" % (message.author.id))
                            level_message = level_message.replace("{member.name}","%s" % (message.author.name))
                            level_message = level_message.replace("{member.mention}","%s" % (message.author.mention))
                            level_message = level_message.replace("{member.tag}","%s" % (message.author.discriminator))
                            level_message = level_message.replace("{server.name}","%s" % (message.guild.name))
                            level_message = level_message.replace("{server.id}","%s" % (message.guild.id))

                            embed = discord.Embed(description=f'{level_message}', color=color.color)

                            for x in check['rewards']:
                                level_reward, role_reward = x.split('¦')

                                if int(level_reward) == level:
                                    role = message.guild.get_role(int(role_reward))
                                    await message.author.add_roles(role)

                            if check['channel'] == 0:
                                if check['mention'] == False:
                                    await message.channel.send(embed=embed)
                                if check['mention'] == True:
                                    await message.channel.send(f'{message.author.mention}', embed=embed)

                            else:
                                level_channel = self.client.get_channel(check['channel'])
                                if check['mention'] == False:
                                    await level_channel.send(embed=embed)
                                if check['mention'] == True:
                                    await level_channel.send(f'{message.author.mention}', embed=embed)

                        else:
                            return

                    else:
                        return
            else:
                pass
        except:
            pass

        await asyncio.sleep(1)

    @commands.command(brief='set your rank background')
    @commands.cooldown(1, 32, commands.BucketType.user)
    @blacklist_check()
    async def rankcard(self, ctx, image=None):
        if premium.find_one({"_id": ctx.message.author.id}):
            if image == None:
                if len(ctx.message.attachments) > 0:
                    for file in ctx.message.attachments:
                        url = ctx.message.attachments[0].url
                        async with aiohttp.ClientSession() as ses:
                            async with ses.get(url) as r:
                                img = BytesIO(await r.read())
                                bytes = img.getvalue()

                            if not rankcard.find_one({"_id": ctx.message.author.id}):
                                cardrank = {"_id": ctx.message.author.id, "image": ctx.message.attachments[0].url}
                                rankcard.insert_one(cardrank)
                            else:
                                rankcard.update_one({"_id": ctx.message.author.id}, {"$set": {"image": ctx.message.attachments[0].url}})
                            embed = discord.Embed(description=f'> {emojis.true} Changed your Rank **background** to:', color=color.success)
                            embed.set_image(url=ctx.message.attachments[0].url)
                            await ctx.send(embed=embed)
                else:
                    embed = discord.Embed(description=f'> {emojis.false} Provide a **Image** or a **Image-link** to set your Rank **background**', color=color.fail)
                    await ctx.send(embed=embed)

            else:
                if not rankcard.find_one({"_id": ctx.message.author.id}):
                    cardrank = {"_id": ctx.message.author.id, "image": image}
                    rankcard.insert_one(cardrank)
                else:
                    rankcard.update_one({"_id": ctx.message.author.id}, {"$set": {"image": image}})
                embed = discord.Embed(description=f'> {emojis.true} Changed your Rank **background** to:', color=color.success)
                embed.set_image(url=image)
                await ctx.send(embed=embed)
        else:
            embed = discord.Embed(description=f'> {emojis.false} This Command is for **Premium** only, find more information [here](https://discord.gg/MVnhjYqfYu)', color=color.color)
            await ctx.send(embed=embed)

    @commands.command(aliases=['old_level', 'old_lvl'])
    @blacklist_check()
    async def old_rank(self, ctx, member: discord.Member=None):
        if member == None:
            member = ctx.message.author

        if collection.find_one({"user": member.id, "server": ctx.message.guild.id}):
            check = collection.find_one({"user": member.id, "server": ctx.message.guild.id})

            xp_check = collection.find_one({"user": member.id, "server": ctx.message.guild.id})['xp']

            level_reach = 750 + (1050 * check['level'])

            if xp_check > level_reach / 100 * 10:
                xp_bar = f'{bar.bar1}'

            if xp_check > level_reach / 100 * 20:
                xp_bar = f'{bar.bar2}'

            if xp_check > level_reach / 100 * 30:
                xp_bar = f'{bar.bar3}'

            if xp_check > level_reach / 100 * 40:
                xp_bar = f'{bar.bar4}'

            if xp_check > level_reach / 100 * 50:
                xp_bar = f'{bar.bar5}'

            if xp_check > level_reach / 100 * 60:
                xp_bar = f'{bar.bar6}'

            if xp_check > level_reach / 100 * 70:
                xp_bar = f'{bar.bar7}'

            if xp_check > level_reach / 100 * 80:
                xp_bar = f'{bar.bar8}'

            if xp_check > level_reach / 100 * 90:
                xp_bar = f'{bar.bar9}'

            if xp_check > level_reach / 100 * 100:
                xp_bar = f'{bar.bar10}'

            embed = discord.Embed(description=f'{emojis.reply2} level: ``{check["level"]}`` \n{emojis.reply} xp: ``{check["xp"]}`` \n \n``{check["xp"]}xp / {level_reach}xp`` \n {xp_bar} **Level {check["level"] + 1}**', color=color.color)
            embed.set_author(name=f"{member.name}'s rank", icon_url=member.display_avatar)
            await ctx.send(embed=embed)

        else:
            embed = discord.Embed(description=f'> {emojis.false} {member.mention} hasnt sent any Message yet', color=color.fail)
            await ctx.send(embed=embed)

    @commands.command(aliases=['lvllb', 'llb'])
    @blacklist_check()
    async def lvlleaderboard(self, ctx):
        if config.find_one({"_id": ctx.message.guild.id}):
            check = config.find_one({"_id": ctx.message.guild.id})
            if check['level'] == True:
                rankings = collection.find({"server": ctx.guild.id}).sort("xp",-1)
                i = 1
                embed = discord.Embed(title=f"{emojis.blade} Level Leaderboard", description=f'{emojis.reply} Top 10 Members \n \n', color=color.color)
                for x in rankings:
                    try:
                        temp = self.client.get_user(x["user"])
                        tempxp = x["level"]
                        embed.description += f"``{i}.`` **{temp.name}**: Level ``{tempxp:,}`` \n"
                        i += 1
                    except:
                        pass
                    if i == 11:
                        break
                await ctx.send(embed=embed)
            else:
                return
        else:
            return

    @commands.group(pass_context=True, invoke_without_command=True, aliases=['lvlc', 'lc'], brief='configurate your leveling', description='config')
    @commands.has_guild_permissions(manage_guild=True)
    @blacklist_check()
    async def levelconfig(self, ctx):
        await ctx.invoke()

    @levelconfig.command(aliases=['r'], biref='add or remove rewards')
    @commands.has_guild_permissions(manage_guild=True)
    @blacklist_check()
    async def reward(self, ctx, function = None, level: int=None, role: discord.Role=None):
        if not config.find_one({"_id": ctx.message.guild.id}):
            lvlconfig = {"_id": ctx.message.guild.id, "level": False, "mention": False, "channel": 0, "rewards": [], "blacklist": [], "level_message": '> 🎉 {member.mention} just leveled up to **Level {level}** 🎉'}
            config.insert_one(lvlconfig)

        check = config.find_one({"_id": ctx.message.guild.id})
        px = functions.get_prefix(ctx)

        if function and level == None:
            embed = discord.Embed(title=f'{emojis.blade} Level', color=color.color,
            description=f'{emojis.reply} *make level rewards*')
            embed.add_field(name=f"{emojis.commands} Command:", value=f"> ``{px}levelconfig reward add [level] [@role]`` add a reward for a level \n> ``{px}levelconfig reward remove [level]`` remove a reward for a level", inline=False)
            embed.add_field(name=f"{emojis.alias} Alias:", value=f"```r```", inline=False)
            await ctx.send(embed=embed)

        else:
            if function == 'add':
                if role == None:
                    embed = discord.Embed(description=f'> {emojis.false} Which Role do you want to give **Level {level}**', color=color.fail)
                    await ctx.send(embed=embed)
                else:
                    autorsp = f'{level}¦{role.id}'

                    config.update_one({"_id": ctx.message.guild.id}, {"$push": {"rewards": autorsp}})

                    embed = discord.Embed(description=f'> {emojis.true} Added **Level {level}** with the Role {role.mention}', color=color.success)
                    await ctx.send(embed=embed)

            if function == 'remove':
                if level == None:
                    embed = discord.Embed(description=f'> {emojis.blade} Which **Level** do you trynna Remove?', color=color.color)
                    await ctx.send(embed=embed)

                else:
                    if role == None:
                        role = None

                    num = 0

                    level = f'{level}'

                    for i in check['rewards']:
                        num = num+1
                        lvl_level, role_id = i.split('¦')

                        if lvl_level in level:
                            collection.update_one({"_id": ctx.message.guild.id}, {"$pull": {"rewards": i}})

                    embed = discord.Embed(description=f'> {emojis.true} Removed ``{num}`` **Rewards** with the Level ``{level}``', color=color.color)

    @commands.command(brief='add a member xp')
    @commands.has_guild_permissions(manage_guild=True)
    async def addxp(self, ctx, member: discord.Member, xp: int):
        if not config.find_one({"_id": ctx.message.guild.id}):
            return

        else:
            if not collection.find_one({"user": member.id, "server": ctx.message.guild.id}):
                embed = discord.Embed(description=f'> {emojis.false} {member.mention} dosnt have a **Rank**', color=color.fail)
                await ctx.send(embed=embed)

            else:
                check = collection.find_one({"user": member.id, "server": ctx.message.guild.id})

                math = xp / (750 + 1050)
                level = round(math)

                collection.update_one({"user": member.id, "server": ctx.message.guild.id}, {"$set": {"xp": check["xp"] + xp}})
                collection.update_one({"user": member.id, "server": ctx.message.guild.id}, {"$set": {"level": check["level"] + level}})
                embed = discord.Embed(description=f'> {emojis.true} You add {member.mention} ``{xp}`` xp', color=color.success)
                await ctx.send(embed=embed)

    @levelconfig.command(aliases=['rs'], brief='see all rewards')
    @commands.has_guild_permissions(manage_guild=True)
    @blacklist_check()
    async def rewards(self, ctx):
        if not config.find_one({"_id": ctx.message.guild.id}):
            lvlconfig = {"_id": ctx.message.guild.id, "level": False, "mention": False, "channel": 0, "rewards": [], "blacklist": [], "level_message": '> 🎉 {member.mention} just leveled up to **Level {level}** 🎉'}
            config.insert_one(lvlconfig)

        check = config.find_one({"_id": ctx.message.guild.id})

        if check['rewards'] == []:
            embed = discord.Embed(description=f'> {emojis.false} There are no **Rewards** set', color=color.fail)
            await ctx.send(embed=embed)

        else:
            i=0
            k=1
            l=0
            mes = ""
            number = []
            messages = []
            for m in check['rewards']: 
                level_reward, role_reward = m.split('¦')
                role = ctx.guild.get_role(int(role_reward))
                mes = f"{mes}> Level: `{level_reward}` for **{role.mention}**\n"
                k+=1
                l+=1
                if l == 10:
                    messages.append(mes)
                    embed = discord.Embed(title=f'{emojis.blade} Level Rewards', description=messages[i], color=color.color)
                    number.append(embed)
                    i+=1
                    mes = ""
                    l=0
            
            messages.append(mes)
            embed = discord.Embed(title=f'{emojis.blade} Level Rewards', description=messages[i], color=color.color)
            number.append(embed)

            if len(number) > 1:
                paginator = pg.Paginator(self.client, number, ctx, invoker=ctx.author.id)
                paginator.add_button('prev', emoji= "<:left_arrow:1111012825511493764>")
                paginator.add_button('delete', emoji = "<:fail:963149868698837062>")
                paginator.add_button('next', emoji="<:right_arrow:1111012858071875594>")
                await paginator.start()  
            else:
                await ctx.send(embed=embed)

    @levelconfig.command(brief='clear the level config')
    @commands.has_guild_permissions(manage_guild=True)
    @blacklist_check()
    async def clear(self, ctx):
        if not config.find_one({"_id": ctx.message.guild.id}):
            lvlconfig = {"_id": ctx.message.guild.id, "level": False, "mention": False, "channel": 0, "rewards": [], "blacklist": [], "level_message": '> 🎉 {member.mention} just leveled up to **Level {level}** 🎉'}
            config.insert_one(lvlconfig)

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
                for x in collection.find({"server": ctx.guild.id}):
                    collection.delete_one({"user": x['user'], "server": ctx.guild.id})

                collection.delete_one({"_id": ctx.message.guild.id})
                config.delete_one({"_id": ctx.message.guild.id})
                embed = discord.Embed(description=f'> {emojis.true} You cleared the **Level** config', color=color.success)
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
                embed = discord.Embed(description=f'> {emojis.true} Your **Level** hasnt been **Cleared**', color=color.success)
                await interaction.response.edit_message(embed=embed, view=view)

        accept.callback = accept_callback
        decline.callback = decline_callback

        view = discord.ui.View()
        view.add_item(item=accept)
        view.add_item(item=decline)

        embed = discord.Embed(description=f'> Are you sure to clear your **Level** config and the Servers XP?', color=color.color)
        await ctx.send(embed=embed, view=view)

    @levelconfig.command(brief='see all blacklisted channels')
    @commands.has_guild_permissions(manage_guild=True)
    @blacklist_check()
    async def list(self, ctx):
        if not config.find_one({"_id": ctx.message.guild.id}):
            lvlconfig = {"_id": ctx.message.guild.id, "level": False, "mention": False, "channel": 0, "rewards": [], "blacklist": [], "level_message": '> 🎉 {member.mention} just leveled up to **Level {level}** 🎉'}
            config.insert_one(lvlconfig)

        check = config.find_one({"_id": ctx.message.guild.id})
        px = functions.get_prefix(ctx)

        embed = discord.Embed(title=f'{emojis.blade} Level', color=color.color,
        description=f'{emojis.reply} *blacklisted channels* \n \n')

        if check['blacklist'] != []:
            for i in check['blacklist']:
                channel = self.client.get_channel(i)
                embed.description += f"> {channel.mention} | `{i}`\n"
        else:
            embed.description += f"> {emojis.false} *no blacklisted channels*"

        await ctx.send(embed=embed)

    @levelconfig.command(aliases=['bl'], brief='blacklist a channel')
    @commands.has_guild_permissions(manage_guild=True)
    @blacklist_check()
    async def blacklist(self, ctx, channel: discord.TextChannel=None):
        if not config.find_one({"_id": ctx.message.guild.id}):
            lvlconfig = {"_id": ctx.message.guild.id, "level": False, "mention": False, "channel": 0, "rewards": [], "blacklist": [], "level_message": '> 🎉 {member.mention} just leveled up to **Level {level}** 🎉'}
            config.insert_one(lvlconfig)

        check = config.find_one({"_id": ctx.message.guild.id})
        px = functions.get_prefix(ctx)

        if channel == None:
            embed = discord.Embed(title=f'{emojis.blade} Level', color=color.color,
            description=f'{emojis.reply} *blacklist a channel from leveling*')
            embed.add_field(name=f"{emojis.commands} Command:", value=f"> ``{px}levelconfig blacklist [#channel]`` blacklist a channel from leveling", inline=False)
            embed.add_field(name=f"{emojis.aliases} Alias:", value=f"```bl```", inline=False)
            await ctx.send(embed=embed)

        else:
            if channel.id in check['blacklist']:
                embed = discord.Embed(description=f'> {emojis.false} The Channel {channel.mention} is already in the Level **Blacklist**', color=color.fail)
                await ctx.send(embed=embed)

            else:
                config.update_one({"_id": ctx.message.guild.id}, {"$push": {"blacklist": channel.id}})
                embed = discord.Embed(description=f'> {emojis.true} The Channel {channel.mention} is now **Blacklisted** from Leveling', color=color.success)
                await ctx.send(embed=embed)

    @levelconfig.command(aliases=['ubl'], brief='unblacklist a channel')
    @commands.has_guild_permissions(manage_guild=True)
    @blacklist_check()
    async def unblacklist(self, ctx, channel: discord.TextChannel=None):
        if not config.find_one({"_id": ctx.message.guild.id}):
            lvlconfig = {"_id": ctx.message.guild.id, "level": False, "mention": False, "channel": 0, "rewards": [], "blacklist": [], "level_message": '> 🎉 {member.mention} just leveled up to **Level {level}** 🎉'}
            config.insert_one(lvlconfig)

        check = config.find_one({"_id": ctx.message.guild.id})
        px = functions.get_prefix(ctx)

        if channel == None:
            embed = discord.Embed(title=f'{emojis.blade} Level', color=color.color,
            description=f'{emojis.reply} *unblacklist a channel from leveling*')
            embed.add_field(name=f"{emojis.commands} Command:", value=f"> ``{px}levelconfig unblacklist [#channel]`` blacklist a channel from leveling", inline=False)
            embed.add_field(name=f"{emojis.aliases} Alias:", value=f"```ubl```", inline=False)
            await ctx.send(embed=embed)
        else:
            if channel.id not in check['blacklist']:
                embed = discord.Embed(description=f'> {emojis.false} The Channel {channel.mention} is not in the Level **Blacklist**')
                await ctx.send(embed=embed)

            else:
                config.update_one({"_id": ctx.message.guild.id}, {"$pull": {"blacklist": channel.id}})
                embed = discord.Embed(description=f'> {emojis.true} The Channel {channel.mention} is now **Unblacklisted** from Leveling')
                await ctx.send(embed=embed)

    @levelconfig.command(brief='set the level up message')
    @commands.has_guild_permissions(manage_guild=True)
    @blacklist_check()
    async def message(self, ctx, *, message=None):
        if not config.find_one({"_id": ctx.message.guild.id}):
            lvlconfig = {"_id": ctx.message.guild.id, "level": False, "mention": False, "channel": 0, "rewards": [], "blacklist": [], "level_message": '> 🎉 {member.mention} just leveled up to **Level {level}** 🎉'}
            config.insert_one(lvlconfig)

        check = config.find_one({"_id": ctx.message.guild.id})
        px = functions.get_prefix(ctx)

        if message == None:
            check2 = collection.find_one({"user": ctx.message.author.id, "server": ctx.message.guild.id})
            level_message = check['level_message']
            level_message = level_message.replace("{level}","%s" % (check2['level']))
            level_message = level_message.replace("{xp}","%s" % (check2['xp']))
            level_message = level_message.replace("{member.id}","%s" % (ctx.author.id))
            level_message = level_message.replace("{member.name}","%s" % (ctx.author.name))
            level_message = level_message.replace("{member.mention}","%s" % (ctx.author.mention))
            level_message = level_message.replace("{member.tag}","%s" % (ctx.author.discriminator))
            level_message = level_message.replace("{server.name}","%s" % (ctx.guild.name))
            level_message = level_message.replace("{server.id}","%s" % (ctx.guild.id))

            embed = discord.Embed(title=f'{emojis.blade} Level', color=color.color,
            description=f'{emojis.reply} *set the level up announcement message*')
            embed.add_field(name=f"{emojis.commands} Command:", value=f"> ``{px}levelconfig message [message]`` set your Leveling message", inline=False)
            embed.add_field(name=f"{emojis.config} Variables:", value="> ``{level}`` the level they got \n> ``{xp}`` display they current xp \n> ``{member.mention}`` mentions the member \n> ``{member.name}`` shows the members name \n> ``{member.tag}`` shows the members tag \n> ``{member.id}`` shows members id \n> ``{server.name}`` shows the name of the server \n> ``{server.id}`` shows the id of the server", inline=False)
            embed.add_field(name=f"{emojis.config} Current Message:", value=f"{level_message}", inline=False)
            await ctx.send(embed=embed)

        else:
            config.update_one({"_id": ctx.message.guild.id}, {"$set": {"level_message": message}})
            embed = discord.Embed(description=f'> {emojis.true} You set the **Level Up** announce **Message** to: \n {message}', color=color.success)
            await ctx.send(embed=embed)

    @levelconfig.command(brief='set the level announce channel')
    @commands.has_guild_permissions(manage_guild=True)
    @blacklist_check()
    async def channel(self, ctx, channel: discord.TextChannel=None):
        if not config.find_one({"_id": ctx.message.guild.id}):
            lvlconfig = {"_id": ctx.message.guild.id, "level": False, "mention": False, "channel": 0, "rewards": [], "blacklist": [], "level_message": '> 🎉 {member.mention} just leveled up to **Level {level}** 🎉'}
            config.insert_one(lvlconfig)

        check = config.find_one({"_id": ctx.message.guild.id})
        px = functions.get_prefix(ctx)

        if channel == None:
            embed = discord.Embed(title=f'{emojis.blade} Level', color=color.color,
            description=f'{emojis.reply} *set the level up announcement channel*')
            embed.add_field(name=f"{emojis.commands} Command:", value=f"> ``{px}levelconfig channel [#channel]`` set your Level Up announce channel", inline=False)
            await ctx.send(embed=embed)

        else:
            config.update_one({"_id": ctx.message.guild.id}, {"$set": {"channel": channel.id}})
            embed = discord.Embed(description=f'> {emojis.true} You set the **Level Up Announce** channel as {channel.mention}', color=color.success)
            await ctx.send(embed=embed)

    @levelconfig.command(brief='turn mentioning on or off')
    @commands.has_guild_permissions(manage_guild=True)
    @blacklist_check()
    async def mention(self, ctx, turn=None):
        if not config.find_one({"_id": ctx.message.guild.id}):
            lvlconfig = {"_id": ctx.message.guild.id, "level": False, "mention": False, "channel": 0, "rewards": [], "blacklist": [], "level_message": '> 🎉 {member.mention} just leveled up to **Level {level}** 🎉'}
            config.insert_one(lvlconfig)

        check = config.find_one({"_id": ctx.message.guild.id})
        px = functions.get_prefix(ctx)

        if turn == None:
            embed = discord.Embed(title=f'{emojis.blade} Level', color=color.color,
            description=f'{emojis.reply} *set mentioning the user on or off*')
            embed.add_field(name=f"{emojis.commands} Command:", value=f"> ``{px}levelconfig mention [on/off]`` activate or deactive the mentioning of the user", inline=False)
            embed.add_field(name=f"{emojis.config} Variables for Channel:", value=f"``tag a channel`` if you tag a channel, the level up message will send in the channel u set \n ``member_channel`` the message will be send in the current channel the member is in", inline=False)
            await ctx.send(embed=embed)

        if turn == 'on' or turn == 'true':
            if check['mention'] == True:
                embed = discord.Embed(description=f'> {emojis.false} The **Mentioning** of the **Levelling member** is already **activated**', color=color.fail)
                await ctx.send(embed=embed)
            else:
                config.update_one({"_id": ctx.message.guild.id}, {"$set": {"mention": True}})
                embed = discord.Embed(description=f'> {emojis.true} You **activated** the **Mentioning** of the **Levelling member** ', color=color.success)
                await ctx.send(embed=embed)

        elif turn == 'off' or turn == 'false':
            if check['mention'] == False:
                embed = discord.Embed(description=f'> {emojis.false} The **Mentioning** of the **Levelling member** is not **activated**', color=color.fail)
                await ctx.send(embed=embed)
            else:
                config.update_one({"_id": ctx.message.guild.id}, {"$set": {"mention": True}})
                embed = discord.Embed(description=f'> {emojis.true} You **deactivated** the **Mentioning** of the **Levelling member** ', color=color.success)
                await ctx.send(embed=embed)

        else:
            embed = discord.Embed(description=f'> {emojis.true} You cant set **Mentioning** to ``{turn}``, use ``on`` or ``off``', color=color.fail)
            await ctx.send(embed=embed)

    @levelconfig.command(brief="resets a members level and xp")
    @commands.has_guild_permissions(manage_guild=True)
    @blacklist_check()
    async def reset(self, ctx, member: discord.Member):
        if not config.find_one({"_id": ctx.message.guild.id}):
            lvlconfig = {"_id": ctx.message.guild.id, "level": False, "mention": False, "channel": 0, "rewards": [], "blacklist": [], "level_message": '> 🎉 {member.mention} just leveled up to **Level {level}** 🎉'}
            config.insert_one(lvlconfig)

        check = config.find_one({"_id": ctx.message.guild.id})

        if collection.find_one({"user": member.id, "server": ctx.message.guild.id}):
            collection.delete_one({"user": member.id, "server": ctx.message.guild.id})
            embed = discord.Embed(description=f"> {emojis.true} **Succesfully** resetted {member.mention} progress")
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(description=f"> {emojis.false} {member.mention} has no progress")
            await ctx.send(embed=embed)

    @levelconfig.command(brief='turn level on or off')
    @commands.has_guild_permissions(manage_guild=True)
    @blacklist_check()
    async def set(self, ctx, turn=None):
        if not config.find_one({"_id": ctx.message.guild.id}):
            lvlconfig = {"_id": ctx.message.guild.id, "level": False, "mention": False, "channel": 0, "rewards": [], "blacklist": [], "level_message": '> 🎉 {member.mention} just leveled up to **Level {level}** 🎉'}
            config.insert_one(lvlconfig)

        check = config.find_one({"_id": ctx.message.guild.id})
        px = functions.get_prefix(ctx)

        if turn == None:
            embed = discord.Embed(title=f'{emojis.blade} Level', color=color.color,
            description=f'{emojis.reply} *turn the leveling on or off*')
            embed.add_field(name=f"{emojis.commands} Command:", value=f"> ``{px}levelconfig set [on/off]`` set your Leveling on or off", inline=False)
            await ctx.send(embed=embed)

        if turn == 'on' or turn == 'true':
            if check['level'] == True:
                embed = discord.Embed(description=f'> {emojis.false} **Leveling** is already **activated**', color=color.fail)
                await ctx.send(embed=embed)
            else:
                config.update_one({"_id": ctx.message.guild.id}, {"$set": {"level": True}})
                embed = discord.Embed(description=f'> {emojis.true} You **activated** **Leveling**', color=color.success)
                await ctx.send(embed=embed)

        elif turn == 'off' or turn == 'false':
            if check['level'] == False:
                embed = discord.Embed(description=f'> {emojis.false} **Leveling** is not **activated**', color=color.fail)
                await ctx.send(embed=embed)
            else:
                config.update_one({"_id": ctx.message.guild.id}, {"$set": {"level": False}})
                embed = discord.Embed(description=f'> {emojis.true} You **deactivated** **Leveling**', color=color.success)
                await ctx.send(embed=embed)

        else:
            embed = discord.Embed(description=f'> {emojis.false} You cant set **Leveling** to ``{turn}``', color=color.fail)
            await ctx.send(embed=embed)

async def setup(client):
    await client.add_cog(level(client))
