import io
from pathlib import Path
import json
import requests
import os
import numpy
from scipy.optimize import linprog

LOOKUP_PATH = "https://secure.runescape.com/m=hiscore_oldschool/index_lite.ws?player="
WEB_ID_SKILLS = ["attack","defence","strength","hitpoints","range","prayer","magic","cooking","woodcutting","fletching","fishing","firemaking","crafting","smithing","mining","herblore","agility","thieving","slayer","farming","runecrafting","hunter","construction"]
LEVEL_99_XP = 13034431
TWO_HUNDRED_MIL_XP = 200000000

def add_rate(file_url, rate_owner, rate_name, folder_path = Path("xp_rates")):
    owners_folder_path = folder_path / rate_owner
    file_path = owners_folder_path / rate_name
    if not owners_folder_path.exists():
        os.makedirs(owners_folder_path)
    with open(file_path, "w+") as writer:
        writer.write(file_url)

def get_rates(rate_owner, rate_name, folder_path = Path("xp_rates")):
    file_path = folder_path / rate_owner / rate_name
    if file_path.exists():
        with open(file_path) as reader:
            url = reader.read()
            rates = requests.get(url)
            return json.loads(rates.text)
    else:
        return None

def get_player_xp(user_name):
    res = requests.get(LOOKUP_PATH + user_name)
    split_res = res.text.split("\n")
    current_xp_amounts = {}
    for i in range(24):
        if i == 0:
            continue
        current_xp_amounts[WEB_ID_SKILLS[i - 1]] = int(split_res[i].split(",")[2])
    return current_xp_amounts

def get_needed_xp(current_xp_amounts, target_xp = LEVEL_99_XP):
    needed_xp_amounts = {}
    for skill, xp in current_xp_amounts.items():
        if target_xp - xp < 0:
            needed_xp_amounts[skill] = 0
        else:
            needed_xp_amounts[skill] = target_xp - xp
    return needed_xp_amounts

def do_TTM(method_rates, xp_needed):
    all_skills = []
    for method, rates in method_rates.items():
        for xp_type in list(rates.keys()):
            if not xp_type in all_skills:
                all_skills.append(xp_type)

    method_indexes = {}
    index_methods = {}
    for index, training_method in enumerate(list(method_rates.keys())):
        method_indexes[training_method] = index
        index_methods[index] = training_method

    skill_indexes = {}
    for index, skill in enumerate(all_skills):
        skill_indexes[skill] = index

    xp_needed_matrix = numpy.empty(len(all_skills))
    for skill, xp in xp_needed.items():
        if skill in all_skills:
            xp_needed_matrix[skill_indexes[skill]] = -xp

    rate_matrix = numpy.zeros([len(all_skills), len(method_indexes)])
    for method, rates in method_rates.items():
        for skill, rate in rates.items():
            rate_matrix[skill_indexes[skill]][method_indexes[method]] = rate

    c = [-1 for i in range(len(method_indexes))]
    bounds = [(None, 0) for i in range(len(method_indexes))]
    efficient_time_spent = -linprog(c, rate_matrix, xp_needed_matrix, bounds=bounds).x
    how_to_train = {}
    for index, hours in enumerate(efficient_time_spent):
        how_to_train[index_methods[index]] = round(hours, 1)
    return (how_to_train, round(numpy.sum(efficient_time_spent), 1))

def get_ttm(user_name, rate_owner, rate_name):
    rates = get_rates(rate_owner, rate_name)
    current_xp = get_player_xp(user_name)
    xp_needed = get_needed_xp(current_xp)
    return do_TTM(rates, xp_needed)

def get_tt200m(user_name, rate_owner, rate_name):
    rates = get_rates(rate_owner, rate_name)
    current_xp = get_player_xp(user_name)
    xp_needed = get_needed_xp(current_xp, TWO_HUNDRED_MIL_XP)
    return do_TTM(rates, xp_needed)