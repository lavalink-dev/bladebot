import discord
import json
import pymongo
from pymongo import MongoClient
from discord.ext import commands
from discord.utils import get
from utils import functions
from utils.emojis import emojis
from utils.color import color

cluster = MongoClient('mongodb+srv://blade:lolidkbruh12333333333@cluster0.wbxaj.mongodb.net/myFirstDatabase?retryWrites=true&w=majority')
db = cluster["blade"]
welcome = db["welcome_messages"]
leave = db["leave_messages"]
joindm = db["joindm"]
joinping = db["joinping"]
autorole = db["autorole"]
antinuke = db["antinuke"]
antispam = db["antispam"]
reaction = db["reaction"]
responder = db["responder"]
boost = db["boost"]
autopfp = db["autopfp"]
filter = db["filter"]
tags = db["tags"]
tracker = db["tracker"]
logger = db["logger"]
autoresponder = db["autoresponder"]
level = db["level"]
levelconfig = db["levelconfig"]
onlyimg = db["onlyimg"]
ticket = db["ticket"]
silence = db["silence"]
voicemaster = db["voicemaster"]
antilink = db["antilink"]
blacklist = db["blacklist"]


class on_guild(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        if blacklist.find_one({"_id": guild.owner.id}):
            owner = self.client.get_user(guild.owner.id)
            owner_embed = discord.Embed(description=f'> {emojis.false} You are **Blacklisted** from Blade, reason: **{blacklist.find_one({"_id": guild.owner.id})["reason"]}**. Thats why u cant Invite him in your **Server** \n> You think this was a **Mistake**? Join our Support [``here``]("https://discord.gg/MVnhjYqfYu)', color=color.color)
            await owner.send(embed=owner_embed)

            channel = self.client.get_channel(1213479263618072576)
            embed = discord.Embed(title=f'{emojis.blade} blacklisted guild', color=color.color, 
            description=f'> **Server**: ``{guild.name}`` | ``({guild.id})`` \n> **Owner**: ``{guild.owner}`` | ``{guild.owner.id}`` \n> **Members**: ``{guild.member_count}``') #**invite:** {link}
            embed.set_thumbnail(url=guild.icon)
            embed.set_footer(text=f'blade is now in {len(self.client.guilds)} server with {len(self.client.users):,} members')
            await channel.send(embed=embed)
            await self.client.get_guild(guild.id).leave()
            return

        with open("data/prefixes.json", "r") as f:
            prefixes = json.load(f)
        prefixes[str(guild.id)] = "$"
        with open("data/prefixes.json", "w") as f:
            json.dump(prefixes,f)

        buttons = discord.ui.View()
        style = discord.ButtonStyle.gray
        invite = discord.ui.Button(style=style, label="Invite", url="https://discord.com/api/oauth2/authorize?client_id=896550468128505877&permissions=8&scope=bot")
        support = discord.ui.Button(style=style, label="Support", url="https://discord.gg/MVnhjYqfYu")
        website = discord.ui.Button(style=style, label="Website", url="https://bladebot.org/")
        buttons.add_item(item=invite)
        buttons.add_item(item=support)
        buttons.add_item(item=website)

        if guild.vanity_url_code != None:
            vanity = f'> **Vanity**: [``.gg/{guild.vanity_url_code}``](https://discord.gg/{guild.vanity_url_code})'
        else:
            vanity = ''

        channel = self.client.get_channel(1213479263618072576)
        #link = await guild.text_channels[0].create_invite()
        embed = discord.Embed(title=f'{emojis.blade} guild joined', color=color.color,
        description=f'{emojis.dash} **Server**: ``{guild.name}`` | ``({guild.id})`` \n{emojis.reply2} **Owner**: ``{guild.owner}`` | ``{guild.owner.id}`` \n{emojis.reply}**Members**: ``{guild.member_count}``\n {vanity}') #**invite:** {link}
        embed.set_thumbnail(url=guild.icon)
        embed.set_footer(text=f'blade is now in {len(self.client.guilds)} servers with {len(self.client.users):,} members')
        await channel.send(embed=embed)

        owner = self.client.get_user(guild.owner.id)
        embed = discord.Embed(title=f'{emojis.blade} **blade**', color=color.color,
        description=f'{emojis.reply} Thanks for inviting **blade** to your Server **{guild.name}** \n \n{emojis.dash} **General Help**: \n{emojis.reply2} use the help command for the common help \n{emojis.reply} if you need help join our [Support Server](https://discord.gg/MVnhjYqfYu) \n \n{emojis.dash} To change the Prefix, type `$prefix [prefix]`')
        embed.set_thumbnail(url=self.client.user.display_avatar)
        await owner.send(embed=embed, view=buttons)

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        if guild.vanity_url_code != None:
            vanity = f'> **Vanity**: [``.gg/{guild.vanity_url_code}``](https://discord.gg/{guild.vanity_url_code})'
        else:
            vanity = ''

        try:
            channel = self.client.get_channel(1213479263618072576)
            embed = discord.Embed(title=f'{emojis.blade} guild left', color=color.color,
            description=f'{emojis.dash} **Server**: ``{guild.name}`` | ``({guild.id})`` \n{emojis.reply2} **Owner**: ``{guild.owner}`` | ``{guild.owner.id}`` \n{emojis.reply}**Members**: ``{guild.member_count}``\n {vanity}')
            embed.set_footer(text=f'blade is now in {len(self.client.guilds)} servers with {len(self.client.users):,} members')
            embed.set_thumbnail(url=guild.icon)
        except:
            pass
        await channel.send(embed=embed)

        if welcome.find_one({"_id": guild.id}):
            welcome.delete_one({"_id": guild.id})

        if leave.find_one({"_id": guild.id}):
            leave.delete_one({"_id": guild.id})

        if antinuke.find_one({"_id": guild.id}):
            antinuke.delete_one({"_id": guild.id})

        if antilink.find_one({"_id": guild.id}):
            antilink.delete_one({"_id": guild.id})

        if autoresponder.find_one({"_id": guild.id}):
            autoresponder.delete_one({"_id": guild.id})

        if joindm.find_one({"_id": guild.id}):
            joindm.delete_one({"_id": guild.id})

        if joinping.find_one({"_id": guild.id}):
            joinping.delete_one({"_id": guild.id})

        if onlyimg.find_one({"_id": guild.id}):
            onlyimg.delete_one({"_id": guild.id})

        if autorole.find_one({"_id": guild.id}):
            autorole.delete_one({"_id": guild.id})

        if filter.find_one({"_id": guild.id}):
            filter.delete_one({"_id": guild.id})

        if logger.find_one({"_id": guild.id}):
            logger.delete_one({"_id": guild.id})

        if autopfp.find_one({"_id": guild.id}):
            autopfp.delete_one({"_id": guild.id})

        if tags.find_one({"_id": guild.id}):
            tags.delete_one({"_id": guild.id})

        if tracker.find_one({"_id": guild.id}):
            tracker.delete_one({"_id": guild.id})

        if ticket.find_one({"_id": guild.id}):
            ticket.delete_one({"_id": guild.id})

        if silence.find_one({"_id": guild.id}):
            silence.delete_one({"_id": guild.id})

        if voicemaster.find_one({"_id": guild.id}):
            voicemaster.delete_one({"_id": guild.id})

        if antispam.find_one({"_id": guild.id}):
            antispam.delete_one({"_id": guild.id})

        if boost.find_one({"_id": guild.id}):
            boost.delete_one({"_id": guild.id})

        if responder.find_one({"_id": guild.id}):
            responder.delete_one({"_id": guild.id})

        if reaction.find_one({"_id": guild.id}):
            reaction.delete_one({"_id": guild.id})

        if levelconfig.find_one({"_id": guild.id}):
            for x in level.find({"server": guild.id}):
                    level.delete_one({"user": x['user'], "server": guild.id})
            levelconfig.delete_one({"_id": guild.id})

async def setup(client):
    await client.add_cog(on_guild(client))
