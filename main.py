import csv
import json
import string
import pandas as pd
import numpy as np
from time import gmtime
from time import strftime
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.dates as dates
from scipy.interpolate import make_interp_spline
from numpyencoder import NumpyEncoder


def format_json(json_data):

    json_formatted = json.dumps(json_data, default=int,indent=4)

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


def save_match_overview(match_list, player_puuid, save_file):
   

    with open(save_file, "w") as outfile:

        for match in match_list:

            match_overview = {}

            player_data = get_player_match_info_by_player_puuid(match, player_puuid)

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


def save_ping_overview(match_list, match_settings, player_puuid, save_path, player_alias):

    print(f"Getting : {player_alias}  puuid => {player_puuid}")

    geral_pings_overview = []

    for match in match_list:

        if (check_match_settings(match, match_settings) == True):

            player_data = get_player_match_info_by_player_puuid(match, player_puuid)
            
            if "allInPings" in player_data:

                pings_overview = {}

                # Convert miliseconds timestamp to seconds
                match_duration_seconds = match['info']['gameDuration']
                match_duration = strftime(
                    "%H:%M:%S", gmtime(match_duration_seconds))

                # Convert miliseconds timestamp to date
                # match_creation = int(match['info']['gameCreation']/1000)
                # match_creation = datetime.utcfromtimestamp(
                #     match_creation).strftime('%d-%m-%Y')
    
                match_creation = match['info']['gameCreation']
                all_in_pings = player_data['allInPings']
                bait_pings = player_data['baitPings']
                command_pings = player_data['commandPings']
                danger_pings = player_data['dangerPings']  
                enemy_missing_pings = player_data['enemyMissingPings']
                enemy_vision_pings = player_data['enemyVisionPings']
                get_back_pings = player_data['getBackPings'] 
                hold_pings = player_data['getBackPings'] 
                need_vision_pings = player_data['needVisionPings']
                
                basic_pings = player_data['basicPings']
                on_my_way_pings = player_data['onMyWayPings']
                push_pings = player_data['pushPings']
                total_pings = all_in_pings + bait_pings + basic_pings + command_pings + danger_pings + enemy_missing_pings + \
                    enemy_vision_pings + get_back_pings + hold_pings + \
                    need_vision_pings + on_my_way_pings + push_pings
                ratio_pings = (total_pings/match_duration_seconds)*60

                pings_overview['gameCreation'] = match_creation
                pings_overview['gameDuration'] = match_duration
                pings_overview['championName'] = player_data['championName']
                pings_overview['win'] = player_data['win']
                pings_overview['totalPings'] = total_pings
                pings_overview['ratioPings'] = ratio_pings
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

    pings_overview_analysis = analysis_ping_overview(geral_pings_overview, save_path,player_alias)
    
    geral_pings_overview = format_json(geral_pings_overview)

    save_file = f"{save_path}ping_overview_{player_alias}.json"
    with open(save_file, "w") as outfile:

        outfile.write(geral_pings_overview)

    return pings_overview_analysis


def analysis_ping_overview(geral_pings_overview, save_path,player_alias):

    analysis_pings = {}

    df = pd.DataFrame(geral_pings_overview)
    df['gameCreation'] = pd.to_datetime(df['gameCreation'], unit='ms')
    df['gameCreation'] = df['gameCreation'].dt.strftime('%Y-%m-%d')

    df.sort_values(by=['gameCreation'], inplace=True)

    win_df = df[df["win"] == True]
    lose_df = df[df['win'] == False]

    start_date = df['gameCreation'].min()
    end_date = df['gameCreation'].max()

    analysis_pings['player_alias'] = player_alias
    analysis_pings['start_date'] = start_date
    analysis_pings['end_date'] = end_date
    analysis_pings['pings_count'] = df['totalPings'].count()
    analysis_pings['pings_mean'] = df['totalPings'].mean()
    analysis_pings['pings_ratio'] = df['ratioPings'].mean()
    analysis_pings['pings_median'] = df['totalPings'].median()
    analysis_pings['pings_sum'] = df['totalPings'].sum()
    analysis_pings['pings_std'] = df['totalPings'].std()
    analysis_pings['win_pings_count'] = win_df['totalPings'].count()
    analysis_pings['win_pings_mean'] = win_df['totalPings'].mean()
    analysis_pings['win_pings_median'] = win_df['totalPings'].median()
    analysis_pings['win_pings_sum'] = win_df['totalPings'].sum()
    analysis_pings['win_pings_std'] = win_df['totalPings'].std()
    analysis_pings['win_pings_ratio_mean'] = win_df['ratioPings'].mean()
    analysis_pings['win_pings_ratio_std'] = win_df['ratioPings'].std()
    analysis_pings['lose_pings_count'] = lose_df['totalPings'].count()
    analysis_pings['lose_pings_mean'] = lose_df['totalPings'].mean()
    analysis_pings['lose_pings_median'] = lose_df['totalPings'].median()
    analysis_pings['lose_pings_sum'] = lose_df['totalPings'].sum()
    analysis_pings['lose_pings_std'] = lose_df['totalPings'].std()
    analysis_pings['lose_pings_ratio_mean'] = lose_df['ratioPings'].mean()
    analysis_pings['lose_pings_ratio_std'] = lose_df['ratioPings'].std()
 
    for key in analysis_pings:
        if(isinstance(analysis_pings[key], float)):
            analysis_pings[key] = round(analysis_pings[key],3)
        


    analysis_pings_formatted = json.dumps(analysis_pings, default=str,indent=4)
    save_file = f"{save_path}ping_overview_analysis_{player_alias}.json"
    with open(save_file, "w") as outfile:
        outfile.write(analysis_pings_formatted)

    # print(analysis_pings)

    df_ratio_dates_mean = df[['gameCreation', 'ratioPings']].copy()
    df_ratio_dates_mean = df_ratio_dates_mean.groupby(
        'gameCreation', as_index=False)['ratioPings'].mean()

    max_pings = df['totalPings'].max()
    max_ratio = df['ratioPings'].max()

    # Ping Total Overview Scatter Chart
    fig_total_pings, axs_total_pings = plt.subplots(figsize=(8, 4))
    df.plot(kind='scatter', x='gameCreation',
            y='totalPings', ax=axs_total_pings)

    axs_total_pings.set_ylim([0, max_pings+(max_pings/10)])
    axs_total_pings.set_xticks(df['gameCreation'])
    axs_total_pings.set_xticklabels(df['gameCreation'])
    axs_total_pings.xaxis.set_major_locator(mdates.MonthLocator(interval=1))
    axs_total_pings.set_xlabel("")
    axs_total_pings.set_ylabel("Quantidade de Pings")
    axs_total_pings.set_title(f"Dispersão Pings {player_alias.capitalize()}")

    file_total_pings = f"{save_path}ping_overview_total_{player_alias}_scatter"
    fig_total_pings.savefig(file_total_pings)

    # Ping Per Minute Overview Line Chart
    fig_ratio_pings, axs_ratio_pings = plt.subplots(figsize=(8, 4))
    df_ratio_dates_mean.plot(
        kind='line', x='gameCreation', y='ratioPings', ax=axs_ratio_pings)
    axs_ratio_pings.xaxis.set_major_locator(mdates.MonthLocator(interval=1))
    axs_ratio_pings.legend(['Frequência'])
    axs_ratio_pings.set_xlabel("")
    axs_ratio_pings.set_ylabel("Pings/Minuto")
    axs_ratio_pings.set_title(f"Frequência Pings {player_alias.capitalize()}")

    file_ratio_pings = f"{save_path}ping_overview_ratio_{player_alias}_line"
    fig_ratio_pings.savefig(file_ratio_pings)

    plt.close()

    return analysis_pings


def save_all_players_pings_overview(match_settings, player_type,players_type_alias_puuid):
   
    geral_pings_overview_analysis = []
    
    for player in  players_type_alias_puuid[player_type] :

        player_alias = player
        player_puuid = players_type_alias_puuid[player_type][player]

        save_path = f"data/{player_type}/{player_alias}/"

        raw_data_matchs_file = f"{save_path}matchs_metadata_{player_alias}.json"
        raw_data_matchs_file = open(raw_data_matchs_file)
        raw_matches_data = json.load(raw_data_matchs_file)
        raw_data_matchs_file.close()

        pings_overview_analysis = save_ping_overview(raw_matches_data, match_settings, player_puuid, save_path, player_alias)

        geral_pings_overview_analysis.append(pings_overview_analysis)

    
    geral_pings_overview_analysis =format_json(geral_pings_overview_analysis)

    save_file =  f"analysis/{player_type}_geral_ping_overview_analysis.json"
    with open(save_file, "w") as outfile:

        outfile.write(geral_pings_overview_analysis)

    return

# Set matchs settings filter search
match_settings = {}
match_settings['game_type'] = ["CUSTOM_GAME", "MATCHED_GAME"]
match_settings['game_mode'] = ["CLASSIC"]


# Load players puuid alias
file_puuids_alias = open("players_type_alias_puuid.json", "r")
players_type_alias_puuid = json.loads(file_puuids_alias.read())
file_puuids_alias.close()

# Select player type
player_type = 'proplayer'

# Select player alias
# player_alias = 'nataruk'

# Get player puuid by alias
# puuid = players_type_alias_puuid[player_type][player_alias]

# # Set path to save player analysis
# save_path = f"data/{player_type}/{player_alias}/"

# # Load raw data from exported matches json
# raw_data_matchs_file = f"{save_path}matchs_metadata_{player_alias}.json"
# raw_data_matchs_file = open(raw_data_matchs_file)
# raw_matches_data = json.load(raw_data_matchs_file)
# raw_data_matchs_file.close()

# Save all players type
save_all_players_pings_overview(match_settings,player_type,players_type_alias_puuid)

# Save only 1 player
# save_pings_overview(raw_matches_data, match_settings,puuid, save_path, player_alias)
