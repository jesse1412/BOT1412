from fractions import Fraction

import discord

import drop_simulations
import probability_flavour_text
from drop_simulations import tob

MAX_TRIALS = 10000

async def cmd_finish(ctx, name: str, trials = 1, variable_arg = "True", mvp_all_rooms = "False"):
    if trials > MAX_TRIALS:
            await ctx.send("Limit exceeded, rolling maximum ({}).".format(MAX_TRIALS))
            trials = MAX_TRIALS
    elif trials < 1:
        trials = 1
    ignore_trash = variable_arg.lower() == "true"
    mvp_all_rooms = mvp_all_rooms.lower() == "true"
    average_kc = 0
    average_item_kcs = {}
    average_items_found = {}
    title = ""
    description = "The average amount of each item obtained during completion, as well as the average KC to first see each item."
    embed = discord.Embed(description=description)
    async with ctx.typing():
        if name.lower() == "tob":
            team_size = 4
            if variable_arg.isnumeric():
                team_size = max(1, min(5, variable_arg))
            mvp_text = "where you do not get MvP in any room"
            if mvp_all_rooms:
                mvp_text = "where you get MvP in every room"
            title = "Simulation of {} Theatre of Blood completion(s), with a team size of {} {}".format(
                str(trials), 
                mvp_text,
                team_size)
            average_kc, average_item_kcs, average_items_found, trash_drops = tob.simulate(trials, team_size, mvp_all_rooms)
        else:
            title = "Simulation of {} {} completion(s)".format(str(trials), name)
            average_kc, average_item_kcs, average_items_found, trash_drops = drop_simulations.simulate(name, trials, variable_arg.lower() == "true")
        for itemName in average_item_kcs.keys():
            empirical_rate = average_items_found[itemName] / average_kc
            empirical_rate_frac = Fraction(empirical_rate).limit_denominator(100000)
            empirical_rate_frac_simplified = Fraction(1, round(empirical_rate_frac.denominator / empirical_rate_frac.numerator))
            embed.add_field(name=itemName, value="Amount: {}\nFirst seen: {}\nEmpirical rate: {}".format(
                str(round(average_items_found[itemName], 3)), 
                str(round(average_item_kcs[itemName], 3)),
                str(empirical_rate_frac_simplified)))
        footer = "Average completion KC: " + str(average_kc)
        if ignore_trash and len(trash_drops) > 0:
            footer = footer + "\nIgnored drops: " + ", ".join(trash_drops[slice(0,-1)]) + ", and " + trash_drops[-1]
        embed.set_footer(text=footer)
    embed.title = title
    await ctx.send(embed=embed)

async def cmd_dry(ctx, name: str, trials = 100, variable_arg = "True", mvp_all_rooms = "False"):
    """Calculates the probability of a dry streak at an activity.
    Syntax:
        !dry activity ?*ignoretrash
    parameters:
        activity - The activity to simulate (bandos, corp,.. See !activities)
        ignoretrash - Whether to exclude the drops generally considered trash (jars, etc)
    
    Note: ? denotes optional. * denotes boolean (True or False, case sensitive))"""
    ignore_trash = variable_arg.lower() == "true"
    mvp_all_rooms = mvp_all_rooms.lower() == "true"
    if trials < 1:
        trials = 1
    if name == "tob":
        # If dry command called for ToB, this arg represents team size.
        team_size = 4
        if variable_arg.isnumeric():
            team_size = max(1, min(5, int(variable_arg)))
        probability = tob.dry(trials, team_size, mvp_all_rooms)
        mvp_text = "where you do not get MvP in any room"
        if mvp_all_rooms:
            mvp_text = "where you get MvP in every room"
        title = "Chance of going {} dry at the Theatre of Blood, with a team size of {} {}: {}%\n".format(
            trials,
            team_size,
            mvp_text,
            probability * 100)
    else:
        probability, trash_drops = drop_simulations.dry(name, trials, ignore_trash)
        title = "Chance of going {} dry at {}: {}%\n".format(
            trials,
            name,
            probability * 100
        )
    description = probability_flavour_text.get_flavour(probability)
    embed = discord.Embed(title=title, description=description)
    if ignore_trash and name != "tob":
        embed.set_footer(text="Ignored drops: " + ", ".join(trash_drops[slice(0,-1)]) + ", and " + trash_drops[-1])
    await ctx.send(embed=embed)
