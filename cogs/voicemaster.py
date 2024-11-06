import discord
import pymongo
from discord.ext import commands
from discord.ui import Modal, Select, View
from pymongo import MongoClient
from utils import functions
from utils.emojis import emojis
from utils.color import color

cluster = MongoClient('no')
db = cluster["blade"]
collection = db["voicemaster"]
vm_channels = db["voicemaster_channels"]
blacklist = db["blacklist"]

class vcModal(Modal, title=f"Rename your Voice Channel"):
    name = discord.ui.TextInput(
    label="voice channel name",
    placeholder="give your channel a better name",
    required=True,
    style=discord.TextStyle.short
    )

    async def on_submit(self, interaction: discord.Interaction):
        name = self.name.value
        await interaction.user.voice.channel.edit(name=name)   
        embed = discord.Embed(description=f"> {emojis.true} Changed the **Name** to ``{name}``", color=color.success)
        await interaction.response.send_message(embed=embed, ephemeral=True)

def blacklist_check():
    def predicate(ctx):
        if blacklist.find_one({'_id': ctx.author.id}):
            return False
        return True
    return commands.check(predicate)

class voicemaster(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(brief='help', description='none')
    @commands.is_owner()
    async def vmfix(self, ctx):
        for i in vm_channels.find({}):
            await vm_channels.delete_one({"_id": i["_id"]})

        await ctx.send("done")

    @commands.Cog.listener() 
    async def on_voice_state_update(self, member: discord.Member, before: discord.VoiceState, after: discord.VoiceState):
        if not collection.find_one({"_id": member.guild.id}):
            return
        
        else:
            try:
                check = collection.find_one({"_id": member.guild.id})
                if (after.channel is not None and before.channel is None) or (after.channel is not None and before.channel is not None):
                    if after.channel.id == check['channel']:

                        if vm_channels.find_one({"owner": member.id}):
                            check2 = vm_channels.find_one({"owner": member.id})
                            vm_channel = self.client.get_channel(check2['_id'])
                            await member.move_to(channel=vm_channel)

                        else:
                            channel = await member.guild.create_voice_channel(f"{member.name}'s channel", category=after.channel.category)
                            vm_channels.insert_one({"_id": channel.id, "owner": member.id})
                            await member.move_to(channel)

                else:
                        pass

                if before.channel != after.channel:
                    if vm_channels.find_one({"_id": before.channel.id}):
                        check2 = vm_channels.find_one({"_id": before.channel.id})

                        if len(before.channel.members) == 0:
                            vm_channels.delete_one({"_id": before.channel.id})
                            await before.channel.delete()
                        else:
                            if member.id == check2['owner']:
                                members = []
                                for user in before.channel.members:
                                    members.append(user.id)
                                    members.append(user.name)

                                vm_channels.update_one({"_id": before.channel.id}, {"$set": {"owner": members[0]}})
                                await before.channel.edit(name=f"{members[1]}'s channel")
                            else:
                                pass
                    else:
                        pass

                if before.channel and not after.channel:
                    if vm_channels.find_one({"_id": before.channel.id}):
                        check2 = vm_channels.find_one({"_id": before.channel.id})

                        if len(before.channel.members) == 0:
                            vm_channels.delete_one({"_id": before.channel.id})
                            await before.channel.delete()
                        else:
                            if member.id == check2['owner']:
                                members = []
                                for user in before.channel.members:
                                    members.append(user.id)
                                    members.append(user.name)

                                vm_channels.update_one({"_id": before.channel.id}, {"$set": {"owner": members[0]}})
                                await before.channel.edit(name=f"{members[1]}'s channel")
                            else:
                                pass
                    else:
                        pass
                            
            except:
                pass

    @commands.group(pass_context=True, invoke_without_command=True, aliases=['vm'], description="config", brief='join 2 create voice channel with panel')
    @commands.has_guild_permissions(manage_guild=True)
    @blacklist_check()
    async def voicemaster(self, ctx):
        if not collection.find_one({"_id": ctx.message.guild.id}):
            voicemaster = {"_id": ctx.message.guild.id, "channel": 0, "panel": 0}
            collection.insert_one(voicemaster)

        await ctx.invoke()

    @voicemaster.command(brief='create voicemaster channel and panel')
    @commands.has_guild_permissions(manage_guild=True)
    @blacklist_check()
    async def create(self, ctx):
        if not collection.find_one({"_id": ctx.message.guild.id}):
            voicemaster = {"_id": ctx.message.guild.id, "channel": 0, "panel": 0}
            collection.insert_one(voicemaster)

        embed = discord.Embed(description=f'> {emojis.false} Creating the **Channel**...')
        message = await ctx.send(embed=embed)
        
        category = await ctx.guild.create_category('-')
        interface = await ctx.guild.create_text_channel('interface', category=category)
        channel = await ctx.guild.create_voice_channel('create', category=category)

        overwrites = {ctx.guild.default_role: discord.PermissionOverwrite(send_messages=False)}
        await interface.edit(overwrites=overwrites)

        async def lock_callback(interaction):
            if not vm_channels.find_one({"owner": interaction.user.id}):
                embed = discord.Embed(description=f"> {emojis.false} You are ether not in a Channel or you dont own a Channel", color=color.fail)
                await interaction.response.send_message(embed=embed, ephemeral=True)
            else:
                check = vm_channels.find_one({"owner": interaction.user.id})
                channel = self.client.get_channel(check['_id'])

                overwrite = channel.overwrites_for(ctx.guild.default_role)
                overwrite.connect = False
                await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)

                embed = discord.Embed(description=f"> {emojis.true} Your channel has been **Locked**", color=color.success)
                await interaction.response.send_message(embed=embed, ephemeral=True)

        async def unlock_callback(interaction):
            if not vm_channels.find_one({"owner": interaction.user.id}):
                embed = discord.Embed(description=f"> {emojis.false} You are ether not in a Channel or you dont own a Channel", color=color.fail)
                await interaction.response.send_message(embed=embed, ephemeral=True)
            else:
                check = vm_channels.find_one({"owner": interaction.user.id})
                channel = self.client.get_channel(check['_id'])

                overwrite = channel.overwrites_for(ctx.guild.default_role)
                overwrite.connect = True
                await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)

                embed = discord.Embed(description=f"> {emojis.true} Your channel has been **Unlocked**", color=color.success)
                await interaction.response.send_message(embed=embed, ephemeral=True)

        async def increase_callback(interaction):
            if not vm_channels.find_one({"owner": interaction.user.id}):
                embed = discord.Embed(description=f"> {emojis.false} You are ether not in a Channel or you dont own a Channel", color=color.fail)
                await interaction.response.send_message(embed=embed, ephemeral=True)
            else:
                check = vm_channels.find_one({"owner": interaction.user.id})
                channel = self.client.get_channel(check['_id'])
                limit = channel.user_limit

                await channel.edit(user_limit=limit+1)

                embed = discord.Embed(description=f"> {emojis.true} Set the **Limit** to ``{limit+1}`` Members", color=color.success)
                await interaction.response.send_message(embed=embed, ephemeral=True)

        async def decrease_callback(interaction):
            if not vm_channels.find_one({"owner": interaction.user.id}):
                embed = discord.Embed(description=f"> {emojis.false} You are ether not in a Channel or you dont own a Channel", color=color.fail)
                await interaction.response.send_message(embed=embed, ephemeral=True)
            else:
                check = vm_channels.find_one({"owner": interaction.user.id})
                channel = self.client.get_channel(check['_id'])
                limit = channel.user_limit

                if limit == 0:
                    embed = discord.Embed(description=f"> {emojis.false} You cant go **Lower** than ``0`` Members", color=color.fail)
                    await interaction.response.send_message(embed=embed, ephemeral=True)

                else:
                    await channel.edit(user_limit=limit - 1)

                    embed = discord.Embed(description=f"> {emojis.true} Successfully set the **Limit** to ``{limit - 1}`` Members", color=color.success)
                    await interaction.response.send_message(embed=embed, ephemeral=True)

        async def ghost_callback(interaction):
            if not vm_channels.find_one({"owner": interaction.user.id}):
                embed = discord.Embed(description=f"> {emojis.false} You are ether not in a Channel or you dont own a Channel", color=color.fail)
                await interaction.response.send_message(embed=embed, ephemeral=True)
            else:
                check = vm_channels.find_one({"owner": interaction.user.id})
                channel = self.client.get_channel(check['_id'])

                overwrite = channel.overwrites_for(ctx.guild.default_role)
                overwrite.view_channel = False
                await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)

                embed = discord.Embed(description=f"> {emojis.true} Your **Channel** is now **ghosted**", color=color.success)
                await interaction.response.send_message(embed=embed, ephemeral=True)

        async def unghost_callback(interaction):
            if not vm_channels.find_one({"owner": interaction.user.id}):
                embed = discord.Embed(description=f"> {emojis.false} You are ether not in a Channel or you dont own a Channel", color=color.fail)
                await interaction.response.send_message(embed=embed, ephemeral=True)
            else:
                check = vm_channels.find_one({"owner": interaction.user.id})
                channel = self.client.get_channel(check['_id'])

                overwrite = channel.overwrites_for(ctx.guild.default_role)
                overwrite.view_channel = True
                await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)

                embed = discord.Embed(description=f"> {emojis.true} Your **Channel** is now **unghosted**", color=color.success)
                await interaction.response.send_message(embed=embed, ephemeral=True)

        async def rename_callback(interaction):
            if not vm_channels.find_one({"owner": interaction.user.id}):
                embed = discord.Embed(description=f"> {emojis.false} You are ether not in a Channel or you dont own a Channel", color=color.fail)
                await interaction.response.send_message(embed=embed, ephemeral=True)
            else:
                rename = vcModal()
                await interaction.response.send_modal(rename)

        async def settings_callback(interaction):
            if interaction.user.voice == None:
                embed = discord.Embed(description=f"> {emojis.false} You are ether not in a Channel or you dont own a Channel", color=color.fail)
                await interaction.response.send_message(embed=embed, ephemeral=True)
            else:
                check = vm_channels.find_one({"owner": interaction.user.id})
                owner = self.client.get_user(check['owner'])
                channel = interaction.user.voice.channel

                embed = discord.Embed(title=f'{emojis.blade} Voicemaster', color=color.color,
                                       description=f"> ``Name`` {channel.name} \n> ``Owner`` {owner.mention} \n> ``Channel`` {channel.mention} \n> ``Channel ID`` {channel.id}")
                await interaction.response.send_message(embed=embed, ephemeral=True)

        lock = discord.ui.Button(emoji=emojis.lock)
        unlock = discord.ui.Button(emoji=emojis.unlock)
        increase = discord.ui.Button(emoji='<:add:1127747607662432326>')
        decrease = discord.ui.Button(emoji='<:remove:1127748098987409429>')
        ghost = discord.ui.Button(emoji='<:ghost:1127754743285022830> ')
        unghost = discord.ui.Button(emoji='<:unghost:1127754713174126712>')
        rename = discord.ui.Button(emoji='<:rename:1127770274226520125>')
        settings = discord.ui.Button(emoji=emojis.config)

        invite = discord.ui.Button(emoji=emojis.link, url="https://discord.com/api/oauth2/authorize?client_id=896550468128505877&permissions=8&scope=bot")
        support = discord.ui.Button(emoji=emojis.badge, url="https://discord.gg/MVnhjYqfYu")

        lock.callback = lock_callback
        unlock.callback = unlock_callback
        increase.callback = increase_callback
        decrease.callback = decrease_callback
        ghost.callback = ghost_callback
        unghost.callback = unghost_callback
        rename.callback = rename_callback
        settings.callback = settings_callback

        view = discord.ui.View(timeout=None)
        view.add_item(item=lock)
        view.add_item(item=unlock)
        view.add_item(item=increase)
        view.add_item(item=decrease)
        view.add_item(item=invite)
        view.add_item(item=ghost)
        view.add_item(item=unghost)
        view.add_item(item=rename)
        view.add_item(item=settings)
        view.add_item(item=support)
    

        interface_embed = discord.Embed(title=f'{emojis.blade} Voicemaster', color=color.color,
                              description=f'{emojis.reply} *manage your voice channel* \n \n> {emojis.lock} ``lock`` the voice channel \n> {emojis.unlock} ``unlock`` the voice channel \n> <:add:1127747607662432326> ``increase`` the user limit \n> <:remove:1127748098987409429> ``decrease`` the user limit \n> <:ghost:1127754743285022830> ``ghost`` the voice channel \n> <:unghost:1127754713174126712> ``unghost`` the voice channel \n> <:rename:1127770274226520125> ``rename`` the voice channel \n> {emojis.config} ``settings`` of the voice channel')
        interface_embed.set_thumbnail(url=ctx.guild.icon)
        await interface.send(embed=interface_embed, view=view)

        collection.update_one({"_id": ctx.message.guild.id}, {"$set": {"channel": channel.id}})
        collection.update_one({"_id": ctx.message.guild.id}, {"$set": {"panel": interface.id}})
        embed = discord.Embed(description=f'> {emojis.true} Successfully setup **VoiceMaster** \n {emojis.reply2} Created the **Channel**: {channel.mention} \n {emojis.reply} Interface: {interface.mention}', color=color.success)
        await message.edit(embed=embed)

    @voicemaster.command(brief='clear voicemaster config')
    @commands.has_guild_permissions(manage_guild=True)
    @blacklist_check()
    async def clear(self, ctx):
        if not collection.find_one({"_id": ctx.message.guild.id}):
            voicemaster = {"_id": ctx.message.guild.id, "channel": 0, "panel": 0}
            collection.insert_one(voicemaster)

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
                embed = discord.Embed(description=f'> {emojis.true} You cleared the **Voicemaster** config', color=color.success)
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
                embed = discord.Embed(description=f'> {emojis.true} Your **Voicemaster** hasnt been **Cleared**', color=color.success)
                await interaction.response.edit_message(embed=embed, view=view)

        accept.callback = accept_callback
        decline.callback = decline_callback

        view = discord.ui.View()
        view.add_item(item=accept)
        view.add_item(item=decline)

        embed = discord.Embed(description=f'> Are you sure to clear your **Voicemaster** config?', color=color.color)
        await ctx.send(embed=embed, view=view)

    @voicemaster.command(brief='resends the voicemaster panel')
    @commands.has_guild_permissions(manage_guild=True)
    @blacklist_check()
    async def panel(self, ctx):
        panel_channel = collection.find_one({"_id": ctx.message.guild.id})["panel"]

        async def lock_callback(interaction):
            if not vm_channels.find_one({"owner": interaction.user.id}):
                embed = discord.Embed(description=f"> {emojis.false} You are ether not in a Channel or you dont own a Channel", color=color.fail)
                await interaction.response.send_message(embed=embed, ephemeral=True)
            else:
                check = vm_channels.find_one({"owner": interaction.user.id})
                channel = self.client.get_channel(check['_id'])

                overwrite = channel.overwrites_for(ctx.guild.default_role)
                overwrite.connect = False
                await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)

                embed = discord.Embed(description=f"> {emojis.true} Your channel has been **Locked**", color=color.success)
                await interaction.response.send_message(embed=embed, ephemeral=True)

        async def unlock_callback(interaction):
            if not vm_channels.find_one({"owner": interaction.user.id}):
                embed = discord.Embed(description=f"> {emojis.false} You are ether not in a Channel or you dont own a Channel", color=color.fail)
                await interaction.response.send_message(embed=embed, ephemeral=True)
            else:
                check = vm_channels.find_one({"owner": interaction.user.id})
                channel = self.client.get_channel(check['_id'])

                overwrite = channel.overwrites_for(ctx.guild.default_role)
                overwrite.connect = True
                await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)

                embed = discord.Embed(description=f"> {emojis.true} Your channel has been **Unlocked**", color=color.success)
                await interaction.response.send_message(embed=embed, ephemeral=True)

        async def increase_callback(interaction):
            if not vm_channels.find_one({"owner": interaction.user.id}):
                embed = discord.Embed(description=f"> {emojis.false} You are ether not in a Channel or you dont own a Channel", color=color.fail)
                await interaction.response.send_message(embed=embed, ephemeral=True)
            else:
                check = vm_channels.find_one({"owner": interaction.user.id})
                channel = self.client.get_channel(check['_id'])
                limit = channel.user_limit

                await channel.edit(user_limit=limit+1)

                embed = discord.Embed(description=f"> {emojis.true} Set the **Limit** to ``{limit+1}`` Members", color=color.success)
                await interaction.response.send_message(embed=embed, ephemeral=True)

        async def decrease_callback(interaction):
            if not vm_channels.find_one({"owner": interaction.user.id}):
                embed = discord.Embed(description=f"> {emojis.false} You are ether not in a Channel or you dont own a Channel", color=color.fail)
                await interaction.response.send_message(embed=embed, ephemeral=True)
            else:
                check = vm_channels.find_one({"owner": interaction.user.id})
                channel = self.client.get_channel(check['_id'])
                limit = channel.user_limit

                if limit == 0:
                    embed = discord.Embed(description=f"> {emojis.false} You cant go **Lower** than ``0`` Members", color=color.fail)
                    await interaction.response.send_message(embed=embed, ephemeral=True)

                else:
                    await channel.edit(user_limit=limit - 1)

                    embed = discord.Embed(description=f"> {emojis.true} Successfully set the **Limit** to ``{limit - 1}`` Members", color=color.success)
                    await interaction.response.send_message(embed=embed, ephemeral=True)

        async def ghost_callback(interaction):
            if not vm_channels.find_one({"owner": interaction.user.id}):
                embed = discord.Embed(description=f"> {emojis.false} You are ether not in a Channel or you dont own a Channel", color=color.fail)
                await interaction.response.send_message(embed=embed, ephemeral=True)
            else:
                check = vm_channels.find_one({"owner": interaction.user.id})
                channel = self.client.get_channel(check['_id'])

                overwrite = channel.overwrites_for(ctx.guild.default_role)
                overwrite.view_channel = False
                await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)

                embed = discord.Embed(description=f"> {emojis.true} Your **Channel** is now **ghosted**", color=color.success)
                await interaction.response.send_message(embed=embed, ephemeral=True)

        async def unghost_callback(interaction):
            if not vm_channels.find_one({"owner": interaction.user.id}):
                embed = discord.Embed(description=f"> {emojis.false} You are ether not in a Channel or you dont own a Channel", color=color.fail)
                await interaction.response.send_message(embed=embed, ephemeral=True)
            else:
                check = vm_channels.find_one({"owner": interaction.user.id})
                channel = self.client.get_channel(check['_id'])

                overwrite = channel.overwrites_for(ctx.guild.default_role)
                overwrite.view_channel = True
                await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)

                embed = discord.Embed(description=f"> {emojis.true} Your **Channel** is now **unghosted**", color=color.success)
                await interaction.response.send_message(embed=embed, ephemeral=True)

        async def rename_callback(interaction):
            if not vm_channels.find_one({"owner": interaction.user.id}):
                embed = discord.Embed(description=f"> {emojis.false} You are ether not in a Channel or you dont own a Channel", color=color.fail)
                await interaction.response.send_message(embed=embed, ephemeral=True)
            else:
                rename = vcModal()
                await interaction.response.send_modal(rename)

        async def settings_callback(interaction):
            if interaction.user.voice == None:
                embed = discord.Embed(description=f"> {emojis.false} You are ether not in a Channel or you dont own a Channel", color=color.fail)
                await interaction.response.send_message(embed=embed, ephemeral=True)
            else:
                check = vm_channels.find_one({"owner": interaction.user.id})
                owner = self.client.get_user(check['owner'])
                channel = interaction.user.voice.channel

                embed = discord.Embed(title=f'{emojis.blade} Voicemaster', color=color.color,
                                       description=f"> ``Name`` {channel.name} \n> ``Owner`` {owner.mention} \n> ``Channel`` {channel.mention} \n> ``Channel ID`` {channel.id}")
                await interaction.response.send_message(embed=embed, ephemeral=True)

        lock = discord.ui.Button(emoji=emojis.lock)
        unlock = discord.ui.Button(emoji=emojis.unlock)
        increase = discord.ui.Button(emoji='<:add:1127747607662432326>')
        decrease = discord.ui.Button(emoji='<:remove:1127748098987409429>')
        ghost = discord.ui.Button(emoji='<:ghost:1127754743285022830> ')
        unghost = discord.ui.Button(emoji='<:unghost:1127754713174126712>')
        rename = discord.ui.Button(emoji='<:rename:1127770274226520125>')
        settings = discord.ui.Button(emoji=emojis.config)

        invite = discord.ui.Button(emoji=emojis.link, url="https://discord.com/api/oauth2/authorize?client_id=896550468128505877&permissions=8&scope=bot")
        support = discord.ui.Button(emoji=emojis.badge, url="https://discord.gg/MVnhjYqfYu")

        lock.callback = lock_callback
        unlock.callback = unlock_callback
        increase.callback = increase_callback
        decrease.callback = decrease_callback
        ghost.callback = ghost_callback
        unghost.callback = unghost_callback
        rename.callback = rename_callback
        settings.callback = settings_callback

        view = discord.ui.View(timeout=None)
        view.add_item(item=lock)
        view.add_item(item=unlock)
        view.add_item(item=increase)
        view.add_item(item=decrease)
        view.add_item(item=invite)
        view.add_item(item=ghost)
        view.add_item(item=unghost)
        view.add_item(item=rename)
        view.add_item(item=settings)
        view.add_item(item=support)
    
        channel = self.client.get_channel(panel_channel)

        embed = discord.Embed(title=f'{emojis.blade} Voicemaster', color=color.color,
                              description=f'{emojis.reply} *manage your voice channel* \n \n> {emojis.lock} ``lock`` the voice channel \n> {emojis.unlock} ``unlock`` the voice channel \n> <:add:1127747607662432326> ``increase`` the user limit \n> <:remove:1127748098987409429> ``decrease`` the user limit \n> <:ghost:1127754743285022830> ``ghost`` the voice channel \n> <:unghost:1127754713174126712> ``unghost`` the voice channel \n> <:rename:1127770274226520125> ``rename`` the voice channel \n> {emojis.config} ``settings`` of the voice channel')
        embed.set_thumbnail(url=ctx.guild.icon)

        await channel.send(embed=embed, view=view)

async def setup(client):
    await client.add_cog(voicemaster(client))
