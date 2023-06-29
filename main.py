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


def save_json_to_csv(data,file):

    headers = data[0].keys()
    
    with open(file, 'w') as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        writer.writerows(data)


# Load data from exported matches json
file = open('matchs_metadata_example.json')
raw_matches_data = json.load(file)
file.close()


match_id = 'BR1_2755319405'
puuid_akaashi = 'jkgVko75HkHz9kHMYrVKYuPPC60s59vKct4Dj2djr0ETBLd52pqBO6xERuqLPsL7VbNR8sHHh7cFNg'
save_file = "match_overview_akaashi.json"

# count_matches = save_data_file(puuid_akaashi,save_file)

# player_match_info = get_player_match_info_by_player_puuid(raw_matches_data[0],puuid_akaashi)
# print(player_match_info)



save_match_overview(raw_matches_data,puuid_akaashi,save_file)

# save_json_to_csv(overview, "match_overview_akaashi.csv")



# with open(save_file, "w") as outfile:
#     data = json.dumps(raw_matches_data[0], indent=4)
#     outfile.write(data)
