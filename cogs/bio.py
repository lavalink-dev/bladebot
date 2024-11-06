import discord
import pymongo
from pymongo import MongoClient
from discord.ext import commands
from utils import functions
from utils.emojis import emojis
from utils.color import color

cluster = MongoClient('mongodb+srv://blade:lolidkbruh12333333333@cluster0.wbxaj.mongodb.net/myFirstDatabase?retryWrites=true&w=majority')
db = cluster["blade"]
collection = db["bio"]
premium = db["premium"]
staff = db["staff"]
economy = db["economy"]
marriage = db["marriage"]
blacklist = db["blacklist"]

def blacklist_check():
    def predicate(ctx):
        if blacklist.find_one({'_id': ctx.author.id}):
            return False
        return True
    return commands.check(predicate)

class bio(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['blb', 'biolb'], description='utility')
    @blacklist_check()
    async def bioleaderboard(self, ctx):
        rankings = collection.find().sort("followers",-1)
        i = 1
        embed = discord.Embed(title=f"{emojis.blade} Bio Leaderboard", description=f'\n', color=color.color)
        for x in rankings:
            try:
                temp = self.client.get_user(x["_id"])
                tempxp = x["followers"]
                embed.description += f"``{i}.`` **{temp.name}**: ``{tempxp:,} Followers`` \n"
                i += 1
            except:
                pass
            if i == 11:
                break
        await ctx.send(embed=embed)

    @commands.group(brief='look at members bio',pass_context=True, invoke_without_command=True, description='utility')
    @blacklist_check()
    async def bio(self, ctx, user: discord.User=None):
        if not collection.find_one({"_id": ctx.message.author.id}):
            px = functions.get_prefix(ctx)
            bios = {"_id": ctx.message.author.id, "verified": False, "staff": False, "extra": 'none', "name": 'none', "bio": 'no bio', "instagram": 'none', "twitter": 'none', "tiktok": 'none', "discord": 'none', "website": 'none', "footer": 'none', "thumbnail": 'none', "economy": False, "marriage": False, "followers": 0, "following": []}
            collection.insert_one(bios)

            embed = discord.Embed(description=f'> {emojis.true} Created a **Bio** for you. \n{emojis.reply} use ``{px}bio config`` to set your **Bio** up')
            await ctx.send(embed=embed)

        else:
            if user == None:
                user = ctx.message.author

            if user:
                if not collection.find_one({"_id": user.id}):
                    embed = discord.Embed(description=f'> {emojis.false} {user.mention} dont have a **Bio**')
                    await ctx.send(embed=embed)
                    return

            user = self.client.get_user(user.id)
            check = collection.find_one({"_id": user.id})
            check2 = economy.find_one({"_id": user.id})
            check3 = marriage.find_one({"_id": user.id})

            badge = []
            if staff.find_one({"_id": user.id}):
                badge.append(emojis.blade)
            if check["extra"] != 'none':
                badge.append(f"{check['extra']}")
            if check["verified"] == True:
                badge.append("<a:verified:1044334464005845042>")
            if premium.find_one({"_id": user.id}):
                badge.append("<:dollar:1038593747287560222>")
            if badge == []:
                badge=""

            links = []
            if check['instagram'] != 'none':
                links.append(f'<:insta:1044346513993773126>[instagram]({check["instagram"]})')
            if check['twitter'] != 'none':
                links.append(f'<:twt:1044346549695684658>[twitter]({check["twitter"]})')
            if check['tiktok'] != 'none':
                links.append(f'<:tiktok:1044346585103994951>[tiktok]({check["tiktok"]})')
            if check['website'] != 'none':
                links.append(f'<:website:1045033046715408425>[website]({check["website"]})')
            if check['discord'] != 'none':
                links.append(f'\n<:discord:1045037414386774127>[discord]({check["discord"]})')

            if check['name'] == 'none':
                username = f'{user.name}'
            else:
                username = f"{check['name']}"

            if check['thumbnail'] != 'none':
                thumbnail = f"{check['thumbnail']}"
            else:
                thumbnail = f'{user.display_avatar}'

            async def following_callback(interaction):
                checking = collection.find_one({"_id": user.id})
                checking2 = collection.find_one({"_id": interaction.user.id})

                if user.id in checking2['following']:
                    embed = discord.Embed(description=f'> {emojis.false} You already **Follow** {user.mention}', color=color.fail)
                    await interaction.response.send_message(embed=embed, view=None, ephemeral=True)

                else:
                    collection.update_one({"_id": interaction.user.id}, {"$push": {"following": user.id}})
                    collection.update_one({"_id": user.id}, {"$set": {"followers": checking['followers'] + 1}})
                    embed = discord.Embed(description=f'> {emojis.true} You **Follow** {user.mention} now', color=color.success)
                    await interaction.response.send_message(embed=embed, view=None, ephemeral=True)

            async def unfollowing_callback(interaction):
                checking = collection.find_one({"_id": user.id})
                checking2 = collection.find_one({"_id": interaction.user.id})

                if user.id in checking2['following']:
                    collection.update_one({"_id": interaction.user.id}, {"$pull": {"following": user.id}})
                    collection.update_one({"_id": user.id}, {"$set": {"followers": checking['followers'] - 1}})
                    embed = discord.Embed(description=f'> {emojis.true} You **Unfollowed** {user.mention}', color=color.success)
                    await interaction.response.send_message(embed=embed, view=None, ephemeral=True)

                else:
                    embed = discord.Embed(description=f'> {emojis.false} You dont **Follow** {user.mention}', color=color.fail)
                    await interaction.response.send_message(embed=embed, view=None, ephemeral=True)

            buttons = discord.ui.View()
            follow = discord.ui.Button(style=discord.ButtonStyle.gray, label="Follow")
            unfollow = discord.ui.Button(style=discord.ButtonStyle.gray, label="Unfollow")
            follow.callback = following_callback
            unfollow.callback = unfollowing_callback

            if badge == []:
                badge = ''
            else:
                badge="・" + " ".join(emoji for emoji in badge)

            embed = discord.Embed(description=f"`{username}` | ``{check['followers']} Followers`` {badge}\n{check['bio']}", color=color.color)
            embed.set_thumbnail(url=thumbnail)
            embed.set_author(name=f"{user.name}", url="https://bladecord.com/", icon_url=user.display_avatar)

            if links != []:
                link=" ".join(links)
                embed.add_field(name="links", value=f"{link}", inline=True)

            if check['economy'] == True or check['marriage'] == True:
                extras = ''
                if check['economy'] == True:
                    extras += f'**bal**: ``{check2["money"]:,}💵``'
                if check['marriage'] == True:
                    try:
                        if check3["married"] != 0:
                            user = self.client.get_user(check3['married'])
                            extras += f'\nmarried to **{user.name}**'
                        else:
                            extras += f'\nnot married'
                    except:
                        extras += f'\nnot married'
                embed.add_field(name="extra", value=f"{extras}", inline=True)

            if check["footer"] != 'none':
                embed.set_footer(text=f'{check["footer"]}')

            if user.id == ctx.message.author.id:
                await ctx.send(embed=embed)
            else:
                checking = collection.find_one({"_id": ctx.message.author.id})
                if user.id in checking['following']:
                    buttons.add_item(item=unfollow)
                    await ctx.send(embed=embed, view=buttons)

                else:
                    buttons.add_item(item=follow)
                    await ctx.send(embed=embed, view=buttons)

    @bio.command(brief='configurate your bio')
    @blacklist_check()
    async def config(self, ctx):
        if not collection.find_one({"_id": ctx.message.author.id}):
            embed = discord.Embed(description=f'> {emojis.false} Type ``{px}bio`` before setting up **Profile** up', color=color.color)
            await ctx.send(embed=embed)
        else:
            check = collection.find_one({"_id": ctx.message.author.id})
            px = functions.get_prefix(ctx)

            embed = discord.Embed(title=f'{emojis.blade} Bio',
            description=f'{emojis.reply} *setup your profile*')
            embed.add_field(name=f"{emojis.config} Bio:", value=f"{check['bio']}", inline=False)
            embed.add_field(name=f"{emojis.config} Links:", value=f'> ``Instagram``: {check["instagram"]} \n> ``Twitter``: {check["twitter"]} \n> ``TikTok``: {check["tiktok"]} \n> ``Discord``: {check["discord"]} \n> ``Website``: {check["website"]}', inline=False)
            embed.add_field(name=f"{emojis.config} Usage:", value=f"> ``{px}bio message [message]`` set your bio message \n> ``{px}bio link [link] [username]`` set your links \n> ``{px}bio name [name]`` change the name next from your badges \n> ``{px}bio footer [text]`` add a custom footer \n> ``{px}bio thumbnail [image-link]`` change the thumbnail image \n> ``{px}bio add [economy/marriage]`` add your economy or marriage to your profile \n> ``{px}bio remove [function]`` remove links or economy/marriage", inline=False)
            await ctx.send(embed=embed)

    @bio.command(brief='set a custom name')
    @blacklist_check()
    async def name(self, ctx, *, name=None):
        if not collection.find_one({"_id": ctx.message.author.id}):
            px = functions.get_prefix(ctx)
            embed = discord.Embed(description=f'> {emojis.false} Type ``{px}bio`` before setting up **Profile** up', color=color.fail)
            await ctx.send(embed=embed)
        else:
            if premium.find_one({"_id": ctx.message.author.id}):
                if name == None:
                    embed = discord.Embed(description=f'> {emojis.false} Please provide a **Name**', color=color.fail)
                    await ctx.send(embed=embed)
                else:
                    if len(name)> 32:
                        embed = discord.Embed(description=f'> {emojis.false} You can set your **Bio** with only ``32`` Characters', color=color.fail)
                        await ctx.send(embed=embed)
                    else:
                        collection.update_one({"_id": ctx.message.author.id}, {"$set": {"name": name}})
                        embed = discord.Embed(description=f'> {emojis.true} Set your **Bio** name to: ``{name}``', color=color.success)
                        await ctx.send(embed=embed)
            else:
                px = functions.get_prefix(ctx)
                embed = discord.Embed(description=f'> {emojis.false} This command is a **Premium** only feature, to learn more about it, join our [``Support Server``](https://discord.gg/snore)', color=color.color)
                await ctx.send(embed=embed)

    @bio.command(brief='set your own footer')
    @blacklist_check()
    async def footer(self, ctx, *, text=None):
        if not collection.find_one({"_id": ctx.message.author.id}):
            px = functions.get_prefix(ctx)
            embed = discord.Embed(description=f'> {emojis.false} Type ``{px}bio`` before setting up **Profile** up', color=color.fail)
            await ctx.send(embed=embed)
        else:
            if premium.find_one({"_id": ctx.message.author.id}):
                if text == None:
                    embed = discord.Embed(description=f'> {emojis.false} Please provide a **Name**', color=color.fail)
                    await ctx.send(embed=embed)
                else:
                    if len(text)> 50:
                        embed = discord.Embed(description=f'> {emojis.false} You can set your **Bio** with only ``50`` Characters', color=color.fail)
                        await ctx.send(embed=embed)
                    else:
                        collection.update_one({"_id": ctx.message.author.id}, {"$set": {"footer": text}})
                        embed = discord.Embed(description=f'> {emojis.true} Set you **Bio** footer to ``{text}``', color=color.__text_signature__)
                        await ctx.send(embed=embed)
            else:
                px = functions.get_prefix(ctx)
                embed = discord.Embed(description=f'> {emojis.false} This command is a **Premium** only feature, to learn more about it, join our [``Support Server``](https://discord.gg/snore)', color=color.color)
                await ctx.send(embed=embed)

    @bio.command(brief='set a custom thumbnail')
    @blacklist_check()
    async def thumbnail(self, ctx, content=None):
        if not collection.find_one({"_id": ctx.message.author.id}):
            px = functions.get_prefix(ctx)
            embed = discord.Embed(description=f'> {emojis.false} Type ``{px}bio`` before setting up **Profile** up', color=color.fail)
            await ctx.send(embed=embed)
        else:
            if premium.find_one({"_id": ctx.message.author.id}):
                if content == None:
                    await ctx.send('nuh uh uh, you need to send an image link')
                    return
                
                collection.update_one({"_id": ctx.message.author.id}, {"$set": {"thumbnail": content}})
                embed = discord.Embed(description=f'> {emojis.true} Changed your Bio **Thumbnail** to', color=color.success)
                embed.set_image(url=content)
                await ctx.send(embed=embed)
            else:
                px = functions.get_prefix(ctx)
                embed = discord.Embed(description=f'> {emojis.false} This command is a **Premium** only feature, to learn more about it, join our [``Support Server``](https://discord.gg/snore)', color=color.color)
                await ctx.send(embed=embed)

    @bio.command(brief='add economy or marriage to your bio')
    @blacklist_check()
    async def add(self, ctx, function=None):
        if not collection.find_one({"_id": ctx.message.author.id}):
            px = functions.get_prefix(ctx)
            embed = discord.Embed(description=f'> {emojis.false} Type ``{px}bio`` before setting up **Profile** up', color=color.fail)
            await ctx.send(embed=embed)
        else:
            if function == None:
                embed = discord.Embed(description=f'> {emojis.false} Please provide a **Function**', color=color.fail)
                await ctx.send(embed=embed)
            if function == 'economy':
                collection.update_one({"_id": ctx.message.author.id}, {"$set": {"economy": True}})
                embed = discord.Embed(description=f'> {emojis.true} Added **Economy** to your **Bio**', color=color.success)
                await ctx.send(embed=embed)
            elif function == 'marriage':
                collection.update_one({"_id": ctx.message.author.id}, {"$set": {"marriage": True}})
                embed = discord.Embed(description=f'> {emojis.true} Added **Marriage** to your **Bio**', color=color.success)
                await ctx.send(embed=embed)
            else:
                embed = discord.Embed(description=f'> {emojis.false} You cant add ``{function}`` to your **Bio**', color=color.fail)
                await ctx.send(embed=embed)


    @bio.command(brief='remove things from your bio')
    @blacklist_check()
    async def remove(self, ctx, function=None):
        if not collection.find_one({"_id": ctx.message.author.id}):
            px = functions.get_prefix(ctx)
            embed = discord.Embed(description=f'> {emojis.false} Type ``{px}bio`` before setting up **Profile** up', color=color.fail)
            await ctx.send(embed=embed)
        else:
            if function == 'bio':
                collection.update_one({"_id": ctx.message.author.id}, {"$set": {"bio": 'none'}})
                embed = discord.Embed(description=f'> {emojis.true} Removed **Economy** from your **Bio**', color=color.success)
                await ctx.send(embed=embed)
            elif function == 'name':
                collection.update_one({"_id": ctx.message.author.id}, {"$set": {"name": 'none'}})
                embed = discord.Embed(description=f'> {emojis.true} Removed your **Name** from your **Bio**', color=color.success)
                await ctx.send(embed=embed)
            elif function == 'thumbnail' or function == 'image':
                collection.update_one({"_id": ctx.message.author.id}, {"$set": {"thumbnail": 'none'}})
                embed = discord.Embed(description=f'> {emojis.true} Removed your **Thumbnail** from your **Bio**', color=color.success)
                await ctx.send(embed=embed)
            elif function == 'footer':
                collection.update_one({"_id": ctx.message.author.id}, {"$set": {"footer": 'none'}})
                embed = discord.Embed(description=f'> {emojis.true} Removed your **Footer** from your **Bio**', color=color.success)
                await ctx.send(embed=embed)

            elif function == 'economy':
                collection.update_one({"_id": ctx.message.author.id}, {"$set": {"economy": False}})
                embed = discord.Embed(description=f'> {emojis.true} Removed your **Bio message** from your **Bio**', color=color.success)
                await ctx.send(embed=embed)
            elif function == 'marriage':
                collection.update_one({"_id": ctx.message.author.id}, {"$set": {"marriage": False}})
                embed = discord.Embed(description=f'> {emojis.true} Removed **Marriage** from your **Bio**', color=color.success)
                await ctx.send(embed=embed)

            elif function == 'insta' or function == 'instagram' or function == 'ig':
                collection.update_one({"_id": ctx.message.author.id}, {"$set": {"instagram": 'none'}})
                embed = discord.Embed(description=f'> {emojis.true} Removed your **Instagram** Link', color=color.success)
                await ctx.send(embed=embed)
            elif function == 'twitter' or function == 'twt':
                collection.update_one({"_id": ctx.message.author.id}, {"$set": {"twitter": 'none'}})
                embed = discord.Embed(description=f'> {emojis.true} Removed your **Twitter** Link', color=color.success)
                await ctx.send(embed=embed)
            elif function == 'tiktok' or function == 'tt':
                collection.update_one({"_id": ctx.message.author.id}, {"$set": {"tiktok": 'none'}})
                embed = discord.Embed(description=f'> {emojis.true} Removed your **TikTok** Link', color=color.success)
                await ctx.send(embed=embed)
            else:
                embed = discord.Embed(description=f'> {emojis.false} You cant remove ``{function}`` as a **Link** in your **Bio**', color=color.fail)
                await ctx.send(embed=embed)

    @bio.command(brief='add socials to your bio')
    @blacklist_check()
    async def link(self, ctx, link=None, name=None):
        if not collection.find_one({"_id": ctx.message.author.id}):
            px = functions.get_prefix(ctx)
            embed = discord.Embed(description=f'> {emojis.false} Type ``{px}bio`` before setting up **Profile** up', color=color.fail)
            await ctx.send(embed=embed)
        else:
            if link == 'insta' or link == 'instagram' or link == 'ig':
                if name == None:
                    embed = discord.Embed(description=f'> {emojis.false} Please provide a **Name**', color=color.fail)
                    await ctx.send(embed=embed)
                elif 'https://' in name or '.com' in name or '@' in name:
                    embed = discord.Embed(description=f'> {emojis.false} Please just type your **User**', color=color.fail)
                    await ctx.send(embed=embed)
                else:
                    collection.update_one({"_id": ctx.message.author.id}, {"$set": {"instagram": f'https://instagram.com/{name}'}})
                    embed = discord.Embed(description=f'> {emojis.true} Set [``@{name}``](https://instagram.com/{name}) as **Instagram** link', color=color.success)
                    await ctx.send(embed=embed)

            elif link == 'twitter' or link == 'twt':
                if name == None:
                    embed = discord.Embed(description=f'> {emojis.false} Please provide a **Name**', color=color.fail)
                    await ctx.send(embed=embed)
                elif 'https://' in name or '.com' in name or '@' in name:
                    embed = discord.Embed(description=f'> {emojis.false} Please just type your **User**', color=color.fail)
                    await ctx.send(embed=embed)
                else:
                    collection.update_one({"_id": ctx.message.author.id}, {"$set": {"twitter": f'https://twitter.com/{name}'}})
                    embed = discord.Embed(description=f'> {emojis.true} Set [``@{name}``](https://twitter.com/{name}) as **Twitter** link', color=color.success)
                    await ctx.send(embed=embed)

            elif link == 'tiktok' or link == 'tt':
                if name == None:
                    embed = discord.Embed(description=f'> {emojis.false} Please provide a **Name**', color=color.fail)
                    await ctx.send(embed=embed)
                elif 'https://' in name or '.com' in name or '@' in name:
                    embed = discord.Embed(description=f'> {emojis.false} Please just type your **User**', color=color.fail)
                    await ctx.send(embed=embed)
                else:
                    collection.update_one({"_id": ctx.message.author.id}, {"$set": {"tiktok": f'https://tiktok.com/@{name}'}})
                    embed = discord.Embed(description=f'> {emojis.true} Set [``@{name}``](https://tiktok.com/@{name}) as **TikTok** link', color=color.success)
                    await ctx.send(embed=embed)

            elif link == 'website' or link == 'web':
                if name == None:
                    embed = discord.Embed(description=f'> {emojis.false} Please provide a **Link**', color=color.fail)
                    await ctx.send(embed=embed)
                elif 'https://' in name or 'http://' in name:
                    collection.update_one({"_id": ctx.message.author.id}, {"$set": {"website": f'{name}'}})
                    embed = discord.Embed(description=f'> {emojis.true} Set [``{name}``]({name}) as your **Website**', color=color.success)
                    await ctx.send(embed=embed)
                else:
                    embed = discord.Embed(description=f'> {emojis.false} Please send your **Website URL** with **https://**', color=color.fail)
                    await ctx.send(embed=embed)

            elif link == 'discord' or link == 'dc':
                if name == None:
                    embed = discord.Embed(description=f'> {emojis.false} Please provide a **Link**', color=color.fail)
                    await ctx.send(embed=embed)
                elif 'https://' in name or 'http://' in name:
                    collection.update_one({"_id": ctx.message.author.id}, {"$set": {"discord": f'{name}'}})
                    embed = discord.Embed(description=f'> {emojis.true} Set [``{name}``]({name}) as your **Server Invite**', color=color.success)
                    await ctx.send(embed=embed)
                else:
                    embed = discord.Embed(description=f'> {emojis.false} Please send your **Server Invite** with **https://**', color=color.fail)
                    await ctx.send(embed=embed)


            else:
                embed = discord.Embed(description=f'> {emojis.false} You cant add ``{link}`` as a **Link** in your **Bio**.', color=color.fail)
                await ctx.send(embed=embed)

    @bio.command(brief='set a custom message')
    @blacklist_check()
    async def message(self, ctx, *, bio=None):
        if not collection.find_one({"_id": ctx.message.author.id}):
            px = functions.get_prefix(ctx)
            embed = discord.Embed(description=f'> {emojis.false} Type ``{px}bio`` before setting up **Profile** up', color=color.fail)
            await ctx.send(embed=embed)
        else:
            if bio == None:
                embed = discord.Embed(description=f'> {emojis.false} Please provide a **Bio**', color=color.fail)
                await ctx.send(embed=embed)
            else:
                if len(bio)> 120:
                    embed = discord.Embed(description=f'> {emojis.false} You can set your **Bio** with only ``120`` Characters', color=color.fail)
                    await ctx.send(embed=embed)
                else:
                    collection.update_one({"_id": ctx.message.author.id}, {"$set": {"bio": bio}})
                    embed = discord.Embed(description=f'> {emojis.true} Your **Bio** got set to: \n ``{bio}``', color=color.success)
                    await ctx.send(embed=embed)

async def setup(client):
    await client.add_cog(bio(client))
