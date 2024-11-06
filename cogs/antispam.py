import discord
import datetime
import pymongo
import asyncio
from pymongo import MongoClient
from datetime import timedelta
from discord.ext import commands
from utils import functions
from utils.emojis import emojis
from utils.color import color 

cluster = MongoClient('mongodb+srv://blade:lolidkbruh12333333333@cluster0.wbxaj.mongodb.net/myFirstDatabase?retryWrites=true&w=majority')
db = cluster["blade"]
collection = db["antispam"]
warn_collection = db["warn"]
blacklist = db["blacklist"]

def blacklist_check():
    def predicate(ctx):
        if blacklist.find_one({'_id': ctx.author.id}):
            return False
        return True
    return commands.check(predicate)

whitelist = {"Wealthy"}

def custom_cooldown(ctx):
    roles = {role.name for role in ctx.author.roles}
    if not whitelist.isdisjoint(roles):
        return None
    elif "SomeOtherPrivelagedRole" in roles:
        #some other privileged role
        discord.app_commands.Cooldown(1, 180)
    else:
        #everyone else
        return discord.app_commands.Cooldown(1, 300)

class antispam(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.anti_spam = commands.CooldownMapping.from_cooldown(8, 15, commands.BucketType.member)
        self.too_many_violations = commands.CooldownMapping.from_cooldown(2, 60, commands.BucketType.member)

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot or not collection.find_one({"_id": message.guild.id}) or message.author.id == 1213465243708162048:
            return

        try:
            checks = collection.find_one({"_id": message.guild.id})

            if checks['antispam'] == True:
                warn_message = checks['warn_message']
                warn_message = warn_message.replace("{member.id}","%s" % (message.author.id))
                warn_message = warn_message.replace("{member.name}","%s" % (message.author.name))
                warn_message = warn_message.replace("{member.mention}","%s" % (message.author.mention))
                warn_message = warn_message.replace("{member.tag}","%s" % (message.author.discriminator))
                warn_message = warn_message.replace("{server.name}","%s" % (message.guild.name))
                warn_message = warn_message.replace("{server.id}","%s" % (message.guild.id))
                warn_message = warn_message.replace("{punishment}", f"{checks['punishment']}")

                punishment_message = checks['punishment_message']
                punishment_message = punishment_message.replace("{member.id}","%s" % (message.author.id))
                punishment_message = punishment_message.replace("{member.name}","%s" % (message.author.name))
                punishment_message = punishment_message.replace("{member.mention}","%s" % (message.author.mention))
                punishment_message = punishment_message.replace("{member.tag}","%s" % (message.author.discriminator))
                punishment_message = punishment_message.replace("{server.name}","%s" % (message.guild.name))
                punishment_message = punishment_message.replace("{server.id}","%s" % (message.guild.id))
                punishment_message = punishment_message.replace("{punishment}", f"{checks['punishment']}")

                if type(message.channel) is not discord.TextChannel or message.author.id in checks['whitelist']: 
                    return
                
                for i in collection.find_one({"_id": message.guild.id})["roles"]:
                    role = message.guild.get_role(i)
                    if role in message.author.roles:
                        return
                    else:
                        pass

                bucket = self.anti_spam.get_bucket(message)
                retry_after = bucket.update_rate_limit()

                if retry_after:
                    await message.delete()
                    embed = discord.Embed(description=f'{warn_message}', color=color.fail)
                    await message.channel.send(embed=embed, delete_after = 4)
                    violations = self.too_many_violations.get_bucket(message)
                    check = violations.update_rate_limit()

                    if check:
                        if checks['punishment'] == 'off':
                            return

                        if checks['punishment'] == 'timeout':
                            await message.author.timeout(timedelta(days = 1), reason='antispam ; Spamming')
                                    
                        if checks['punishment'] == 'kick':
                            await message.author.kick(reason='antispam ; Spamming')

                        if checks['punishment'] == 'ban':
                            await message.author.ban(reason='antispam ; Spamming')

                        if checks['punishment'] == 'warn':
                            if not warn_collection.find_one({"member": message.author.id, "server": message.guild.id}):
                                warning = {"member": message.author.id, "server": message.guild.id, "warn1": '', "warn2": '', "warn3": ''}
                                collection.insert_one(warning)

                                warn_check = warn_collection.find_one({"member": message.author.id, "server": message.guild.id})
                            if warn_check['warn1'] == '':
                                warn_collection.update_one({"member": message.author.id, "server": message.guild.id}, {"$set": {"warn1": f'Filter ; wrote a Filtered Word ¦ {self.client.user.id}'}})

                            elif warn_check['warn2'] == '':
                                warn_collection.update_one({"member": message.author.id, "server": message.guild.id}, {"$set": {"warn2": f'Filter ; wrote a Filtered Word ¦ {self.client.user.id}'}})

                            elif warn_check['warn3'] == '':
                                warn_collection.update_one({"member": message.author.id, "server": message.guild.id}, {"$set": {"warn3": f'Filter ; wrote a Filtered Word ¦ {self.client.user.id}'}})
                                                    
                            else:
                                await message.author.ban(reason='Warn ; To many Warns (banned due AntiSpam)')

                            embed = discord.Embed(description=f'{punishment_message}', color=color.fail)
                            await message.channel.send(embed=embed, delete_after = 4)
        except:
            pass

        await asyncio.sleep(1)

    @commands.group(pass_context=True, invoke_without_command=True, aliases=['as'], brief='deletes spam messages', description='config')
    @commands.has_guild_permissions(manage_messages=True)
    @blacklist_check()
    async def antispam(self, ctx):
        if not collection.find_one({"_id": ctx.message.guild.id}):
            antispamdb = {"_id": ctx.message.guild.id, "antispam": False, "punishment": 'timeout', "warn_message": '> <:fail:963149868698837062> Please dont **Spam** in here', "punishment_message": '> <:fail:963149868698837062> You have been **Timeouted** due **Spam**', "whitelist": []}
            collection.insert_one(antispamdb)
        await ctx.invoke()
        
    @antispam.command(brief='set the punishment')
    @commands.has_guild_permissions(manage_messages=True)
    @blacklist_check()
    async def punishment(self, ctx, punishment=None):
        if not collection.find_one({"_id": ctx.message.guild.id}):
            antispamdb = {"_id": ctx.message.guild.id, "antispam": False, "punishment": 'timeout', "warn_message": '> <:fail:963149868698837062> Please dont **Spam** in here', "punishment_message": '> <:fail:963149868698837062> You have been **Timeouted** due **Spam**', "whitelist": []}
            collection.insert_one(antispamdb)

        check = collection.find_one({"_id": ctx.message.guild.id})
        px = functions.get_prefix(ctx)

        if punishment == None:
            embed = discord.Embed(title=f'{emojis.blade} AntiSpam', color=color.color,
            description=f'{emojis.reply} *set the antispam messages*')
            embed.add_field(name=f"{emojis.commands} Command:", value=f"> ``{px}antispamconfig message [message]`` set your antispaming message", inline=False)
            embed.add_field(name=f"{emojis.config} Punishment:", value="> ``ban`` bans the member \n> ``kick`` kicks the member \n> ``timeout`` timeouts the member for 1 day \n> ``off`` no punishment", inline=False)
            embed.add_field(name=f"{emojis.config} Current Punishment:", value=f"> ``Punishment`` {check['punishment']}", inline=False)
            await ctx.send(embed=embed)

        else:
            if punishment == 'ban':
                collection.update_one({"_id": ctx.message.guild.id}, {"$set": {"punishment": 'ban'}})
                embed = discord.Embed(description=f'> {emojis.true} **Successfully** set the **Punishment** to: ``ban``', color=color.success)
                await ctx.send(embed=embed)

            elif punishment == 'kick':
                collection.update_one({"_id": ctx.message.guild.id}, {"$set": {"punishment": 'kick'}})
                embed = discord.Embed(description=f'> {emojis.true} **Successfully** set the **Punishment** to: ``kick``', color=color.success)
                await ctx.send(embed=embed)

            elif punishment == 'timeout':
                collection.update_one({"_id": ctx.message.guild.id}, {"$set": {"punishment": 'timeout'}})
                embed = discord.Embed(description=f'> {emojis.true} **Successfully** set the **Punishment** to: ``timeout``', color=color.success)
                await ctx.send(embed=embed)

            elif punishment == 'warn':
                collection.update_one({"_id": ctx.message.guild.id}, {"$set": {"punishment": 'warn'}})
                embed = discord.Embed(description=f'> {emojis.true} **Successfully** set the **Punishment** to: ``warn``', color=color.success)
                await ctx.send(embed=embed)

            elif punishment == 'off':
                collection.update_one({"_id": ctx.message.guild.id}, {"$set": {"punishment": 'warn'}})
                embed = discord.Embed(description=f'> {emojis.true} **Successfully** turned **off** the **Punishment**', color=color.success)
                await ctx.send(embed=embed)
            
            else:
                embed = discord.Embed(description=f'> {emojis.false} You cant set the **Punishment** to ``{function}``', color=color.fail)
                await ctx.send(embed=embed)


    @antispam.command(brief='set the messages')
    @commands.has_guild_permissions(manage_messages=True)
    @blacklist_check()
    async def message(self, ctx, function=None, *, message=None):
        if not collection.find_one({"_id": ctx.message.guild.id}):
            antispamdb = {"_id": ctx.message.guild.id, "antispam": False, "punishment": 'timeout', "warn_message": '> <:fail:963149868698837062> Please dont **Spam** in here', "punishment_message": '> <:fail:963149868698837062> You have been **{punishment}** due **Spam**', "whitelist": []}
            collection.insert_one(antispamdb)

        check = collection.find_one({"_id": ctx.message.guild.id})
        px = functions.get_prefix(ctx)

        warn_messages = check['warn_message']
        warn_messages = warn_messages.replace("{member.id}","%s" % (ctx.author.id))
        warn_messages = warn_messages.replace("{member.name}","%s" % (ctx.author.name))
        warn_messages = warn_messages.replace("{member.mention}","%s" % (ctx.author.mention))
        warn_messages = warn_messages.replace("{member.tag}","%s" % (ctx.author.discriminator))
        warn_messages = warn_messages.replace("{server.name}","%s" % (ctx.guild.name))
        warn_messages = warn_messages.replace("{server.id}","%s" % (ctx.guild.id))

        punishment_messages = check['punishment_message']
        punishment_messages = punishment_messages.replace("{member.id}","%s" % (ctx.author.id))
        punishment_messages = punishment_messages.replace("{member.name}","%s" % (ctx.author.name))
        punishment_messages = punishment_messages.replace("{member.mention}","%s" % (ctx.author.mention))
        punishment_messages = punishment_messages.replace("{member.tag}","%s" % (ctx.author.discriminator))
        punishment_messages = punishment_messages.replace("{server.name}","%s" % (ctx.guild.name))
        punishment_messages = punishment_messages.replace("{server.id}","%s" % (ctx.guild.id))

        if function == None and message == None:
            embed = discord.Embed(title=f'{emojis.blade} AntiSpam', color=color.color,
            description=f'{emojis.reply} *set the antispam messages*')
            embed.add_field(name=f"{emojis.commands} Command:", value=f"> ``{px}antispam message [warn/punishment] [message]`` set your antispaming message", inline=False)
            embed.add_field(name=f"{emojis.config} Variables:", value="> ``{member.mention}`` mentions the member \n> ``{member.name}`` shows the members name \n> ``{member.tag}`` shows the members tag \n> ``{member.id}`` shows members id \n> ``{server.name}`` shows the name of the server \n> ``{server.id}`` shows the id of the server \n> ``{punishment}`` show the punishment", inline=False)
            embed.add_field(name=f"{emojis.config} Current Messages:", value=f"> **Warn** \n {warn_messages} \n\n> **Punishment** \n {punishment_messages} ", inline=False)
            await ctx.send(embed=embed)

        else:
            if function == 'warn':
                if message == None:
                    embed = discord.Embed(description=f'> {emojis.false} You need to write something to set the **Message**', color=color.fail)
                    await ctx.send(embed=embed)
                else:
                    collection.update_one({"_id": ctx.message.guild.id}, {"$set": {"warn_message": message}})
                    embed = discord.Embed(description=f'> {emojis.true} You set the **Warn** message to: \n {message}', color=color.success)
                    await ctx.send(embed=embed)

            elif function == 'punishment':
                if message == None:
                    embed = discord.Embed(description=f'> {emojis.false} You need to write something to set the **Message**', color=color.fail)
                    await ctx.send(embed=embed)
                else:
                    collection.update_one({"_id": ctx.message.guild.id}, {"$set": {"punishment_message": message}})
                    embed = discord.Embed(description=f'> {emojis.true} You set the **Punishment** message to: \n {message}', color=color.success)
                    await ctx.send(embed=embed)

            else:
                embed = discord.Embed(description=f'> {emojis.false} You cant set ``{function}`` in the **Config**', color=color.fail)
                await ctx.send(embed=embed)

    @antispam.command(brief='turn it on or off')
    @commands.has_guild_permissions(manage_messages=True)
    @blacklist_check()
    async def set(self, ctx, turn=None):
        if not collection.find_one({"_id": ctx.message.guild.id}):
            antispamdb = {"_id": ctx.message.guild.id, "antispam": False, "punishment": 'timeout', "warn_message": '> <:fail:963149868698837062> Please dont **Spam** in here', "punishment_message": '> <:fail:963149868698837062> You have been **Timeouted** due **Spam**', "whitelist": []}
            collection.insert_one(antispamdb)

        check = collection.find_one({"_id": ctx.message.guild.id})
        px = functions.get_prefix(ctx)

        if turn == None:
            embed = discord.Embed(title=f'{emojis.blade} AntiSpam', color=color.success,
            description=f'{emojis.reply} *turn the antispam on or off*')
            embed.add_field(name=f"{emojis.commands} Command:", value=f"> ``{px}antispam set [on/off]`` set antispam on or off", inline=False)
            await ctx.send(embed=embed)

        if turn == 'on' or turn == 'true':
            if check['antispam'] == True:
                embed = discord.Embed(description=f'> {emojis.false} **AntiSpam** is already **activated**', color=color.fail)
                await ctx.send(embed=embed)
            else:
                collection.update_one({"_id": ctx.message.guild.id}, {"$set": {"antispam": True}})
                embed = discord.Embed(description=f'> {emojis.true} **AntiSpam** has been activated', color=color.success)
                await ctx.send(embed=embed)

        elif turn == 'off' or turn == 'false':
            if check['antispam'] == False:
                embed = discord.Embed(description=f'> {emojis.false} **AntiSpam** is not **activated**', color=color.fail)
                await ctx.send(embed=embed)
            else:
                collection.update_one({"_id": ctx.message.guild.id}, {"$set": {"antispam": False}})
                embed = discord.Embed(description=f'> {emojis.true} **AntiSpam** has been deactivated', color=color.success)
                await ctx.send(embed=embed)

        else:
            embed = discord.Embed(description=f'> {emojis.false} You cant set **AntiSpam** to ``{turn}``', color=color.fail)
            await ctx.send(embed=embed)

    @antispam.command(brief='whitelist roles', aliases=['wr', 'rw'])
    @commands.has_guild_permissions(manage_messages=True)
    @blacklist_check()
    async def rolewhitelist(self, ctx, role: discord.Role=None):
        if not collection.find_one({"_id": ctx.message.guild.id}):
            antispamdb = {"_id": ctx.message.guild.id, "antispam": False, "punishment": 'timeout', "warn_message": '> <:fail:963149868698837062> Please dont **Spam** in here', "punishment_message": '> <:fail:963149868698837062> You have been **Timeouted** due **Spam**', "whitelist": []}
            collection.insert_one(antispamdb)
        check = collection.find_one({"_id": ctx.message.guild.id})

        collection.update_one({"_id": ctx.message.guild.id}, {"$set": {"roles": []}})

        if role == None:
            data = collection.find_one({"_id": ctx.guild.id })['roles']
            embed = discord.Embed(title=f"{emojis.blade} AntiSpam", description=f"{emojis.reply} antispam role whitelist: \n", color=color.color)
            if check["roles"] == []:
                embed.description += f"> {emojis.false} there are no roles in **whitelist**!"
            else:
                for i in data:
                    embed.description += f"<@{i}> | `{i}`\n"
            await ctx.send(embed=embed)
        else:
            if role.id not in check["roles"]:
                collection.update_one({"_id": ctx.message.guild.id}, {"$push": {"roles": role.id}})
                embed = discord.Embed(description=f'> {emojis.true} {role.mention} has been added to **Whitelist**', color=color.success)
                await ctx.send(embed=embed)
            else:
                embed = discord.Embed(description=f'> {emojis.false} {role.mention} is already **Whitelisted**', color=color.fail)
                await ctx.send(embed=embed)

    @antispam.command(brief='whitelist roles', aliases=['uwr', 'ruw'])
    @commands.has_guild_permissions(manage_messages=True)
    @blacklist_check()
    async def roleunwhitelist(self, ctx, role: discord.Role=None):
        if not collection.find_one({"_id": ctx.message.guild.id}):
            antispamdb = {"_id": ctx.message.guild.id, "antispam": False, "punishment": 'timeout', "warn_message": '> <:fail:963149868698837062> Please dont **Spam** in here', "punishment_message": '> <:fail:963149868698837062> You have been **Timeouted** due **Spam**', "whitelist": []}
            collection.insert_one(antispamdb)
        check = collection.find_one({"_id": ctx.message.guild.id})

        collection.update_one({"_id": ctx.message.guild.id}, {"$set": {"roles": []}})

        if role == None:
            data = collection.find_one({"_id": ctx.guild.id })['roles']
            embed = discord.Embed(title=f"{emojis.blade} AntiSpam", description=f"{emojis.reply} antispam role whitelist: \n", color=color.color)
            if check["roles"] == []:
                embed.description += f"> {emojis.false} there are no roles in **whitelist**!"
            else:
                for i in data:
                    embed.description += f"<@{i}> | `{i}`\n"
            await ctx.send(embed=embed)
        else:
            if role.id not in check["roles"]:
                collection.update_one({"_id": ctx.message.guild.id}, {"$pull": {"roles": role.id}})
                embed = discord.Embed(description=f'> {emojis.true} {role.mention} has been added to **Whitelist**', color=color.success)
                await ctx.send(embed=embed)
            else:
                embed = discord.Embed(description=f'> {emojis.false} {role.mention} is already **Whitelisted**', color=color.fail)
                await ctx.send(embed=embed)

    @antispam.command(brief='whitelist members')
    @commands.has_guild_permissions(manage_messages=True)
    @blacklist_check()
    async def whitelist(self, ctx, user: discord.Member=None):
        if not collection.find_one({"_id": ctx.message.guild.id}):
            antispamdb = {"_id": ctx.message.guild.id, "antispam": False, "punishment": 'timeout', "warn_message": '> <:fail:963149868698837062> Please dont **Spam** in here', "punishment_message": '> <:fail:963149868698837062> You have been **Timeouted** due **Spam**', "whitelist": []}
            collection.insert_one(antispamdb)
        check = collection.find_one({"_id": ctx.message.guild.id})

        if user == None:
            data = collection.find_one({"_id": ctx.guild.id })['whitelist']
            embed = discord.Embed(title=f"{emojis.blade} AntiSpam", description=f"{emojis.reply} antispam whitelist: \n", color=color.color)
            if check["whitelist"] == []:
                embed.description += f"> {emojis.false} there are no users in **whitelist**!"
            else:
                for i in data:
                    if ctx.bot.get_user(i) != None:
                        if ctx.bot.get_user(i) == ctx.guild.owner:
                            embed.description += f"``Owner`` <@{i}> | `{i}`\n"
                        if ctx.bot.get_user(i) != ctx.guild.owner:
                            if ctx.bot.get_user(i).bot:
                                embed.description += f"``Bot`` <@{i}> | `{i}`\n"
                            else:
                                 embed.description += f"``User`` <@{i}> | `{i}`\n"
            await ctx.send(embed=embed)
        else:
            if user.id not in check["whitelist"]:
                collection.update_one({"_id": ctx.message.guild.id}, {"$push": {"whitelist": user.id}})
                embed = discord.Embed(description=f'> {emojis.true} {user.mention} has been added to **Whitelist**', color=color.success)
                await ctx.send(embed=embed)
            else:
                embed = discord.Embed(description=f'> {emojis.false} {user.mention} is already **Whitelisted**', color=color.fail)
                await ctx.send(embed=embed)

    @antispam.command(brief='unwhitelist members')
    @commands.has_guild_permissions(manage_messages=True)
    @blacklist_check()
    async def unwhitelist(self, ctx, user: discord.Member=None):
        if not collection.find_one({"_id": ctx.message.guild.id}):
            antispamdb = {"_id": ctx.message.guild.id, "antispam": False, "punishment": 'timeout', "warn_message": '> <:fail:963149868698837062> Please dont **Spam** in here', "punishment_message": '> <:fail:963149868698837062> You have been **Timeouted** due **Spam**', "whitelist": []}
            collection.insert_one(antispamdb)
        check = collection.find_one({"_id": ctx.message.guild.id})
        if user == None:
            embed = discord.Embed(description=f'> {emojis.false} Tag a user to Remove him from the **Whitelist**', color=color.fail)
            await ctx.send(embed=embed)
        else:
            if user.id in check["whitelist"]:
                collection.update_one({"_id": ctx.message.guild.id}, {"$pull": {"whitelist": user.id}})
                embed = discord.Embed(description=f'> {emojis.true} {user.mention} has been **Unwhitelisted**', color=color.success)
                await ctx.send(embed=embed)
            else:
                embed = discord.Embed(description=f'> {emojis.false} {user.mention} is not **Whitelisted**', color=color.fail)
                await ctx.send(embed=embed)

    @antispam.command(brief='clear antispam')
    @commands.has_guild_permissions(manage_messages=True)
    @blacklist_check()
    async def clear(self, ctx):
        if not collection.find_one({"_id": ctx.message.guild.id}):
            antispamdb = {"_id": ctx.message.guild.id, "antispam": False, "punishment": 'timeout', "warn_message": '> <:fail:963149868698837062> Please dont **Spam** in here', "punishment_message": '> <:fail:963149868698837062> You have been **Timeouted** due **Spam**', "whitelist": []}
            collection.insert_one(antispamdb)

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
                embed = discord.Embed(description=f'> {emojis.false} You cleared the **AntiSpam** config', color=color.success)
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
                embed = discord.Embed(description=f'> {emojis.true} The **AntiSpam** hasnt been **Cleared**', color=color.success)
                await interaction.response.edit_message(embed=embed, view=view)

        accept.callback = accept_callback
        decline.callback = decline_callback

        view = discord.ui.View()
        view.add_item(item=accept)
        view.add_item(item=decline)

        embed = discord.Embed(description=f'> Are you sure to clear your **AntiSpam** config?', color=color.color)
        await ctx.send(embed=embed, view=view)

async def setup(client):
    await client.add_cog(antispam(client))
