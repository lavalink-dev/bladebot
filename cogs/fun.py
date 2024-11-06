import discord
import random
import asyncio
import json
import random
import aiohttp
import requests
import pymongo
from pymongo import MongoClient
from discord.ext import commands
from discord.utils import get
from io import BytesIO
from typing import Union, Optional
from utils import functions
from utils.emojis import emojis
from utils.color import color

cluster = MongoClient('mongodb+srv://blade:lolidkbruh12333333333@cluster0.wbxaj.mongodb.net/myFirstDatabase?retryWrites=true&w=majority')
db = cluster["blade"]
collection = db["blacklist"]
niggerdb = db["nword"]
collections = db["interaction"]

def blacklist_check():
    def predicate(ctx):
        if collection.find_one({'_id': ctx.author.id}):
            return False
        return True
    return commands.check(predicate)

class fun(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        if 'nigger' in message.content.lower():
            if not niggerdb.find_one({"_id": message.author.id}):
                antialtdb = {"_id": message.author.id, "count": 1}
                niggerdb.insert_one(antialtdb)

            else:
                count = niggerdb.find_one({"_id": message.author.id})["count"]
                niggerdb.update_one({"_id": message.author.id}, {"$set": {"count": count + 1}})

    @commands.command(brief='check a members pfp if its a catfish', description='fun')
    async def catfish(self, ctx, user: discord.User):
        header = {'api_key': random.choice(['e60376598d9525c7391702fd01f23a1a8b9eb5287a43152b73e95c8ba096d9c2', '3fb5e099326bfa1603d7b852f0f907f383b92614f00e68f130d17876f933aabb'])}

        r = requests.get(f"https://serpapi.com/search.json?engine=google_reverse_image&image_url={user.display_avatar.url}", params=header)
        data = r.json()

        results = data["search_information"]["total_results"]

        embed = discord.Embed(description=f'> {emojis.blade} Found ``{results}`` similair Images', color=color.color)
        await ctx.send(embed=embed)

    @commands.command(aliases=['nc'], brief='nword counter', description='none')
    async def niggercount(self, ctx, member: discord.User = None):
        if member == None:
            member = ctx.message.author

        if niggerdb.find_one({"_id": member.id}):
            check = niggerdb.find_one({"_id": member.id})
            embed = discord.Embed(description=f'{emojis.reply} said the **N-Word** ``{check["count"]}`` Times', color=color.color)
            embed.set_author(name=f"{member.name}", icon_url=member.display_avatar)
            await ctx.send(embed=embed)
        else:   
            embed = discord.Embed(description=f'> {emojis.false} No **Data** Found', color=color.fail)
            await ctx.send(embed=embed)

    @commands.command(aliases=['nlb'], brief='n-word leaderboard', description='none')
    async def niggerleaderboard(self, ctx):
        rankings = niggerdb.find().sort("count",-1)
        i = 1
        embed = discord.Embed(title=f"{emojis.blade} N-Word Leaderboard", description=f'{emojis.reply} Top 10 \n \n', color=color.color)
        for x in rankings:
            try:
                temp = self.client.get_user(x["_id"])
                tempxp = x["count"]
                embed.description += f"``{i}.`` **{temp.name}** said it ``{tempxp:,}`` Times  \n"
                i += 1
            except:
                pass
            if i == 11:
                break

        await ctx.send(embed=embed)

    @commands.command(brief='play kiss marry kill', aliases=["kmk"], description="fun")
    async def kissmarykill(self, ctx):
        kiss = discord.ui.Button(label="kiss", custom_id="kiss")
        marry = discord.ui.Button(label="marry", custom_id="marry")
        kill = discord.ui.Button(label="kill", custom_id="kill")

        randomMember = random.choice(ctx.channel.guild.members)

        kmk = f"> {randomMember}"

        embed = discord.Embed(title=f'{emojis.blade} Kiss Marry Kill', color=color.color, description="")
        embed.description += f"{kmk}"

        view = discord.ui.View()
        view.add_item(item=kiss)
        view.add_item(item=marry)
        view.add_item(item=kill)
    
        await ctx.send(embed=embed, view=view)

        interaction = await self.client.wait_for("button_click", check = lambda i: i.custom_id == "kiss")
        await interaction.send(content = "Button clicked!")

    @commands.command(brief='funny lil command', description='fun')
    async def blade(self, ctx, protocol=None, type=None, strike=None, member: discord.Member=None):
        accept = discord.ui.Button(style=discord.ButtonStyle.green, label="accept", emoji=emojis.true)
        decline = discord.ui.Button(style=discord.ButtonStyle.red, label="decline", emoji=emojis.false)

        async def accept_callback(interaction):
            if interaction.user != ctx.author:
                embed = discord.Embed(description=f"> {emojis.false} This is not your message", color=color.fail)
                await interaction.response.send_message(embed=embed, view=None, ephemeral=True)
                return
            else:
                embed = discord.Embed(description=f'> {emojis.true} {strike} has been sent to {member.mention}', color=color.success)
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
                embed = discord.Embed(description=f'> {emojis.true} {strike} has been canceled', color=color.success)
                await interaction.response.edit_message(embed=embed, view=None)

        accept.callback = accept_callback
        decline.callback = decline_callback

        view = discord.ui.View()
        view.add_item(item=accept)
        view.add_item(item=decline)

        if protocol == 'protocol':
            if type != None:
                if strike != None:
                    if member != None:
                        embed = discord.Embed(title='Confirmation Required', color=color.color, 
                                              description=f'{ctx.message.author.mention} your {strike} is ready to start, \nplease confirm attack on target: {member.mention}')
                        await ctx.send(embed=embed, view=view)

    @commands.command(aliases=['ss'], brief='screenshot a website', description='fun')
    async def screenshot(self, ctx, website):

        site = ctx.message.content.lower()
        if 'https://' in website or 'http://' in website:
            embed = discord.Embed(description=f'> Screenshot of **{website}**', color=color.color)
            embed.set_image(url=f'https://sensui-useless-apis.codersensui.repl.co/api/tools/ss?url={site}')
            await ctx.send(embed=embed)
            return
        else:
            embed = discord.Embed(description=f'> Screenshot of **{website}**')
            embed.set_image(url=f"https://sensui-useless-apis.codersensui.repl.co/api/tools/ss?url=https://{site}")
            await ctx.send(embed=embed)
            return

    @commands.command(aliases=['tod'], brief='get a random truth or dare', description='fun')
    @blacklist_check()
    async def truthordare(self, ctx):
        truth = ["Have you ever kissed an animal?","Have you ever cheated on a test?","What was the last thing you ate?","Do you have any unusual talents?","Do you have any phobias?","Have you ever used someone else's password?","Have you ever ridden the bus without paying the fare?","Do you message people during your classes?","Have you ever fallen asleep during a class?","Have you ever bitten a toenail?","Have you ever stolen something?","Are you a hard-working student?","What was the best day of you life?","What was the strangest dream you ever had?","What is the most annoying thing to you (pet peeve)?","If you could have a superpower, what would it be?", "Who was your first crush, or who is your current crush?","How old were you when you had your first kiss?","What would you do if your current boyfriend/girlfriend ended things right now?","Have you ever cheated on a boyfriend/girlfriend?","Have you ever been cheated on by a boyfriend/girlfriend?","If you could go on a date with anyone in the room, who would it be?","What personality traits would cause you to end a friendship?","Would you go behind a friend's back with a crush?","Have you ever lied to your best friend?","Would you ever cheat off a friends paper?","How many different best friends have you had during your lifetime?","If you were stuck on a deserted island, which friend would you want with you?","How long have you gone without showering?","Have you ever told a lie during a game of Truth or Dare? What was it and why?","Have you ever had a crush on anyone here?","Have you ever stolen anything?","What's your scariest nightmare?","What do you think is your biggest physical flaw?","Have you ever gone skinny dipping?","What kind of pajamas do you wear to bed?","What's the dumbest thing you've ever done on a dare?","What color is your underwear?","Have you ever peed in the swimming pool?","If you weren't here, what would you be doing?", "If you couldn't go to the college or get the job of your dreams, what would you do?","What is one thing you've never told anyone else?","What do you want to be when you grow up?","What kind of person do you want to marry someday?","Do you want to have kids? How many?","If you could switch places with someone for a day, who would it be?","If you could invent anything, what would it be?","If you knew the world was about to end, what would you do?","If you could be born again, who would you come back as?","Are you scared of dying? Why?","What is your biggest fear?","What happened on worst day of your life?","Have you ever climbed a tree?","Have you ever sang and danced in the grocery store?","If you could be a superhero, what would your power be?","What would you do if you were invisible for a day?","If you life were made into a movie, who would play you?","What's your biggest pet peeve?","What is your special talent?","What's the best meal you've ever had?","What's you favorite Disney movie and why?","What would you do with a million dollars if you ever won the lottery?"]

        dare = ["Sing a song.","Post 'I love English!' on social media.","Say the English alphabet backwards.","Give someone near you a compliment.","Show the last photo you took with your phone.","Do your best dance.","Act like a cat.","Act like a monkey and a donkey at the same time.","Introduce yourself to someone you don't know.","Smell the inside of your shoe.","Call someone and ask if they believe in aliens.","Act like a pirate.","Talk about the last time you apologized.","Act like you are swimming.","Say the months of the year backwards.", "Go outside and sing a clip of your favorite Disney song at the top of your lungs.","Exchange shirts with the person next to you for the next round of questions.","Wear a funny hat on your head for the next three rounds of questions.","Drink a mystery brew concocted by the rest of the group. Make sure there is nothing harmful or dangerous in the concoction, and set areasonable limit of sips the person must take to complete the dare.","Everything you say for the rest of the game has to rhyme.","Give someone in the group a piggyback ride around the room.","Pretend that you're swimming underwater for the next three rounds of questions.","Prank call someone you know (perhaps another girl in the group that couldn't make it that night).","Set up a tea party between any of the stuffed animals in the house. Invite the girls in your group to come join.","Eat a mouthful of crackers and try to whistle.","If there is a pet at the event, have that person try and hold the pet for the rest of the night.","Repeat everything another player says for the next three rounds of the game.","Wear your pants backward for the rest of the game.","Ask the neighbors to borrow a cup of sugar.","Sing instead of speaking for the next two rounds of the game.","Post a YouTube video after singing a currently popular song.","Make up a rap about the person to your right.","Run around the room imitating a monkey.","Say the alphabet backwards in a British accent.","Crack an egg on your head."]

        embed = discord.Embed(title=f'{emojis.blade} Truth or Dare', color=color.color)

        choice =random.choice(['truth', 'dare'])

        if choice == 'truth':
            embed.add_field(name=f'{emojis.reply} Truth', value=f'```{random.choice(truth)}```', inline= False)
        if choice == 'dare':
            embed.add_field(name=f'{emojis.reply} Dare', value=f'```{random.choice(dare)}```', inline= False)
        await ctx.send(embed=embed)

    @commands.command(aliases=['wyr'], brief='would you rather this or that', description='fun')
    @blacklist_check()
    async def wouldyourather(self, ctx):
        async with aiohttp.ClientSession() as cs:
            async with cs.get(f"https://api.popcat.xyz/wyr") as r:
                data = await r.json()
                ops1 = data['ops1']
                ops2 = data['ops2']

                embed = discord.Embed(title=f'{emojis.blade} Would you Rather', color=color.color)
                embed.add_field(name=f'> Option 1', value=f'```{ops1}```', inline= True)
                embed.add_field(name=f'> Option 2', value=f'```{ops2}```', inline= True)
                message = await ctx.send(embed=embed)

                await message.add_reaction('<:blde_oneb:897546906484477973>')
                await message.add_reaction('<:blde_twob:897546906249617500>')

    @commands.command(aliases=['pul'], brief='get a random pickup line', description='fun')
    @blacklist_check()
    async def pickupline(self, ctx):
        async with aiohttp.ClientSession() as cs:
            async with cs.get(f"https://api.popcat.xyz/pickuplines") as r:
                data = await r.json()
                pickupline = data['pickupline']

                embed = discord.Embed(title=f'{emojis.blade} Pickup Line', color=color.color,
                description=f'{emojis.reply} ``{pickupline}``')
                await ctx.send(embed=embed)

    @commands.command(aliases=['d'], brief='get a random dare', description='fun')
    @blacklist_check()
    async def dare(self, ctx):
        dare = ["Sing a song.","Post 'I love English!' on social media.","Say the English alphabet backwards.","Give someone near you a compliment.","Show the last photo you took with your phone.","Do your best dance.","Act like a cat.","Act like a monkey and a donkey at the same time.","Introduce yourself to someone you don't know.","Smell the inside of your shoe.","Call someone and ask if they believe in aliens.","Act like a pirate.","Talk about the last time you apologized.","Act like you are swimming.","Say the months of the year backwards.", "Go outside and sing a clip of your favorite Disney song at the top of your lungs.","Exchange shirts with the person next to you for the next round of questions.","Wear a funny hat on your head for the next three rounds of questions.","Drink a mystery brew concocted by the rest of the group. Make sure there is nothing harmful or dangerous in the concoction, and set areasonable limit of sips the person must take to complete the dare.","Everything you say for the rest of the game has to rhyme.","Give someone in the group a piggyback ride around the room.","Pretend that you're swimming underwater for the next three rounds of questions.","Prank call someone you know (perhaps another girl in the group that couldn't make it that night).","Set up a tea party between any of the stuffed animals in the house. Invite the girls in your group to come join.","Eat a mouthful of crackers and try to whistle.","If there is a pet at the event, have that person try and hold the pet for the rest of the night.","Repeat everything another player says for the next three rounds of the game.","Wear your pants backward for the rest of the game.","Ask the neighbors to borrow a cup of sugar.","Sing instead of speaking for the next two rounds of the game.","Post a YouTube video after singing a currently popular song.","Make up a rap about the person to your right.","Run around the room imitating a monkey.","Say the alphabet backwards in a British accent.","Crack an egg on your head."]

        embed = discord.Embed(title=f'{emojis.blade} Truth or Dare', color=color.color)
        embed.add_field(name=f'{emojis.reply} Dare', value=f'```{random.choice(dare)}```', inline= False)
        await ctx.send(embed=embed)

    @commands.command(aliases=['t'], brief='get a random truth', description='fun')
    @blacklist_check()
    async def truth(self, ctx):
        truth = ["Have you ever kissed an animal?","Have you ever cheated on a test?","What was the last thing you ate?","Do you have any unusual talents?","Do you have any phobias?","Have you ever used someone else's password?","Have you ever ridden the bus without paying the fare?","Do you message people during your classes?","Have you ever fallen asleep during a class?","Have you ever bitten a toenail?","Have you ever stolen something?","Are you a hard-working student?","What was the best day of you life?","What was the strangest dream you ever had?","What is the most annoying thing to you (pet peeve)?","If you could have a superpower, what would it be?", "Who was your first crush, or who is your current crush?","How old were you when you had your first kiss?","What would you do if your current boyfriend/girlfriend ended things right now?","Have you ever cheated on a boyfriend/girlfriend?","Have you ever been cheated on by a boyfriend/girlfriend?","If you could go on a date with anyone in the room, who would it be?","What personality traits would cause you to end a friendship?","Would you go behind a friend's back with a crush?","Have you ever lied to your best friend?","Would you ever cheat off a friends paper?","How many different best friends have you had during your lifetime?","If you were stuck on a deserted island, which friend would you want with you?","How long have you gone without showering?","Have you ever told a lie during a game of Truth or Dare? What was it and why?","Have you ever had a crush on anyone here?","Have you ever stolen anything?","What's your scariest nightmare?","What do you think is your biggest physical flaw?","Have you ever gone skinny dipping?","What kind of pajamas do you wear to bed?","What's the dumbest thing you've ever done on a dare?","What color is your underwear?","Have you ever peed in the swimming pool?","If you weren't here, what would you be doing?", "If you couldn't go to the college or get the job of your dreams, what would you do?","What is one thing you've never told anyone else?","What do you want to be when you grow up?","What kind of person do you want to marry someday?","Do you want to have kids? How many?","If you could switch places with someone for a day, who would it be?","If you could invent anything, what would it be?","If you knew the world was about to end, what would you do?","If you could be born again, who would you come back as?","Are you scared of dying? Why?","What is your biggest fear?","What happened on worst day of your life?","Have you ever climbed a tree?","Have you ever sang and danced in the grocery store?","If you could be a superhero, what would your power be?","What would you do if you were invisible for a day?","If you life were made into a movie, who would play you?","What's your biggest pet peeve?","What is your special talent?","What's the best meal you've ever had?","What's you favorite Disney movie and why?","What would you do with a million dollars if you ever won the lottery?"]

        embed = discord.Embed(title=f'{emojis.blade} Truth or Dare', color=color.color)
        embed.add_field(name=f'{emojis.reply} Truth', value=f'```{random.choice(truth)}```', inline= False)
        await ctx.send(embed=embed)

    @commands.command(brief='ask ben your questions', description='fun')
    @blacklist_check()
    async def ben(self, ctx, *, question):
        ben = ['https://media.discordapp.net/attachments/862090082613985281/977934505790820452/ezgif-3-e84e253fc9.gif', 'https://media.discordapp.net/attachments/862090082613985281/977934938261311519/ezgif-3-76a265bf17.gif', 'https://media.discordapp.net/attachments/862090082613985281/977935217895546940/ezgif-3-b08efe3886.gif', 'https://media.discordapp.net/attachments/862090082613985281/977935838606397540/ezgif-3-893e1be6f6.gif']

        embed = discord.Embed(title=f'{emojis.blade} Talking Ben', color=color.color,
                            description=f'{emojis.reply} **Question**: {question}')
        embed.set_author(name=f"{ctx.message.author}", icon_url=ctx.message.author.display_avatar)
        embed.set_image(url=random.choice(ben))
        await ctx.send(embed=embed)

    @commands.command(brief='how long can you spin', description='fun')
    @blacklist_check()
    async def fidgetspinner(self, ctx):
        embed = discord.Embed(description=f'> <a:spinner:950083483190067200> | You spin the **Fidget Spinner**', color=color.color)
        await ctx.send(embed=embed)

        spin = random.randint(1, 360)
        await asyncio.sleep(spin)

        embed2 = discord.Embed(description=f'> <:fidgetspinner:1111012269007052831> | Your **Fidget Spinner** spinned for ``{str(spin)}s``', color=color.color)
        try:
            await ctx.message.reply(embed=embed2, mention_author=False)
        except:
            await ctx.send(embed=embed2)

    @commands.command(brief='a vert checker', description='fun')
    async def bombthreat(self, ctx):
        threat = self.client.get_user(1154608202701340774)
        if threat in ctx.guild.members:
            embed = discord.Embed(description=f'> {emojis.true} There is a **Bomb Threat** in the Server', color=color.success)
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(description=f'> {emojis.false} There is no **Bomb Threat** in the Server', color=color.fail)
            await ctx.send(embed=embed)

    @commands.command()
    @blacklist_check()
    async def hentai(self, ctx):
        await ctx.send('good taste')

    @commands.command()
    @blacklist_check()
    async def bootyhole(self, ctx):
        await ctx.send(':peach: :hole: ')

    @commands.command()
    @blacklist_check()
    async def spank(self, ctx):
        await ctx.send('yamete kudasai :weary:')

    @commands.command()
    @blacklist_check()
    async def gommemode(self, ctx):
        await ctx.send('gommemode trololololol')

    @commands.command(aliases=['8ball'], brief='ask the 8ball questions', description='fun')
    @blacklist_check()
    async def _8ball(self, ctx, *, question):
        answers = ['🟢 It is certain', '🟢 It is decidedly so', '🟢 Without a doubt', '🟢 Yes - definetly', '🟢 You may rely on it', '🟢 As I see it, yes', '🟢 Most likely', '🟢 Outlook good', '🟢 Yes', '🟢 Signs point to yes', '🟡 Reply hazy, try later', '🟡 Ask again later', '🟡 Better not tell you now', '🟡 Cannot predict now', '🟡 Concentrate and ask again', '🔴 Don´t count on it', '🔴 My reply is no', '🔴 My sources say no', '🔴 Outlook not so good', '🔴 Very doubtful']
        embed = discord.Embed(title='🎱 8ball',
                               description=f"{emojis.reply2} **Question**: {question} \n{emojis.reply} **Answer**: {random.choice(answers)}", color=color.color)
        await ctx.send(embed=embed)

    @commands.command(brief='turn into a ghoul', description='fun')
    @blacklist_check()
    async def ghoul(self, ctx):
        embed = discord.Embed(color=0x781212,
        description=f"> **{ctx.message.author.mention}** is turning into a ghoul.")
        embed.set_image(url='https://c.tenor.com/KqmIFA5bt7UAAAAC/kaneki-tokyo-ghoul.gif')
        await ctx.send(embed=embed)

    @commands.command(brief='shows a random cat image', description='fun')
    async def cat(self, ctx):
        async with aiohttp.ClientSession() as cs:
            async with cs.get('https://cataas.com/cat?json=true') as r:
                res = await r.json()

                if res["mimetype"][:6] == "image/jpeg":
                    format = "jpeg"
                else:
                    format = "png"

        embed = discord.Embed(title=f'{emojis.blade} Cat', color=color.color)
        embed.set_image(url=f'https://cataas.com/cat/{res["_id"]}.{format}')
        await ctx.send(embed=embed)

    @commands.command(aliases=['pp'], brief='who has the biggest', description='fun')
    @blacklist_check()
    async def peepee(self, ctx, user:discord.Member=None):
        if user == None:
            user = ctx.message.author

        peepee = [ '8=D', '8==D', '8===D', '8====D', '8=====D', '8======D', '8=======D', '8========D', '8=========D', '8==========D', '8===========D', '8============D', '8=============D', '8==============D', '8===============D', '8================D', '8=================D', '8=================D']
        pp = random.choice(peepee)

        embed = discord.Embed(description=f"{emojis.dash} **{user.mention}'s PP Size** \n{emojis.reply} {pp}", color=color.color)
        await ctx.send(embed=embed)

    @commands.command(brief='hack a other member', description='fun')
    @blacklist_check()
    async def hack(self, ctx, user:discord.Member=None):
        name = ['Lien', 'Anna', 'Rachel', 'Jakob', 'Brian', 'Kathrin', 'Collin', 'Finneas', 'Ashley', 'Robin', 'Lea', 'Lena', 'Alina', 'Leyla', 'Ilaria', 'Max', 'Mads' 'Leon', 'Angelina', 'Amelia', 'Ben', 'John', 'Kevin']
        lname = ['Barmore', 'Brown', 'Creek', 'Ponds', 'Crown', 'June', 'Miller', 'Van-derwoods', 'Amber', 'Coles', 'Smith']

        gender = ['Male', 'Female', 'Trans', 'Non-Binary']
        age = ['14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '60', '65', '90']

        height = ["3'4", "4'11", "5'3", "6'1", "'4'1", "5'5", "5'11", "6'1", "6'4", "6'9'"]
        weight = ['120', '130', '133', '140', '270', '90', '121', '111', '132', '194', '153', '200', '334', '589']

        haircolor = ['Brown', 'Blonde', 'Black', 'Red']
        skincolor = ['White', 'Black', 'Yellow', 'Light']

        dob = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12']
        dob2 = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31']
        dob3 = ['2004', '2003', '1999', '2005', '1994', '1997', '2000', '2008', '1977', '1974', '1993', '2001', '2008', '2010', '2020', '1943', '1945', '1964']

        location = ['NYC', 'Staten Island', 'Daly City', 'Amaguana', 'Petepa', 'San Antonio', 'Oklahoma City', 'Berlin', 'Hamburg']
        phone = ['827', '772', '509', '934', '904', '923', '290', '111', '290']
        phone2 = ['888', '183', '593', '424', '189', '189', '593', '904']
        phone3 = ['934', '115', '056', '190', '843', '194', '864', '901', ' 065']
        email = ['web.de', 'gmx.com', 'gmail.com', 'yahoo.com', 'yandex.com', 'aol.com', 'gmx.de']
        passwords = ['ilovediscord', '1234567', 'mypasswordispassword', 'password', 'passwordisnotmypassword', 'p4ssw0rd', "iLickFeet", '000000000!W']
        passwords2 = ['987654321', '123321', 'tree123', 'cat1010', 'bladeismyfavbot']
        passwords3 = ['passwords', 'youcanthackme', 'heartbroken', 'd3pr3ss10n', 'lilpeepfanpw1', 'ilikeD1KK!!']
        occupation = ['Clerk', 'Trapper', 'Docotr', 'military']
        annaulslry = ['1', '10', '100', '20,000', '10', '100,000', '300,000', '0.01', '300', '4,000', '6,900', '69,420', '-1000', '-1', '-69.420']
        ethincy = ['Asian', 'European', 'American', 'Native American', 'African American', 'Latino']
        religion = ['Christ', 'Islam', 'Hinduism', 'Budhism', 'Judaism']
        sexuality = ['Straight', 'Bi', 'Pan', 'Lesbian', 'Gay']
        eduction = ['Pre School', 'Kindergarten', 'Middleschool', 'Highschool', 'University']

        if not user:
            user = ctx.message.author
        message = await ctx.send(f'``Hacking {user}``')
        await asyncio.sleep(2)
        await message.edit(content=f"``Hacking {user}`` \n``Hacking into the mainframe...``")
        await asyncio.sleep(2)
        await message.edit(content=f"``Hacking {user}`` \n``Hacking into the mainframe...`` \n``Caching data...``")
        await asyncio.sleep(1)
        await message.edit(content=f"``Hacking {user}`` \n``Hacking into the mainframe...`` \n``Caching data...`` \n``Cracking SSN information...``")
        await asyncio.sleep(1)
        await message.edit(content=f"``Hacking {user}`` \n``Hacking into the mainframe...`` \n``Caching data...`` \n``Cracking SSN information...`` \n``Bruteforcing love life details...``")
        await asyncio.sleep(2)
        await message.edit(content='<a:blde_loading:1077990826619195472>')
        await asyncio.sleep(4)
        await message.delete()

        embed = discord.Embed(title=f'{emojis.blade} **HACKED** {user}', color=color.color,
        description=f'\n \n> **Name:** {random.choice(name)} {random.choice(lname)} \n> **Gender:** {random.choice(gender)} \n> **Age:** {random.choice(age)} \n> **Height:** {random.choice(height)} \n> **Weight:** {random.choice(weight)} \n> **Hair Color:** {random.choice(haircolor)} \n> **Skin Color:** {random.choice(skincolor)} \n> **DOB:** {random.choice(dob)}/{random.choice(dob2)}/{random.choice(dob3)} \n> **Location:** {random.choice(location)} \n> **Phone:** ({random.choice(phone)})-{random.choice(phone2)}-{random.choice(phone3)} \n> **E-Mail:** {user.name}@{random.choice(email)} \n> **Passwords:** [{random.choice(passwords)}, {random.choice(passwords2)}, {random.choice(passwords3)}] \n> **Occupation:** {random.choice(occupation)} \n> **Annual Salary:** ${random.choice(annaulslry)} \n> **Ethincy:** {random.choice(ethincy)} \n> **Religion:** {random.choice(religion)} \n> **Sexuality:** {random.choice(sexuality)} \n> **Education:** {random.choice(eduction)}')
        embed.set_footer(text=f'hacked by {ctx.message.author}')
        embed.set_thumbnail(url=user.display_avatar)
        await ctx.send(embed=embed)

    @commands.command(brief='look at your rizz', description='fun')
    @blacklist_check()
    async def rizz(self, ctx, user:discord.Member=None):
        if user == None:
            user = ctx.message.author

        embed = discord.Embed(title='😍 Rizz', color=color.color,
        description=f'{emojis.dash} **Raiting {user.mention}** \n{emojis.reply} Your Rizz game is a **{random.randint(1, 10)}/10**')
        embed.set_thumbnail(url=user.display_avatar)
        await ctx.send(embed=embed)

    @commands.command(brief='look at your rating', description='fun')
    @blacklist_check()
    async def rate(self, ctx, user:discord.Member=None):
        if user == None:
            user = ctx.message.author

        embed = discord.Embed(title='🍸 Rate', color=color.color,
        description=f'{emojis.dash} **Raiting {user.mention}** \n{emojis.reply} You are an **{random.randint(1, 10)}/10**')
        embed.set_thumbnail(url=user.display_avatar)
        await ctx.send(embed=embed)

    @commands.command(brief='look how swaggy you are', description='fun')
    @blacklist_check()
    async def swagrate(self, ctx, user:discord.Member=None):
            if not user:
                user = ctx.message.author

            embed = discord.Embed(title='💯 Swagrate', color=color.color,
            description=f'{emojis.dash} Swagrating {user.mention} \n{emojis.reply} You are to **{random.randint(1, 100)}%** swag.')
            embed.set_thumbnail(url=user.display_avatar)
            await ctx.send(embed=embed)

    @commands.command(brief='look how hot you are', description='fun')
    @blacklist_check()
    async def hotrate(self, ctx, user:discord.Member=None):
            if not user:
                user = ctx.message.author

            embed = discord.Embed(title='🥵 Hotrate', color=color.color,
            description=f'{emojis.dash} Hotrating {user.mention} \n{emojis.reply} You are to **{random.randint(1, 100)}%** hot.')
            embed.set_thumbnail(url=user.display_avatar)
            await ctx.send(embed=embed)

    @commands.command(brief='look how much a simp you are', description='fun')
    @blacklist_check()
    async def simprate(self, ctx, user:discord.Member=None):
            if not user:
                user = ctx.message.author

            embed = discord.Embed(title='🥺 Simprate', color=color.color,
            description=f'{emojis.dash} Simprating {user.mention} \n{emojis.reply} You are to **{random.randint(1, 100)}%** a simp.')
            embed.set_thumbnail(url=user.display_avatar)
            await ctx.send(embed=embed)

    @commands.command(brief='ship with other members', description='fun')
    @blacklist_check()
    async def ship(self, ctx, user: discord.Member=None, user2: discord.Member=None):
        rate = ['<:bar1:1006975151730085929><:bar2:1006975159829274644><:bar2:1006975159829274644><:bar2:1006975159829274644><:bar2:1006975159829274644><:bar2:1006975159829274644><:bar2:1006975159829274644><:bar2:1006975159829274644><:bar2:1006975159829274644><:bar3:1006975412913586297> 0%',
                '<:bar1full:1006975153684611083><:bar2:1006975159829274644><:bar2:1006975159829274644><:bar2:1006975159829274644><:bar2:1006975159829274644><:bar2:1006975159829274644><:bar2:1006975159829274644><:bar2:1006975159829274644><:bar2:1006975159829274644><:bar3:1006975412913586297> 5%',
                '<:bar1full:1006975153684611083><:bar2:1006975159829274644><:bar2:1006975159829274644><:bar2:1006975159829274644><:bar2:1006975159829274644><:bar2:1006975159829274644><:bar2:1006975159829274644><:bar2:1006975159829274644><:bar2:1006975159829274644><:bar3:1006975412913586297> 10%',
                '<:bar1full:1006975153684611083><:bar2half:1006975409411342487><:bar2:1006975159829274644><:bar2:1006975159829274644><:bar2:1006975159829274644><:bar2:1006975159829274644><:bar2:1006975159829274644><:bar2:1006975159829274644><:bar2:1006975159829274644><:bar3:1006975412913586297> 15%',
                '<:bar1full:1006975153684611083><:bar2full:1006975883032137778><:bar2:1006975159829274644><:bar2:1006975159829274644><:bar2:1006975159829274644><:bar2:1006975159829274644><:bar2:1006975159829274644><:bar2:1006975159829274644><:bar2:1006975159829274644><:bar3:1006975412913586297> 20%',
                '<:bar1full:1006975153684611083><:bar2full:1006975883032137778><:bar2half:1006975409411342487><:bar2:1006975159829274644><:bar2:1006975159829274644><:bar2:1006975159829274644><:bar2:1006975159829274644><:bar2:1006975159829274644><:bar2:1006975159829274644><:bar3:1006975412913586297> 25%',
                '<:bar1full:1006975153684611083><:bar2full:1006975883032137778><:bar2full:1006975883032137778><:bar2:1006975159829274644><:bar2:1006975159829274644><:bar2:1006975159829274644><:bar2:1006975159829274644><:bar2:1006975159829274644><:bar2:1006975159829274644><:bar3:1006975412913586297> 30%',
                '<:bar1full:1006975153684611083><:bar2full:1006975883032137778><:bar2full:1006975883032137778><:bar2half:1006975409411342487><:bar2:1006975159829274644><:bar2:1006975159829274644><:bar2:1006975159829274644><:bar2:1006975159829274644><:bar2:1006975159829274644><:bar3:1006975412913586297> 35%',
                '<:bar1full:1006975153684611083><:bar2full:1006975883032137778><:bar2full:1006975883032137778><:bar2full:1006975883032137778><:bar2:1006975159829274644><:bar2:1006975159829274644><:bar2:1006975159829274644><:bar2:1006975159829274644><:bar2:1006975159829274644><:bar3:1006975412913586297> 40%',
                '<:bar1full:1006975153684611083><:bar2full:1006975883032137778><:bar2full:1006975883032137778><:bar2full:1006975883032137778><:bar2half:1006975409411342487><:bar2:1006975159829274644><:bar2:1006975159829274644><:bar2:1006975159829274644><:bar2:1006975159829274644><:bar3:1006975412913586297> 45%',
                '<:bar1full:1006975153684611083><:bar2full:1006975883032137778><:bar2full:1006975883032137778><:bar2full:1006975883032137778><:bar2full:1006975883032137778><:bar2:1006975159829274644><:bar2:1006975159829274644><:bar2:1006975159829274644><:bar2:1006975159829274644><:bar3:1006975412913586297> 50%',
                '<:bar1full:1006975153684611083><:bar2full:1006975883032137778><:bar2full:1006975883032137778><:bar2full:1006975883032137778><:bar2full:1006975883032137778><:bar2half:1006975409411342487><:bar2:1006975159829274644><:bar2:1006975159829274644><:bar2:1006975159829274644><:bar3:1006975412913586297> 55%',
                '<:bar1full:1006975153684611083><:bar2full:1006975883032137778><:bar2full:1006975883032137778><:bar2full:1006975883032137778><:bar2full:1006975883032137778><:bar2full:1006975883032137778><:bar2:1006975159829274644><:bar2:1006975159829274644><:bar2:1006975159829274644><:bar3:1006975412913586297> 60%',
                '<:bar1full:1006975153684611083><:bar2full:1006975883032137778><:bar2full:1006975883032137778><:bar2full:1006975883032137778><:bar2full:1006975883032137778><:bar2half:1006975409411342487><:bar2:1006975159829274644><:bar2:1006975159829274644><:bar3:1006975412913586297> 65%',
                '<:bar1full:1006975153684611083><:bar2full:1006975883032137778><:bar2full:1006975883032137778><:bar2full:1006975883032137778><:bar2full:1006975883032137778><:bar2full:1006975883032137778><:bar2full:1006975883032137778><:bar2:1006975159829274644><:bar2:1006975159829274644><:bar3:1006975412913586297> 70%',
                '<:bar1full:1006975153684611083><:bar2full:1006975883032137778><:bar2full:1006975883032137778><:bar2full:1006975883032137778><:bar2full:1006975883032137778><:bar2full:1006975883032137778><:bar2full:1006975883032137778><:bar2half:1006975409411342487><:bar2:1006975159829274644><:bar3:1006975412913586297> 75%',
                '<:bar1full:1006975153684611083><:bar2full:1006975883032137778><:bar2full:1006975883032137778><:bar2full:1006975883032137778><:bar2full:1006975883032137778><:bar2full:1006975883032137778><:bar2full:1006975883032137778><:bar2full:1006975883032137778><:bar2:1006975159829274644><:bar3:1006975412913586297> 80%',
                '<:bar1full:1006975153684611083><:bar2full:1006975883032137778><:bar2full:1006975883032137778><:bar2full:1006975883032137778><:bar2full:1006975883032137778><:bar2full:1006975883032137778><:bar2full:1006975883032137778><:bar2full:1006975883032137778><:bar2half:1006975409411342487><:bar3:1006975412913586297> 85%',
                '<:bar1full:1006975153684611083><:bar2full:1006975883032137778><:bar2full:1006975883032137778><:bar2full:1006975883032137778><:bar2full:1006975883032137778><:bar2full:1006975883032137778><:bar2full:1006975883032137778><:bar2full:1006975883032137778><:bar2full:1006975883032137778><:bar3:1006975412913586297> 90%',
                '<:bar1full:1006975153684611083><:bar2full:1006975883032137778><:bar2full:1006975883032137778><:bar2full:1006975883032137778><:bar2full:1006975883032137778><:bar2full:1006975883032137778><:bar2full:1006975883032137778><:bar2full:1006975883032137778><:bar2full:1006975883032137778><:bar3full:1006975407377096805> | 95%',
                '<:bar1full:1006975153684611083><:bar2full:1006975883032137778><:bar2full:1006975883032137778><:bar2full:1006975883032137778><:bar2full:1006975883032137778><:bar2full:1006975883032137778><:bar2full:1006975883032137778><:bar2full:1006975883032137778><:bar2full:1006975883032137778><:bar3full:1006975407377096805> | 100%']

        channel = ctx.message.channel
        randomMember = random.choice(channel.guild.members)

        if user == None:
            user = ctx.message.author
            user2 = randomMember

            image = f'https://api.popcat.xyz/ship?user1={user.display_avatar}&user2={user2.display_avatar}'
            image = image.replace("webp", "png")

            embed = discord.Embed(title='Ship💕',
            description=f'> 🔻 {user.mention} \n > 🔺 {user2.mention} \n<:mixed_names:930820456863371294> {user.name[:3]}{user2.name[3:]}\n \n> **Rating:** {random.choice(rate)}', color=color.color)
            embed.set_image(url=image)
            await ctx.send(embed=embed)

        elif user2 == None:
            user2 = user
            user = ctx.message.author

            image = f'https://api.popcat.xyz/ship?user1={user.display_avatar}&user2={user2.display_avatar}'
            image = image.replace("webp", "png")

            embed = discord.Embed(title='Ship💕',
            description=f'> 🔻 {user.mention} \n > 🔺 {user2.mention} \n<:mixed_names:930820456863371294> {user.name[:3]}{user2.name[3:]}\n \n > **Rating:** {random.choice(rate)}', color=color.color)
            embed.set_image(url=image)
            await ctx.send(embed=embed)

        else:
            user = user
            user2 = user2

            image = f'https://api.popcat.xyz/ship?user1={user.display_avatar}&user2={user2.display_avatar}'
            image = image.replace("webp", "png")

            embed = discord.Embed(title='Ship💕',
            description=f'> 🔻 {user.mention} \n > 🔺 {user2.mention} \n<:mixed_names:930820456863371294> {user.name[:3]}{user2.name[3:]}\n \n > **Rating:** {random.choice(rate)}', color=color.color)
            embed.set_image(url=image)
            await ctx.send(embed=embed)

    @commands.command(brief='look at how funny you are', description='fun')
    @blacklist_check()
    async def funny(self, ctx):
        rate = ['⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛ | 0%',
                '🟨⬛⬛⬛⬛⬛⬛⬛⬛⬛ | 5%',
                '🟥⬛⬛⬛⬛⬛⬛⬛⬛⬛ | 10%',
                '🟥🟨⬛⬛⬛⬛⬛⬛⬛⬛ | 15%',
                '🟥🟥⬛⬛⬛⬛⬛⬛⬛⬛ | 20%',
                '🟥🟥🟨⬛⬛⬛⬛⬛⬛⬛ | 25%',
                '🟥🟥🟥⬛⬛⬛⬛⬛⬛⬛ | 30%',
                '🟥🟥🟥🟨⬛⬛⬛⬛⬛⬛ | 35%',
                '🟥🟥🟥🟥⬛⬛⬛⬛⬛⬛ | 40%',
                '🟥🟥🟥🟥🟨⬛⬛⬛⬛⬛ | 45%',
                '🟥🟥🟥🟥🟥⬛⬛⬛⬛⬛ | 50%',
                '🟥🟥🟥🟥🟥🟨⬛⬛⬛⬛ | 55%',
                '🟥🟥🟥🟥🟥🟥⬛⬛⬛⬛ | 60%',
                '🟥🟥🟥🟥🟥🟥🟨⬛⬛⬛ | 65%',
                '🟥🟥🟥🟥🟥🟥🟥⬛⬛⬛ | 70%',
                '🟥🟥🟥🟥🟥🟥🟥🟨⬛⬛ | 75%',
                '🟥🟥🟥🟥🟥🟥🟥🟥⬛⬛ | 80%',
                '🟥🟥🟥🟥🟥🟥🟥🟥🟨⬛ | 85%',
                '🟥🟥🟥🟥🟥🟥🟥🟥🟥⬛ | 90%',
                '🟥🟥🟥🟥🟥🟥🟥🟥🟥🟨 | 95%',
                '🟥🟥🟥🟥🟥🟥🟥🟥🟥🟥 | 100%']
        embed = discord.Embed(description=f'You are funny to: \n {random.choice(rate )}', color=color.color)
        await ctx.send(embed=embed)

    @commands.command(brief='get a random meme', description='fun')
    @blacklist_check()
    async def meme(self, ctx):
        refresh = discord.ui.Button(emoji='🔃')

        async def refresh_callback(interaction):
            if interaction.user != ctx.author:
                embed = discord.Embed(description=f"> {emojis.false} This is not your message", color=color.fail)
                await interaction.response.send_message(embed=embed, view=None, ephemeral=True)
                return
            else:
                async with aiohttp.ClientSession() as cs:
                    async with cs.get('https://api.popcat.xyz/meme') as r:
                        res = await r.json()

                        title = res['title']
                        image = res['image']

                        embed = discord.Embed(description=title, color=color.color)
                        embed.set_image(url=image)
                        embed.set_footer(text=f'requested by {ctx.message.author}')
                        await interaction.response.edit_message(embed=embed)

        async with aiohttp.ClientSession() as cs:
            async with cs.get('https://api.popcat.xyz/meme') as r:
                res = await r.json()

                title = res['title']
                image = res['image']

                embed = discord.Embed(description=title, color=color.color)
                embed.set_image(url=image)
                embed.set_footer(text=f'requested by {ctx.message.author}', icon_url=ctx.message.author.display_avatar)

        refresh.callback = refresh_callback

        view = discord.ui.View()
        view.add_item(item=refresh)
        await ctx.send(embed=embed, view=view)

async def setup(client):
    await client.add_cog(fun(client))
