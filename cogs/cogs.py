import discord
import sys
import os
from discord.ext import commands
from utils import functions
from utils.emojis import emojis
from utils.color import color

class cogs(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.is_owner()
    async def load(self, ctx, extension):
        try:
            if extension == 'all':
                for filename in os.listdir('./cogs'):
                    if filename.endswith('.py'):
                        await self.client.load_extension(f'cogs.{filename[:-3]}')

                embed = discord.Embed(description=f"> {emojis.true} **Succesfully** loaded **{extension}** ", color=color.success)
                message = await ctx.send(embed=embed)
                await message.delete()
                await ctx.message.delete()
            else:
                await self.client.load_extension(f'cogs.{extension}')
                embed = discord.Embed(description=f"> {emojis.true} **Succesfully** loaded **{extension}** ", color=color.success)
                message = await ctx.send(embed=embed)
                await message.delete()
                await ctx.message.delete()
        except Exception as e:
            print(e)
            embed = discord.Embed(description=f"> {emojis.false} **{extension}** couldnt be **loaded**", color=color.fail)
            message = await ctx.send(embed=embed)
            await message.delete()
            await ctx.message.delete()

    @commands.command()
    @commands.is_owner()
    async def unload(self, ctx, extension):
        try:
            await self.client.unload_extension(f'cogs.{extension}')
            embed = discord.Embed(description=f"> {emojis.true} **Succesfully** unloaded **{extension}**", color=color.success)
            message = await ctx.send(embed=embed)
            await message.delete()
            await ctx.message.delete()
        except Exception as e:
            print(e)
            embed = discord.Embed(description=f"> {emojis.false} **{extension}** couldnt be **unloaded**", color=color.fail)
            message = await ctx.send(embed=embed)
            await message.delete()
            await ctx.message.delete()

    @commands.command(aliases=['rl'])
    @commands.is_owner()
    async def reload(self, ctx, extension):
        try:
            if extension == 'all':
                for filename in os.listdir('./cogs'):
                    if filename.endswith('.py'):
                        await self.client.unload_extension(f'cogs.{filename[:-3]}')
                        await self.client.load_extension(f'cogs.{filename[:-3]}')
                        embed = discord.Embed(description=f"> {emojis.true} **Succesfully** reloaded all **Cogs**", color=color.success)
                        message = await ctx.send(embed=embed)
                        await message.delete()
                        await ctx.message.delete()
            else:
                await self.client.unload_extension(f'cogs.{extension}')
                await self.client.load_extension(f'cogs.{extension}')
                embed = discord.Embed(description=f"> {emojis.true} **Succesfully** reloaded **{extension}**", color=color.success)
                message = await ctx.send(embed=embed)
                await message.delete()
                await ctx.message.delete()
        except Exception as e:
                print(e)
                embed = discord.Embed(description=f"> {emojis.false} **{extension}** couldnt be **reloaded**", color=color.fail)
                message = await ctx.send(embed=embed)
                await message.delete()
                await ctx.message.delete()

async def setup(client):
    await client.add_cog(cogs(client))
