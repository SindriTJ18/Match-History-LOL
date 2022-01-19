from riotwatcher import LolWatcher, ApiError
import pprint
import PySimpleGUI as sg


# golbal variables
api_key = "RGAPI-6730c41d-271e-43b4-8906-c1dfe70b6452"
lol_watcher = LolWatcher(api_key)
my_region = "euw1"


# PLAYERS TO TRACK
player_names = ["Simbï", "TheSayHesTheBest", "SteveoBadBoy"]
players = dict()
last_matches = dict()
for i in range(len(player_names)):
    players[player_names[i]] = lol_watcher.summoner.by_name(
        my_region, player_names[i])
    last_matches[player_names[i]] = lol_watcher.match.matchlist_by_puuid(
        region="EUROPE", puuid=players[player_names[i]]["puuid"])


# GRAB LAST 10 MATCHES


def main():
    history = grab_matchdata(
        last_matches, players)

    sg.theme("DarkAmber")
    layout = [
        [sg.Text("Match history searcher")],
        [
            sg.Text("Enter summoner name"),
            sg.InputText(),
        ],
        [sg.Button("Ok"), sg.Button("Cancel")],
    ]
    this = {player_names[0]: [[name_disp(player_names[0])]], player_names[1]: [
        [name_disp(player_names[1])]], player_names[2]: [[name_disp(player_names[0])]]}
    for i in player_names:
        for j in history[i]:
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
            this[i].append(thing)
    # Create the Window

    layin = [
        [sg.Column(layout)],
        [sg.Column(this[player_names[0]]), sg.VSeparator(), sg.Column(
            this[player_names[1]]), sg.VSeparator(), sg.Column(this[player_names[2]])]
    ]
    window = sg.Window("FRYSTATIONS MATCH INSPECTOR",
                       layin, size=(1600, 960))
    while True:
        event, values = window.read()
        if (
            event == sg.WIN_CLOSED or event == "Cancel"
        ):  # if user closes window or clicks cancel
            break
        print("You entered summoner:", values[0])
    window.close()


def grab_matchdata(my_matches, me):
    history = dict()
    for i in player_names:
        player = []
        participants = []
        for x in my_matches[i]:
            match_detail = lol_watcher.match.by_id(region="EUROPE", match_id=x)
            # USE THE INFO TAB OF THE JSON
            data = match_detail["info"]
            for row in data["participants"]:
                participants_row = {}
                if row["puuid"] == me[i]["puuid"]:
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
        history[i] = player
    return history


def name_disp(summ_name):
    name = sg.Text(summ_name)
    return name


main()
