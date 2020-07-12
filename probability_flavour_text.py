def get_flavour(probability):
    if probability == 0:
        description = "Congratulations. You did it. You made python round down to 0. I hope you're happy knowing you'll never go this dry. It's not possible. You'll die first. Everyone will. Even the heat death of the universe is a blip on the radar compared to this dry streak."
    elif probability < 10**-80:
        description = "What are you doing. Stop this. I don't know why python even supports numbers this small, but it does, so this description exists."
    elif probability < 10**-79:
        description = "Let's play roulette, except instead of 36 numbers, we'll use atoms in the universe. Are you feeling lucky? Becuase you're more likely to win single atom universe-roulette than go this dry."
    elif probability < 10**-21:
        description = "If we bottled every drop of water in the world into 1L bottles and added a winning gold ticket to one, you'd be more likely to pick the right bottle than go this dry."
    elif probability < 10**-17:
        description = "Why don't you pick two random seconds out of the history of lets say... The entire time the universe has existed? You're less more to pick two consecutive seconds than go this dry..."
    elif probability < 10**-13:
        description = "Do you have a least favourite cell in your body? That'd be one unlucky cell... More unlucky than you going on this dry ."
    elif probability < 10**-11:
        description = "I'm thinking of a random star in the Milky Way. Think you can guess it? Good luck, you've got better odds than going this dry."
    elif probability < 10**-8:
        description = "Did you play the lottery today? If your luck balances out... You're a winner."
    elif probability < 0.5 ** 20:
        description = "You're more likely to win 20 stakes... In a row..."
    elif probability < 1/700000:
        description = "Zzzt! Unlucky, more unlucky than getting struck by lightning, actually!"
    elif probability < 1/20000:
        description = "From the USA? You've got a higher chance of getting murdered this year than going this dry...?"
    elif probability < 1/13616:
        description = "Rarer than... third age..."
    elif probability < 1/128 ** 2:
        description = "Ssss!! More likely to get double uniques from Zulrah than go this dry."
    elif probability < 1/5000:
        description = "Rex brooo!!, More likely to get 1 KC pet rex than hit this streak!"
    elif probability < 1/127:
        description =  "SCREEEEEEE!!!!!! More likely for Kree'arra to drop you some godly armour than be this dry."
    elif probability < 1/73:
        description =  "You're more likely to AGS b0aty a 73 :joy: than go this dry"
    elif probability < 0.083:
        description =  "Getting a specific +5 from a spicy stew isn't as rare as being this dry..."
    elif probability < 1/6:
        description = "Guessing a dice roll correctly happens more often than this."
    elif probability < 1/2:
        description = "Going this dry is worse than trying to guess a coin flip... Getting there..."
    elif probability > 0.5:
        description = "You still not unlucky, Jalyt!"
    return description
