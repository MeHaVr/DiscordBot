from cogs.mods.fuzzy_blacklist import FuzzyBlacklist


blacklist = FuzzyBlacklist("blacklist.txt","whitelist.txt", max_score=80)

messages = [
    "Hallo Erich",
    "Er sie es",
    "123455"
]

for message in messages:
    score = blacklist.match(message)
    print(f"{message}: {score}")

