import copy
import drop_simulation

drop_tables = [
                {
                    "Scythe of Vitur": 1/19,
                    "Ghrazi rapier": 2/19,
                    "Sanguinesti staff": 2/19,
                    "Justiciar faceguard": 2/19,
                    "Justiciar chestguard": 2/19,
                    "Justiciar legguards": 2/19,
                    "Avernic defender hilt": 8/19
                },
                {
                    "Lil' zik": 1/650
                }
            ]

trash_drops = []

description = "The Theatre of Blood, an areana-like establishment located beneath the castle of Ver Sinhaza."

def simulate(trials, teamSize = 4, mvp = False):
    your_deaths = 0
    others_deaths = 0

    # Can ignore the rest.

    PARTICIPATION_POINTS = 3
    NUM_ROOMS = 6
    MVP_MAIDEN = 2
    MVP_BLOAT = 2
    MVP_NYLO = 1
    MVP_SOTETSTEG = 1
    MVP_XARPUS = 2
    MVP_VERZIK_P1 = 2
    MVP_VERZIK_P2 = 2
    MVP_VERZIK_P3 = 2
    TOTAL_MVP = MVP_MAIDEN + MVP_BLOAT + MVP_NYLO + MVP_SOTETSTEG \
        + MVP_XARPUS + MVP_VERZIK_P1 + MVP_VERZIK_P2 + MVP_VERZIK_P3
    DEATH = -4

    BASE_DROP_RATE = 1/9.1

    max_points = TOTAL_MVP + PARTICIPATION_POINTS * NUM_ROOMS * teamSize

    your_mvp_points = mvp * (MVP_MAIDEN + MVP_BLOAT + MVP_NYLO + MVP_SOTETSTEG + MVP_XARPUS + MVP_VERZIK_P1 \
        + MVP_VERZIK_P2 + MVP_VERZIK_P3)

    your_total_points = max(0, your_mvp_points \
        + NUM_ROOMS * PARTICIPATION_POINTS \
        + your_deaths * DEATH)

    your_teammates_mvp_points = TOTAL_MVP - your_mvp_points

    if teamSize > 1:
        your_team_mates_total_points = max(0, your_teammates_mvp_points \
        + NUM_ROOMS * PARTICIPATION_POINTS * (teamSize - 1) \
        + others_deaths * DEATH)
    else:
        your_team_mates_total_points = 0

    your_team_total_points = your_team_mates_total_points + your_total_points
    purple_factor = your_team_total_points / max_points
    purple_rate_team = BASE_DROP_RATE * purple_factor
    purple_rate_you = (your_total_points / your_team_total_points) * purple_rate_team
    chance_purple_is_yours = purple_rate_you / purple_rate_team
    if teamSize > 1:
        chance_pruple_is_others_unique = (1 - chance_purple_is_yours) / (teamSize - 1)
    else:
        chance_pruple_is_others_unique = 0

    your_drop_tables = copy.deepcopy(drop_tables)
    for table in your_drop_tables:
        for item_name in table.keys():
            if item_name == "Lil' zik":
                continue
            table[item_name] *= purple_rate_you

    return drop_simulation.simulate(your_drop_tables, trials) + (trash_drops,)

def get_specific_drop_tables(team_size = 4, mvp = False):
    your_deaths = 0
    others_deaths = 0

    # Can ignore the rest.

    PARTICIPATION_POINTS = 3
    NUM_ROOMS = 6
    MVP_MAIDEN = 2
    MVP_BLOAT = 2
    MVP_NYLO = 1
    MVP_SOTETSTEG = 1
    MVP_XARPUS = 2
    MVP_VERZIK_P1 = 2
    MVP_VERZIK_P2 = 2
    MVP_VERZIK_P3 = 2
    TOTAL_MVP = MVP_MAIDEN + MVP_BLOAT + MVP_NYLO + MVP_SOTETSTEG \
        + MVP_XARPUS + MVP_VERZIK_P1 + MVP_VERZIK_P2 + MVP_VERZIK_P3
    DEATH = -4

    BASE_DROP_RATE = 1/9.1

    max_points = TOTAL_MVP + PARTICIPATION_POINTS * NUM_ROOMS * team_size

    your_mvp_points = mvp * (MVP_MAIDEN + MVP_BLOAT + MVP_NYLO + MVP_SOTETSTEG + MVP_XARPUS + MVP_VERZIK_P1 \
        + MVP_VERZIK_P2 + MVP_VERZIK_P3)

    your_total_points = max(0, your_mvp_points \
        + NUM_ROOMS * PARTICIPATION_POINTS \
        + your_deaths * DEATH)

    your_team_mates_mvp_points = TOTAL_MVP - your_mvp_points

    if team_size > 1:
        your_team_mates_total_points = max(0, your_team_mates_mvp_points \
        + NUM_ROOMS * PARTICIPATION_POINTS * (team_size - 1) \
        + others_deaths * DEATH)
    else:
        your_team_mates_total_points = 0

    your_team_total_points = your_team_mates_total_points + your_total_points
    purple_factor = your_team_total_points / max_points
    purple_rate_team = BASE_DROP_RATE * purple_factor
    purple_rate_you = (your_total_points / your_team_total_points) * purple_rate_team
    chance_purple_is_yours = purple_rate_you / purple_rate_team
    if team_size > 1:
        chance_purple_is_others_unique = (1 - chance_purple_is_yours) / (team_size - 1)
    else:
        chance_purple_is_others_unique = 0

    your_drop_tables = copy.deepcopy(drop_tables)
    for table in your_drop_tables:
        for item_name in table.keys():
            if item_name == "Lil' zik":
                continue
            table[item_name] *= purple_rate_you
    return your_drop_tables

def dry(trials, teamSize = 4, mvp = False):
    specific_drop_table = get_specific_drop_tables(teamSize, mvp)
    return drop_simulation.dry(specific_drop_table, trials)