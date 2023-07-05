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


def save_pings_overview(match_list, match_settings, puuid, save_path, player_alias):

    geral_pings_overview = []

    for match in match_list:

        if (check_match_settings(match, match_settings) == True):

            pings_overview = {}

            player_data = get_player_match_info_by_player_puuid(match, puuid)

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

    analysis_ping_overview(geral_pings_overview, save_path)

    geral_pings_overview = format_json(geral_pings_overview)

    save_file = save_path + f"ping_overview_{player_alias}.json"
    with open(save_file, "w") as outfile:

        outfile.write(geral_pings_overview)

    return


def analysis_ping_overview(geral_pings_overview, save_path):

    df = pd.DataFrame(geral_pings_overview)
    df['gameCreation'] = pd.to_datetime(df['gameCreation'], unit='ms')
    df['gameCreation'] = df['gameCreation'].dt.strftime('%Y-%m-%d')

    df.sort_values(by=['gameCreation'], inplace=True)

    # win_df = df[df["win"] == True]
    # lose_df = df[df['win'] == False]

    # win_total_pings_mean = win_df['totalPings'].mean()
    # win_total_pings_median = win_df['totalPings'].median()
    # win_total_pings_count = win_df['totalPings'].count()
    # win_total_pings_sum = win_df['totalPings'].sum()
    # win_total_pings_std = win_df['totalPings'].std()
    # win_total_pings_var = win_df['totalPings'].var()

    # lose_total_pings_mean = lose_df['totalPings'].mean()
    # lose_total_pings_median = lose_df['totalPings'].median()
    # lose_total_pings_count = lose_df['totalPings'].count()
    # lose_total_pings_sum = lose_df['totalPings'].sum()
    # lose_total_pings_std = lose_df['totalPings'].std()
    # lose_total_pings_var = lose_df['totalPings'].var()

    # total_pings_mean = df['totalPings'].mean()
    # total_pings_median = df['totalPings'].median()
    # total_pings_count = df['totalPings'].count()
    # total_pings_sum = df['totalPings'].sum()
    # total_pings_min = df['totalPings'].min()
    # total_pings_max = df['totalPings'].max()
    # total_pings_std = df['totalPings'].std()
    # total_pings_var = df['totalPings'].var()

    # date_start= df['gameCreation'].min()
    # date_end = df['gameCreation'].max()

    # start_date = df['gameCreation'].min()
    # end_date = df['gameCreation'].max()

    df_ratio_dates = df[['gameCreation', 'ratioPings']].copy()
    df_ratio_dates= df_ratio_dates.groupby('gameCreation', as_index=False)['ratioPings'].mean()
  
    print(df_ratio_dates)
    # create data
    date_np = np.array(list(df_ratio_dates['gameCreation']))
    value_np = np.array(list(df_ratio_dates['ratioPings']))
    date_num = dates.date2num(date_np)
    # smooth
    date_num_smooth = np.linspace(date_num.min(), date_num.max(), 100) 
    spl = make_interp_spline(date_num, value_np, k=3)
    value_np_smooth = spl(date_num_smooth)
    # print
    plt.plot(date_np, value_np)
    plt.plot(dates.num2date(date_num_smooth), value_np_smooth)
    plt.show()


    max_date = df['gameCreation'].max()
    min_date = df['gameCreation'].min()
    
    max_pings = df['totalPings'].max()
    max_ratio = df['ratioPings'].max()

    # Ping Total Overview Scatter Chart
    fig_total_pings, axs_total_pings = plt.subplots(figsize=(8, 4))
    df.plot(kind='scatter', x='gameCreation', y='totalPings', ax=axs_total_pings)
    
    axs_total_pings.set_ylim([0, max_pings+(max_pings/10)])
    axs_total_pings.set_xticks(df['gameCreation'])
    axs_total_pings.xaxis.set_major_locator(mdates.MonthLocator(interval=1))
    axs_total_pings.set_xlabel("")
    axs_total_pings.set_ylabel("Quantidade de Pings")
    axs_total_pings.set_title(f"Dispersão Pings {player_alias.capitalize()}")

    file_total_pings = save_path + f"ping_overview_total_{player_alias}_scatter"
    fig_total_pings.savefig(file_total_pings)

    # Ping Per Minute Overview Line Chart

    fig_ratio_pings, axs_ratio_pings = plt.subplots(figsize=(8, 4))
    df.plot(kind='line', x='gameCreation', y='ratioPings', ax=axs_ratio_pings)
     
    # axs_ratio_pings.set_ylim([0, max_ratio+(max_ratio/10)])
    # axs_ratio_pings.set_xticks(df['gameCreation'])
    # axs_ratio_pings.xaxis.set_major_locator(mdates.MonthLocator(interval=1))
    # axs_ratio_pings.set_xlabel("")
    axs_ratio_pings.set_ylabel("Pings/Minuto")
    axs_ratio_pings.set_title(f"Frequência Pings {player_alias.capitalize()}")

    file_ratio_pings = save_path + f"ping_overview_ratio_{player_alias}_line"
    fig_ratio_pings.savefig(file_ratio_pings)


    return


# Set matchs settings search
match_settings = {}
match_settings['game_type'] = ["CUSTOM_GAME", "MATCHED_GAME"]
match_settings['game_mode'] = ["CLASSIC"]


# Load players puuid alias
file_puuids_alias = open("players_puuids_alias.json", "r")
puuids_alias = json.loads(file_puuids_alias.read())
file_puuids_alias.close()

# Select player type and alias
player_type = 'raky'
player_alias = 'akaashi'
puuid = puuids_alias[player_type][player_alias]
print("puuid => "+puuid)

# Set path to save player analysis
save_path = f"data/{player_type }/{player_alias}/"

# Load raw data from exported matches json
raw_data_matchs_file = f"{save_path}matchs_metadata_{player_alias}.json"
raw_data_matchs_file = open(raw_data_matchs_file)
raw_matches_data = json.load(raw_data_matchs_file)
raw_data_matchs_file.close()

# Do little things
save_pings_overview(raw_matches_data, match_settings,
                    puuid, save_path, player_alias)
