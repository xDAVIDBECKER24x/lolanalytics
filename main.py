import csv
import json
import pandas as pd
from time import gmtime
from time import strftime
from datetime import datetime


def format_json(json_data):

    json_formatted = json.dumps(json_data, indent=4)

    return json_formatted


def check_game_mode(match, mode):

    if (match['info']['gameMode'] in mode):
        return True

    return False


def check_game_type(match, type):

    if (match['info']['gameType'] in type):
        return True

    return False


def check_match_settings(match, match_settings):

    if ((check_game_type(match, match_settings['game_type']) & check_game_mode(match, match_settings['game_mode'])) == True):

        return True

    return False


def get_player_match_info_by_player_puuid(match, puuid):

    print("Getting Match => "+match['metadata']['matchId'])

    participants_info = match['metadata']['participants']
    player_idx = participants_info.index(puuid)

    player_match_info = match['info']['participants'][player_idx]

    return player_match_info


def save_match_overview(match_list, puuid, save_file):

    with open(save_file, "w") as outfile:

        for match in match_list:

            match_overview = {}

            player_data = get_player_match_info_by_player_puuid(match, puuid)

            match_duration = match['info']['gameDuration']
            match_duration = strftime("%H:%M:%S", gmtime(match_duration))

            match_overview['gameDuration'] = match_duration
            match_overview['championName'] = player_data['championName']
            match_overview['kills'] = player_data['kills']
            match_overview['deaths'] = player_data['deaths']
            match_overview['totalDamageDealtToChampions'] = player_data['totalDamageDealtToChampions']
            match_overview['goldEarned'] = player_data['goldEarned']

            match_overview = format_json(match_overview)

            outfile.write(match_overview)

    return


def save_pings_overview(match_list, match_settings, puuid, save_file):

    geral_pings_overview = []

    for match in match_list:

        if (check_match_settings(match, match_settings) == True):

            pings_overview = {}

            player_data = get_player_match_info_by_player_puuid(match, puuid)

            match_duration = match['info']['gameDuration']
            match_duration = strftime("%H:%M:%S", gmtime(match_duration))

            # Convert miliseconds timestamp to seconds
            match_creation = int(match['info']['gameCreation']/1000)
            match_creation = datetime.utcfromtimestamp(
                match_creation).strftime('%d-%m-%Y')

            print(match_creation)
            pings_overview['gameCreation'] = match_creation
            pings_overview['gameDuration'] = match_duration
            pings_overview['championName'] = player_data['championName']
            pings_overview['win'] = player_data['win']
            pings_overview['allInPings'] = player_data['allInPings']
            pings_overview['baitPings'] = player_data['baitPings']
            pings_overview['basicPings'] = player_data['basicPings']
            pings_overview['commandPings'] = player_data['commandPings']
            pings_overview['dangerPings'] = player_data['dangerPings']
            pings_overview['enemyMissingPings'] = player_data['enemyMissingPings']
            pings_overview['enemyVisionPings'] = player_data['enemyVisionPings']
            pings_overview['getBackPings'] = player_data['getBackPings']
            pings_overview['holdPings'] = player_data['holdPings']
            pings_overview['needVisionPings'] = player_data['needVisionPings']
            pings_overview['onMyWayPings'] = player_data['onMyWayPings']
            pings_overview['pushPings'] = player_data['pushPings']

            geral_pings_overview.append(pings_overview)

    with open(save_file, "w") as outfile:

        geral_pings_overview = format_json(geral_pings_overview)
        outfile.write(geral_pings_overview)

    return


def save_date_matchs(match_list, save_file):

    with open(save_file, "w") as outfile:

        for match in match_list:

            date_overview = {}

            date_overview['gameCreation'] = match['info']['gameCreation']

            date_overview = format_json(date_overview)

            outfile.write(date_overview)

    return


def save_json_to_csv(data, file):

    headers = data[0].keys()

    with open(file, 'w') as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        writer.writerows(data)

    return


# https://developer.riotgames.com/apis#match-v5/GET_getMatch
match_settings = {}
match_settings['game_type'] = ["CUSTOM_GAME", "MATCHED_GAME"]
match_settings['game_mode'] = ["CLASSIC"]

file_puuids_alias = open("players_puuids_alias.json", "r")
puuids_alias = json.loads(file_puuids_alias.read())
file_puuids_alias.close()

player_type = 'raky'
player_alias = 'akaashi'
puuid = puuids_alias[player_type][player_alias]
print("puuid => "+puuid)

path = f"data/{player_type }/{player_alias}/"

raw_data_matchs_file = f"{path}matchs_metadata_{player_alias}.json"

# Load raw data from exported matches json
raw_data_matchs_file = open(raw_data_matchs_file)
raw_matches_data = json.load(raw_data_matchs_file)
raw_data_matchs_file.close()

save_file = path + f"ping_overview_{player_alias}.json"

save_pings_overview(raw_matches_data, match_settings,
                    puuid, save_file)
