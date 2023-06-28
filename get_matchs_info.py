import json


def check_game_mode(match, mode):

    if (match['info']['gameMode'] in mode):

        return True

    return False


def check_game_type(match, type):

    if (match['info']['gameType'] in type):
        return True

    return False


def save_data_file(puuid):

    count_matches = 0

    with open("akaashi.json", "w") as outfile:

        for match in data:

            if ((check_game_type(match, ["CUSTOM_GAME", "MATCHED_GAME"]) & check_game_mode(match, ["CLASSIC"])) == True):

                print("Getting Match => "+match['metadata']['matchId'])

                participants_info = match['metadata']['participants']
                player_idx = participants_info.index(puuid)

                player_info = match['info']['participants'][player_idx]
                player_info = json.dumps(player_info, indent=4)
                outfile.write(player_info)

                count_matches += 1

    return count_matches


# Load data from exported matches json
file = open('matchs_metada_example.json')
data = json.load(file)
file.close()


puuid_akaashi = 'jkgVko75HkHz9kHMYrVKYuPPC60s59vKct4Dj2djr0ETBLd52pqBO6xERuqLPsL7VbNR8sHHh7cFNg'


count_matches = save_data_file(puuid_akaashi)

print("Finished number of matches : "+count_matches +
      " player data => " + puuid_akaashi)
