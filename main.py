import json
import operator 
import pandas as pd
import numpy as np
from time import gmtime
from time import strftime
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.dates as dates
from numpyencoder import NumpyEncoder
from scipy.interpolate import interp1d
from scipy.interpolate import make_interp_spline
import scipy.stats as stats
import math

def format_json(json_data):

    json_formatted = json.dumps(json_data, default=int, indent=4)

    return json_formatted


def settings_match_filter(match_list, settings, player_puuid):

    filtered_matches = []

    for match in match_list:

        check_settings = True

        for match_settings in settings['matchSettings']:
            
            if match['info'][match_settings] not in settings['matchSettings'][match_settings]: 
                
                check_settings = False
                
        if check_settings == False : continue

        player_match_data = get_player_match_info_by_player_puuid(match, player_puuid)

        for player_settings in settings['playerSettings']:

            if player_match_data[player_settings] not in settings['playerSettings'][player_settings]:

                check_settings = False

        if check_settings == True:

            filtered_matches.append(match)

    if not filtered_matches: 
        print("\tmatchs => None matchs found")
    else :
        print(f"\tmatchs filtered => {len(filtered_matches)}")


    return filtered_matches


def get_player_match_info_by_player_puuid(match, player_puuid):

    participants_info = match['metadata']['participants']
    player_idx = participants_info.index(player_puuid)

    player_match_info = match['info']['participants'][player_idx]

    return player_match_info


def save_match_overview(match_list, player_puuid, save_file):

    with open(save_file, "w") as outfile:

        for match in match_list:

            match_overview = {}

            player_data = get_player_match_info_by_player_puuid(
                match, player_puuid)

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


def save_ping_overview(match_list, settings, player_puuid, save_path, player_alias):

    print(f"Getting : {player_alias}\n\tpuuid => {player_puuid}")

    geral_pings_overview = []

    filtered_mach_list = settings_match_filter(match_list, settings, player_puuid)

    if not filtered_mach_list : return

    for match in filtered_mach_list:

        player_data = get_player_match_info_by_player_puuid(
            match, player_puuid)

        if ("allInPings" in player_data):

            pings_overview = {}

            # Convert miliseconds timestamp to seconds
            match_duration_seconds = match['info']['gameDuration']
            match_duration = strftime(
                "%H:%M:%S", gmtime(match_duration_seconds))

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
            vision_cleared_pings = player_data['visionClearedPings']
            basic_pings = player_data['basicPings']
            on_my_way_pings = player_data['onMyWayPings']
            push_pings = player_data['pushPings']
            total_pings = all_in_pings + bait_pings + basic_pings + command_pings + danger_pings + enemy_missing_pings + \
                enemy_vision_pings + get_back_pings + hold_pings + vision_cleared_pings +\
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
            pings_overview['visionClearedPings'] = vision_cleared_pings
            pings_overview['getBackPings'] = get_back_pings
            pings_overview['holdPings'] = hold_pings
            pings_overview['needVisionPings'] = need_vision_pings
            pings_overview['onMyWayPings'] = on_my_way_pings
            pings_overview['pushPings'] = push_pings

            geral_pings_overview.append(pings_overview)

    pings_overview_analysis = analysis_ping_overview(
        geral_pings_overview, save_path, player_alias)

    geral_pings_overview = format_json(geral_pings_overview)

    save_file = f"{save_path}ping_overview_{player_alias}.json"
    with open(save_file, "w") as outfile:

        outfile.write(geral_pings_overview)

    return pings_overview_analysis


def analysis_ping_overview(geral_pings_overview, save_path, player_alias):

    analysis_pings = {}
    df = pd.DataFrame(geral_pings_overview)
    df['gameCreation'] = pd.to_datetime(df['gameCreation'], unit='ms')
    df['gameCreation'] = df['gameCreation'].dt.strftime('%Y-%m-%d')

    matchs_count = len(df.index)
    pings_std = df['totalPings'].std()
    pings_mean = df['totalPings'].mean()
    pings_ratio_mean = df['ratioPings'].mean()
    pings_ratio_std = df['ratioPings'].std()
    pings_mean_constancy_indicator_1 = len(df[
        (df["totalPings"] <= (pings_mean + pings_std)) &
        (df["totalPings"] >= (pings_mean - pings_std))
    ])
    pings_mean_constancy_indicator_2 = len(df[
        (df["totalPings"] <= (pings_mean + (2*pings_std))) &
        (df["totalPings"] >= (pings_mean - (2*pings_std)))
    ])
    pings_mean_constancy_indicator_3 = len(df[
        (df["totalPings"] <= (pings_mean + (3*pings_std))) &
        (df["totalPings"] >= (pings_mean - (3*pings_std)))
    ])
    pings_ratio_constancy_indicator_1 = len(df[
        (df["ratioPings"] <= (pings_ratio_mean + pings_ratio_std)) &
        (df["ratioPings"] >= (pings_ratio_mean - pings_ratio_std))
    ])
    pings_ratio_constancy_indicator_2 = len(df[
        (df["ratioPings"] <= (pings_ratio_mean + (2*pings_ratio_std))) &
        (df["ratioPings"] >= (pings_ratio_mean - (2*pings_ratio_std)))
    ])
    pings_ratio_constancy_indicator_3 = len(df[
        (df["ratioPings"] <= (pings_ratio_mean + (3*pings_ratio_std))) &
        (df["ratioPings"] >= (pings_ratio_mean - (3*pings_ratio_std)))
    ])

    pings_mean_constancy_indicator_1 = (
        pings_mean_constancy_indicator_1/matchs_count)*100
    pings_mean_constancy_indicator_2 = (
        pings_mean_constancy_indicator_2/matchs_count)*100
    pings_mean_constancy_indicator_3 = (
        pings_mean_constancy_indicator_3/matchs_count)*100

    pings_ratio_constancy_indicator_1 = (
        pings_ratio_constancy_indicator_1/matchs_count)*100
    pings_ratio_constancy_indicator_2 = (
        pings_ratio_constancy_indicator_2/matchs_count)*100
    pings_ratio_constancy_indicator_3 = (
        pings_ratio_constancy_indicator_3/matchs_count)*100

    pings_most_frequency = df["totalPings"].mode()
    pings_most_frequency = df['totalPings'].value_counts()[:5].index.tolist()

    df_frequency = df['totalPings'].value_counts()

    # print(df_frequency.index.value_counts())
    # print(df_frequency.tolist())

    df.sort_values(by=['gameCreation'], inplace=True)

    win_df = df[df["win"] == True]
    lose_df = df[df['win'] == False]

    wins = win_df['totalPings'].count()
    winrate = (wins/matchs_count)*100

    start_date = df['gameCreation'].min()
    end_date = df['gameCreation'].max()

    analysis_pings['player_alias'] = player_alias
    analysis_pings['matchs_count'] = matchs_count
    analysis_pings['start_date'] = start_date
    analysis_pings['end_date'] = end_date
    analysis_pings['winrate'] = winrate
    analysis_pings['pings_sum'] = df['totalPings'].sum()
    analysis_pings['pings_mean'] = pings_mean
    analysis_pings['pings_ratio'] = pings_ratio_mean
    analysis_pings['pings_median'] = df['totalPings'].median()
    analysis_pings['pings_most_frequency'] = pings_most_frequency
    analysis_pings['pings_mean_constancy_indicator_1'] = pings_mean_constancy_indicator_1
    analysis_pings['pings_mean_constancy_indicator_2'] = pings_mean_constancy_indicator_2
    analysis_pings['pings_mean_constancy_indicator_3'] = pings_mean_constancy_indicator_3
    analysis_pings['pings_ratio_constancy_indicator_1'] = pings_ratio_constancy_indicator_1
    analysis_pings['pings_ratio_constancy_indicator_2'] = pings_ratio_constancy_indicator_2
    analysis_pings['pings_ratio_constancy_indicator_3'] = pings_ratio_constancy_indicator_3
    analysis_pings['pings_std'] = pings_std
    analysis_pings['pings_ratio_std'] = pings_ratio_std
    analysis_pings['wins_count'] = win_df['totalPings'].count()
    analysis_pings['win_pings_mean'] = win_df['totalPings'].mean()
    analysis_pings['win_pings_median'] = win_df['totalPings'].median()
    analysis_pings['win_pings_sum'] = win_df['totalPings'].sum()
    analysis_pings['win_pings_std'] = win_df['totalPings'].std()
    analysis_pings['win_pings_ratio_mean'] = win_df['ratioPings'].mean()
    analysis_pings['win_pings_ratio_std'] = win_df['ratioPings'].std()
    analysis_pings['lose_count'] = lose_df['totalPings'].count()
    analysis_pings['lose_pings_mean'] = lose_df['totalPings'].mean()
    analysis_pings['lose_pings_median'] = lose_df['totalPings'].median()
    analysis_pings['lose_pings_sum'] = lose_df['totalPings'].sum()
    analysis_pings['lose_pings_std'] = lose_df['totalPings'].std()
    analysis_pings['lose_pings_ratio_mean'] = lose_df['ratioPings'].mean()
    analysis_pings['lose_pings_ratio_std'] = lose_df['ratioPings'].std()

    for key in analysis_pings:
        if (isinstance(analysis_pings[key], float)):
            analysis_pings[key] = round(analysis_pings[key], 3)

    analysis_pings_formatted = json.dumps(
        analysis_pings, default=str, indent=4)
    save_file = f"{save_path}ping_overview_analysis_{player_alias}.json"
    with open(save_file, "w") as outfile:
        outfile.write(analysis_pings_formatted)

    df_ratio_dates_mean = df[['gameCreation', 'ratioPings']].copy()
    df_ratio_dates_mean = df_ratio_dates_mean.groupby(
        'gameCreation', as_index=False)['ratioPings'].mean()


    df_distribution_pings = df[['totalPings']].copy()
    df_distribution_pings = pd.DataFrame(df_distribution_pings['totalPings'].value_counts().reset_index().values, columns=["totalPings", "counts"])
    df_distribution_pings = df_distribution_pings.sort_values(by=['totalPings'], ascending=True)

    max_pings = df['totalPings'].max()
    min_pings = df['totalPings'].min()
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
    axs_total_pings.grid(True, alpha=0.3, linestyle="--")

    file_total_pings = f"{save_path}ping_overview_total_{player_alias}_scatter"
    fig_total_pings.savefig(file_total_pings)

    plt.close()

    # Ping Ratio Overview Line Chart

    fig_ratio_pings, axs_ratio_pings = plt.subplots(figsize=(8, 4))
    df_ratio_dates_mean.plot(
        kind='line', x='gameCreation', y='ratioPings', ax=axs_ratio_pings)
    axs_ratio_pings.xaxis.set_major_locator(mdates.MonthLocator(interval=1))
    axs_ratio_pings.legend(['Frequência'])
    axs_ratio_pings.set_xlabel("")
    axs_ratio_pings.set_ylabel("Pings/Minuto")
    axs_ratio_pings.set_title(f"Frequência Pings {player_alias.capitalize()}")
    axs_ratio_pings.grid(True, alpha=0.3, linestyle="--")

    file_ratio_pings = f"{save_path}ping_overview_ratio_{player_alias}_line"
    fig_ratio_pings.savefig(file_ratio_pings)

    idx = df_frequency.index.values
    frequency = df_frequency.values

    plt.close()

    # # 1º
    # # print(df_distribution_pings['totalPings'])
    # # Dataset
    # y = np.array(df_distribution_pings['counts'])
    # x = np.array(df_distribution_pings['totalPings'])
    
    # print(x)
    # print(y)

    # X_Y_Spline = make_interp_spline(x, y)
    
    
    # # Returns evenly spaced numbers
    # # over a specified interval.
    # X_ = np.linspace(x.min(), x.max(), 1000)
    # Y_ = X_Y_Spline(X_)
    
    # # Plotting the Graph
    # plt.plot(X_, Y_)
    # plt.title("Plot Smooth")
    # plt.xlabel("X")
    # plt.ylabel("Y")
    # plt.show()

    # # 2
    # # Dataset
    # y = np.array(df_distribution_pings['counts'])
    # x = np.array(df_distribution_pings['totalPings'])
    
    # cubic_interpolation_model = interp1d(x, y, kind = "quadratic")
    
    # # Plotting the Graph
    # X_=np.linspace(x.min(), x.max(), 500)
    # Y_=cubic_interpolation_model(X_)
  
    # plt.plot(X_, Y_)
    # plt.title("Plot Smooth")
    # plt.xlabel("X")
    # plt.ylabel("Y")
    # plt.show()


    # # 3
    
    # mu = 0
    # variance = 1
    # sigma = math.sqrt(variance)
    # x = np.linspace(mu - 3*sigma, mu + 3*sigma, 100)
    # plt.plot(x, stats.norm.pdf(x, mu, sigma))
    # plt.show()

    # 4
    # Calculating mean and Stdev of AGW

   
    # Ping Match Distribution Range Chart 
    axs_probability_density_pings = plt.subplots(figsize=(8, 4))
    # Calculating probability density function (PDF)
    axs_probability_density_pings = stats.norm.pdf(df["totalPings"].sort_values(), pings_mean, pings_std)
    
    plt.plot(df["totalPings"].sort_values(), axs_probability_density_pings)
    plt.xlim([0,df["totalPings"].max()])  
    plt.xlabel("Quantidade", size=12)    
    plt.ylabel("Frequência", size=12)        
    plt.title(f"Probabilidade Densidade {player_alias.capitalize()}")        
    plt.grid(True, alpha=0.3, linestyle="--")
    plt.savefig(f"{save_path}ping_probability_density_{player_alias}_line")
    
    plt.close()

    # Ping Match Distribution Overview Line Chart
    fig_distribution_pings, axs_distribution_pings = plt.subplots(figsize=(8, 4))
    df_distribution_pings.plot(
        kind='bar', x='totalPings', y='counts', ax=axs_distribution_pings)
    axs_distribution_pings.legend(['Distribuição'])
    axs_distribution_pings.set_xlabel("Quantidade")
    axs_distribution_pings.set_ylabel("Ocorrências")
    axs_distribution_pings.set_title(f"Distribuição Pings {player_alias.capitalize()}")
    axs_distribution_pings.grid(True, alpha=0.3, linestyle="--")

    file_distribution_pings = f"{save_path}ping_overview_distribution_{player_alias}_bar"
    fig_distribution_pings.savefig(file_distribution_pings)

    plt.close()


    return analysis_pings


def save_vision_overview(match_list, settings, player_puuid, save_path, player_alias):

    print(f"Getting : {player_alias}\n\tpuuid => {player_puuid}")

    geral_vision_overview = []
    
    filtered_mach_list = settings_match_filter(match_list, settings, player_puuid)

    if not filtered_mach_list : return

    for match in filtered_mach_list:

        player_data = get_player_match_info_by_player_puuid(
            match, player_puuid)

        if ("challenges" in player_data) & ("enemyVisionPings" in player_data):

            vision_overview = {}

            # Convert miliseconds timestamp to seconds
            match_duration_seconds = match['info']['gameDuration']
            match_duration = strftime(
                "%H:%M:%S", gmtime(match_duration_seconds))

            match_creation = match['info']['gameCreation']
            vision_score = player_data['visionScore']
            vision_score_per_minute = player_data['challenges']['visionScorePerMinute']
            # ratio_vision_pings = (total_vision_pings/match_duration_seconds)*60
            complete_support_quest_in_time = player_data['challenges']['completeSupportQuestInTime']
            control_wards_placed = player_data['challenges']['controlWardsPlaced']
            stealth_wards_placed = player_data['challenges']['stealthWardsPlaced']
            detector_wards_placed = player_data['detectorWardsPlaced']
            vision_wards_bought_in_game = player_data['visionWardsBoughtInGame']

            ward_takedowns = player_data['challenges']['wardTakedowns']
            ward_takedowns_before_20M = player_data['challenges']['wardTakedownsBefore20M']

            # vision_score_advantage_lane_opponent = player_data['challenges']['visionScoreAdvantageLaneOpponent']
            # control_ward_time_coverage_in_river_or_enemy_half = player_data['challenges']['controlWardTimeCoverageInRiverOrEnemyHalf']

            wards_killed = player_data['wardsKilled']
            wards_placed = player_data['wardsPlaced']

            enemy_vision_pings = player_data['enemyVisionPings']
            need_vision_pings = player_data['needVisionPings']
            vision_cleared_pings = player_data['visionClearedPings']
            total_vision_pings = enemy_vision_pings + \
                need_vision_pings + vision_cleared_pings

            vision_overview['gameCreation'] = match_creation
            vision_overview['gameDuration'] = match_duration
            vision_overview['win'] = player_data['win']
            vision_overview['championName'] = player_data['championName']
            vision_overview['visionScore'] = vision_score
            vision_overview['visionScorePerMinute'] = vision_score_per_minute
            # vision_overview['ratioVisionPings'] = ratio_vision_pings
            vision_overview['completeSupportQuestInTime'] = complete_support_quest_in_time
            vision_overview['controlWardsPlaced'] = control_wards_placed
            vision_overview['stealthWardsPlaced'] = stealth_wards_placed
            vision_overview['detectorWardsPlaced'] = detector_wards_placed
            vision_overview['visionWardsBoughtInGame'] = vision_wards_bought_in_game
            vision_overview['wardsKilled'] = wards_killed
            vision_overview['wardsPlaced'] = wards_placed
            vision_overview['wardTakedowns'] = ward_takedowns
            vision_overview['wardTakedownsBefore20M'] = ward_takedowns_before_20M
            # vision_overview['visionScoreAdvantageLaneOpponent'] = vision_score_advantage_lane_opponent
            # vision_overview['controlWardTimeCoverageInRiverOrEnemyHalf'] = control_ward_time_coverage_in_river_or_enemy_half
            vision_overview['totalVisionPings'] = total_vision_pings
            vision_overview['enemyVisionPings'] = enemy_vision_pings
            vision_overview['needVisionPings'] = need_vision_pings
            vision_overview['visionClearedPings'] = vision_cleared_pings

            geral_vision_overview.append(vision_overview)

    
    vision_overview_analysis = analysis_vision_overview(geral_vision_overview, save_path,player_alias)
   
    geral_vision_overview = format_json(geral_vision_overview)

    save_file = f"{save_path}vision_overview_{player_alias}.json"
    with open(save_file, "w") as outfile:

        outfile.write(geral_vision_overview)

    return vision_overview_analysis


def analysis_vision_overview(geral_vision_overview, save_path, player_alias):

    analysis_vision = {}

    df = pd.DataFrame(geral_vision_overview)
    df['gameCreation'] = pd.to_datetime(df['gameCreation'], unit='ms')
    df['gameCreation'] = df['gameCreation'].dt.strftime('%Y-%m-%d')

    matchs_count = len(df.index)
    vision_std = df['visionScore'].std()
    vision_mean = df['visionScore'].mean()
    vision_ratio_mean = df['visionScorePerMinute'].mean()
    vision_ratio_std = df['visionScorePerMinute'].std()
    vision_mean_constancy_indicator_1 = len(df[
        (df["visionScore"] <= (vision_mean + vision_std)) &
        (df["visionScore"] >= (vision_mean - vision_std))
    ])
    vision_mean_constancy_indicator_2 = len(df[
        (df["visionScore"] <= (vision_mean + (2*vision_std))) &
        (df["visionScore"] >= (vision_mean - (2*vision_std)))
    ])
    vision_mean_constancy_indicator_3 = len(df[
        (df["visionScore"] <= (vision_mean + (3*vision_std))) &
        (df["visionScore"] >= (vision_mean - (3*vision_std)))
    ])
    vision_ratio_constancy_indicator_1 = len(df[
        (df["visionScorePerMinute"] <= (vision_ratio_mean + vision_ratio_std)) &
        (df["visionScorePerMinute"] >= (vision_ratio_mean - vision_ratio_std))
    ])
    vision_ratio_constancy_indicator_2 = len(df[
        (df["visionScorePerMinute"] <= (vision_ratio_mean + (2*vision_ratio_std))) &
        (df["visionScorePerMinute"] >= (vision_ratio_mean - (2*vision_ratio_std)))
    ])
    vision_ratio_constancy_indicator_3 = len(df[
        (df["visionScorePerMinute"] <= (vision_ratio_mean + (3*vision_ratio_std))) &
        (df["visionScorePerMinute"] >= (vision_ratio_mean - (3*vision_ratio_std)))
    ])

    vision_mean_constancy_indicator_1 = (
        vision_mean_constancy_indicator_1/matchs_count)*100
    vision_mean_constancy_indicator_2 = (
        vision_mean_constancy_indicator_2/matchs_count)*100
    vision_mean_constancy_indicator_3 = (
        vision_mean_constancy_indicator_3/matchs_count)*100

    vision_ratio_constancy_indicator_1 = (
        vision_ratio_constancy_indicator_1/matchs_count)*100
    vision_ratio_constancy_indicator_2 = (
        vision_ratio_constancy_indicator_2/matchs_count)*100
    vision_ratio_constancy_indicator_3 = (
        vision_ratio_constancy_indicator_3/matchs_count)*100

    vision_most_frequency = df["visionScore"].mode()
    vision_most_frequency = df['visionScore'].value_counts()[:5].index.tolist()

    df_frequency = df['visionScore'].value_counts()

    df.sort_values(by=['gameCreation'], inplace=True)

    win_df = df[df["win"] == True]
    lose_df = df[df['win'] == False]

    wins = win_df['visionScore'].count()
    winrate = (wins/matchs_count)*100

    start_date = df['gameCreation'].min()
    end_date = df['gameCreation'].max()

    analysis_vision['player_alias'] = player_alias
    analysis_vision['matchs_count'] = matchs_count
    analysis_vision['start_date'] = start_date
    analysis_vision['end_date'] = end_date
    analysis_vision['winrate'] = winrate
    analysis_vision['vision_sum'] = df['visionScore'].sum()
    analysis_vision['vision_mean'] = vision_mean
    analysis_vision['vision_ratio'] = vision_ratio_mean
    analysis_vision['vision_median'] = df['visionScore'].median()
    analysis_vision['vision_most_frequency'] = vision_most_frequency
    analysis_vision['vision_mean_constancy_indicator_1'] = vision_mean_constancy_indicator_1
    analysis_vision['vision_mean_constancy_indicator_2'] = vision_mean_constancy_indicator_2
    analysis_vision['vision_mean_constancy_indicator_3'] = vision_mean_constancy_indicator_3
    analysis_vision['vision_ratio_constancy_indicator_1'] = vision_ratio_constancy_indicator_1
    analysis_vision['vision_ratio_constancy_indicator_2'] = vision_ratio_constancy_indicator_2
    analysis_vision['vision_ratio_constancy_indicator_3'] = vision_ratio_constancy_indicator_3
    analysis_vision['vision_std'] = vision_std
    analysis_vision['vision_ratio_std'] = vision_ratio_std
    analysis_vision['wins_count'] = win_df['visionScore'].count()
    analysis_vision['win_vision_mean'] = win_df['visionScore'].mean()
    analysis_vision['win_vision_median'] = win_df['visionScore'].median()
    analysis_vision['win_vision_sum'] = win_df['visionScore'].sum()
    analysis_vision['win_vision_std'] = win_df['visionScore'].std()
    analysis_vision['win_vision_ratio_mean'] = win_df['visionScorePerMinute'].mean()
    analysis_vision['win_vision_ratio   _std'] = win_df['visionScorePerMinute'].std()
    analysis_vision['lose_count'] = lose_df['visionScore'].count()
    analysis_vision['lose_vision_mean'] = lose_df['visionScore'].mean()
    analysis_vision['lose_vision_median'] = lose_df['visionScore'].median()
    analysis_vision['lose_vision_sum'] = lose_df['visionScore'].sum()
    analysis_vision['lose_vision_std'] = lose_df['visionScore'].std()
    analysis_vision['lose_vision_ratio_mean'] = lose_df['visionScorePerMinute'].mean()
    analysis_vision['lose_vision_ratio_std'] = lose_df['visionScorePerMinute'].std()

    for key in analysis_vision:
        if (isinstance(analysis_vision[key], float)):
            analysis_vision[key] = round(analysis_vision[key], 3)

    analysis_vision_formatted = json.dumps(
        analysis_vision, default=str, indent=4)
    save_file = f"{save_path}ping_overview_analysis_{player_alias}.json"
    with open(save_file, "w") as outfile:
        outfile.write(analysis_vision_formatted)

    df_ratio_dates_mean = df[['gameCreation', 'visionScorePerMinute']].copy()
    df_ratio_dates_mean = df_ratio_dates_mean.groupby(
        'gameCreation', as_index=False)['visionScorePerMinute'].mean()
    
        
    df_distribution_vision = df[['visionScore']].copy()
    df_distribution_vision = pd.DataFrame(df_distribution_vision['visionScore'].value_counts().reset_index().values, columns=["visionScore", "counts"])
    df_distribution_vision = df_distribution_vision.sort_values(by=['visionScore'], ascending=True)
    # print(df_distribution_vision)
   

    max_vision = df['visionScore'].max()
    min_vision = df['visionScore'].min()
    max_ratio = df['visionScorePerMinute'].max()

    # Vision Total Overview Scatter Chart
    fig_total_vision, axs_total_vision = plt.subplots(figsize=(8, 4))
    df.plot(kind='scatter', x='gameCreation',
            y='visionScore', ax=axs_total_vision)

    axs_total_vision.set_ylim([0, max_vision+(max_vision/10)])
    axs_total_vision.set_xticks(df['gameCreation'])
    axs_total_vision.set_xticklabels(df['gameCreation'])
    axs_total_vision.xaxis.set_major_locator(mdates.MonthLocator(interval=1))
    axs_total_vision.set_xlabel("")
    axs_total_vision.set_ylabel("Pontos de Visão")
    axs_total_vision.set_title(f"Dispersão S {player_alias.capitalize()}")

    file_total_vision = f"{save_path}vision_overview_total_{player_alias}_scatter"
    fig_total_vision.savefig(file_total_vision)

    plt.close()



    # Vision Ratio Overview Line Chart
    fig_ratio_vision, axs_ratio_vision = plt.subplots(figsize=(8, 4))
    df_ratio_dates_mean.plot(
        kind='line', x='gameCreation', y='visionScorePerMinute', ax=axs_ratio_vision)
    axs_ratio_vision.xaxis.set_major_locator(mdates.MonthLocator(interval=1))
    axs_ratio_vision.legend(['Frequência'])
    axs_ratio_vision.set_xlabel("")
    axs_ratio_vision.set_ylabel("Visão/Minuto")
    axs_ratio_vision.set_title(f"Frequência Score Visão {player_alias.capitalize()}")

    file_ratio_vision = f"{save_path}vision_overview_ratio_{player_alias}_line"
    fig_ratio_vision.savefig(file_ratio_vision)

    idx = df_frequency.index.values
    frequency = df_frequency.values

    plt.close()

    # Vision Match Distribution Overview Line Chart
    fig_distribution_vision, axs_distribution_vision = plt.subplots(figsize=(8, 4))
    df_distribution_vision.plot(
        kind='bar', x='visionScore', y='counts', ax=axs_distribution_vision)
    axs_distribution_vision.legend(['Distribuição'])
    axs_distribution_vision.set_xlabel("Quantidade")
    axs_distribution_vision.set_ylabel("Ocorrências")
    axs_distribution_vision.set_title(f"Distribuição Placar Visão {player_alias.capitalize()}")

    file_distribution_vision = f"{save_path}vision_overview_distribution_{player_alias}_line"
    fig_distribution_vision.savefig(file_distribution_vision)

    plt.close()

    return analysis_vision


def save_all_players_pings_overview(match_settings, player_type, players_type_alias_puuid):

    geral_pings_overview_analysis = []

    for player in players_type_alias_puuid[player_type]:

        player_alias = player
        player_puuid = players_type_alias_puuid[player_type][player]

        save_path = f"data/{player_type}/{player_alias}/"

        raw_data_matchs_file = f"{save_path}matchs_metadata_{player_alias}.json"
        raw_data_matchs_file = open(raw_data_matchs_file)
        raw_matches_data = json.load(raw_data_matchs_file)
        raw_data_matchs_file.close()

        pings_overview_analysis = save_ping_overview(
            raw_matches_data, match_settings, player_puuid, save_path, player_alias)

        geral_pings_overview_analysis.append(pings_overview_analysis)

    geral_pings_overview_analysis = format_json(geral_pings_overview_analysis)

    save_file = f"analysis/{player_type}_geral_ping_overview_analysis.json"
    with open(save_file, "w") as outfile:

        outfile.write(geral_pings_overview_analysis)

    return


def save_all_players_vision_overview(match_settings, player_type, players_type_alias_puuid):

    geral_vision_overview_analysis = []

    for player in players_type_alias_puuid[player_type]:

        player_alias = player
        player_puuid = players_type_alias_puuid[player_type][player]

        save_path = f"data/{player_type}/{player_alias}/"

        raw_data_matchs_file = f"{save_path}matchs_metadata_{player_alias}.json"
        raw_data_matchs_file = open(raw_data_matchs_file)
        raw_matches_data = json.load(raw_data_matchs_file)
        raw_data_matchs_file.close()
        
        vision_overview_analysis = save_vision_overview(raw_matches_data, match_settings,
                             player_puuid, save_path, player_alias)

        geral_vision_overview_analysis.append(vision_overview_analysis)

    geral_vision_overview_analysis =format_json(geral_vision_overview_analysis)

    save_file =  f"analysis/{player_type}_geral_vision_overview_analysis.json"
    with open(save_file, "w") as outfile:

        outfile.write(geral_vision_overview_analysis)

    return

# Load settings match filter
file_settings_filter = open("settings_match_filter.json", "r")
settings_filter = json.loads(file_settings_filter.read())
file_settings_filter.close()

# settings_filter['playerSettings']['championName'] = ['Akali']
# settings_filter['playerSettings']['role'] = ['SOLO']
# settings_filter['playerSettings']['lane'] = ['MIDDLE']
# settings_filter['playerSettings']['individualPosition'] = ['MIDDLE']

# Role: SOLO, CARRY, NONE, SUPPORT
# Lane: JUNGLE, MIDDLE, BOTTOM, TOP
# Position: TOP, MIDDLE, JUNGLE, BOTTOM, UTILITY, APEX, NONE



# Load players puuid alias
file_puuids_alias = open("players_type_alias_puuid.json", "r")
players_type_alias_puuid = json.loads(file_puuids_alias.read())
file_puuids_alias.close()

# Select player type
player_type = 'proplayer'

# Select player alias
player_alias = 'brance'

# Get player puuid by alias
player_puuid = players_type_alias_puuid[player_type][player_alias]

# Set path to save player analysis
save_path = f"data/{player_type}/{player_alias}/"

# # Load raw data from exported matches json
raw_data_matchs_file = f"{save_path}matchs_metadata_{player_alias}.json"
raw_data_matchs_file = open(raw_data_matchs_file)
raw_matches_data = json.load(raw_data_matchs_file)
raw_data_matchs_file.close()

# Save all players type
# save_all_players_pings_overview(settings_filter,player_type,players_type_alias_puuid)
# save_all_players_vision_overview(settings_filter,player_type,players_type_alias_puuid)

# Save only 1 player
# save_vision_overview(raw_matches_data, settings_filter,
                #    player_puuid, save_path, player_alias)
save_ping_overview(raw_matches_data, settings_filter,
                   player_puuid, save_path, player_alias)

# Test code area
