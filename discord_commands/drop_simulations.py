from fractions import Fraction

import discord

import drop_simulations
import probability_flavour_text
from drop_simulations import tob

async def cmd_finish(ctx, name: str, trials = 1, extraArg1 = "True", extraArg2 = "False"):
    if trials > 10000:
            await ctx.send("I like to actually use my PC, prick, 10k completions for you. If you tried Zulrah then double fuck you, my PC weeps.")
            trials = 10000
    elif trials < 1:
        trials = 1
    average_kc = 0
    average_item_kcs = {}
    average_items_found = {}
    title = ""
    description = "The average amount of each item obtained during completion, as well as the average KC to first see each item."
    embed = discord.Embed(description=description)
    async with ctx.typing():
        if name.lower() == "tob":
            if extraArg1 == "True":
                extraArg1 = "4"
            if trials > 1:
                title = "Simulation of " + str(trials) + " Theatre of Blood completions, with a team size of " + extraArg1
            else:
                title = "Simulation of a Theatre of Blood completion, with a team size of " + extraArg1
            if extraArg2 == "False":
                title += ", where you do not get MvP in any room"
            else: 
                title += ", where you get MvP in every room"
            average_kc, average_item_kcs, average_items_found, trash_drops = tob.simulate(trials, int(extraArg1), extraArg2 == "True")
        else:
            title = "Simulation of " + str(trials) + " " + name + " completion(s)"
            average_kc, average_item_kcs, average_items_found, trash_drops = drop_simulations.simulate(name, trials, extraArg1 == "True")
        for itemName in average_item_kcs.keys():
            empirical_rate = average_items_found[itemName] / average_kc
            empirical_rate_frac = Fraction(empirical_rate).limit_denominator(100000)
            empirical_rate_frac_simplified = Fraction(1, round(empirical_rate_frac.denominator / empirical_rate_frac.numerator))
            embed.add_field(name=itemName, value="Amount: " + str(average_items_found[itemName]) + "\nFirst seen: " + str(average_item_kcs[itemName]) + \
                "\nEmpirical rate: " + str(empirical_rate_frac_simplified))
        footer = "Average completion KC: " + str(average_kc)
        if extraArg1 == "True" and len(trash_drops) > 0:
            footer = footer + "\nIgnored drops: " + str(trash_drops)
        embed.set_footer(text=footer)
    embed.title = title
    await ctx.send(embed=embed)

async def cmd_dry(ctx, name: str, trials = 100, extraArg1 = "True", extraArg2 = "False"):
    """Calculates the probability of a dry streak at an activity.
    Syntax:
        !dry activity ?*ignoretrash
    parameters:
        activity - The activity to simulate (bandos, corp,.. See !activities)
        ignoretrash - Whether to exclude the drops generally considered trash (jars, etc)
    
    Note: ? denotes optional. * denotes boolean (True or False, case sensitive))"""
    # Tob drop table varies based on various factors.
    if name == "tob":
        # If dry command called for ToB, this arg represents team size.
        if extraArg1 == "True":
            # Replace the default value.
            extraArg1 = "4"
        # The second extra arg represents MvP in all rooms or not.
        probability = tob.dry(trials, int(extraArg1), extraArg2 == "True")
        title = "Chance of going " + str(trials) + " dry at the Theatre of Blood, with a team size of " + \
            extraArg1 + ""
        if extraArg2 == "False":
            title += ", where you do not get MvP in any room:\n\n"
        else: 
            title += ", where you get MvP in every room:\n\n" 
        title += str(probability * 100) + "%\n"
    else:
        probability, trash_drops = drop_simulations.dry(name, trials, extraArg1 == "True")
        title = "Chance of going " + str(trials) + " dry at " + name + ": " + str(probability * 100) + "%\n"
    description = probability_flavour_text.get_flavour(probability)
    embed = discord.Embed(title=title, description=description)
    if extraArg1 == "True" and name != "tob":
        embed.set_footer(text="Ignored drops: " + ", ".join(trash_drops[slice(0,-1)]) + " and " + trash_drops[-1])
    await ctx.send(embed=embed)
