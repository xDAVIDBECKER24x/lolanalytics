import csv
import json
from time import gmtime
from time import strftime

def format_json(json_data):

    json_formatted = json.dumps(json_data, indent=4) 

    return json_formatted

def check_game_mode(match, mode):

    if (match['info']['gameMode'] in mode): return True

    return False


def check_game_type(match, type):

    if (match['info']['gameType'] in type): return True

    return False

def get_player_match_info_by_player_puuid(match, puuid):
    
    print("Getting Match => "+match['metadata']['matchId'])

    participants_info = match['metadata']['participants']
    player_idx = participants_info.index(puuid)

    player_match_info = match['info']['participants'][player_idx]
   

    return player_match_info

def save_formatted_data_file(puuid,save_file):

    with open(save_file, "w") as outfile:

        for match in data:

            if ((check_game_type(match, ["CUSTOM_GAME", "MATCHED_GAME"]) & check_game_mode(match, ["CLASSIC"])) == True):

                match_info = get_player_match_info_by_player_puuid(match, puuid)
                outfile.write(match_info)

    return

def save_match_overview(match_list,puuid,save_file):

    with open(save_file, "w") as outfile:

        for match in match_list:

            match_overview = {}

            player_data = get_player_match_info_by_player_puuid(match,puuid)

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

def save_pings_overview(match_list,puuid,save_file):

    with open(save_file, "w") as outfile:

        for match in match_list:

            pings_overview = {}

            player_data = get_player_match_info_by_player_puuid(match,puuid)

            match_duration = match['info']['gameDuration']
            match_duration = strftime("%H:%M:%S", gmtime(match_duration))

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


            pings_overview = format_json(pings_overview)    

            outfile.write(pings_overview)
        
    return

def save_date_matchs(match_list,save_file):

    with open(save_file, "w") as outfile:

       for match in match_list:

            date_overview = {}

            date_overview['gameCreation'] = match['info']['gameCreation']

            date_overview = format_json(date_overview)    

            outfile.write(date_overview)

    return


def save_json_to_csv(data,file):

    headers = data[0].keys()
    
    with open(file, 'w') as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        writer.writerows(data)

    return

    

#https://developer.riotgames.com/apis#match-v5/GET_getMatch


path = 'newplayers/tekendol/'

raw_data_matchs_file = path + 'matchs_metadata_tekendol.json'

# Load raw data from exported matches json
raw_data_matchs_file = open(raw_data_matchs_file)   
raw_matches_data = json.load(raw_data_matchs_file)
raw_data_matchs_file.close()


# match_id = 'BR1_2755319405'

puuid_akaashi = 'jkgVko75HkHz9kHMYrVKYuPPC60s59vKct4Dj2djr0ETBLd52pqBO6xERuqLPsL7VbNR8sHHh7cFNg'
puuid_tekendol = 'z2RlhdFkRh2CJ052bFeAd1SgdGIG9pyLJMPRpQImpELnUCgR0o4Gw2k2S6RR4vQ85daZ7imGU6w4hQ'
puuid_nataruk = 'LdDeMb13ze9R_iYpMxyT5xP9PeiabtBtQ7FC65nrxXCDwLob2KGirZv__t71vwP9bDR-rhIf24m7vg'
puuid_titan = 'dgBKuZgDjSv5F8Tgnuzi158sZlyyMtv1X9icbWvjFt7NbvIt7U31Ss6-IGyyJosYUIShfQzQpl4KHw'
puuid_tinows = 'VqN8fBYVLJeXt4LiADsU71WoFtl19lY_cb0prtH_gI4HAAZ2LzHj84s4eD-bTrKPjRuC2IriGyoVdg'
puuid_jojo = 'PNw506k5hy7E_TVBM0-3f3m9WNk1I_A0qgakr2yqH7_aS7s5G636Y724mT5Do0Gj2FbBpr3QDqxU_g'

save_file = path +  "dates_tekendol.json"

# count_matches = save_data_file(puuid_akaashi,save_file)

# player_match_info = get_player_match_info_by_player_puuid(raw_matches_data[0],puuid_akaashi)
# print(player_match_info)

save_date_matchs(raw_matches_data,save_file)

# save_pings_overview(raw_matches_data,puuid_tinows,save_file)

# save_json_to_csv(overview, "match_overview_akaashi.csv")



# with open(save_file, "w") as outfile:
#     data = json.dumps(raw_matches_data[0], indent=4)
#     outfile.write(data)
