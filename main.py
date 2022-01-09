from riotwatcher import LolWatcher, ApiError
import pprint
import pandas as pd

# golbal variables
api_key = 'RGAPI-dbb63dfb-0687-4f27-977f-ef546fcbd200'
lol_watcher = LolWatcher(api_key)
my_region = 'euw1'
participants = []
player = []

# PLAYERS
me = lol_watcher.summoner.by_name(my_region, 'Simbï')
my_ranked_stats = lol_watcher.league.by_summoner(my_region, me['id'])

# GRAB LAST 10 MATCHES
my_matches = lol_watcher.match.matchlist_by_puuid(
    region="EUROPE", puuid=me["puuid"])

for x in my_matches:
    match_detail = lol_watcher.match.by_id(region="EUROPE", match_id=x)
    # USE THE INFO TAB OF THE JSON
    data = match_detail["info"]
    for row in data["participants"]:
        participants_row = {}
        if row['puuid'] == me["puuid"]:
            player_row = {}
            player_row['champion'] = row['championName']
            player_row['assists'] = row['assists']
            player_row['deaths'] = row['deaths']
            player_row['kills'] = row['kills']
            player_row['win'] = row['win']
            player.append(player_row)
        participants_row['champion'] = row['championName']
        participants_row['assists'] = row['assists']
        participants_row['deaths'] = row['deaths']
        participants_row['kills'] = row['kills']
        participants_row['win'] = row['win']
        participants.append(participants_row)

pprint.pprint(match_detail)
