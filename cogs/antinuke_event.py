import discord
import asyncio
import pymongo
import datetime
from pymongo import MongoClient
from discord.ext import commands
from discord import Embed
from utils import functions
from utils.emojis import emojis
from utils.color import color

cluster = MongoClient('no')
db = cluster["blade"]
collection = db["antinuke"]

class antinuke_event(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_guild_role_delete(self, role):
        if not collection.find_one({"_id": role.guild.id}):
            return
        
        else:
            check = collection.find_one({"_id": role.guild.id})
            try:
                if check["antinuke"] == True:
                    channel_message = self.client.get_channel(check["logs"])
                    async for i in role.guild.audit_logs(limit=1, after=datetime.datetime.now() - datetime.timedelta(minutes = 2), action=discord.AuditLogAction.role_delete):

                        if i.user.id not in check['whitelisted']:
                            reason = "antinuke ; banning member"

                            if check["punishment"] == 'ban':
                                await i.user.ban(reason=reason)
                                punishment = 'ban'

                            if check["punishment"] == 'kick':
                                await i.user.kick(reason=reason)
                                punishment = 'kick'

                            embed = discord.Embed(title=f'{emojis.blade} AntiNuke', color=color.color,
                            description=f'{emojis.reply} **Event**: deleted a role')
                            embed.add_field(name=f"{emojis.dash} Member", value=f"{emojis.reply} {i.user.mention} ``{i.user.name}`` | ``{i.user.id}``", inline=False)
                            embed.add_field(name=f"{emojis.dash} Case:", value=f"{emojis.reply} **Deleted**: {role.name} | ``{role.id}``", inline=False)
                            embed.add_field(name=f"{emojis.dash} Punishment:", value=f"{emojis.reply} ``{punishment}``", inline=False)
                            await channel_message.send(embed=embed)
                    else:
                        return
            except Exception as e:
                print(e)

    @commands.Cog.listener()
    async def on_guild_role_create(self, role):
        if not collection.find_one({"_id": role.guild.id}):
            return
        
        else:
            check = collection.find_one({"_id": role.guild.id})
            try:
                if check["antinuke"] == True:
                    channel_message = self.client.get_channel(check["logs"])
                    async for i in role.guild.audit_logs(limit=1, after=datetime.datetime.now() - datetime.timedelta(minutes = 2), action=discord.AuditLogAction.role_create):

                        if i.user.id not in check['whitelisted']:
                            reason = "antinuke ; banning member"

                            if check["punishment"] == 'ban':
                                await i.user.ban(reason=reason)
                                punishment = 'ban'

                            if check["punishment"] == 'kick':
                                await i.user.kick(reason=reason)
                                punishment = 'kick'

                            embed = discord.Embed(title=f'{emojis.blade} AntiNuke', color=color.color,
                            description=f'{emojis.reply} **Event**: created a role')
                            embed.add_field(name=f"{emojis.dash} Member", value=f"{emojis.reply} {i.user.mention} ``{i.user.name}`` | ``{i.user.id}``", inline=False)
                            embed.add_field(name=f"{emojis.dash} Case:", value=f"{emojis.reply} **Created**: {role.name} | ``{role.id}``", inline=False)
                            embed.add_field(name=f"{emojis.dash} Punishment:", value=f"{emojis.reply} ``{punishment}``", inline=False)
                            await channel_message.send(embed=embed)

                            await role.delete()
                    else:
                        return
            except Exception as e:
                print(e)

    @commands.Cog.listener()
    async def on_member_ban(self, guild, member):
        if not collection.find_one({"_id": guild.id}):
            return
        
        else:
            check = collection.find_one({"_id": guild.id})
            try:
                if check["antinuke"] == True:
                    channel_message = self.client.get_channel(check["logs"])
                    async for i in guild.audit_logs(limit=1, after=datetime.datetime.now() - datetime.timedelta(minutes = 2), action=discord.AuditLogAction.ban):

                        if i.user.id not in check['whitelisted']:
                            reason = "antinuke ; banning member"

                            if check["punishment"] == 'ban':
                                await i.user.ban(reason=reason)
                                punishment = 'ban'

                            if check["punishment"] == 'kick':
                                await i.user.kick(reason=reason)
                                punishment = 'kick'

                            embed = discord.Embed(title=f'{emojis.blade} AntiNuke', color=color.color,
                            description=f'{emojis.reply} **Event**: banned a member')
                            embed.add_field(name=f"{emojis.dash} Member", value=f"{emojis.reply} {i.user.mention} ``{i.user.name}`` | ``{i.user.id}``", inline=False)
                            embed.add_field(name=f"{emojis.dash} Case:", value=f"{emojis.reply} **Banned**: {member} | ``{member.id}``", inline=False)
                            embed.add_field(name=f"{emojis.dash} Punishment:", value=f"{emojis.reply} ``{punishment}``", inline=False)
                            await channel_message.send(embed=embed)
                            await member.unban()
                    else:
                        return
            except:
                pass

    @commands.Cog.listener()
    async def on_member_remove(self, member):
            if not collection.find_one({"_id": member.guild.id}):
                pass

            try:
                check = collection.find_one({"_id": member.guild.id})

                if check["antinuke"] == True:
                    channel_message = self.client.get_channel(check["logs"])
                    async for i in member.guild.audit_logs(limit=1, after=datetime.datetime.now() - datetime.timedelta(minutes = 2), action=discord.AuditLogAction.kick):
                        if i.user.id not in check['whitelisted']:
                            if i.target.id == member.id:
                                reason = "antinuke ; kicking members"

                                if check["punishment"] == 'ban':
                                    await i.user.ban(reason=reason)
                                    punishment = 'ban'

                                if check["punishment"] == 'kick':
                                    await i.user.kick(reason=reason)
                                    punishment = 'kick'

                                embed = discord.Embed(title=f'{emojis.blade} AntiNuke', color=color.color,
                                description=f'{emojis.reply} **Event**: kicking a member')
                                embed.add_field(name=f"{emojis.dash} Member", value=f"{emojis.reply} {i.user.mention} ``{i.user.name}`` | ``{i.user.id}``", inline=False)
                                embed.add_field(name=f"{emojis.dash} Case:", value=f"{emojis.reply} **Kicked**: {member} | ``{member.id}``", inline=False)
                                embed.add_field(name=f"{emojis.dash} Punishment:", value=f"{emojis.reply} ``{punishment}``", inline=False)
                                await channel_message.send(embed=embed)
                    else:
                        return
            except:
                pass

    @commands.Cog.listener()
    async def on_guild_channel_create(self, channel):
        if not collection.find_one({"_id": channel.guild.id}):
            return
            
        try:
            guild = channel.guild
            check = collection.find_one({"_id": guild.id})

            if check["antinuke"] == True:
                channel_message = self.client.get_channel(check["logs"])
                async for i in guild.audit_logs(limit=1, after=datetime.datetime.now() - datetime.timedelta(minutes = 2), action=discord.AuditLogAction.channel_create):

                    if i.user.id not in check['whitelisted']:
                        reason = "antinuke ; creating channels"

                        if check["punishment"] == 'ban':
                            await i.user.ban(reason=reason)
                            punishment = 'ban'

                        if check["punishment"] == 'kick':
                            await i.user.kick(reason=reason)
                            punishment = 'kick'

                        embed = discord.Embed(title=f"{emojis.blade} AntiNuke", color=color.color,
                        description=f'{emojis.reply} **Event**: a member created a channel')
                        embed.add_field(name=f"{emojis.dash} Member:", value=f"{emojis.reply} {i.user.mention} | ``{i.user.name}`` | ``{i.user.id}``", inline=False)
                        embed.add_field(name=f"{emojis.dash} Case:", value=f"{emojis.reply} **Created**: {channel.mention} | ``{channel.name}`` | ``{channel.id}``", inline=False)
                        embed.add_field(name=f"{emojis.dash} Punishment:", value=f"{emojis.reply} ``{punishment}``", inline=False)
                        await channel_message.send(embed=embed)
                        await channel.delete()
        except:
            pass

    @commands.Cog.listener()
    async def on_guild_channel_delete(self, channel):
        if not collection.find_one({"_id": channel.guild.id}):
            return

        try:
            guild = channel.guild
            check = collection.find_one({"_id": guild.id})

            if check["antinuke"] == True:
                channel_message = self.client.get_channel(check["logs"])
                async for i in guild.audit_logs(limit=1, after=datetime.datetime.now() - datetime.timedelta(minutes = 2), action=discord.AuditLogAction.channel_delete):
                    if i.user.id not in check['whitelisted']:
                        reason = "antinuke ; deleting channels"

                        if check["punishment"] == 'ban':
                            await i.user.ban(reason=reason)
                            punishment = 'ban'

                        if check["punishment"] == 'kick':
                            await i.user.kick(reason=reason)
                            punishment = 'kick'

                        embed = discord.Embed(title=f"{emojis.blade} AntiNuke", color=color.color,
                        description=f'{emojis.reply} **Event**: a member deleted a channel')
                        embed.add_field(name=f"{emojis.dash} Member:", value=f"{emojis.reply} {i.user.mention} | ``{i.user.name}`` | ``{i.user.id}``", inline=False)
                        embed.add_field(name=f"{emojis.dash} Case:", value=f"{emojis.reply} **Deleted**: {channel.mention} | ``{channel.name}`` | ``{channel.id}``", inline=False)
                        embed.add_field(name=f"{emojis.dash} Punishment:", value=f"{emojis.reply} ``{punishment}``", inline=False)
                        await channel_message.send(embed=embed)
                            
                    else:
                        return  
        except:
            pass

async def setup(client):
    await client.add_cog(antinuke_event(client))
