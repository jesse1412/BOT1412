import copy
import dropsim
dropTables = [
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

trashDrops = []

description = "The Theatre of Blood, an areana-like establishment located beneath the castle of Ver Sinhaza."

def simulate(trials, teamSize = 4, mvp = False):
    yourDeaths = 0
    othersDeaths = 0

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

    maxPoints = TOTAL_MVP + PARTICIPATION_POINTS * NUM_ROOMS * teamSize

    yourMVPPoints = mvp * (MVP_MAIDEN + MVP_BLOAT + MVP_NYLO + MVP_SOTETSTEG + MVP_XARPUS + MVP_VERZIK_P1 \
        + MVP_VERZIK_P2 + MVP_VERZIK_P3)

    yourTotalPoints = max(0, yourMVPPoints \
        + NUM_ROOMS * PARTICIPATION_POINTS \
        + yourDeaths * DEATH)

    yourTeamMatesMVPPoints = TOTAL_MVP - yourMVPPoints

    if teamSize > 1:
        yourTeamMatesTotalPoints = max(0, yourTeamMatesMVPPoints \
        + NUM_ROOMS * PARTICIPATION_POINTS * (teamSize - 1) \
        + othersDeaths * DEATH)
    else:
        yourTeamMatesTotalPoints = 0

    yourTeamTotalPoints = yourTeamMatesTotalPoints + yourTotalPoints
    purpleFactor = yourTeamTotalPoints / maxPoints
    purpleRateTeam = BASE_DROP_RATE * purpleFactor
    purpleRateYou = (yourTotalPoints / yourTeamTotalPoints) * purpleRateTeam
    chancePurpleIsYours = purpleRateYou / purpleRateTeam
    if teamSize > 1:
        chancePurpleIsOthersUnique = (1 - chancePurpleIsYours) / (teamSize - 1)
    else:
        chancePurpleIsOthersUnique = 0

    yourDropTables = copy.deepcopy(dropTables)
    for table in yourDropTables:
        for itemName in table.keys():
            if itemName == "Lil' zik":
                continue
            table[itemName] *= purpleRateYou

    return dropsim.simulate(yourDropTables, trials) + (trashDrops,)

def getSpecificDropTables(teamSize = 4, mvp = False):
    yourDeaths = 0
    othersDeaths = 0

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

    maxPoints = TOTAL_MVP + PARTICIPATION_POINTS * NUM_ROOMS * teamSize

    yourMVPPoints = mvp * (MVP_MAIDEN + MVP_BLOAT + MVP_NYLO + MVP_SOTETSTEG + MVP_XARPUS + MVP_VERZIK_P1 \
        + MVP_VERZIK_P2 + MVP_VERZIK_P3)

    yourTotalPoints = max(0, yourMVPPoints \
        + NUM_ROOMS * PARTICIPATION_POINTS \
        + yourDeaths * DEATH)

    yourTeamMatesMVPPoints = TOTAL_MVP - yourMVPPoints

    if teamSize > 1:
        yourTeamMatesTotalPoints = max(0, yourTeamMatesMVPPoints \
        + NUM_ROOMS * PARTICIPATION_POINTS * (teamSize - 1) \
        + othersDeaths * DEATH)
    else:
        yourTeamMatesTotalPoints = 0

    yourTeamTotalPoints = yourTeamMatesTotalPoints + yourTotalPoints
    purpleFactor = yourTeamTotalPoints / maxPoints
    purpleRateTeam = BASE_DROP_RATE * purpleFactor
    purpleRateYou = (yourTotalPoints / yourTeamTotalPoints) * purpleRateTeam
    chancePurpleIsYours = purpleRateYou / purpleRateTeam
    if teamSize > 1:
        chancePurpleIsOthersUnique = (1 - chancePurpleIsYours) / (teamSize - 1)
    else:
        chancePurpleIsOthersUnique = 0

    yourDropTables = copy.deepcopy(dropTables)
    for table in yourDropTables:
        for itemName in table.keys():
            if itemName == "Lil' zik":
                continue
            table[itemName] *= purpleRateYou
    return yourDropTables

def dry(trials, teamSize = 4, mvp = False):
    specificDropTable = getSpecificDropTables(teamSize, mvp)
    return dropsim.dry(specificDropTable, trials)