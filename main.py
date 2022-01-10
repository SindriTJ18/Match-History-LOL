from riotwatcher import LolWatcher, ApiError
import pprint
import PySimpleGUI as sg

# golbal variables
api_key = "RGAPI-dbb63dfb-0687-4f27-977f-ef546fcbd200"
lol_watcher = LolWatcher(api_key)
my_region = "euw1"
participants = []
player = []

# PLAYERS
# me = lol_watcher.summoner.by_name(my_region, "TheSayHesTheBest")
me = lol_watcher.summoner.by_name(my_region, "Simbï")
my_ranked_stats = lol_watcher.league.by_summoner(my_region, me["id"])

# GRAB LAST 10 MATCHES
my_matches = lol_watcher.match.matchlist_by_puuid(region="EUROPE", puuid=me["puuid"])

for x in my_matches:
    match_detail = lol_watcher.match.by_id(region="EUROPE", match_id=x)
    # USE THE INFO TAB OF THE JSON
    data = match_detail["info"]
    for row in data["participants"]:
        participants_row = {}
        if row["puuid"] == me["puuid"]:
            player_row = {}
            player_row["champion"] = row["championName"]
            player_row["assists"] = row["assists"]
            player_row["deaths"] = row["deaths"]
            player_row["kills"] = row["kills"]
            player_row["win"] = row["win"]
            player.append(player_row)
        participants_row["champion"] = row["championName"]
        participants_row["assists"] = row["assists"]
        participants_row["deaths"] = row["deaths"]
        participants_row["kills"] = row["kills"]
        participants_row["win"] = row["win"]
        participants.append(participants_row)


sg.theme("DarkAmber")  # Add a touch of color
# All the stuff inside your window.
layout = [
    [sg.Text("Match history searcher")],
    [
        sg.Text("Enter summoner name"),
        sg.InputText(),
    ],
    [sg.Button("Ok"), sg.Button("Cancel")],
    [sg.Text("Summoner name: "), sg.Text(me["name"])],
]

for j in player:
    if j["win"] == True:
        win = sg.Text("WIN", size=(5, 1), text_color="green")
    else:
        win = sg.Text("LOSS", size=(5, 1), text_color="red")
    thing = [
        win,
        sg.Text(j["champion"], size=(10, 1), text_color="white"),
        sg.Text(j["kills"], size=(2, 1), text_color="green"),
        sg.Text("/"),
        sg.Text(j["deaths"], size=(2, 1), text_color="red"),
        sg.Text("/"),
        sg.Text(j["assists"], size=(2, 1), text_color="blue"),
    ]
    layout.append(thing)
# Create the Window
window = sg.Window("FRYSTATIONS MATCH INSPECTOR", layout, size=(1100, 700))
while True:
    event, values = window.read()
    if (
        event == sg.WIN_CLOSED or event == "Cancel"
    ):  # if user closes window or clicks cancel
        break
    print("You entered summoner:", values[0])

window.close()
