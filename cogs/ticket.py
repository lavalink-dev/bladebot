import discord
import pymongo
import aiohttp
from io import BytesIO
from pymongo import MongoClient
from discord.ext import commands
from utils import functions
from utils.emojis import emojis
from utils.bar import bar
from utils.color import color

cluster = MongoClient('no')
db = cluster["blade"]
collection = db["ticket"]
blacklist = db["blacklist"]

def blacklist_check():
    def predicate(ctx):
        if blacklist.find_one({'_id': ctx.author.id}):
            return False
        return True
    return commands.check(predicate)

class ticket(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.group(pass_context=True, invoke_without_command=True, brief='create tickets', description='config')
    @commands.has_guild_permissions(manage_guild=True)
    @blacklist_check()
    async def ticket(self, ctx):
        if not collection.find_one({"_id": ctx.message.guild.id}):
            tickets = {"_id": ctx.message.guild.id, "ticket": False, "channel": 0, "mod": 0, "message": '{member.mention}', "embed1_title": 'Ticket', "embed1_description": '> To create Ticket, press :tickets: button below this Message', "embed2_title": 'Ticket Created', "embed2_description": '> Thank you for creating a ticket, staff will be right with you shortly'}
            collection.insert_one(tickets)
        check = collection.find_one({"_id": ctx.message.guild.id})
        px = functions.get_prefix(ctx)

        if check['channel'] != 0:
            channels = self.client.get_channel(check['channel'])
            channel = f'{emojis.true} | {channels.mention}'
        else:
            channel = f'{emojis.false} *(no channel set)*'

        px = functions.get_prefix(ctx)
        embed = discord.Embed(title=f'{emojis.blade} Ticket', color=color.color,
        description=f'{emojis.reply} *configurate your ticket system*')
        embed.add_field(name=f"{emojis.commands} Commands:", value=f"\n> ``{px}ticket create`` create the ticket \n> ``{px}ticket mod [@role]`` set the mod role  \n> ``{px}ticket message [message]`` set the ticket message \n> ``{px}ticket embed [ticket/created] [title/description] [message]`` set the ticket embed \n> ``{px}ticket channel [#channel]`` set the channel for your ticket \n> ``{px}ticket clear`` clear your ticket config", inline=False)
        embed.add_field(name=f"{emojis.config} Config:", value=f"> ``Channel`` {channel}", inline=False)
        embed.add_field(name=f"{emojis.alias} Aliases:", value=f"```none```", inline=False)
        await ctx.send(embed=embed)

    @ticket.command()
    @commands.has_guild_permissions(manage_guild=True)
    @blacklist_check()
    async def create(self, ctx):
        if not collection.find_one({"_id": ctx.message.guild.id}):
            tickets = {"_id": ctx.message.guild.id, "ticket": False, "channel": 0, "mod": 0, "message": '{member.mention}', "embed1_title": 'Ticket', "embed1_description": '> To create Ticket, press :tickets: button below this Message', "embed2_title": 'Ticket Created', "embed2_description": '> Thank you for creating a ticket, staff will be right with you shortly'}
            collection.insert_one(tickets)
        check = collection.find_one({"_id": ctx.message.guild.id})

        if check['mod'] == 0:
            embed = discord.Embed(description=f'> {emojis.false} You need to set a **Mod Role** to create the **Ticket**', color=color.fail)
            await ctx.send(embed=embed)
            return

        create = discord.ui.Button(label="Create a Ticket", emoji='🎟️')

        async def create_callback(interaction):
            ticket_user = interaction.user

            createded_channel = discord.utils.get(ctx.guild.channels, name=f'ticket-{interaction.user.name}')
            if createded_channel:
                embed = discord.Embed(description=f'> {emojis.true} You already have a **Ticket** - {createded_channel.mention}', color=color.color)
                await interaction.response.send_message(embed=embed, view=None, ephemeral=True)

            async def close_callback(interaction):
                overwrites = {interaction.guild.default_role: discord.PermissionOverwrite(read_messages=False, connect=False), mod: discord.PermissionOverwrite(read_messages=True, connect=True), ticket_user: discord.PermissionOverwrite(read_messages=False, connect=False)}
                await interaction.channel.edit(overwrites=overwrites)

                reopen = discord.ui.Button(label="Reopen", emoji='<:locked:1045748710837063751>')
                delete = discord.ui.Button(label="Delete", emoji=emojis.false, style=discord.ButtonStyle.red)

                async def delete_callback(interaction):
                    await interaction.channel.delete()

                async def reopen_callback(interaction):
                    overwrites = {interaction.guild.default_role: discord.PermissionOverwrite(read_messages=False, connect=False), mod: discord.PermissionOverwrite(read_messages=True, connect=True), ticket_user: discord.PermissionOverwrite(read_messages=True, connect=True)}
                    await interaction.channel.edit(overwrites=overwrites)

                    embed = discord.Embed(description=f'> {emojis.true} The Ticket has been **Reopened**', color=color.color)
                    await interaction.channel.send(embed=embed)


                embed = discord.Embed(description=f'> Ticket closed by {ticket_user.mention}', color=color.success)
                reopen.callback = reopen_callback
                delete.callback = delete_callback
                closed_view = discord.ui.View(timeout=None)
                closed_view.add_item(item=reopen)
                closed_view.add_item(item=delete)

                await interaction.channel.send(embed=embed, view=closed_view)

            close = discord.ui.Button(label="Close the Ticket", emoji='<:locked:1045748710837063751>')
            close.callback = close_callback
            view = discord.ui.View(timeout=None)
            view.add_item(item=close)

            message = check['message']
            message = message.replace("{member.id}","%s" % (interaction.user.id))
            message = message.replace("{member.name}","%s" % (interaction.user.name))
            message = message.replace("{member.mention}","%s" % (interaction.user.mention))
            message = message.replace("{member.tag}","%s" % (interaction.user.discriminator))
            message = message.replace("{server.name}","%s" % (interaction.guild.name))
            message = message.replace("{server.id}","%s" % (interaction.guild.id))

            title = check['embed2_title']
            title = title.replace("{member.id}","%s" % (interaction.user.id))
            title = title.replace("{member.name}","%s" % (interaction.user.name))
            title = title.replace("{member.mention}","%s" % (interaction.user.mention))
            title = title.replace("{member.tag}","%s" % (interaction.user.discriminator))
            title = title.replace("{server.name}","%s" % (interaction.guild.name))
            title = title.replace("{server.id}","%s" % (interaction.guild.id))

            description = check['embed2_description']
            description = description.replace("{member.id}","%s" % (interaction.user.id))
            description = description.replace("{member.name}","%s" % (interaction.user.name))
            description = description.replace("{member.mention}","%s" % (interaction.user.mention))
            description = description.replace("{member.tag}","%s" % (interaction.user.discriminator))
            description = description.replace("{server.name}","%s" % (interaction.guild.name))
            description = description.replace("{server.id}","%s" % (interaction.guild.id))


            mod = interaction.guild.get_role(check['mod'])
            overwrites = {interaction.guild.default_role: discord.PermissionOverwrite(read_messages=False, connect=False), mod: discord.PermissionOverwrite(read_messages=True, connect=True), interaction.user: discord.PermissionOverwrite(read_messages=True, connect=True)}
            channel = await ctx.guild.create_text_channel(f'ticket - {interaction.user.name}', category=interaction.channel.category, overwrites=overwrites)
            embed = discord.Embed(title=f'{title}', description=f'{description}', color=color.color)
            embed.set_footer(icon_url=self.client.user.display_avatar, text='powered by blade')
            await channel.send(f'{message}', embed=embed, view=view)

            created_channel = discord.Embed(description=f'> {emojis.true} You Ticket has been **Created** - {channel.mention}', color=color.success)
            await interaction.response.send_message(embed=created_channel, ephemeral=True)

        title = check['embed1_title']
        title = title.replace("{member.id}","%s" % (ctx.author.id))
        title = title.replace("{member.name}","%s" % (ctx.author.name))
        title = title.replace("{member.mention}","%s" % (ctx.author.mention))
        title = title.replace("{member.tag}","%s" % (ctx.author.discriminator))
        title = title.replace("{server.name}","%s" % (ctx.guild.name))
        title = title.replace("{server.id}","%s" % (ctx.guild.id))

        description = check['embed1_description']
        description = description.replace("{member.id}","%s" % (ctx.author.id))
        description = description.replace("{member.name}","%s" % (ctx.author.name))
        description = description.replace("{member.mention}","%s" % (ctx.author.mention))
        description = description.replace("{member.tag}","%s" % (ctx.author.discriminator))
        description = description.replace("{server.name}","%s" % (ctx.guild.name))
        description = description.replace("{server.id}","%s" % (ctx.guild.id))

        embed = discord.Embed(title=f'{title}', description=f'{description}', color=color.color)
        embed.set_footer(icon_url=self.client.user.display_avatar, text='powered by blade')
        embed.set_thumbnail(url=ctx.guild.icon)

        create.callback = create_callback
        view = discord.ui.View(timeout=None)
        view.add_item(item=create)

        channel = self.client.get_channel(check['channel'])
        await channel.send(embed=embed, view=view)

        embed_send = discord.Embed(description=f'> {emojis.true} Created your **Ticket** in {channel.mention}', color=color.success)
        await ctx.send(embed=embed_send)

    @ticket.command()
    @commands.has_guild_permissions(manage_guild=True)
    @blacklist_check()
    async def message(self, ctx, *, message=None):
        if not collection.find_one({"_id": ctx.message.guild.id}):
            tickets = {"_id": ctx.message.guild.id, "ticket": False, "channel": 0, "mod": 0, "message": '{member.mention}', "embed1_title": 'Ticket', "embed1_description": '> To create Ticket, press :tickets: button below this Message', "embed2_title": 'Ticket Created', "embed2_description": '> Thank you for creating a ticket, staff will be right with you shortly'}
            collection.insert_one(tickets)
        check = collection.find_one({"_id": ctx.message.guild.id})
        px = functions.get_prefix(ctx)

        if message == None:
            ticket_message = check['message']
            ticket_message = ticket_message.replace("{member.id}","%s" % (ctx.author.id))
            ticket_message = ticket_message.replace("{member.name}","%s" % (ctx.author.name))
            ticket_message = ticket_message.replace("{member.mention}","%s" % (ctx.author.mention))
            ticket_message = ticket_message.replace("{member.tag}","%s" % (ctx.author.discriminator))
            ticket_message = ticket_message.replace("{server.name}","%s" % (ctx.guild.name))
            ticket_message = ticket_message.replace("{server.id}","%s" % (ctx.guild.id))

            embed = discord.Embed(title=f'{emojis.blade} Ticket', color=color.color,
            description=f'{emojis.reply} *set the ticket message*')
            embed.add_field(name=f"{emojis.commands} Command:", value=f"> ``{px}ticket message [message]`` set your ticket message", inline=False)
            embed.add_field(name=f"{emojis.config} Variables:", value="> ``{member.mention}`` mentions the member \n> ``{member.name}`` shows the members name \n> ``{member.tag}`` shows the members tag \n> ``{member.id}`` shows members id \n> ``{server.name}`` shows the name of the server \n> ``{server.id}`` shows the id of the server", inline=False)
            embed.add_field(name=f"{emojis.config} Current Message:", value=f"{ticket_message}", inline=False)
            await ctx.send(embed=embed)

        else:
            collection.update_one({"_id": ctx.message.guild.id}, {"$set": {"message": message}})
            embed = discord.Embed(description=f'> {emojis.true} You set the Ticket **Message** to: \n {message}', color=color.success)
            await ctx.send(embed=embed)

    @ticket.command()
    @commands.has_guild_permissions(manage_guild=True)
    async def embed(self, ctx, embeds=None, function=None, *, message=None):
        if not collection.find_one({"_id": ctx.message.guild.id}):
            tickets = {"_id": ctx.message.guild.id, "ticket": False, "channel": 0, "mod": 0, "message": '{member.mention}', "embed1_title": 'Ticket', "embed1_description": '> To create Ticket, press :tickets: button below this Message', "embed2_title": 'Ticket Created', "embed2_description": '> Thank you for creating a ticket, staff will be right with you shortly'}
            collection.insert_one(tickets)
        check = collection.find_one({"_id": ctx.message.guild.id})
        px = functions.get_prefix(ctx)

        if embeds == None:
            embed = discord.Embed(title=f'{emojis.blade} Ticket', color=color.color,
            description=f'{emojis.reply} *set the ticket embed*')
            embed.add_field(name=f"{emojis.commands} Command:", value=f"> ``{px}ticket embed [ticket/created] [title/description] [message]`` set your ticket embeds", inline=False)
            embed.add_field(name=f"{emojis.config} Variables:", value="> ``{member.mention}`` mentions the member \n> ``{member.name}`` shows the members name \n> ``{member.tag}`` shows the members tag \n> ``{member.id}`` shows members id \n> ``{server.name}`` shows the name of the server \n> ``{server.id}`` shows the id of the server", inline=False)
            embed.add_field(name=f"{emojis.function} Functions:", value=f"> ``ticket`` changes the embed of the **Create Ticket** embed \n> ``create`` changes the embed of the **Ticket Created** embed", inline=False)
            embed.add_field(name=f"{emojis.config} Ticket Embed:", value=f"> **Title**: \n```{check['embed1_title']}``` \n> **Description:** \n```{check['embed1_description']}```", inline=False)
            embed.add_field(name=f"{emojis.config} Created Ticket Embed:", value=f"> **Title**: \n```{check['embed2_title']}``` \n> **Description:** \n```{check['embed2_description']}```", inline=False)
            await ctx.send(embed=embed)
        else:
            if embeds == 'ticket' or embeds == 'Ticket':
                if function == None:
                    embed = discord.Embed(title=f'{emojis.blade} Ticket', color=color.color,
                    description=f'{emojis.reply} *set the ticket embed*')
                    embed.add_field(name=f"{emojis.commands} Command:", value=f"> ``{px}ticket embed ticket [title/description] [message]`` set your ticket embeds", inline=False)
                    embed.add_field(name=f"{emojis.config} Variables:", value="> ``{member.mention}`` mentions the member \n> ``{member.name}`` shows the members name \n> ``{member.tag}`` shows the members tag \n> ``{member.id}`` shows members id \n> ``{server.name}`` shows the name of the server \n> ``{server.id}`` shows the id of the server", inline=False)
                    await ctx.send(embed=embed)
                elif function == 'title':
                    if message == None:
                        embed = discord.Embed(description=f'> {emojis.false} Write a **Message** to set the Tickets Embed **Title**', color=color.fail)
                        await ctx.send(embed=embed)
                    else:
                        collection.update_one({"_id": ctx.message.guild.id}, {"$set": {"embed1_title": message}})
                        embed = discord.Embed(description=f'> {emojis.true} You set the Tickets Embed **Title** to: \n ```{message}```', color=color.success)
                        await ctx.send(embed=embed)
                elif function == 'description':
                    if message == None:
                        embed = discord.Embed(description=f'> {emojis.false} Write a **Message** to set the Tickets Embed **Title**', color=color.fail)
                        await ctx.send(embed=embed)
                    else:
                        collection.update_one({"_id": ctx.message.guild.id}, {"$set": {"embed1_description": message}})
                        embed = discord.Embed(description=f'> {emojis.true} You set the Tickets Embed **Description** to: \n ```{message}```', color=color.success)
                        await ctx.send(embed=embed)
                else:
                    embed = discord.Embed(description=f'> {emojis.false} You cant change ``{function}`` in the **Ticket** Embed', color=color.fail)
                    await ctx.send(embed=embed)

            elif embeds == 'create' or embeds == 'created':
                if function == None:
                    embed = discord.Embed(title=f'{emojis.blade} Ticket', color=color.color,
                    description=f'{emojis.reply} *set the created ticket embed*')
                    embed.add_field(name=f"{emojis.commands} Command:", value=f"> ``{px}ticket embed create [title/description] [message]`` set your ticket embeds", inline=False)
                    embed.add_field(name=f"{emojis.config} Variables:", value="> ``{member.mention}`` mentions the member \n> ``{member.name}`` shows the members name \n> ``{member.tag}`` shows the members tag \n> ``{member.id}`` shows members id \n> ``{server.name}`` shows the name of the server \n> ``{server.id}`` shows the id of the server", inline=False)
                    await ctx.send(embed=embed)
                elif function == 'title':
                    if message == None:
                        embed = discord.Embed(description=f'> {emojis.false} Write a **Message** to set the Tickets Embed **Title**', color=color.fail)
                        await ctx.send(embed=embed)
                    else:
                        collection.update_one({"_id": ctx.message.guild.id}, {"$set": {"embed2_title": message}})
                        embed = discord.Embed(description=f'> {emojis.true} You set the Tickets Embed **Title** to: \n ```{message}```', color=color.success)
                        await ctx.send(embed=embed)
                elif function == 'description':
                    if message == None:
                        embed = discord.Embed(description=f'> {emojis.false} Write a **Message** to set the Tickets Embed **Title**', color=color.fail)
                        await ctx.send(embed=embed)
                    else:
                        collection.update_one({"_id": ctx.message.guild.id}, {"$set": {"embed2_description": message}})
                        embed = discord.Embed(description=f'> {emojis.true} You set the Tickets Embed **Description** to: \n ```{message}```', color=color.success)
                        await ctx.send(embed=embed)
                else:
                    embed = discord.Embed(description=f'> {emojis.false} You cant change ``{function}`` in the **Ticket** Embed', color=color.fail)
                    await ctx.send(embed=embed)
            else: 
                embed = discord.Embed(description=f'> {emojis.false} There is no ``{embeds}``, color=color.f    ')
                await ctx.send(embed=embed)

    @ticket.command()
    @commands.has_guild_permissions(manage_guild=True)
    @blacklist_check()
    async def mod(self, ctx, role: discord.Role=None):
        if not collection.find_one({"_id": ctx.message.guild.id}):
            tickets = {"_id": ctx.message.guild.id, "ticket": False, "channel": 0, "mod": 0, "message": '{member.mention}', "embed1_title": 'Ticket', "embed1_description": '> To create Ticket, press :tickets: button below this Message', "embed2_title": 'Ticket Created', "embed2_description": '> Thank you for creating a ticket, staff will be right with you shortly'}
            collection.insert_one(tickets)
        check = collection.find_one({"_id": ctx.message.guild.id})
        px = functions.get_prefix(ctx)

        if role == None:
            embed = discord.Embed(title=f'{emojis.blade} Ticket', color=color.color,
            description=f'{emojis.reply} *set the mod role*')
            embed.add_field(name=f"{emojis.commands} Command:", value=f"> ``{px}ticket mod [@role]`` set your mod role", inline=False)
            await ctx.send(embed=embed)

        else:
            collection.update_one({"_id": ctx.message.guild.id}, {"$set": {"mod": role.id}})
            embed = discord.Embed(description=f'> {emojis.true} You set the **Ticket** Mod role to {role.mention}', color=color.success)
            await ctx.send(embed=embed)       

    @ticket.command()
    @commands.has_guild_permissions(manage_guild=True)
    @blacklist_check()
    async def channel(self, ctx, channel: discord.TextChannel=None):
        if not collection.find_one({"_id": ctx.message.guild.id}):
            tickets = {"_id": ctx.message.guild.id, "ticket": False, "channel": 0, "mod": 0, "message": '{member.mention}', "embed1_title": 'Ticket', "embed1_description": '> To create Ticket, press :tickets: button below this Message', "embed2_title": 'Ticket Created', "embed2_description": '> Thank you for creating a ticket, staff will be right with you shortly'}
            collection.insert_one(tickets)
        check = collection.find_one({"_id": ctx.message.guild.id})
        px = functions.get_prefix(ctx)

        if channel == None:
            embed = discord.Embed(title=f'{emojis.blade} Ticket', color=color.color,
            description=f'{emojis.reply} *set the ticket channel*')
            embed.add_field(name=f"{emojis.commands} Command:", value=f"> ``{px}ticket ticket [#channel]`` set your ticket channel", inline=False)
            await ctx.send(embed=embed)

        else:
            collection.update_one({"_id": ctx.message.guild.id}, {"$set": {"channel": channel.id}})
            embed = discord.Embed(description=f'> {emojis.true} You set the **Ticket** channel to {channel.mention}', color=color.success)
            await ctx.send(embed=embed)

    @ticket.command()
    @commands.has_guild_permissions(manage_guild=True)
    @blacklist_check()
    async def clear(self, ctx):
        if not collection.find_one({"_id": ctx.message.guild.id}):
            tickets = {"_id": ctx.message.guild.id, "ticket": False, "channel": 0, "mod": 0, "message": '{member.mention}', "embed1_title": 'Ticket', "embed1_description": '> To create Ticket, press :tickets: button below this Message', "embed2_title": 'Ticket Created', "embed2_description": '> Thank you for creating a ticket, staff will be right with you shortly'}
            collection.insert_one(tickets)

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
                embed = discord.Embed(description=f'> {emojis.true} You cleared the **Ticket** config', color=color.success)
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
                embed = discord.Embed(description=f'> {emojis.true} Your **Ticket** hasnt been **Cleared**', color=color.success)
                await interaction.response.edit_message(embed=embed, view=view)

        accept.callback = accept_callback
        decline.callback = decline_callback

        view = discord.ui.View()
        view.add_item(item=accept)
        view.add_item(item=decline)

        embed = discord.Embed(description=f'> Are you sure to clear your **Ticket** config?', color=color.color)
        await ctx.send(embed=embed, view=view)

async def setup(client):
    await client.add_cog(ticket(client))
