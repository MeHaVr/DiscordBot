from cogs.mods.fuzzy_blacklist import FuzzyBlacklist


blacklist = FuzzyBlacklist("blacklist.txt","whitelist.txt", max_score=80)

messages = [
    "Hallo Erich",
    "Er sie es",
    "123455",
    "4055416489552590",
    "er"
]

for message in messages:
    score = blacklist.match(message)
    print(f"{message}: {score}")

