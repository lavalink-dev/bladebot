import discord
import pymongo
import asyncio
import datetime
from pymongo import MongoClient
from discord.ext import commands
from utils import functions
from utils.emojis import emojis
from utils.color import color

cluster = MongoClient('no')
db = cluster["blade"]
collection = db["logger"]

class logger_event(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        try:
            if collection.find_one({"_id": message.guild.id}):
                check = collection.find_one({"_id": message.guild.id})
                if check["logger"] == True:
                    if message.author.id in check["whitelist"]:
                        return
                    else:
                        channel = self.client.get_channel(check["channel"])
                        embed = discord.Embed(title=f"{emojis.blade} Logger", color=color.color,
                        description=f'{emojis.reply} **Event**: a message got deleted')
                        embed.add_field(name=f'{emojis.dash} Member:', value=f'{emojis.reply} {message.author.mention} | ``{message.author}`` | ``{message.author.id}``', inline=False)
                        embed.add_field(name=f'{emojis.dash} Message:', value=f'```{message.content} ```', inline=False)
                        embed.add_field(name=f'{emojis.dash} Channel:', value=f'{emojis.reply} {message.channel.mention} | ``{message.channel.id}``', inline=False)
                        try:
                            await channel.send(embed=embed)
                        except:
                            pass
            else:
                return
        except:
            pass

        await asyncio.sleep(4)

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        try:
            if collection.find_one({"_id": before.guild.id}):
                check = collection.find_one({"_id": before.guild.id})
                if check["logger"] == True:
                    if before.author.id in check["whitelist"]:
                        return
                    else:
                        channel = self.client.get_channel(check["channel"])
                        embed = discord.Embed(title=f"{emojis.blade} Logger", color=color.color,
                        description=f'{emojis.reply} **Event**: a message got edited')
                        embed.add_field(name=f'{emojis.dash} Member:', value=f'{emojis.reply} {before.author.mention} | ``{before.author}`` | ``{before.author.id}``', inline=False)
                        embed.add_field(name=f"{emojis.dash} Before:", value=f'```{before.content}```', inline=True)
                        embed.add_field(name=f"{emojis.dash} After:", value=f'```{after.content}```', inline=True)
                        embed.add_field(name=f'{emojis.dash} Channel:', value=f'{emojis.reply} {before.channel.mention} | ``{before.channel.id}``', inline=False)
                        try:
                            await channel.send(embed=embed)
                        except:
                            pass
            else:
                return
        except:
            pass

        await asyncio.sleep(4)

    @commands.Cog.listener()
    async def on_member_ban(self, guild, member):
        try:
            if collection.find_one({"_id": member.guild.id}):
                check = collection.find_one({"_id": member.guild.id})
                if check["logger"] == True:
                    channel_message = self.client.get_channel(check["channel"])
                    async for i in guild.audit_logs( limit=1, after=datetime.datetime.now() - datetime.timedelta(minutes = 2), action=discord.AuditLogAction.ban):

                        if i.user.id in check["whitelist"]:
                            return
                        else:
                            embed = discord.Embed(title=f"{emojis.blade} Logger", color=color.color,
                            description=f'{emojis.reply} **Event**: a member has been banned')
                            embed.add_field(name=f"{emojis.dash} Member:", value=f"{emojis.reply} {i.user.mention} | ``{i.user.name}`` | ``{i.user.id}``", inline=False)
                            embed.add_field(name=f"{emojis.dash} Case:", value=f"{emojis.reply} **Banned**: {member} | ``{member.id}``", inline=False)
                            try:
                                await channel_message.send(embed=embed)
                            except:
                                pass
            else:
                return
        except:
            pass

        await asyncio.sleep(4)

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        try:
            if collection.find_one({"_id": member.guild.id}):
                check = collection.find_one({"_id": member.guild.id})
                if check["logger"] == True:
                    channel_message = self.client.get_channel(check["channel"])
                    async for i in member.guild.audit_logs(limit=1, after=datetime.datetime.now() - datetime.timedelta(minutes = 2), action=discord.AuditLogAction.kick):
                        if i.user.id in check["whitelist"]:
                            return
                        else:
                            if i.target.id == member.id:
                                embed = discord.Embed(title=f"{emojis.blade} Logger", color=color.color,
                                description=f'{emojis.reply} **Event**: a member has been kicked')
                                embed.add_field(name=f"{emojis.dash} Member:", value=f"{emojis.reply} {i.user.mention} | ``{i.user.name}`` | ``{i.user.id}``", inline=False)
                                embed.add_field(name=f"{emojis.dash} Case:", value=f"{emojis.reply} **Kicked**: {member} | ``{member.id}``", inline=False)
                                try:
                                    await channel_message.send(embed=embed)
                                except:
                                    pass
            else:
                return
        except:
            pass

        await asyncio.sleep(4)

    @commands.Cog.listener()
    async def on_guild_channel_create(self, channel):
        try:
            guild = channel.guild
            if collection.find_one({"_id": channel.guild.id}):
                check = collection.find_one({"_id": channel.guild.id})
                if check["logger"] == True:
                    channel_message = self.client.get_channel(check["channel"])
                    async for i in guild.audit_logs(limit=1, after=datetime.datetime.now() - datetime.timedelta(minutes = 2), action=discord.AuditLogAction.channel_create):
                        if i.user.id in check["whitelist"]:
                            return
                        else:
                            try:
                                embed = discord.Embed(title=f"{emojis.blade} Logger", color=color.color,
                                description=f'{emojis.reply} **Event**: a member created a channel')
                                embed.add_field(name=f"{emojis.dash} Member:", value=f"{emojis.reply} {i.user.mention} | ``{i.user.name}`` | ``{i.user.id}``", inline=False)
                                embed.add_field(name=f"{emojis.dash} Case:", value=f"{emojis.reply} **Created**: {channel.mention} | ``{channel.name}`` | ``{channel.id}``", inline=False)
                                await channel_message.send(embed=embed)
                            except:
                                pass
            else:
                return
        except:
            pass

        await asyncio.sleep(4)

    @commands.Cog.listener()
    async def on_guild_channel_delete(self, channel):
        try:
            guild = channel.guild
            if collection.find_one({"_id": channel.guild.id}):
                check = collection.find_one({"_id": channel.guild.id})
                if check["logger"] == True:
                    channel_message = self.client.get_channel(check["channel"])
                    async for i in guild.audit_logs(limit=1, after=datetime.datetime.now() - datetime.timedelta(minutes = 2), action=discord.AuditLogAction.channel_delete):
                        if i.user.id in check["whitelist"]:
                            return
                        else:
                            try:
                                embed = discord.Embed(title=f"{emojis.blade} Logger", color=color.color,
                                description=f'{emojis.reply} **Event**: a member deleted a channel')
                                embed.add_field(name=f"{emojis.dash} Member:", value=f"{emojis.reply} {i.user.mention} | ``{i.user.name}`` | ``{i.user.id}``", inline=False)
                                embed.add_field(name=f"{emojis.dash} Case:", value=f"{emojis.reply} **Deleted**: {channel.mention} | ``{channel.name}`` | ``{channel.id}``", inline=False)
                                await channel_message.send(embed=embed)
                            except:
                                pass
            else:
                return
        except:
            pass

        await asyncio.sleep(4)

    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        try:
            if collection.find_one({"_id": before.guild.id}):
                check = collection.find_one({"_id": before.guild.id})
                if check["logger"] == True:
                    if before.id in check["whitelist"]:
                        return
                    else:
                        channel_message = self.client.get_channel(check["channel"])
                        if len(before.roles) > len(after.roles):
                            role = next(role for role in before.roles if role not in after.roles)
                            embed = discord.Embed(title=f"{emojis.blade} Logger", color=color.color,
                            description=f'{emojis.reply} **Event**: member removed a role')
                            embed.add_field(name=f"{emojis.dash} Member:", value=f"{emojis.reply} {before.mention} | ``{before.name}`` | ``{before.id}``", inline=False)
                            embed.add_field(name=f"{emojis.dash} Case:", value=f"{emojis.reply} **Removed**: {role.mention} | ``{role.name}`` | ``{role.id}``", inline=False)

                        elif len(after.roles) > len(before.roles):
                            role = next(role for role in after.roles if role not in before.roles)
                            embed = discord.Embed(title=f"{emojis.blade} Logger", color=color.color,
                            description=f'{emojis.reply} **Event**: member added a role')
                            embed.add_field(name=f"{emojis.dash} Member:", value=f"{emojis.reply} {before.mention} | ``{before.name}`` | ``{before.id}``", inline=False)
                            embed.add_field(name=f"{emojis.dash} Case:", value=f"{emojis.reply} **Added**: {role.mention} | ``{role.name}`` | ``{role.id}``", inline=False)

                        elif before.nick != after.nick:
                            embed = discord.Embed(title=f"{emojis.blade} Logger", color=color.color,
                            description=f'{emojis.reply} **Event**: member has changed his nickname')
                            if before.nick == None:
                                before.nick = f'{before.name} (real name)'
                            if after.nick == None:
                                after.nick = f'{before.name} (real name)'

                            embed.add_field(name=f"{emojis.dash} Member:", value=f"{emojis.reply} {before.mention} | ``{before.name}`` | ``{before.id}``", inline=False)
                            embed.add_field(name=f"{emojis.dash} Before:", value=f'```{before.nick}```', inline=True)
                            embed.add_field(name=f"{emojis.dash} After:", value=f'```{after.nick}```', inline=True)
                    try:
                        await channel_message.send(embed=embed)
                    except Exception as e:
                        pass
            else:
                return
        except Exception as e:
            pass

        await asyncio.sleep(4)
    
    @commands.Cog.listener()
    async def on_invite_create(self, invite):
        try:
            if collection.find_one({"_id": invite.guild.id}):
                check = collection.find_one({"_id": invite.guild.id})
                if check["logger"] == True:
                    if invite.inviter.id in check["whitelist"]:
                        return
                    else:
                        channel_message = self.client.get_channel(check["channel"])
                        embed = discord.Embed(title=f"{emojis.blade} Logger", color=color.color,
                        description=f'{emojis.reply} **Event**: an invite has been created')
                        embed.add_field(name=f"{emojis.dash} Member:", value=f"{emojis.reply} {invite.inviter.mention} | ``{invite.inviter.name}`` | ``{invite.inviter.id}``", inline=False)
                        embed.add_field(name=f"{emojis.dash} Case:", value=f"{emojis.reply2} **Created**: {invite} | ``{invite.id}`` \n {emojis.reply} **Channel:** {invite.channel.mention} | ``{invite.channel.name}`` | ``{invite.channel.id}``", inline=False)
                        await channel_message.send(embed=embed)

            else:
                return
        except Exception as e:
            pass

        await asyncio.sleep(4)

async def setup(client):
    await client.add_cog(logger_event(client))
