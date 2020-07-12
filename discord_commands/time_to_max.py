import os
from pathlib import Path

import time_to_max as TTM
import discord

MAX_FILE_SIZE = 10 ** 7

async def cmd_time_to_max(ctx, arg1, arg2 = "EHP", arg3 = "Main"):
    if len(ctx.message.attachments):
        file = ctx.message.attachments[0]
        TTM.add_rate(file.url, str(ctx.author.id), arg1.lower())
        await ctx.send("Rates successfully added.")
    else:
        if arg2 != "EHP":
            arg2 = arg2[3:-1]
        how_to_train, ttm = TTM.get_ttm(arg1, arg2.lower(), arg3.lower())
        embed = discord.Embed(description="Time required for each skilling method to max (in hours)")
        embed.title = "Time to max for " + arg1
        maxed = True
        for method, time in how_to_train.items():
            if time > 0:
                maxed = False
                embed.add_field(name=method, value=str(time), inline=True)
        if maxed:
            embed.add_field(name="Anything", value="0, you're already maxed!")
        embed.set_footer(text="Time to max: " + str(ttm))
        await ctx.send(embed=embed)

async def cmd_time_to_200m_all(ctx, arg1, arg2 = "EHP", arg3 = "Main"):
    if len(ctx.message.attachments):
        file = ctx.message.attachments[0]
        TTM.add_rate(file.url, str(ctx.author.id), arg1.lower())
        await ctx.send("Rates successfully added.")
    else:
        if arg2 != "EHP":
            arg2 = arg2[3:-1]
        how_to_train, ttm = TTM.get_tt200m(arg1, arg2.lower(), arg3.lower())
        embed = discord.Embed(description="Time required for each skilling method to 200m xp (in hours)")
        embed.title = "Time to 200m for " + arg1
        maxed = True
        for method, time in how_to_train.items():
            if time > 0:
                maxed = False
                embed.add_field(name=method, value=str(time), inline=True)
        if maxed:
            embed.add_field(name="Anything", value="0, you're already 200m!")
        embed.set_footer(text="Time to 200m: " + str(ttm))
        await ctx.send(embed=embed)

async def cmd_rates(ctx, discord_handle = None):
    """Shows a list of rates the mentioned person has uploaded:
        !rates ?@name
    parameters:
        discord_handle - The discord handle of the person (@them)
        ignoretrash - Whether to exclude the drops generally considered trash (jars, etc)
    
    Note: ? denotes optional."""
    discord_id = ctx.author.id
    if discord_handle != None:
        discord_id = int(discord_handle[3:-1])
    owners_name = ctx.bot.get_user(discord_id).name
    title = "Rates uploaded by " + owners_name
    folder_path = Path("xp_rates") / str(discord_id)
    description = "\n".join(os.listdir(folder_path))
    embed = discord.Embed(title=title, description=description)
    await ctx.send(embed=embed)
