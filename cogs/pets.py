import discord
import pymongo
import asyncio
import random
from pymongo import MongoClient
from discord.ext import commands, tasks
from discord.ui import Select, View
from utils import functions
from utils.emojis import emojis
from utils.bar import bar
from utils.color import color

cluster = MongoClient('no')
db = cluster["blade"]
collection = db["pets"]
inventory = db["pets_inventory"]
premium = db["premium"]
blacklist = db["blacklist"]

def blacklist_check():
    def predicate(ctx):
        if blacklist.find_one({'_id': ctx.author.id}):
            return False
        return True
    return commands.check(predicate)

class pets(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.is_owner()
    async def petdata(self, ctx, user: discord.User=None):
        if user == None:
            user = ctx.message.author
        await ctx.send(collection.find_one({"_id": user.id}))

    @commands.command()
    @commands.is_owner()
    async def petstart(self, ctx):
        try:
            self.pet_loop.start()
            embed = discord.Embed(description=f'> {emojis.true} **Succesfully** started the **Pet** Event', color=color.success)
            await ctx.send(embed=embed)
        except Exception as e:
            embed = discord.Embed(description=f'> {emojis.false} {e}', color=color.fail)
            await ctx.send(embed=embed)

    @tasks.loop(seconds=1500)
    async def pet_loop(self):
        for i in collection.find({}):
            if i['hunger'] > 0:
                collection.update_one({"_id": i['_id']}, {"$set": {"hunger": i['hunger'] - random.randint(0, 1)}})
            if i['thirst'] > 0:
                collection.update_one({"_id": i['_id']}, {"$set": {"thirst": i['thirst'] - random.randint(0, 1)}})
            if i['fun'] > 0:
                collection.update_one({"_id": i['_id']}, {"$set": {"fun": i['fun'] - random.randint(0, 1)}})
            if i['energy'] > 0:
                collection.update_one({"_id": i['_id']}, {"$set": {"energy": i['energy'] - random.randint(0, 1)}})
            if i['hygiene'] > 0:
                collection.update_one({"_id": i['_id']}, {"$set": {"hygiene": i['hygiene'] - random.randint(0, 1)}})
            if i['love'] > 0:
                collection.update_one({"_id": i['_id']}, {"$set": {"love": i['love'] - random.randint(0, 1)}})

            if i['hygiene'] == 0 and i['energy'] == 0 and i['fun'] == 0 and i['thirst'] == 0 and i['hunger'] == 0 and i['love'] == 0:
                if i['health'] > 0:
                    collection.update_one({"_id": i['_id']}, {"$set": {"health": i['health'] - random.randint(0, 1)}})
                if i['health'] == 0:
                    user = self.client.get_user(i["_id"])
                    try:
                        embed = discord.Embed(description=f'> Hey, {user.mention}. Your Pet **{i["pet"]}** died because you didnt took care of them \n Because of that, we needed to clear your **Pet** Inventory', color=color.color)
                        await user.send(embed=embed)
                    except:
                        return
                    collection.delete_one({"_id": i['_id']})
                    inventory.delete_one({"_id": i['_id']})

            if i['hygiene'] > 0 and i['energy'] > 0 and i['fun'] > 0 and i['thirst'] > 0 and i['hunger'] > 0 and i['love'] > 0:
                if i['health'] < 10:
                    collection.update_one({"_id": i['_id']}, {"$set": {"health": i['health'] + random.randint(0, 1)}})

    @commands.group(pass_context=True, invoke_without_command=True, brief='look at your pet', description='pets')
    @blacklist_check()
    async def pet(self, ctx):
        if premium.find_one({"_id": ctx.message.author.id}):
            if collection.find_one({"_id": ctx.message.author.id}):
                check = collection.find_one({"_id": ctx.message.author.id})

                if check['health'] == 10:
                    health = bar.bar10
                if check['health'] == 9:
                    health = bar.bar9
                if check['health'] == 8:
                    health = bar.bar8
                if check['health'] == 7:
                    health = bar.bar7
                if check['health'] == 6:
                    health = bar.bar6
                if check['health'] == 5:
                    health = bar.bar5
                if check['health'] == 4:
                    health = bar.bar4
                if check['health'] == 3:
                    health = bar.bar3
                if check['health'] == 2:
                    health = bar.bar2
                if check['health'] == 1:
                    health = bar.bar1
                if check['health'] == 0:
                    health = bar.bar0

                if check['hunger'] == 10:
                    hunger = bar.bar10
                if check['hunger'] == 9:
                    hunger = bar.bar9
                if check['hunger'] == 8:
                    hunger = bar.bar8
                if check['hunger'] == 7:
                    hunger = bar.bar7
                if check['hunger'] == 6:
                    hunger = bar.bar6
                if check['hunger'] == 5:
                    hunger = bar.bar5
                if check['hunger'] == 4:
                    hunger = bar.bar4
                if check['hunger'] == 3:
                    hunger = bar.bar3
                if check['hunger'] == 2:
                    hunger = bar.bar2
                if check['hunger'] == 1:
                    hunger = bar.bar1
                if check['hunger'] == 0:
                    hunger = bar.bar0

                if check['thirst'] == 10:
                    thirst = bar.bar10
                if check['thirst'] == 9:
                    thirst = bar.bar9
                if check['thirst'] == 8:
                    thirst = bar.bar8
                if check['thirst'] == 7:
                    thirst = bar.bar7
                if check['thirst'] == 6:
                    thirst = bar.bar6
                if check['thirst'] == 5:
                    thirst = bar.bar5
                if check['thirst'] == 4:
                    thirst = bar.bar4
                if check['thirst'] == 3:
                    thirst = bar.bar3
                if check['thirst'] == 2:
                    thirst = bar.bar2
                if check['thirst'] == 1:
                    thirst = bar.bar1
                if check['thirst'] == 0:
                    thirst = bar.bar0

                if check['hygiene'] == 10:
                    hygiene = bar.bar10
                if check['hygiene'] == 9:
                    hygiene = bar.bar9
                if check['hygiene'] == 8:
                    hygiene = bar.bar8
                if check['hygiene'] == 7:
                    hygiene = bar.bar7
                if check['hygiene'] == 6:
                    hygiene = bar.bar6
                if check['hygiene'] == 5:
                    hygiene = bar.bar5
                if check['hygiene'] == 4:
                    hygiene = bar.bar4
                if check['hygiene'] == 3:
                    hygiene = bar.bar3
                if check['hygiene'] == 2:
                    hygiene = bar.bar2
                if check['hygiene'] == 1:
                    hygiene = bar.bar1
                if check['hygiene'] == 0:
                    hygiene = bar.bar0

                if check['fun'] == 10:
                    fun = bar.bar10
                if check['fun'] == 9:
                    fun = bar.bar9
                if check['fun'] == 8:
                    fun = bar.bar8
                if check['fun'] == 7:
                    fun = bar.bar7
                if check['fun'] == 6:
                    fun = bar.bar6
                if check['fun'] == 5:
                    fun = bar.bar5
                if check['fun'] == 4:
                    fun = bar.bar4
                if check['fun'] == 3:
                    fun = bar.bar3
                if check['fun'] == 2:
                    fun = bar.bar2
                if check['fun'] == 1:
                    fun = bar.bar1
                if check['fun'] == 0:
                    fun = bar.bar0

                if check['love'] == 10:
                    love = bar.bar10
                if check['love'] == 9:
                    love = bar.bar9
                if check['love'] == 8:
                    love = bar.bar8
                if check['love'] == 7:
                    love = bar.bar7
                if check['love'] == 6:
                    love = bar.bar6
                if check['love'] == 5:
                    love = bar.bar5
                if check['love'] == 4:
                    love = bar.bar4
                if check['love'] == 3:
                    love = bar.bar3
                if check['love'] == 2:
                    love = bar.bar2
                if check['love'] == 1:
                    love = bar.bar1
                if check['love'] == 0:
                    love = bar.bar0

                if check['energy'] == 10:
                    energy = bar.bar10
                if check['energy'] == 9:
                    energy = bar.bar9
                if check['energy'] == 8:
                    energy = bar.bar8
                if check['energy'] == 7:
                    energy = bar.bar7
                if check['energy'] == 6:
                    energy = bar.bar6
                if check['energy'] == 5:
                    energy = bar.bar5
                if check['energy'] == 4:
                    energy = bar.bar4
                if check['energy'] == 3:
                    energy = bar.bar3
                if check['energy'] == 2:
                    energy = bar.bar2
                if check['energy'] == 1:
                    energy = bar.bar1
                if check['energy'] == 0:
                    energy = bar.bar0

                embed = discord.Embed(title=f'{emojis.blade} Pet', color=color.color,
                description=f'{emojis.reply2} **Pet**: ``{check["pet"]}`` \n{emojis.reply} **Name**: ``{check["name"]}`` \n> **Health**: {health}')
                embed.add_field(name=f'{emojis.dash} Hunger', value=f'{hunger}', inline=True)
                embed.add_field(name=f'{emojis.dash} Thirst', value=f'{thirst}', inline=True)
                embed.add_field(name=f'{emojis.dash} Hygiene', value=f'{hygiene}', inline=True)
                embed.add_field(name=f'{emojis.dash} Fun', value=f'{fun}', inline=True)
                embed.add_field(name=f'{emojis.dash} Love', value=f'{love}', inline=True)
                embed.add_field(name=f'{emojis.dash} Energy', value=f'{energy}', inline=True)
                await ctx.send(embed=embed)
            else:
                px = functions.get_prefix(ctx)
                embed = discord.Embed(description=f'> {emojis.false} You dont own a **Pet**, buy one in the ``{px}shop``', color=color.fail)
                await ctx.send(embed=embed)
        else:
            embed = discord.Embed(description=f'> {emojis.false} This command is a **Premium** only feature, to learn more about it, join our [``Support Server``](https://discord.gg/snore)', color=color.color)
            await ctx.send(embed=embed)

    @pet.command(aliases=['inv'], brief='look at your pet inventory', description='pets')
    @blacklist_check()
    async def inventory(self, ctx):
        if not premium.find_one({"_id": ctx.message.author.id}):
            embed = discord.Embed(description=f'> {emojis.false} This command is a **Premium** only feature, to learn more about it, join our [``Support Server``](https://discord.gg/snore)', color=color.color)
            await ctx.send(embed=embed)
        else:
            if not collection.find_one({"_id": ctx.message.author.id}):
                px = functions.get_prefix(ctx)
                embed = discord.Embed(description=f'> {emojis.false} You dont own a **Pet**, buy one in the ``{px}shop``', color=color.fail)
                await ctx.send(embed=embed)
            else:
                check = collection.find_one({"_id": ctx.message.author.id})
                check2 = inventory.find_one({"_id": ctx.message.author.id})
                embed = discord.Embed(title=f'{emojis.blade} Pet Inventory', color=color.color)

                if check['pet'] == 'Spider':
                    embed.add_field(name=f'{emojis.dash} Food', value=f'{emojis.reply2}Flys: ``{check2["flys"]}`` \n{emojis.reply} Insects: ``{check2["insects"]}``')
                    embed.add_field(name=f'{emojis.dash} Drinks', value=f'{emojis.reply}Water: ``{check2["water"]}``')

                if check['pet'] == 'Snake':
                    embed.add_field(name=f'{emojis.dash} Food', value=f'{emojis.reply}Rats: ``{check2["rats"]}``')
                    embed.add_field(name=f'{emojis.dash} Drinks', value=f'{emojis.reply}Water: ``{check2["water"]}``')

                if check['pet'] == 'Dog':
                    embed.add_field(name=f'{emojis.dash} Food', value=f'{emojis.reply}Steak: ``{check2["steak"]}``')
                    embed.add_field(name=f'{emojis.dash} Drinks', value=f'{emojis.reply}Water: ``{check2["water"]}``')

                if check['pet'] == 'Cat':
                    embed.add_field(name=f'{emojis.dash} Food', value=f'{emojis.reply}Fish: ``{check2["fish"]}``')
                    embed.add_field(name=f'{emojis.dash} Drinks', value=f'{emojis.reply}Milk: ``{check2["milk"]}``')

                if check['pet'] == 'Monkey':
                    embed.add_field(name=f'{emojis.dash} Food', value=f'{emojis.reply}Bananas: ``{check2["bananas"]}``')
                    embed.add_field(name=f'{emojis.dash} Drinks', value=f'{emojis.reply}Water: ``{check2["water"]}``')
                
                if check['pet'] == 'Unicorn':
                    embed.add_field(name=f'{emojis.dash} Food', value=f'{emojis.reply}Corn: ``{check2["corn"]}``')
                    embed.add_field(name=f'{emojis.dash} Drinks', value=f'{emojis.reply}Water: ``{check2["water"]}``')

                if check['pet'] == 'Sloth':
                    embed.add_field(name=f'{emojis.dash} Food', value=f'{emojis.reply}Leaf: ``{check2["leaf"]}``')
                    embed.add_field(name=f'{emojis.dash} Drinks', value=f'{emojis.reply}Water: ``{check2["water"]}``')

                await ctx.send(embed=embed)

    @pet.command(brief='rename your pet', description='pets')
    @blacklist_check()
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def rename(self, ctx, *, name=None):
        if premium.find_one({"_id": ctx.message.author.id}):
            if collection.find_one({"_id": ctx.message.author.id}):
                if name == None:
                    embed = discord.Embed(description=f'> {emojis.false} You have to write a **Name** to name it', color=color.fail)
                    await ctx.send(embed=embed)

                else:
                    collection.update_one({"_id": ctx.message.author.id}, {"$set": {"name": name}})
                    embed = discord.Embed(description=f'> {emojis.true} Changed your **Pets** name to ``{name}``', color=color.success)
                    await ctx.send(embed=embed)

            else:
                px = functions.get_prefix(ctx)
                embed = discord.Embed(description=f'> {emojis.false} You dont own a **Pet**, buy one in the ``{px}shop``', color=color.fail)
                await ctx.send(embed=embed)

        else:
            embed = discord.Embed(description=f'> {emojis.false} This command is a **Premium** only feature, to learn more about it, join our [``Support Server``](https://discord.gg/snore)', color=color.color)
            await ctx.send(embed=embed)

    @commands.command(brief='give your pet some love', description='pets')
    @blacklist_check()
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def love(self, ctx):
        if not premium.find_one({"_id": ctx.message.author.id}):
            embed = discord.Embed(description=f'> {emojis.false} This command is a **Premium** only feature, to learn more about it, join our [``Support Server``](https://discord.gg/snore)', color=color.color)
            await ctx.send(embed=embed)
        else:
            if not collection.find_one({"_id": ctx.message.author.id}):
                px = functions.get_prefix(ctx)
                embed = discord.Embed(description=f'> {emojis.false} You dont own a **Pet**, buy one in the ``{px}shop``', color=color.fail)
                await ctx.send(embed=embed)

            else:
                check = collection.find_one({"_id": ctx.message.author.id})

                love = ['pet', 'hug']

                embed = discord.Embed(description=f'> :revolving_hearts: You **{random.choice(love)}** your **{check["pet"]}**', color=color.color)
                message = await ctx.send(embed=embed)

                await asyncio.sleep(3)

                embed2 = discord.Embed(description=f'> :heart: Your **{check["pet"]}** is now full of **Love** again', color=color.color)
                try:
                    collection.update_one({"_id": ctx.message.author.id}, {"$set": {"love": 10}})
                    await ctx.message.reply(embed=embed2, mention_author=False)
                except:
                    await ctx.send(embed=embed2)

    @commands.command(brief='wash your pet', description='pets')
    @blacklist_check()
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def wash(self, ctx):
        if not premium.find_one({"_id": ctx.message.author.id}):
            embed = discord.Embed(description=f'> {emojis.false} This command is a **Premium** only feature, to learn more about it, join our [``Support Server``](https://discord.gg/snore)', color=color.color)
            await ctx.send(embed=embed)

        else:
            if not collection.find_one({"_id": ctx.message.author.id}):
                px = functions.get_prefix(ctx)
                embed = discord.Embed(description=f'> {emojis.false} You dont own a **Pet**, buy one in the ``{px}shop``', color=color.fail)
                await ctx.send(embed=embed)

            else:
                check = collection.find_one({"_id": ctx.message.author.id})

                if check['energy'] < 3:
                    embed = discord.Embed(description=f'> :low_battery: Your **{check["pet"]}** dosnt have enough **Energy** let him ``Sleep`` first.', color=color.color)
                    await ctx.send(embed=embed)

                elif check['hygiene'] < 10:
                    embed = discord.Embed(description=f'> :shower: You **wash** your **{check["pet"]}**', color=color.color)
                    message = await ctx.send(embed=embed)

                    await asyncio.sleep(3)

                    embed2 = discord.Embed(description=f'> :sweat_drops: Your **{check["pet"]}** is now **Clean** again', color=color.color)

                    try:
                        collection.update_one({"_id": ctx.message.author.id}, {"$set": {"hygiene": 10}})
                        await ctx.message.reply(embed=embed2, mention_author=False)

                    except:
                        await ctx.send(embed=embed2)
                        
                else:
                    embed = discord.Embed(description=f'> Your **{check["pet"]}** isnt **Dirty**', color=color.color)
                    await ctx.send(embed=embed)

    @commands.command(brief='put your pet to sleep', description='pets')
    @blacklist_check()
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def sleep(self, ctx):
        if not premium.find_one({"_id": ctx.message.author.id}):
            embed = discord.Embed(description=f'> {emojis.false} This command is a **Premium** only feature, to learn more about it, join our [``Support Server``](https://discord.gg/snore)', color=color.color)
            await ctx.send(embed=embed)
        else:
            if not collection.find_one({"_id": ctx.message.author.id}):
                px = functions.get_prefix(ctx)
                embed = discord.Embed(description=f'> {emojis.false} You dont own a **Pet**, buy one in the ``{px}shop``', color=color.fail)
                await ctx.send(embed=embed)
            else:
                check = collection.find_one({"_id": ctx.message.author.id})
                if check['energy'] < 10:
                    embed = discord.Embed(description=f'> :zzz: You put your **{check["pet"]}** to **Sleep**', color=color.color)
                    message = await ctx.send(embed=embed)

                    time = (10 - check['energy']) * 10
                    await asyncio.sleep(time)

                    embed2 = discord.Embed(description=f'> :zzz: Your **{check["pet"]}** sleeped for ``{str(time)}s`` and has now **Energy** again!', color=color.color)
                    try:
                        collection.update_one({"_id": ctx.message.author.id}, {"$set": {"energy": 10}})
                        await ctx.message.reply(embed=embed2, mention_author=False)
                    except:
                        await ctx.send(embed=embed2)
                else:
                    embed = discord.Embed(description=f'> Your **{check["pet"]}** dosnt need to **Sleep** right now', color=color.color)
                    await ctx.send(embed=embed)

    @commands.command(brief='play with your pet', description='pets')
    @blacklist_check()
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def play(self, ctx):
        if not premium.find_one({"_id": ctx.message.author.id}):
            embed = discord.Embed(description=f'> {emojis.false} This command is a **Premium** only feature, to learn more about it, join our [``Support Server``](https://discord.gg/snore)', color=color.color)
            await ctx.send(embed=embed)
        else:
            if not collection.find_one({"_id": ctx.message.author.id}):
                px = functions.get_prefix(ctx)
                embed = discord.Embed(description=f'> {emojis.false} You dont own a **Pet**, buy one in the ``{px}shop``', color=color.fail)
                await ctx.send(embed=embed)
            else:
                check = collection.find_one({"_id": ctx.message.author.id})
                if check['energy'] < 3:
                    embed = discord.Embed(description=f'> :low_battery: Your **{check["pet"]}** dosnt have enough **Energy** let him ``Sleep`` first.', color=color.color)
                    await ctx.send(embed=embed)
                elif check['fun'] < 10:
                    embed = discord.Embed(description=f'> :zap: You started to **Play** with your **{check["pet"]}**', color=color.color)
                    message = await ctx.send(embed=embed)

                    spin = random.randint(1, 360)
                    await asyncio.sleep(spin)

                    embed2 = discord.Embed(description=f'> :zap: You **Played** with your **{check["pet"]}** for ``{str(spin)}s``', color=color.color)
                    try:
                        collection.update_one({"_id": ctx.message.author.id}, {"$set": {"hygiene": check['hygiene'] - random.randint(0, 2)}})
                        collection.update_one({"_id": ctx.message.author.id}, {"$set": {"energy": check['energy'] - random.randint(0, 2)}})
                        collection.update_one({"_id": ctx.message.author.id}, {"$set": {"fun": 10}})
                        await ctx.message.reply(embed=embed2, mention_author=False)
                    except:
                        await ctx.send(embed=embed2)
                else:
                    embed = discord.Embed(description=f'> Your **{check["pet"]}** dosnt want to **Play** right now', color=color.color)
                    await ctx.send(embed=embed)

    @commands.command(brief='have a meetup with others', description='pets')
    @blacklist_check()
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def meetup(self, ctx, user: discord.Member=None):
        if not premium.find_one({"_id": ctx.message.author.id}):
            embed = discord.Embed(description=f'> {emojis.false} This command is a **Premium** only feature, to learn more about it, join our [``Support Server``](https://discord.gg/snore)', color=color.color)
            await ctx.send(embed=embed)
        else:
            if not collection.find_one({"_id": ctx.message.author.id}):
                px = functions.get_prefix(ctx)
                embed = discord.Embed(description=f'> {emojis.false} You dont own a **Pet**, buy one in the ``{px}shop``', color=color.fail)
                await ctx.send(embed=embed)
            else:
                if collection.find_one({"_id": ctx.message.author.id, "pet": 'Dog'}) or collection.find_one({"_id": ctx.message.author.id, "pet": 'Cat'}):
                    if user == None:
                        embed = discord.Embed(description=f'> With which **Member** do you want to **Meet up**?', color=color.color)
                        await ctx.send(embed=embed)
                    else:
                        if collection.find_one({"_id": ctx.message.author.id})['energy'] < 3:
                            embed = discord.Embed(description=f'> Your **{check["pet"]}** dosnt have enough **Energy** let him ``Sleep`` first.', color=color.color)
                            await ctx.send(embed=embed)
                        elif not collection.find_one({"_id": user.id}):
                            embed = discord.Embed(description=f'> {emojis.false} {user.mention} dosnt own a Pet!', color=color.color)
                            await ctx.send(embed=embed)
                        else:
                            if collection.find_one({"_id": ctx.message.author.id, "pet": 'Dog'}) and collection.find_one({"_id": user.id, "pet": 'Dog'}):
                                check = collection.find_one({"_id": ctx.message.author.id})
                                check2 = collection.find_one({"_id": user.id})

                                accept = discord.ui.Button(style=discord.ButtonStyle.green, label="yes", emoji=emojis.true)
                                decline = discord.ui.Button(style=discord.ButtonStyle.red, label="no", emoji=emojis.false)

                                async def accept_callback(interaction):
                                    if interaction.user != user:
                                        embed = discord.Embed(description=f"> {emojis.false} This is not your message", color=color.fail)
                                        await interaction.response.send_message(embed=embed, view=None, ephemeral=True)
                                        return
                                    else:
                                        embed = discord.Embed(description=f'> {user.mention} accepted the Inventation to the **Meet Up**', color=color.color)
                                        message = await interaction.response.edit_message(embed=embed, view=view)

                                        await asyncio.sleep(2)

                                        park = discord.Embed(description=f'> {ctx.message.author.mention} and {user.mention} going to the Park', color=color.color)
                                        await message.edit(embed=park)

                                        await asyncio.sleep(2)

                                        arrived = discord.Embed(description=f'> {check["name"]} and {check2["name"]} are **Playing** now', color=color.color)
                                        await message.edit(embed=arrived)

                                        time = random.randint(1, 360)
                                        await asyncio.sleep(time)

                                        one = ['run a mile', 'chased a squirrel']
                                        two = ['catched balls', 'played fighting']
                                        three = ['fought over a ball', 'swom in water']

                                        collection.update_one({"_id": ctx.message.author.id}, {"$set": {"energy": random.randint(1, 8)}})
                                        collection.update_one({"_id": user.id}, {"$set": {"energy": random.randint(1, 8)}})

                                        collection.update_one({"_id": ctx.message.author.id}, {"$set": {"hygiene": random.randint(1, 8)}})
                                        collection.update_one({"_id": user.id}, {"$set": {"hygiene": random.randint(1, 8)}})

                                        collection.update_one({"_id": ctx.message.author.id}, {"$set": {"fun": 10}})
                                        collection.update_one({"_id": user.id}, {"$set": {"fun": 10}})

                                        done = discord.Embed(description=f'> {check["name"]} and {check2["name"]} played for ``{time}s`` and they {random.choice(one)}, {random.choice(two)} and {random.choice(three)}', color=color.color)
                                        await message.edit(embed=done)

                                async def decline_callback(interaction):
                                    accept = discord.ui.Button(style=discord.ButtonStyle.green, label="yes", emoji=emojis.true, disabled = True)
                                    decline = discord.ui.Button(style=discord.ButtonStyle.red, label="no", emoji=emojis.false, disabled = True)

                                    accept.callback = accept_callback
                                    decline.callback = decline_callback

                                    view = discord.ui.View()
                                    view.add_item(item=accept)
                                    view.add_item(item=decline)

                                    if interaction.user != user:
                                        embed = discord.Embed(description=f"> {emojis.false} This is not your message", color=color.fail)
                                        await interaction.response.send_message(embed=embed, view=None, ephemeral=True)
                                        return
                                    else:
                                        embed = discord.Embed(description=f'> {user.mention} decline the Inventation for the **Meet Up**', color=color.color)
                                        await interaction.response.edit_message(embed=embed, view=view)

                                accept.callback = accept_callback
                                decline.callback = decline_callback

                                view = discord.ui.View()
                                view.add_item(item=accept)
                                view.add_item(item=decline)

                                embed = discord.Embed(description=f'> {user.mention} do you want to have a **Meet Up** with {ctx.message.author.mention}?', color=color.color)
                                await ctx.send(embed=embed, view=view)

                            elif collection.find_one({"_id": ctx.message.author.id, "pet": 'cat'}) and collection.find_one({"_id": user.id, "pet": 'cat'}):
                                await ctx.send('you both have a cat')

                            else:
                                check = collection.find_one({"_id": ctx.message.author.id})
                                check2 = collection.find_one({"_id": user.id})

                                accept = discord.ui.Button(style=discord.ButtonStyle.green, label="yes", emoji=emojis.true)
                                decline = discord.ui.Button(style=discord.ButtonStyle.red, label="no", emoji=emojis.false)

                                async def accept_callback(interaction):
                                    if interaction.user != user:
                                        embed = discord.Embed(description=f"> {emojis.false} This is not your message", color=color.fail)
                                        await interaction.response.send_message(embed=embed, view=None, ephemeral=True)
                                        return
                                    else:
                                        embed = discord.Embed(description=f'> {user.mention} accepted the Inventation to the **Meet Up**', color=color.color)
                                        message = await interaction.response.edit_message(embed=embed, view=view)

                                        await asyncio.sleep(2)

                                        park = discord.Embed(description=f'> {ctx.message.author.mention} and {user.mention} going to the Park', color=color.color)
                                        await message.edit(embed=park)

                                        await asyncio.sleep(2)

                                        arrived = discord.Embed(description=f'> {check["name"]} and {check2["name"]} are **Playing** now', color=color.color)
                                        await message.edit(embed=arrived)

                                        time = random.randint(1, 360)
                                        await asyncio.sleep(time)

                                        one = ['run away from a dog', 'played with a other cat']
                                        two = ['run up on a tree', 'sleep for a time']
                                        three = ['got pet by a kid', 'find a fish to eat']

                                        collection.update_one({"_id": ctx.message.author.id}, {"$set": {"energy": random.randint(1, 8)}})
                                        collection.update_one({"_id": user.id}, {"$set": {"energy": random.randint(1, 8)}})

                                        collection.update_one({"_id": ctx.message.author.id}, {"$set": {"hygiene": random.randint(1, 8)}})
                                        collection.update_one({"_id": user.id}, {"$set": {"hygiene": random.randint(1, 8)}})

                                        collection.update_one({"_id": ctx.message.author.id}, {"$set": {"fun": 10}})
                                        collection.update_one({"_id": user.id}, {"$set": {"fun": 10}})

                                        done = discord.Embed(description=f'> {check["name"]} and {check2["name"]} played for ``{time}s`` and they {random.choice(one)}, {random.choice(two)} and {random.choice(three)}')
                                        await message.edit(embed=done)

                                async def decline_callback(interaction):
                                    accept = discord.ui.Button(style=discord.ButtonStyle.green, label="yes", emoji=emojis.true, disabled = True)
                                    decline = discord.ui.Button(style=discord.ButtonStyle.red, label="no", emoji=emojis.false, disabled = True)

                                    accept.callback = accept_callback
                                    decline.callback = decline_callback

                                    view = discord.ui.View()
                                    view.add_item(item=accept)
                                    view.add_item(item=decline)

                                    if interaction.user != user:
                                        embed = discord.Embed(description=f"> {emojis.false} This is not your message", color=color.fail)
                                        await interaction.response.send_message(embed=embed, view=None, ephemeral=True)
                                        return
                                    else:
                                        embed = discord.Embed(description=f'> {user.mention} decline the Inventation for the **Meet Up**', color=color.color)
                                        await interaction.response.edit_message(embed=embed, view=view)

                                accept.callback = accept_callback
                                decline.callback = decline_callback

                                view = discord.ui.View()
                                view.add_item(item=accept)
                                view.add_item(item=decline)

                                embed = discord.Embed(description=f'> {user.mention} do you want to have a **Meet Up** with {ctx.message.author.mention}?', color=color.color)
                                await ctx.send(embed=embed, view=view)

                else:
                    embed = discord.Embed(description=f'> {emojis.false} To make **Meet ups** you need a ``Dog`` or ``Cat``', color=color.color)
                    await ctx.send(embed=embed)


    @commands.command(brief='let your pet drink something', description='pets')
    @blacklist_check()
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def drink(self, ctx, drink=None):
        if not premium.find_one({"_id": ctx.message.author.id}):
            embed = discord.Embed(description=f'> {emojis.false} This command is a **Premium** only feature, to learn more about it, join our [``Support Server``](https://discord.gg/snore)', color=color.color)
            await ctx.send(embed=embed)
        else:
            if not collection.find_one({"_id": ctx.message.author.id}):
                px = functions.get_prefix(ctx)
                embed = discord.Embed(description=f'> {emojis.false} You dont own a **Pet**, buy one in the ``{px}shop``', color=color.fail)
                await ctx.send(embed=embed)
            else:
                check = collection.find_one({"_id": ctx.message.author.id})
                check2 = inventory.find_one({"_id": ctx.message.author.id})

                if check['thirst'] < 10:
                    if drink == None:
                        embed = discord.Embed(description=f'> {emojis.false} What do you want to give your ``{check["pet"]}``?', color=color.color)
                        await ctx.send(embed=embed)

                    elif check['pet'] == 'Spider':
                        if drink == 'water':
                            if check2['water'] != 0:
                                if check['thirst'] + check2['water'] > 10:
                                    drunk = 10 - check['thirst']
                                    drink = check2['water'] - drunk

                                    collection.update_one({"_id": ctx.message.author.id}, {"$set": {"thirst": 10}})
                                    inventory.update_one({"_id": ctx.message.author.id}, {"$set": {"water": drink}})

                                    embed = discord.Embed(description=f'> :milk: You gave your **{check["pet"]}** ``{drunk}`` sips of Water, you have ``{drink}`` Water now', color=color.color)
                                    await ctx.send(embed=embed)

                                else:
                                    drink = check2['water'] + check['thirst']
                                    collection.update_one({"_id": ctx.message.author.id}, {"$set": {"thirst": drink}})
                                    inventory.update_one({"_id": ctx.message.author.id}, {"$set": {"water": 0}})

                                    embed = discord.Embed(description=f'> :milk: You gave your **{check["pet"]}** ``{check2["water"]}`` sips of Water, you have ``0`` Water now', color=color.color)
                                    await ctx.send(embed=embed)
                            else:
                                embed = discord.Embed(description=f'> {emojis.false} You dont have **Water** for your **{check["pet"]}**', color=color.color)
                                await ctx.send(embed=embed)
                        else:
                            embed = discord.Embed(description=f'> {emojis.false} You cant give your **{check["pet"]}** ``{drink}``', color=color.color)
                            await ctx.send(embed=embed)

                    elif check['pet'] == 'Snake':
                        if drink == 'water':
                            if check2['water'] != 0:
                                if check['thirst'] + check2['water'] > 10:
                                    drunk = 10 - check['thirst']
                                    drink = check2['water'] - drunk

                                    collection.update_one({"_id": ctx.message.author.id}, {"$set": {"thirst": 10}})
                                    inventory.update_one({"_id": ctx.message.author.id}, {"$set": {"water": drink}})

                                    embed = discord.Embed(description=f'> :milk: You gave your **{check["pet"]}** ``{drunk}`` sips of Water, you have ``{drink}`` Water now', color=color.color)
                                    await ctx.send(embed=embed)

                                else:
                                    drink = check2['water'] + check['thirst']
                                    collection.update_one({"_id": ctx.message.author.id}, {"$set": {"thirst": drink}})
                                    inventory.update_one({"_id": ctx.message.author.id}, {"$set": {"water": 0}})

                                    embed = discord.Embed(description=f'> :milk: You gave your **{check["pet"]}** ``{check2["water"]}`` sips of Water, you have ``0`` Water now', color=color.color)
                                    await ctx.send(embed=embed)
                            else:
                                embed = discord.Embed(description=f'> {emojis.false} You dont have **Water** for your **{check["pet"]}**', color=color.color)
                                await ctx.send(embed=embed)
                        else:
                            embed = discord.Embed(description=f'> {emojis.false} You cant give your **{check["pet"]}** ``{drink}``', color=color.color)
                            await ctx.send(embed=embed)

                    elif check['pet'] == 'Dog':
                        if drink == 'water':
                            if check2['water'] != 0:
                                if check['thirst'] + check2['water'] > 10:
                                    drunk = 10 - check['thirst']
                                    drink = check2['water'] - drunk

                                    collection.update_one({"_id": ctx.message.author.id}, {"$set": {"thirst": 10}})
                                    inventory.update_one({"_id": ctx.message.author.id}, {"$set": {"water": drink}})

                                    embed = discord.Embed(description=f'> :milk: You gave your **{check["pet"]}** ``{drunk}`` sips of Water, you have ``{drink}`` Water now', color=color.color)
                                    await ctx.send(embed=embed)

                                else:
                                    drink = check2['water'] + check['thirst']
                                    collection.update_one({"_id": ctx.message.author.id}, {"$set": {"thirst": drink}})
                                    inventory.update_one({"_id": ctx.message.author.id}, {"$set": {"water": 0}})

                                    embed = discord.Embed(description=f'> :milk: You gave your **{check["pet"]}** ``{check2["water"]}`` sips of Water, you have ``0`` Water now', color=color.color)
                                    await ctx.send(embed=embed)
                            else:
                                embed = discord.Embed(description=f'> {emojis.false} You dont have **Water** for your **{check["pet"]}**', color=color.color)
                                await ctx.send(embed=embed)
                        else:
                            embed = discord.Embed(description=f'> {emojis.false} You cant give your **{check["pet"]}** ``{drink}``', color=color.color)
                            await ctx.send(embed=embed)

                    elif check['pet'] == 'Cat':
                        if drink == 'milk':
                            if check2['milk'] != 0:
                                if check['thirst'] + check2['milk'] > 10:
                                    drunk = 10 - check['thirst']
                                    drink = check2['milk'] - drunk

                                    collection.update_one({"_id": ctx.message.author.id}, {"$set": {"thirst": 10}})
                                    inventory.update_one({"_id": ctx.message.author.id}, {"$set": {"milk": drink}})

                                    embed = discord.Embed(description=f'> :milk: You gave your **{check["pet"]}** ``{drunk}`` sips of Milk, you have ``{drink}`` Milk now', color=color.color)
                                    await ctx.send(embed=embed)

                                else:
                                    drink = check2['milk'] + check['thirst']
                                    collection.update_one({"_id": ctx.message.author.id}, {"$set": {"thirst": drink}})
                                    inventory.update_one({"_id": ctx.message.author.id}, {"$set": {"milk": 0}})

                                    embed = discord.Embed(description=f'> :milk: You gave your **{check["pet"]}** ``{check2["milk"]}`` sips of Milk, you have ``0`` Milk now', color=color.color)
                                    await ctx.send(embed=embed)
                            else:
                                embed = discord.Embed(description=f'> {emojis.false} You dont have **Milk** for your **{check["pet"]}**', color=color.color)
                                await ctx.send(embed=embed)
                        else:
                            embed = discord.Embed(description=f'> {emojis.false} You cant give your **{check["pet"]}** ``{drink}``', color=color.color)
                            await ctx.send(embed=embed)

                    elif check['pet'] == 'Monkey':
                        if drink == 'water':
                            if check2['water'] != 0:
                                if check['thirst'] + check2['water'] > 10:
                                    drunk = 10 - check['thirst']
                                    drink = check2['water'] - drunk

                                    collection.update_one({"_id": ctx.message.author.id}, {"$set": {"thirst": 10}})
                                    inventory.update_one({"_id": ctx.message.author.id}, {"$set": {"water": drink}})

                                    embed = discord.Embed(description=f'> :milk: You gave your **{check["pet"]}** ``{drunk}`` sips of Water, you have ``{drink}`` Water now', color=color.color)
                                    await ctx.send(embed=embed)

                                else:
                                    drink = check2['water'] + check['thirst']
                                    collection.update_one({"_id": ctx.message.author.id}, {"$set": {"thirst": drink}})
                                    inventory.update_one({"_id": ctx.message.author.id}, {"$set": {"water": 0}})

                                    embed = discord.Embed(description=f'> :milk: You gave your **{check["pet"]}** ``{check2["water"]}`` sips of Water, you have ``0`` Water now', color=color.color)
                                    await ctx.send(embed=embed)
                            else:
                                embed = discord.Embed(description=f'> {emojis.false} You dont have **Water** for your **{check["pet"]}**', color=color.color)
                                await ctx.send(embed=embed)
                        else:
                            embed = discord.Embed(description=f'> {emojis.false} You cant give your **{check["pet"]}** ``{drink}``', color=color.color)
                            await ctx.send(embed=embed)

                    elif check['pet'] == 'Unicorn':
                        if drink == 'water':
                            if check2['water'] != 0:
                                if check['thirst'] + check2['water'] > 10:
                                    drunk = 10 - check['thirst']
                                    drink = check2['water'] - drunk

                                    collection.update_one({"_id": ctx.message.author.id}, {"$set": {"thirst": 10}})
                                    inventory.update_one({"_id": ctx.message.author.id}, {"$set": {"water": drink}})

                                    embed = discord.Embed(description=f'> :milk: You gave your **{check["pet"]}** ``{drunk}`` sips of Water, you have ``{drink}`` Water now', color=color.color)
                                    await ctx.send(embed=embed)

                                else:
                                    drink = check2['water'] + check['thirst']
                                    collection.update_one({"_id": ctx.message.author.id}, {"$set": {"thirst": drink}})
                                    inventory.update_one({"_id": ctx.message.author.id}, {"$set": {"water": 0}})

                                    embed = discord.Embed(description=f'> :milk: You gave your **{check["pet"]}** ``{check2["water"]}`` sips of Water, you have ``0`` Water now', color=color.color)
                                    await ctx.send(embed=embed)
                            else:
                                embed = discord.Embed(description=f'> {emojis.false} You dont have **Water** for your **{check["pet"]}**', color=color.color)
                                await ctx.send(embed=embed)
                        else:
                            embed = discord.Embed(description=f'> {emojis.false} You cant give your **{check["pet"]}** ``{drink}``', color=color.color)
                            await ctx.send(embed=embed)

                    elif check['pet'] == 'Sloth':
                            if drink == 'water':
                                if check2['water'] != 0:
                                    if check['thirst'] + check2['water'] > 10:
                                        drunk = 10 - check['thirst']
                                        drink = check2['water'] - drunk

                                        collection.update_one({"_id": ctx.message.author.id}, {"$set": {"thirst": 10}})
                                        inventory.update_one({"_id": ctx.message.author.id}, {"$set": {"water": drink}})

                                        embed = discord.Embed(description=f'> :milk: You gave your **{check["pet"]}** ``{drunk}`` sips of Water, you have ``{drink}`` Water now', color=color.color)
                                        await ctx.send(embed=embed)

                                    else:
                                        drink = check2['water'] + check['thirst']
                                        collection.update_one({"_id": ctx.message.author.id}, {"$set": {"thirst": drink}})
                                        inventory.update_one({"_id": ctx.message.author.id}, {"$set": {"water": 0}})

                                        embed = discord.Embed(description=f'> :milk: You gave your **{check["pet"]}** ``{check2["water"]}`` sips of Water, you have ``0`` Water now', color=color.color)
                                        await ctx.send(embed=embed)
                                else:
                                    embed = discord.Embed(description=f'> {emojis.false} You dont have **Water** for your **{check["pet"]}**', color=color.color)
                                    await ctx.send(embed=embed)
                            else:
                                embed = discord.Embed(description=f'> {emojis.false} You cant give your **{check["pet"]}** ``{drink}``', color=color.color)
                                await ctx.send(embed=embed)
                else:
                    embed = discord.Embed(description=f'> Your **{check["pet"]}** is not **Thirsty**', color=color.color)
                    await ctx.send(embed=embed)

    @commands.command(brief='feed your pet', description='pets')
    @blacklist_check()
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def feed(self, ctx, food=None):
        if not premium.find_one({"_id": ctx.message.author.id}):
            embed = discord.Embed(description=f'> {emojis.false} This command is a **Premium** only feature, to learn more about it, join our [``Support Server``](https://discord.gg/snore)', color=color.color)
            await ctx.send(embed=embed)
        else:
            if not collection.find_one({"_id": ctx.message.author.id}):
                px = functions.get_prefix(ctx)
                embed = discord.Embed(description=f'> {emojis.false} You dont own a **Pet**, buy one in the ``{px}shop``', color=color.fail)
                await ctx.send(embed=embed)
            else:
                check = collection.find_one({"_id": ctx.message.author.id})
                check2 = inventory.find_one({"_id": ctx.message.author.id})

                if check['hunger'] < 10:
                    if food == None:
                        embed = discord.Embed(description=f'> {emojis.false} What do you want to give your ``{check["pet"]}``?', color=color.color)
                        await ctx.send(embed=embed)

                    elif check['pet'] == 'Spider':
                        if food == 'flys' or food == 'fly':
                            if check2['flys'] != 0:
                                if check['hunger'] + check2['flys'] > 10:
                                    feed = 10 - check['hunger']
                                    food = check2['flys'] - feed

                                    collection.update_one({"_id": ctx.message.author.id}, {"$set": {"hunger": 10}})
                                    inventory.update_one({"_id": ctx.message.author.id}, {"$set": {"flys": food}})

                                    embed = discord.Embed(description=f'> :carrot: You gave your **{check["pet"]}** ``{feed}`` Flys, you have ``{food}`` Flys now', color=color.color)
                                    await ctx.send(embed=embed)

                                else:
                                    feed = check2['flys'] + check['hunger']
                                    collection.update_one({"_id": ctx.message.author.id}, {"$set": {"hunger": feed}})
                                    inventory.update_one({"_id": ctx.message.author.id}, {"$set": {"flys": 0}})

                                    embed = discord.Embed(description=f'> :carrot: You gave your **{check["pet"]}** ``{check2["flys"]}`` Flys, you have ``0`` Flys now', color=color.color)
                                    await ctx.send(embed=embed)

                            else:
                                embed = discord.Embed(description=f'> {emojis.false} You dont have **Flys** for your **{check["pet"]}**', color=color.color)
                                await ctx.send(embed=embed)
                        elif food == 'insects' or food == 'insect':
                            if check2['insects'] != 0:
                                if check['hunger'] + check2['insects'] > 10:
                                    feed = 10 - check['hunger']
                                    food = check2['insects'] - feed

                                    collection.update_one({"_id": ctx.message.author.id}, {"$set": {"hunger": 10}})
                                    inventory.update_one({"_id": ctx.message.author.id}, {"$set": {"insects": food}})

                                    embed = discord.Embed(description=f'> :carrot: You gave your **{check["pet"]}** ``{feed}`` Insects, you have ``{food}`` Insects now', color=color.color)
                                    await ctx.send(embed=embed)

                                else:
                                    feed = check2['insects'] + check['hunger']
                                    collection.update_one({"_id": ctx.message.author.id}, {"$set": {"hunger": feed}})
                                    inventory.update_one({"_id": ctx.message.author.id}, {"$set": {"insects": 0}})

                                    embed = discord.Embed(description=f'> :carrot: You gave your **{check["pet"]}** ``{check2["insects"]}`` Insects, you have ``0`` Insects now', color=color.color)
                                    await ctx.send(embed=embed)
                            else:
                                embed = discord.Embed(description=f'> {emojis.false} You dont have any **Insects** for your **{check["pet"]}**', color=color.color)
                                await ctx.send(embed=embed)
                        else:
                            embed = discord.Embed(description=f'> {emojis.false} You cant give your **{check["pet"]}** ``{food}``', color=color.color)
                            await ctx.send(embed=embed)

                    elif check['pet'] == 'Snake':
                        if food == 'rat' or food == 'rats':
                            if check2['rats'] != 0:
                                if check['hunger'] + check2['rats'] > 10:
                                    feed = 10 - check['hunger']
                                    food = check2['rats'] - feed

                                    collection.update_one({"_id": ctx.message.author.id}, {"$set": {"hunger": 10}})
                                    inventory.update_one({"_id": ctx.message.author.id}, {"$set": {"rats": food}})

                                    embed = discord.Embed(description=f'> :carrot: You gave your **{check["pet"]}** ``{feed}`` Rats, you have ``{food}`` Rats now', color=color.color)
                                    await ctx.send(embed=embed)

                                else:
                                    feed = check2['rats'] + check['hunger']
                                    collection.update_one({"_id": ctx.message.author.id}, {"$set": {"hunger": feed}})
                                    inventory.update_one({"_id": ctx.message.author.id}, {"$set": {"rats": 0}})

                                    embed = discord.Embed(description=f'> :carrot: You gave your **{check["pet"]}** ``{check2["rats"]}`` Rats, you have ``0`` Rats now', color=color.color)
                                    await ctx.send(embed=embed)
                            else:
                                embed = discord.Embed(description=f'> {emojis.false} You dont have **Rats** for your **{check["pet"]}**', color=color.color)
                                await ctx.send(embed=embed)
                        else:
                            embed = discord.Embed(description=f'> {emojis.false} You cant give your **{check["pet"]}** ``{food}``', color=color.color)
                            await ctx.send(embed=embed)

                    elif check['pet'] == 'Dog':
                        if food == 'steaks' or food == 'steak':
                            if check2['steak'] != 0:
                                if check['hunger'] + check2['steak'] > 10:
                                    feed = 10 - check['hunger']
                                    food = check2['steak'] - feed

                                    collection.update_one({"_id": ctx.message.author.id}, {"$set": {"hunger": 10}})
                                    inventory.update_one({"_id": ctx.message.author.id}, {"$set": {"steak": food}})

                                    embed = discord.Embed(description=f'> :carrot: You gave your **{check["pet"]}** ``{feed}`` Steak, you have ``{food}`` Steak now', color=color.color)
                                    await ctx.send(embed=embed)

                                else:
                                    feed = check2['steak'] + check['hunger']
                                    collection.update_one({"_id": ctx.message.author.id}, {"$set": {"hunger": feed}})
                                    inventory.update_one({"_id": ctx.message.author.id}, {"$set": {"steak": 0}})

                                    embed = discord.Embed(description=f'> :carrot:You gave your **{check["pet"]}** ``{check2["steak"]}`` Steak, you have ``0`` Steak now', color=color.color)
                                    await ctx.send(embed=embed)
                            else:
                                embed = discord.Embed(description=f'> {emojis.false} You dont have **Rats** for your **{check["pet"]}**', color=color.color)
                                await ctx.send(embed=embed)
                        else:
                            embed = discord.Embed(description=f'> {emojis.false} You cant give your **{check["pet"]}** ``{food}``', color=color.color)
                            await ctx.send(embed=embed)

                    elif check['pet'] == 'Cat':
                        if food == 'fish' or food == 'fishs':
                            if check2['fish'] != 0:
                                if check['hunger'] + check2['fish'] > 10:
                                    feed = 10 - check['hunger']
                                    food = check2['fish'] - feed

                                    collection.update_one({"_id": ctx.message.author.id}, {"$set": {"hunger": 10}})
                                    inventory.update_one({"_id": ctx.message.author.id}, {"$set": {"fish": food}})

                                    embed = discord.Embed(description=f'> :carrot:You gave your **{check["pet"]}** ``{feed}`` Fish, you have ``{food}`` Fish now', color=color.color)
                                    await ctx.send(embed=embed)

                                else:
                                    feed = check2['fish'] + check['hunger']
                                    collection.update_one({"_id": ctx.message.author.id}, {"$set": {"hunger": feed}})
                                    inventory.update_one({"_id": ctx.message.author.id}, {"$set": {"fish": 0}})

                                    embed = discord.Embed(description=f'> :carrot: You gave your **{check["pet"]}** ``{check2["fish"]}`` Fish, you have ``0`` Fish now', color=color.color)
                                    await ctx.send(embed=embed)
                            else:
                                embed = discord.Embed(description=f'> {emojis.false} You dont have **Fish** for your **{check["pet"]}**', color=color.color)
                                await ctx.send(embed=embed)
                        else:
                            embed = discord.Embed(description=f'> {emojis.false} You cant give your **{check["pet"]}** ``{food}``', color=color.color)
                            await ctx.send(embed=embed)

                    elif check['pet'] == 'Monkey':
                        if food == 'bananas' or food == 'banana':
                            if check2['bananas'] != 0:
                                if check['hunger'] + check2['bananas'] > 10:
                                    feed = 10 - check['hunger']
                                    food = check2['bananas'] - feed

                                    collection.update_one({"_id": ctx.message.author.id}, {"$set": {"hunger": 10}})
                                    inventory.update_one({"_id": ctx.message.author.id}, {"$set": {"bananas": food}})

                                    embed = discord.Embed(description=f'> :carrot: You gave your **{check["pet"]}** ``{feed}`` Bananas, you have ``{food}`` Bananas now', color=color.color)
                                    await ctx.send(embed=embed)

                                else:
                                    feed = check2['bananas'] + check['hunger']
                                    collection.update_one({"_id": ctx.message.author.id}, {"$set": {"hunger": feed}})
                                    inventory.update_one({"_id": ctx.message.author.id}, {"$set": {"bananas": 0}})

                                    embed = discord.Embed(description=f'> :carrot: You gave your **{check["pet"]}** ``{check2["bananas"]}`` Bananas, you have ``0`` Bananas now', color=color.color)
                                    await ctx.send(embed=embed)
                            else:
                                embed = discord.Embed(description=f'> {emojis.false} You dont have **Banana** for your **{check["pet"]}**', color=color.color)
                                await ctx.send(embed=embed)
                        else:
                            embed = discord.Embed(description=f'> {emojis.false} You cant give your **{check["pet"]}** ``{food}``', color=color.color)
                            await ctx.send(embed=embed)

                    elif check['pet'] == 'Unicorn':
                        if food == 'corn':
                            if check2['corn'] != 0:
                                if check['hunger'] + check2['corn'] > 10:
                                    feed = 10 - check['hunger']
                                    food = check2['corn'] - feed

                                    collection.update_one({"_id": ctx.message.author.id}, {"$set": {"hunger": 10}})
                                    inventory.update_one({"_id": ctx.message.author.id}, {"$set": {"corn": food}})

                                    embed = discord.Embed(description=f'> :carrot: You gave your **{check["pet"]}** ``{feed}`` Corn, you have ``{food}`` Corn now', color=color.color)
                                    await ctx.send(embed=embed)

                                else:
                                    feed = check2['corn'] + check['hunger']
                                    collection.update_one({"_id": ctx.message.author.id}, {"$set": {"hunger": feed}})
                                    inventory.update_one({"_id": ctx.message.author.id}, {"$set": {"corn": 0}})

                                    embed = discord.Embed(description=f'> :carrot: You gave your **{check["pet"]}** ``{check2["corn"]}`` Corn, you have ``0`` Corn now', color=color.color)
                                    await ctx.send(embed=embed)
                            else:
                                embed = discord.Embed(description=f'> {emojis.false} You dont have **Corn** for your **{check["pet"]}**', color=color.color)
                                await ctx.send(embed=embed)
                        else:
                            embed = discord.Embed(description=f'> {emojis.false} You cant give your **{check["pet"]}** ``{food}``', color=color.color)
                            await ctx.send(embed=embed)

                    elif check['pet'] == 'Sloth':
                        if food == 'leaf':
                            if check2['leaf'] != 0:
                                if check['hunger'] + check2['leaf'] > 10:
                                    feed = 10 - check['hunger']
                                    food = check2['leaf'] - feed

                                    collection.update_one({"_id": ctx.message.author.id}, {"$set": {"hunger": 10}})
                                    inventory.update_one({"_id": ctx.message.author.id}, {"$set": {"leaf": food}})

                                    embed = discord.Embed(description=f'> :carrot: You gave your **{check["pet"]}** ``{feed}`` Leaves, you have ``{food}`` Leaves now', color=color.color)
                                    await ctx.send(embed=embed)

                                else:
                                    feed = check2['leaf'] + check['hunger']
                                    collection.update_one({"_id": ctx.message.author.id}, {"$set": {"hunger": feed}})
                                    inventory.update_one({"_id": ctx.message.author.id}, {"$set": {"leaf": 0}})

                                    embed = discord.Embed(description=f'> :carrot:You gave your **{check["pet"]}** ``{check2["leaf"]}`` Leaves, you have ``0`` Leaves now', color=color.color)
                                    await ctx.send(embed=embed)
                            else:
                                embed = discord.Embed(description=f'> {emojis.false} You dont have **Leaves** for your **{check["pet"]}**', color=color.color)
                                await ctx.send(embed=embed)
                        else:
                            embed = discord.Embed(description=f'> {emojis.false} You cant give your **{check["pet"]}** ``{food}``', color=color.color)
                            await ctx.send(embed=embed)
                else:
                    embed = discord.Embed(description=f'> Your **{check["pet"]}** dosnt need to be **Feeded**', color=color.color)
                    await ctx.send(embed=embed)

    @commands.command()
    @commands.is_owner()
    async def rempet(self, ctx, user: discord.Member=None):
        collection.delete_one({"_id": user.id})
        inventory.delete_one({"_id": user.id})

    @commands.command()
    @commands.is_owner()
    async def givepet(self, ctx, user: discord.User=None, item=None):
        if item == 'dog':
            pets = {"_id": user.id, "pet": 'Dog', "name": 'Lucky', "health": 10, "hunger": 10, "thirst": 10, "hygiene": 10, "fun": 10, "love": 10, "energy": 10}
            collection.insert_one(pets)
            inv = {"_id": user.id, "steak": 0, "water": 0}
            inventory.insert_one(inv)

        if item == 'cat':
            pets = {"_id": user.id, "pet": 'Cat', "name": 'Garfield', "health": 10, "hunger": 10, "thirst": 10, "hygiene": 10, "fun": 10, "love": 10, "energy": 10}
            collection.insert_one(pets)
            inv = {"_id": user.id, "fish": 0, "milk": 0}
            inventory.insert_one(inv)

        if item == 'spider':
            pets = {"_id": user.id, "pet": 'Spider', "name": 'Fang', "health": 10, "hunger": 10, "thirst": 10, "hygiene": 10, "fun": 10, "love": 10, "energy": 10}
            collection.insert_one(pets)
            inv = {"_id": user.id, "flys": 0, "insects": 0, "water": 0}
            inventory.insert_one(inv)

        if item == 'snake':
            pets = {"_id": user.id, "pet": 'Snake', "name": 'Buttercup', "health": 10, "hunger": 10, "thirst": 10, "hygiene": 10, "fun": 10, "love": 10, "energy": 10}
            collection.insert_one(pets)
            inv = {"_id": user.id, "rats": 0, "water": 0}
            inventory.insert_one(inv)

        if item == 'monkey':
            pets = {"_id": user.id, "pet": 'Monkey', "name": 'Bob', "health": 10, "hunger": 10, "thirst": 10, "hygiene": 10, "fun": 10, "love": 10, "energy": 10}
            collection.insert_one(pets)
            inv = {"_id": user.id, "bananas": 0, "water": 0}
            inventory.insert_one(inv)

        if item == 'unicorn':
            pets = {"_id": user.id, "pet": 'Unicorn', "name": 'Glitter', "health": 10, "hunger": 10, "thirst": 10, "hygiene": 10, "fun": 10, "love": 10, "energy": 10}
            collection.insert_one(pets)
            inv = {"_id": user.id, "corn": 0, "water": 0}
            inventory.insert_one(inv)

        if item == 'sloth':
            pets = {"_id": user.id, "pet": 'Sloth', "name": 'Sid', "health": 10, "hunger": 10, "thirst": 10, "hygiene": 10, "fun": 10, "love": 10, "energy": 10}
            collection.insert_one(pets)
            inv = {"_id": user.id, "leaf": 0, "water": 0}
            inventory.insert_one(inv)

        embed = discord.Embed(description=f'> {emojis.true} **Successfully** added {item} to {user.mention}', color=color.success)
        await ctx.send(embed=embed)

async def setup(client):
    await client.add_cog(pets(client))
