import discord
import aiohttp
import json
import pymongo
from pymongo import MongoClient
from discord.ext import commands, tasks
from utils import functions
from utils.emojis import emojis
from utils.color import color

apikey = "43693facbb24d1ac893a7d33846b15cc"

cluster = MongoClient('mongodb+srv://blade:lolidkbruh12333333333@cluster0.wbxaj.mongodb.net/myFirstDatabase?retryWrites=true&w=majority')
db = cluster["blade"]
collection = db["lastfm"]
bing = db["lastfm_bing"]
blacklist = db["blacklist"]

def blacklist_check():
    def predicate(ctx):
        if blacklist.find_one({'_id': ctx.author.id}):
            return False
        return True
    return commands.check(predicate)

class lastfm(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.group(pass_context=True, invoke_without_command=True, aliases=['lfm', 'lf'], brief='configurate lastfm', description='lastfm')
    async def lastfm(self, ctx):
        await ctx.invoke()

    @lastfm.command(brief='configurate your lastfm user', description='lastfm')
    async def user(self, ctx, user=None):
        if not collection.find_one({"_id": ctx.message.author.id}):
            economy = {"_id": ctx.message.author.id, "user": 'not set'}
            collection.insert_one(economy)

        check = collection.find_one({"_id": ctx.message.author.id})
        px = functions.get_prefix(ctx)

        if user == None:
            embed = discord.Embed(title=f'{emojis.blade} LastFM', color=color.color,
            description=f'{emojis.reply} *configurate your lastfm user*')
            embed.add_field(name=f'{emojis.commands} Commands:', value=f"> ``{px}lastfm user [user]`` set your lastfm user", inline=False)
            await ctx.send(embed=embed)

        else:
            if len(user) > 16:
                embed = discord.Embed(description=f'> {emojis.false} The **Length** of your **User** is to long', color=color.fail)
                await ctx.send(embed=embed)

            else:
                collection.update_one({"_id": ctx.message.author.id}, {"$set": {"user": user}})
                embed = discord.Embed(description=f'> {emojis.true} **Successfully** set your **LastFM User** to [``{user}``](https://last.fm/user/{user})', color=color.success)
                await ctx.send(embed=embed)

    @commands.command(aliases=['np'], description='lastfm', brief='get your last playing song')
    @blacklist_check()
    async def nowplaying(self, ctx, member: discord.Member=None):
        if member == None:
            member = ctx.message.author

        if collection.find_one({"_id": member.id}):
            check = collection.find_one({"_id": member.id})
            user = check['user']

            if user == 'not set':
                embed = discord.Embed(description=f'> {emojis.false} {member.mention} didnt configurate their **LastFM**', color=color.fail)
                await ctx.send(embed=embed)
                return

            else:
                async with aiohttp.ClientSession() as cs:
                    async with cs.get(f"https://ws.audioscrobbler.com/2.0/?method=user.getrecenttracks&user={user}&api_key={apikey}&format=json&limit=1") as r:
                        data = await r.json()
                        artist = data['recenttracks']['track'][0]['artist']['#text']
                        artist_name = data['recenttracks']['track'][0]['artist']['#text'].replace(" ", "+")
                        album = data['recenttracks']['track'][0]['album']['#text'] or "N/A"
                        album_name = data['recenttracks']['track'][0]['album']['#text'].replace(" ", "+")
                        album_artist = data['recenttracks']['track'][0]['artist']['#text'].replace(" ", "+")
                        album_url = f'https://last.fm/music/{album_artist}/{album_name}'
                        track = data['recenttracks']['track'][0]['name']
                        track_url = data['recenttracks']['track'][0]['url']

                        async with aiohttp.ClientSession() as cs:
                            async with cs.get(f"https://ws.audioscrobbler.com/2.0/?method=track.getInfo&api_key={apikey}&artist={artist}&track={track.lower()}&format=json&username={user}") as r:
                                d = await r.json()
                                plays = d['track']['userplaycount']


                        embed = discord.Embed(title=f'***{track}***', url=f'https://last.fm/music/{artist_name}', color=color.color,
                        description=f'{emojis.reply2} **artist**: [{artist}](https://last.fm/music/{artist_name}) \n{emojis.reply} **album**: [{album}](https://last.fm/music/{album_artist}/{album_name})')
                        embed.set_author(name=f"{member.name}'s most recent", icon_url=member.display_avatar)
                        embed.set_thumbnail(url=(data['recenttracks']['track'][0])['image'][3]['#text'])
                        embed.set_footer(text=f'{plays} plays')
                        await ctx.send(embed=embed)

        else:
            embed = discord.Embed(description=f'> {emojis.false} {member.mention} didnt configurate their **LastFM**', color=color.fail)
            await ctx.send(embed=embed)

    @commands.command(aliases=["lfu"], brief='update your lastfm', description='lastfm')
    @commands.cooldown(1, 4, commands.BucketType.user)
    async def lastfmupdate(self, ctx):
        member = ctx.message.author

        #-track.updateNowPlaying
        if collection.find_one({"_id": member.id}):
            check = collection.find_one({"_id": member.id})
            user = check['user']

            if user == 'not set':
                embed = discord.Embed(description=f'> {emojis.false} {member.mention} didnt configurate their **LastFM**', color=color.fail)
                await ctx.send(embed=embed)
                return
            
            else:
                 async with aiohttp.ClientSession() as cs:
                    async with cs.get(f"https://ws.audioscrobbler.com/2.0/?method=user.getweeklyartistchart&user={user}&api_key={apikey}&format=json") as r:
                        data = await r.json()

                        embed = discord.Embed(description=f'> {emojis.true} Updated your **LastFM**', color=color.success)
                        await ctx.send(embed=embed)   

        else:
            embed = discord.Embed(description=f'> {emojis.false} {member.mention} didnt configurate their **LastFM**', color=color.fail)
            await ctx.send(embed=embed)

    @commands.command(aliases = ['wa'], brief='see your weekly artists', description='lastfm')
    @commands.cooldown(1, 4, commands.BucketType.user)
    @blacklist_check()
    async def weeklyartists(self, ctx, member: discord.Member = None):
        if member == None:
            member = ctx.author
        if collection.find_one({"_id": member.id}):
            check = collection.find_one({"_id": member.id})
            user = check['user']

            if user == 'not set':
                embed = discord.Embed(description=f'> {emojis.false} {member.mention} didnt configurate their **LastFM**', color=color.fail)
                await ctx.send(embed=embed)
                return
            
            else:
                 async with aiohttp.ClientSession() as cs:
                    async with cs.get(f"https://ws.audioscrobbler.com/2.0/?method=user.getweeklyartistchart&user={user}&api_key={apikey}&format=json") as r:
                        data = await r.json()
                        topartist1 = data["weeklyartistchart"]["artist"][0]["name"]
                        topartist2 = data["weeklyartistchart"]["artist"][1]["name"]
                        topartist3 = data["weeklyartistchart"]["artist"][2]["name"]
                        topartist4 = data["weeklyartistchart"]["artist"][3]["name"]
                        topartist5 = data["weeklyartistchart"]["artist"][4]["name"]
                        topartist6 = data["weeklyartistchart"]["artist"][5]["name"]
                        topartist7 = data["weeklyartistchart"]["artist"][6]["name"]
                        topartist8 = data["weeklyartistchart"]["artist"][7]["name"]
                        topartist9 = data["weeklyartistchart"]["artist"][8]["name"]
                        topartist10 = data["weeklyartistchart"]["artist"][9]["name"]
                        topartist1url = data["weeklyartistchart"]["artist"][0]["url"]
                        topartist2url = data["weeklyartistchart"]["artist"][1]["url"]
                        topartist3url = data["weeklyartistchart"]["artist"][2]["url"]
                        topartist4url = data["weeklyartistchart"]["artist"][3]["url"]
                        topartist5url = data["weeklyartistchart"]["artist"][4]["url"]
                        topartist6url = data["weeklyartistchart"]["artist"][5]["url"]
                        topartist7url = data["weeklyartistchart"]["artist"][6]["url"]
                        topartist8url = data["weeklyartistchart"]["artist"][7]["url"]
                        topartist9url = data["weeklyartistchart"]["artist"][8]["url"]
                        topartist10url = data["weeklyartistchart"]["artist"][9]["url"]
                        topartist1plays = data["weeklyartistchart"]["artist"][0]["playcount"]
                        topartist2plays = data["weeklyartistchart"]["artist"][1]["playcount"]
                        topartist3plays = data["weeklyartistchart"]["artist"][2]["playcount"]
                        topartist4plays = data["weeklyartistchart"]["artist"][3]["playcount"]
                        topartist5plays = data["weeklyartistchart"]["artist"][4]["playcount"]
                        topartist6plays = data["weeklyartistchart"]["artist"][5]["playcount"]
                        topartist7plays = data["weeklyartistchart"]["artist"][6]["playcount"]
                        topartist8plays = data["weeklyartistchart"]["artist"][7]["playcount"]
                        topartist9plays = data["weeklyartistchart"]["artist"][8]["playcount"]
                        topartist10plays = data["weeklyartistchart"]["artist"][9]["playcount"]

                        embed = discord.Embed(description = f"`1.` **[{topartist1}]({topartist1url})** {topartist1plays} plays \n `2.` **[{topartist2}]({topartist2url})** {topartist2plays} plays \n `3.` **[{topartist3}]({topartist3url})** {topartist3plays} plays \n `4.` **[{topartist4}]({topartist4url})** {topartist4plays} plays \n `5.` **[{topartist5}]({topartist5url})** {topartist5plays} plays \n `6.` **[{topartist6}]({topartist6url})** {topartist6plays} plays \n `7.` **[{topartist7}]({topartist7url})** {topartist7plays} plays\n `8.`	**[{topartist8}]({topartist8url})** {topartist8plays} plays\n `9.` **[{topartist9}]({topartist9url})** {topartist9plays} plays\n `10.` **[{topartist10}]({topartist10url})** {topartist10plays} plays", color=color.color)
                        embed.set_thumbnail(url = member.display_avatar)
                        embed.set_author(name = f"{ctx.author.name}'s weekly artists", icon_url = member.display_avatar)
                        await ctx.send(embed=embed)   

        else:
            embed = discord.Embed(description=f'> {emojis.false} {member.mention} didnt configurate their **LastFM**', color=color.fail)
            await ctx.send(embed=embed)

    @commands.command(aliases = ['wtr'], brief="check a member's top 10 tracks", description="lastfm")
    @commands.cooldown(1, 4, commands.BucketType.user)
    @blacklist_check()
    async def weeklytracks(self, ctx, *, member: discord.Member=None):
        if member == None:
            member = ctx.author
        if collection.find_one({"_id": member.id}):
            check = collection.find_one({"_id": member.id})
            user = check['user']

            if user == 'not set':
                embed = discord.Embed(description=f'> {emojis.false} {member.mention} didnt configurate their **LastFM**', color=color.fail)
                await ctx.send(embed=embed)
                return
            
            else:
                 async with aiohttp.ClientSession() as cs:
                    async with cs.get(f"https://ws.audioscrobbler.com/2.0/?method=user.getweeklytrackchart&user={user}&api_key={apikey}&format=json") as r:
                        data = await r.json()
                        toptrack1 = data["weeklytrackchart"]["track"][0]["name"]
                        toptrack2 = data["weeklytrackchart"]["track"][1]["name"]
                        toptrack3 = data["weeklytrackchart"]["track"][2]["name"]
                        toptrack4 = data["weeklytrackchart"]["track"][3]["name"]
                        toptrack5 = data["weeklytrackchart"]["track"][4]["name"]
                        toptrack6 = data["weeklytrackchart"]["track"][5]["name"]
                        toptrack7 = data["weeklytrackchart"]["track"][6]["name"]
                        toptrack8 = data["weeklytrackchart"]["track"][7]["name"]
                        toptrack9 = data["weeklytrackchart"]["track"][8]["name"]
                        toptrack10 = data["weeklytrackchart"]["track"][9]["name"]
                        toptrack1url = data["weeklytrackchart"]["track"][0]["url"]
                        toptrack2url = data["weeklytrackchart"]["track"][1]["url"]
                        toptrack3url = data["weeklytrackchart"]["track"][2]["url"]
                        toptrack4url = data["weeklytrackchart"]["track"][3]["url"]
                        toptrack5url = data["weeklytrackchart"]["track"][4]["url"]
                        toptrack6url = data["weeklytrackchart"]["track"][5]["url"]
                        toptrack7url = data["weeklytrackchart"]["track"][6]["url"]
                        toptrack8url = data["weeklytrackchart"]["track"][7]["url"]
                        toptrack9url = data["weeklytrackchart"]["track"][8]["url"]
                        toptrack10url = data["weeklytrackchart"]["track"][9]["url"]
                        toptrack1plays = data["weeklytrackchart"]["track"][0]["playcount"]
                        toptrack2plays = data["weeklytrackchart"]["track"][1]["playcount"]
                        toptrack3plays = data["weeklytrackchart"]["track"][2]["playcount"]
                        toptrack4plays = data["weeklytrackchart"]["track"][3]["playcount"]
                        toptrack5plays = data["weeklytrackchart"]["track"][4]["playcount"]
                        toptrack6plays = data["weeklytrackchart"]["track"][5]["playcount"]
                        toptrack7plays = data["weeklytrackchart"]["track"][6]["playcount"]
                        toptrack8plays = data["weeklytrackchart"]["track"][7]["playcount"]
                        toptrack9plays = data["weeklytrackchart"]["track"][8]["playcount"]
                        toptrack10plays = data["weeklytrackchart"]["track"][9]["playcount"]
                        embed = discord.Embed(description = f"`1` **[{toptrack1}]({toptrack1url})** {toptrack1plays} plays\n`2.` **[{toptrack2}]({toptrack2url})** {toptrack2plays} plays\n`3.` **[{toptrack3}]({toptrack3url})** {toptrack3plays} plays\n`4.` **[{toptrack4}]({toptrack4url})** {toptrack4plays} plays\n`5.` **[{toptrack5}]({toptrack5url})** {toptrack5plays} plays\n`6.` **[{toptrack6}]({toptrack6url})** {toptrack6plays} plays\n`7.` **[{toptrack7}]({toptrack7url})** {toptrack7plays} plays\n`8.`	**[{toptrack8}]({toptrack8url})** {toptrack8plays} plays\n`9.` **[{toptrack9}]({toptrack9url})** {toptrack9plays} plays\n`10.` **[{toptrack10}]({toptrack10url})** {toptrack10plays} plays", color=color.color)
                        embed.set_thumbnail(url = ctx.message.author.avatar)
                        embed.set_author(name = f"{ctx.message.author.name}'s weekly top tracks", icon_url = ctx.message.author.avatar)
                        await ctx.send(embed=embed)

        else:
            embed = discord.Embed(description=f'> {emojis.false} {member.mention} didnt configurate their **LastFM**', color=color.fail)
            await ctx.send(embed=embed)

    @commands.command(aliases = ['ta'], brief='check users top artists', description='lastfm')
    @commands.cooldown(1, 4, commands.BucketType.user)
    @blacklist_check()
    async def topartists(self, ctx, member: discord.Member = None):
        if member == None:
            member = ctx.author
        if collection.find_one({"_id": member.id}):
            check = collection.find_one({"_id": member.id})
            user = check['user']

            if user == 'not set':
                embed = discord.Embed(description=f'> {emojis.false} {member.mention} didnt configurate their **LastFM**', color=color.fail)
                await ctx.send(embed=embed)
                return
            
            else:
                 async with aiohttp.ClientSession() as cs:
                    async with cs.get(f"https://ws.audioscrobbler.com/2.0/?method=user.gettopartists&user={user}&api_key={apikey}&format=json") as r:
                        data = await r.json()
                        topartist1 = data["topartists"]["artist"][0]["name"]
                        topartist2 = data["topartists"]["artist"][1]["name"]
                        topartist3 = data["topartists"]["artist"][2]["name"]
                        topartist4 = data["topartists"]["artist"][3]["name"]
                        topartist5 = data["topartists"]["artist"][4]["name"]
                        topartist6 = data["topartists"]["artist"][5]["name"]
                        topartist7 = data["topartists"]["artist"][6]["name"]
                        topartist8 = data["topartists"]["artist"][7]["name"]
                        topartist9 = data["topartists"]["artist"][8]["name"]
                        topartist10 = data["topartists"]["artist"][9]["name"]
                        topartist1url = data["topartists"]["artist"][0]["url"]
                        topartist2url = data["topartists"]["artist"][1]["url"]
                        topartist3url = data["topartists"]["artist"][2]["url"]
                        topartist4url = data["topartists"]["artist"][3]["url"]
                        topartist5url = data["topartists"]["artist"][4]["url"]
                        topartist6url = data["topartists"]["artist"][5]["url"]
                        topartist7url = data["topartists"]["artist"][6]["url"]
                        topartist8url = data["topartists"]["artist"][7]["url"]
                        topartist9url = data["topartists"]["artist"][8]["url"]
                        topartist10url = data["topartists"]["artist"][9]["url"]
                        topartist1plays = data["topartists"]["artist"][0]["playcount"]
                        topartist2plays = data["topartists"]["artist"][1]["playcount"]
                        topartist3plays = data["topartists"]["artist"][2]["playcount"]
                        topartist4plays = data["topartists"]["artist"][3]["playcount"]
                        topartist5plays = data["topartists"]["artist"][4]["playcount"]
                        topartist6plays = data["topartists"]["artist"][5]["playcount"]
                        topartist7plays = data["topartists"]["artist"][6]["playcount"]
                        topartist8plays = data["topartists"]["artist"][7]["playcount"]
                        topartist9plays = data["topartists"]["artist"][8]["playcount"]
                        topartist10plays = data["topartists"]["artist"][9]["playcount"]

                        embed = discord.Embed(description = f"`1.` **[{topartist1}]({topartist1url})** {topartist1plays} plays \n `2.` **[{topartist2}]({topartist2url})** {topartist2plays} plays \n `3.` **[{topartist3}]({topartist3url})** {topartist3plays} plays \n `4.` **[{topartist4}]({topartist4url})** {topartist4plays} plays \n `5.` **[{topartist5}]({topartist5url})** {topartist5plays} plays \n `6.` **[{topartist6}]({topartist6url})** {topartist6plays} plays \n `7.` **[{topartist7}]({topartist7url})** {topartist7plays} plays\n `8.`	**[{topartist8}]({topartist8url})** {topartist8plays} plays\n `9.` **[{topartist9}]({topartist9url})** {topartist9plays} plays\n `10.` **[{topartist10}]({topartist10url})** {topartist10plays} plays", color=color.color)
                        embed.set_thumbnail(url = member.display_avatar)
                        embed.set_author(name = f"{ctx.author.name}'s overall top artists", icon_url = member.display_avatar)
                        await ctx.send(embed=embed)   

        else:
            embed = discord.Embed(description=f'> {emojis.false} {member.mention} didnt configurate their **LastFM**', color=color.fail)
            await ctx.send(embed=embed)


    @commands.command(aliases = ['tal'], brief='check users top albums', description='lastfm')
    @commands.cooldown(1, 4, commands.BucketType.user)
    @blacklist_check()
    async def topalbums(self,ctx, *, member: discord.Member=None):
        if member == None:
            member = ctx.author
        if collection.find_one({"_id": member.id}):
            check = collection.find_one({"_id": member.id})
            user = check['user']

            if user == 'not set':
                embed = discord.Embed(description=f'> {emojis.false} {member.mention} didnt configurate their **LastFM**', color=color.fail)
                await ctx.send(embed=embed)
                return
            
            else:
                 async with aiohttp.ClientSession() as cs:
                    async with cs.get(f"https://ws.audioscrobbler.com/2.0/?method=user.gettopalbums&user={user}&api_key={apikey}&format=json") as r:
                        data = await r.json()
                        topalbum1 = data["topalbums"]["album"][0]["name"]
                        topalbum2 = data["topalbums"]["album"][1]["name"]
                        topalbum3 = data["topalbums"]["album"][2]["name"]
                        topalbum4 = data["topalbums"]["album"][3]["name"]
                        topalbum5 = data["topalbums"]["album"][4]["name"]
                        topalbum6 = data["topalbums"]["album"][5]["name"]
                        topalbum7 = data["topalbums"]["album"][6]["name"]
                        topalbum8 = data["topalbums"]["album"][7]["name"]
                        topalbum9 = data["topalbums"]["album"][8]["name"]
                        topalbum10 = data["topalbums"]["album"][9]["name"]
                        topalbum1url = data["topalbums"]["album"][0]["url"]
                        topalbum2url = data["topalbums"]["album"][1]["url"]
                        topalbum3url = data["topalbums"]["album"][2]["url"]
                        topalbum4url = data["topalbums"]["album"][3]["url"]
                        topalbum5url = data["topalbums"]["album"][4]["url"]
                        topalbum6url = data["topalbums"]["album"][5]["url"]
                        topalbum7url = data["topalbums"]["album"][6]["url"]
                        topalbum8url = data["topalbums"]["album"][7]["url"]
                        topalbum9url = data["topalbums"]["album"][8]["url"]
                        topalbum10url = data["topalbums"]["album"][9]["url"]
                        topalbum1plays = data["topalbums"]["album"][0]["playcount"]
                        topalbum2plays = data["topalbums"]["album"][1]["playcount"]
                        topalbum3plays = data["topalbums"]["album"][2]["playcount"]
                        topalbum4plays = data["topalbums"]["album"][3]["playcount"]
                        topalbum5plays = data["topalbums"]["album"][4]["playcount"]
                        topalbum6plays = data["topalbums"]["album"][5]["playcount"]
                        topalbum7plays = data["topalbums"]["album"][6]["playcount"]
                        topalbum8plays = data["topalbums"]["album"][7]["playcount"]
                        topalbum9plays = data["topalbums"]["album"][8]["playcount"]
                        topalbum10plays = data["topalbums"]["album"][9]["playcount"]
                        embed = discord.Embed(description = f"`1.` **[{topalbum1}]({topalbum1url})** {topalbum1plays} plays\n `2.` **[{topalbum2}]({topalbum2url})** {topalbum2plays} plays\n `3.` **[{topalbum3}]({topalbum3url})** {topalbum3plays} plays\n `4.` **[{topalbum4}]({topalbum4url})** {topalbum4plays} plays\n `5.` **[{topalbum5}]({topalbum5url})** {topalbum5plays} plays\n `6.` **[{topalbum6}]({topalbum6url})** {topalbum6plays} plays\n `7.` **[{topalbum7}]({topalbum7url})** {topalbum7plays} plays\n `8.`	**[{topalbum8}]({topalbum8url})** {topalbum8plays} plays\n `9.` **[{topalbum9}]({topalbum9url})** {topalbum9plays} plays\n `10.` **[{topalbum10}]({topalbum10url})** {topalbum10plays} plays", color=color.color)
                        embed.set_thumbnail(url = ctx.message.author.avatar)
                        embed.set_author(name = f"{ctx.message.author.name}'s overall top albums", icon_url = ctx.message.author.avatar)
                        await ctx.send(embed=embed)   
        else:
            embed = discord.Embed(description=f'> {emojis.false} {member.mention} didnt configurate their **LastFM**', color=color.fail)
            await ctx.send(embed=embed)

    @commands.command(aliases = ['topt'], brief="check a member's top 10 tracks", description="lastfm")
    @commands.cooldown(1, 4, commands.BucketType.user)
    @blacklist_check()
    async def toptracks(self, ctx, *, member: discord.Member=None):
        if member == None:
            member = ctx.author
        if collection.find_one({"_id": member.id}):
            check = collection.find_one({"_id": member.id})
            user = check['user']

            if user == 'not set':
                embed = discord.Embed(description=f'> {emojis.false} {member.mention} didnt configurate their **LastFM**', color=color.fail)
                await ctx.send(embed=embed)
                return
            
            else:
                 async with aiohttp.ClientSession() as cs:
                    async with cs.get(f"https://ws.audioscrobbler.com/2.0/?method=user.getTopTracks&user={user}&api_key={apikey}&format=json") as r:
                        data = await r.json()
                        toptrack1 = data["toptracks"]["track"][0]["name"]
                        toptrack2 = data["toptracks"]["track"][1]["name"]
                        toptrack3 = data["toptracks"]["track"][2]["name"]
                        toptrack4 = data["toptracks"]["track"][3]["name"]
                        toptrack5 = data["toptracks"]["track"][4]["name"]
                        toptrack6 = data["toptracks"]["track"][5]["name"]
                        toptrack7 = data["toptracks"]["track"][6]["name"]
                        toptrack8 = data["toptracks"]["track"][7]["name"]
                        toptrack9 = data["toptracks"]["track"][8]["name"]
                        toptrack10 = data["toptracks"]["track"][9]["name"]
                        toptrack1url = data["toptracks"]["track"][0]["url"]
                        toptrack2url = data["toptracks"]["track"][1]["url"]
                        toptrack3url = data["toptracks"]["track"][2]["url"]
                        toptrack4url = data["toptracks"]["track"][3]["url"]
                        toptrack5url = data["toptracks"]["track"][4]["url"]
                        toptrack6url = data["toptracks"]["track"][5]["url"]
                        toptrack7url = data["toptracks"]["track"][6]["url"]
                        toptrack8url = data["toptracks"]["track"][7]["url"]
                        toptrack9url = data["toptracks"]["track"][8]["url"]
                        toptrack10url = data["toptracks"]["track"][9]["url"]
                        toptrack1plays = data["toptracks"]["track"][0]["playcount"]
                        toptrack2plays = data["toptracks"]["track"][1]["playcount"]
                        toptrack3plays = data["toptracks"]["track"][2]["playcount"]
                        toptrack4plays = data["toptracks"]["track"][3]["playcount"]
                        toptrack5plays = data["toptracks"]["track"][4]["playcount"]
                        toptrack6plays = data["toptracks"]["track"][5]["playcount"]
                        toptrack7plays = data["toptracks"]["track"][6]["playcount"]
                        toptrack8plays = data["toptracks"]["track"][7]["playcount"]
                        toptrack9plays = data["toptracks"]["track"][8]["playcount"]
                        toptrack10plays = data["toptracks"]["track"][9]["playcount"]
                        embed = discord.Embed(description = f"`1` **[{toptrack1}]({toptrack1url})** {toptrack1plays} plays\n`2.` **[{toptrack2}]({toptrack2url})** {toptrack2plays} plays\n`3.` **[{toptrack3}]({toptrack3url})** {toptrack3plays} plays\n`4.` **[{toptrack4}]({toptrack4url})** {toptrack4plays} plays\n`5.` **[{toptrack5}]({toptrack5url})** {toptrack5plays} plays\n`6.` **[{toptrack6}]({toptrack6url})** {toptrack6plays} plays\n`7.` **[{toptrack7}]({toptrack7url})** {toptrack7plays} plays\n`8.`	**[{toptrack8}]({toptrack8url})** {toptrack8plays} plays\n`9.` **[{toptrack9}]({toptrack9url})** {toptrack9plays} plays\n`10.` **[{toptrack10}]({toptrack10url})** {toptrack10plays} plays", color=color.color)
                        embed.set_thumbnail(url = ctx.message.author.avatar)
                        embed.set_author(name = f"{ctx.message.author.name}'s overall top tracks", icon_url = ctx.message.author.avatar)
                        await ctx.send(embed=embed)

        else:
            embed = discord.Embed(description=f'> {emojis.false} {member.mention} didnt configurate their **LastFM**', color=color.fail)
            await ctx.send(embed=embed)

async def setup(client):
    await client.add_cog(lastfm(client))
