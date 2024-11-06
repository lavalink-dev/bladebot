import discord
import pymongo
from discord import File
from pymongo import MongoClient
from utils.emojis import emojis
from discord.ext import commands
from utils.color import color
from easy_pil import Editor, Canvas, load_image_async, Font

cluster = MongoClient('no')
db = cluster["blade"]
collection = db["level"]
rankcard = db["rankcard"]
config = db["levelconfig"]
blacklist = db["blacklist"]

class rank(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['level', 'lvl'], description='utility', brief='displays members level')
    async def rank(self, ctx, member: discord.Member = None):
        if config.find_one({"_id": ctx.message.guild.id}):
            check = config.find_one({"_id": ctx.message.guild.id})
            if check['level'] == True:

                if not member:
                    member = ctx.author

                check = collection.find_one({"user": member.id, "server": ctx.message.guild.id})

                next_level_xp = 750 + (1050 * check['level'])
                current_level_xp = check["xp"]
                xp_need = next_level_xp - current_level_xp
                xp_have = check["xp"] - current_level_xp

                percentage = 100 - (xp_need / 10)
                percentage = round(percentage)

                if percentage < 0:
                    percentage = 0

                #percentage = (current_level_xp / next_level_xp) * 100

                try:
                    if rankcard.find_one({"_id": member.id}):
                        check2 = rankcard.find_one({"_id": member.id})
                    image = check2['image']
                    background = await load_image_async(image)
                    background = Editor(background).resize((900,300))
                except:
                    background = Editor("./assets/rank/bg.png")
                profile = await load_image_async(str(member.display_avatar))

                profile_background = Editor("./assets/rank/pfp.png").resize((152, 152)).circle_image()
                profile = Editor(profile).resize((150, 150)).circle_image()

                poppins = Font.poppins(size=40)
                poppins_small = Font.poppins(size=30)

                square = Canvas((500, 500), "#06FFBF")
                square = Editor(square)
                square.rotate(30, expand=True)

                background.paste(square.image, (600, -250))
                background.paste(profile.image, (30, 30))
                background.paste(profile_background.image, (29, 29))

                background.rectangle((34, 223), width=650, height=40, fill="gray", radius=20)
                background.rectangle((30, 220), width=650, height=40, fill="white", radius=20)
                background.bar(
                        (30, 220),
                        max_width=650,
                        height=40,
                        percentage=percentage,
                        fill="#8E2DE2",
                        radius=20,
                    )
                background.text((202, 42), str(member), font=poppins, color="gray")
                background.text((200, 40), str(member), font=poppins, color="white")

                background.rectangle((200, 100), width=350, height=2, fill="#1C1B4B")
                background.text(
                        (202, 132),
                        f"Level : {check['level']} | "
                        + f" XP : {check['xp']} / {750 + (1050 * check['level'])}",
                        font=poppins_small,
                        color="gray",)
                background.text(
                        (200, 130),
                        f"Level : {check['level']} | "
                        + f" XP : {check['xp']} / {750 + (1050 * check['level'])}",
                        font=poppins_small,
                        color="white",)

                file = File(fp=background.image_bytes, filename="card.png")
                await ctx.send(file=file)
            else:
                return
            
async def setup(client):
    await client.add_cog(rank(client))
