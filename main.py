import importlib
import json
import pkgutil
from pathlib import Path

import discord
from discord.ext import commands

import drop_simulations

from discord_commands.debt import cmd_debt
from discord_commands.time_to_max import cmd_time_to_max, cmd_time_to_200m_all, cmd_rates
from discord_commands.drop_simulations import cmd_finish, cmd_dry
from discord_token import DISCORD_TOKEN
from roles import allowed_roles

bot = commands.Bot(command_prefix="!")

@bot.command()
async def debt(ctx, name: str, name_2 = None, amount = None):
    """Manage debts
    Syntax:
        !debt name
        !debt name_owes name_owed +amount
        !debt name_owes name_owed -amount
        !debt name_owes name_owed amount
    Without +- specifiers, the debt will be directly replaced by the new amount"""
    await cmd_debt(ctx, name, name_2, amount)

MAX_FILE_SIZE = 10 ** 7
@bot.command()
async def ttm(ctx, arg1, arg2 = "EHP", arg3 = "Main"):
    """Check your TTM with custom, saved xp rates
    Syntax to check rates: 
        !ttm user_name @owner rates_name
    Syntax to upload rates (just attach a file and enter the command in the text field):
        !ttm rates_name
    Example of upload and rate check:
        !ttm my_rates
        !ttm my_osrs_name @my_discord_handle my_rates
    Each person can upload their own custom rates rather than just EHP rates
    These rates are associated with the uploader's discord account
    The rates are accessed directly from discord, if you delete the attachment, the rates are lost
    Hence when accessing, you specify the person and the xp list that they have collected
    EHP rates can be accessed by the following commands, main EHP is used be default:
        !ttm user_name EHP Main
    EHP rates currently only exist for mains.
    Rate files must be in JSON format.
    The format of the Main EHP rates can be seen here:
        https://cdn.discordapp.com/attachments/553676760357535745/702999634074665050/main_ehp.json 
    """
    await cmd_time_to_max(ctx, arg1, arg2, arg3)

@ttm.error
async def ttm_error(ctx, error):
    await ctx.send(str(error))
    print(error)

@bot.command()
async def tt200m(ctx, arg1, arg2 = "EHP", arg3 = "Main"):
    """Check your TTM with custom, saved xp rates
    Syntax to check rates: 
        !ttm user_name @owner rates_name
    Syntax to upload rates (just attach a file and enter the command in the text field):
        !ttm rates_name
    Example of upload and rate check:
        !ttm my_rates
        !ttm my_osrs_name @my_discord_handle my_rates
    Each person can upload their own custom rates rather than just EHP rates
    These rates are associated with the uploader's discord account
    The rates are accessed directly from discord, if you delete the attachment, the rates are lost
    Hence when accessing, you specify the person and the xp list that they have collected
    EHP rates can be accessed by the following commands, main EHP is used be default:
        !ttm user_name EHP Main
    EHP rates currently only exist for mains.
    Rate files must be in JSON format.
    The format of the Main EHP rates can be seen here:
        https://cdn.discordapp.com/attachments/553676760357535745/702999634074665050/main_ehp.json 
    """
    await cmd_time_to_200m_all(ctx, arg1, arg2, arg3)

@tt200m.error
async def tt200m_error(ctx, error):
    await ctx.send(str(error))
    print(error)

@bot.command()
async def rates(ctx, discord_handle = None):
    """Shows a list of rates the mentioned person has uploaded:
        !rates ?@name
    parameters:
        discord_handle - The discord handle of the person (@them)
        ignoretrash - Whether to exclude the drops generally considered trash (jars, etc)
    
    Note: ? denotes optional."""
    await cmd_rates(ctx, discord_handle)

@bot.command()
async def finish(ctx, name: str, trials = 1, extraArg1 = "True", extraArg2 = "False"):
    """Simulates the completion of an activity the requested amount of times and outputs empirical data about the sample.
    Syntax: 
        !finish activity ?trialcount ?*ignoretrash
        !finish tob ?trialcount ?teamsize ?*mvpallrooms
    parameters:
        activity - The activity to simulate (bandos, corp,.. See !activities)
        trialcount - The amount of times to complete the activity (finish getting all items once)
        ignoretrash - Whether to exclude the drops generally considered trash (jars, etc)
        mvpallrooms - To keep input brief, we assume you're either always mvp or never mvp, see https://twitter.com/jagexkieren/status/1145376451446751232?lang=en
    
    Note: ? denotes optional. * denotes boolean (True or False, case sensitive))"""
    await cmd_finish(ctx, name, trials, extraArg1, extraArg2)

@finish.error
async def finish_error(ctx, error):
    await ctx.send("Invalid !finish arguments.\nSyntax: \n\t!finish name trials ignoretrash\n\t" \
        + "!finish tob trials teamsize mvpallrooms\n" + str(error))
    print(error)

@bot.command()
async def stop(ctx):
    await bot.logout()

@bot.command()
async def role(ctx, role: discord.Role = None):
    """Toggle a discord role on or off."""
    if role is None:
        await ctx.send("List of assignable roles: " + str(allowed_roles))
    if role.name in allowed_roles:
        if not role in ctx.message.author.roles:
            await ctx.message.author.add_roles(role)
            await ctx.send("Role added.")
        else:
            await ctx.message.author.remove_roles(role)
            await ctx.send("Role removed.")       
    else:
        await ctx.send("That role doesn't exist, or you don't have permission to modify it.")

@bot.command()
async def activities(ctx):
    """Lists the activities that this bot can simulate."""
    embed = discord.Embed(description="Activities", title="List of activies available for simulation")
    for importer, modname, ispkg in pkgutil.iter_modules(drop_simulations.__path__):
        module = importlib.import_module("drop_simulations." + modname)
        embed.add_field(name=modname, value=module.description)
    await ctx.send(embed=embed)

@bot.command()
async def dry(ctx, name: str, trials = 100, extraArg1 = "True", extraArg2 = "False"):
    """Calculates the probability of a dry streak at an activity.
    Syntax:
        !dry activity ?*ignoretrash
    parameters:
        activity - The activity to simulate (bandos, corp,.. See !activities)
        ignoretrash - Whether to exclude the drops generally considered trash (jars, etc)
    
    Note: ? denotes optional. * denotes boolean (True or False, case sensitive))"""
    await cmd_dry(ctx, name, trials, extraArg1, extraArg2)

@dry.error
async def dry_error(ctx, error):
    await ctx.send("Invalid !dry arguments.\nSyntax: !dry name trials\n" + str(error))
    print(error)

if __name__ == '__main__':
    print("BOT1412 Beginning")
    bot.run(DISCORD_TOKEN)