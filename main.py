import csv
import json
import pandas as pd
from time import gmtime
from time import strftime
from datetime import datetime
import matplotlib.pyplot as plt


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

    # print("Getting Match => "+match['metadata']['matchId'])

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

            # Convert miliseconds timestamp to seconds
            match_duration = match['info']['gameDuration']
            match_duration = strftime("%H:%M:%S", gmtime(match_duration))

            # Convert miliseconds timestamp to date
            # match_creation = int(match['info']['gameCreation']/1000)
            # match_creation = datetime.utcfromtimestamp(
            #     match_creation).strftime('%d-%m-%Y')
            match_creation = match['info']['gameCreation']

            all_in_pings = player_data['allInPings']
            bait_pings = player_data['baitPings']
            basic_pings = player_data['basicPings']
            command_pings = player_data['commandPings']
            danger_pings = player_data['dangerPings']
            enemy_missing_pings = player_data['enemyMissingPings']
            enemy_vision_pings = player_data['enemyVisionPings']
            get_back_pings = player_data['getBackPings']
            hold_pings = player_data['holdPings']
            need_vision_pings = player_data['needVisionPings']
            on_my_way_pings = player_data['onMyWayPings']
            push_pings = player_data['pushPings']
            total_pings = all_in_pings + bait_pings + basic_pings + command_pings + danger_pings + enemy_missing_pings + enemy_vision_pings + get_back_pings + hold_pings + need_vision_pings + on_my_way_pings + push_pings

            pings_overview['gameCreation'] = match_creation
            pings_overview['gameDuration'] = match_duration
            pings_overview['championName'] = player_data['championName']
            pings_overview['win'] = player_data['win']
            pings_overview['totalPings'] = total_pings
            pings_overview['allInPings'] = all_in_pings
            pings_overview['baitPings'] = bait_pings
            pings_overview['basicPings'] = basic_pings
            pings_overview['commandPings'] = command_pings
            pings_overview['dangerPings'] = danger_pings
            pings_overview['enemyMissingPings'] = enemy_missing_pings
            pings_overview['enemyVisionPings'] = enemy_vision_pings
            pings_overview['getBackPings'] = get_back_pings
            pings_overview['holdPings'] = hold_pings
            pings_overview['needVisionPings'] = need_vision_pings
            pings_overview['onMyWayPings'] = on_my_way_pings
            pings_overview['pushPings'] = push_pings

            geral_pings_overview.append(pings_overview)

    analysis_ping_overview(geral_pings_overview)

    geral_pings_overview = format_json(geral_pings_overview)

    with open(save_file, "w") as outfile:

        outfile.write(geral_pings_overview)

    return

def analysis_ping_overview(geral_pings_overview):
    
    df = pd.DataFrame(geral_pings_overview)
    df['gameCreation'] = pd.to_datetime(df['gameCreation'], unit='ms')
    df['gameCreation'] = df['gameCreation'].dt.strftime('%d/%m/%Y')
    df.sort_values(by=['gameCreation'],ascending=True)

    win_df = df[df["win"]==True]
    lose_df = df[df['win'] == False] 

    print("Win")
    print(win_df['totalPings'].mean())
    print(win_df['totalPings'].median())
    print(win_df['totalPings'].count())
    print(win_df['totalPings'].sum())
    print(win_df['totalPings'].std())
    print(win_df['totalPings'].var())
    print("Lose")
    print(lose_df['totalPings'].mean())
    print(lose_df['totalPings'].median())
    print(lose_df['totalPings'].count())
    print(lose_df['totalPings'].sum())
    print(lose_df['totalPings'].std())
    print(lose_df['totalPings'].var())
    print("Geral")
    print(df['totalPings'].mean())
    print(df['totalPings'].median())
    print(df['totalPings'].count())
    print(df['totalPings'].sum())
    print(df['totalPings'].min())
    print(df['totalPings'].max())
    print(df['totalPings'].std())
    print(df['totalPings'].var())

    print(df['gameCreation'].min())
    print(df['gameCreation'].max())

    fig, axs = plt.subplots(figsize=(8, 4))
    
    tics = [df['gameCreation'].min(), df['gameCreation'].max()]
    
    
    df.plot(kind = 'scatter', x = 'gameCreation',y='totalPings',ax=axs)
   
    axs.set_ylim([0, df['totalPings'].max()+df['totalPings'].max()/10])
    axs.set_xticks(tics,tics)

    fig.savefig("plot.png")
    
    # plt.show()

    return 

# https://developer.riotgames.com/apis#match-v5/GET_getMatch
match_settings = {}
match_settings['game_type'] = ["CUSTOM_GAME", "MATCHED_GAME"]
match_settings['game_mode'] = ["CLASSIC"]


# Load players puuid alias
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
