import csv
import json
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

    with open(save_file, "w") as outfile:

        for match in match_list:

            if (check_match_settings(match, match_settings) == True):

                pings_overview = {}

                player_data = get_player_match_info_by_player_puuid(
                    match, puuid)

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

                pings_overview = format_json(pings_overview)

                outfile.write(pings_overview)

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



player_type = 'streamer'
player_alias = 'nicklink'
path = player_type + '/'+player_alias+'/'

raw_data_matchs_file = path + 'matchs_metadata_'+player_alias+'.json'

# Load raw data from exported matches json
raw_data_matchs_file = open(raw_data_matchs_file)
raw_matches_data = json.load(raw_data_matchs_file)
raw_data_matchs_file.close()


players_puuid = {}

# Line Players
players_puuid['akaashi'] = 'jkgVko75HkHz9kHMYrVKYuPPC60s59vKct4Dj2djr0ETBLd52pqBO6xERuqLPsL7VbNR8sHHh7cFNg'
players_puuid['tekendol'] = 'z2RlhdFkRh2CJ052bFeAd1SgdGIG9pyLJMPRpQImpELnUCgR0o4Gw2k2S6RR4vQ85daZ7imGU6w4hQ'
players_puuid['nataruk'] = 'LdDeMb13ze9R_iYpMxyT5xP9PeiabtBtQ7FC65nrxXCDwLob2KGirZv__t71vwP9bDR-rhIf24m7vg'

# Streamer Players
players_puuid['nicklink'] = 'LiK_rfePGdi96HJYh1eyN9RDyz8nr2gI9fDLhU-D0barCr-rIaxXr627Dk5dxqAEe6OPW4vmjY-Njw'

# Pro Players
players_puuid['titan'] = 'dgBKuZgDjSv5F8Tgnuzi158sZlyyMtv1X9icbWvjFt7NbvIt7U31Ss6-IGyyJosYUIShfQzQpl4KHw'
players_puuid['tinows'] = 'VqN8fBYVLJeXt4LiADsU71WoFtl19lY_cb0prtH_gI4HAAZ2LzHj84s4eD-bTrKPjRuC2IriGyoVdg'
players_puuid['jojo'] = 'PNw506k5hy7E_TVBM0-3f3m9WNk1I_A0qgakr2yqH7_aS7s5G636Y724mT5Do0Gj2FbBpr3QDqxU_g'
players_puuid['robo'] = '1MIvsxWx7kzD6qK7Tk8aAH908L59S2BxS1vL6K6fKjGOcSUhdgE4MUdFMm51Srw84ZU171DkJ016wg'
players_puuid['redbert'] = 'EZYRE4MGGQgqQGo8wrKd0nbGsCb8mWNc7Pp0S6VLWyz6ipePiFcn6tqfAYDQkOBIvl8-gkW1rFmkuw'
players_puuid['aegis'] = '-AdfEz26CdEDewsjoPa5Th8SQXtbh3rP672IKoMDMO_-POgjXi_Pje2yIZrx8j2nGfuQeq13jVeDpQ'
players_puuid['ceos'] = 'yJJ-Tv5ruDm6r_u21LBVcZtfwe9MCtB7EYHLLNR8rZdUPkYSeDfryUwcraSxXxltAzolx2z5qrtUfg'
players_puuid['cariok'] = 'KywiMYSX0-Fui38aiX34d18pyayDw_81CWE4qsa-GW7hBZQWQjdR9XRmor448qpDmnsACq1vELB-lQ'
players_puuid['dynquedo'] = '856AWrKcOZK-aAlrw8z4-CK2i7-hsoct_BIzeMDMcbLrGCibfISJGej0vKTtZs_ai6pVVRZ01BJhvA'
players_puuid['zay'] = 'gciJ-QUyWRkiI6Ota4xNKC4ELdu792pqHG0bkVozcPZ-rjBfUT-1jGCk7EtAm2tixOel83sKZEX9fA'
players_puuid['damage'] = 'rnD8fXMqIaIyScczJq-JkjiEN9EVsLlnvOS7O-o4boKwPk1YU9zbh2IhpEdV9RECRpcG00DBE9cuag'
players_puuid['croc'] = 'i16VY0qrzqqPGTAAdBL7hHbtokXDc7ARPhLkmnCfuxoaGrFoYY5Pk7KgIuaK67cF0mCm45sZvNQckg'
players_puuid['brance'] = 'IH-gtERps3P_hpAw2sYJ6Lq1qo_D-WZbP-sWWm9VsqE8VCk-Up65cOyO0e-W9_GYeVFy7mEyxMyJyg'
players_puuid['ayu'] = 'QWwXTNR7ej2kBByiH9lztGGQYELHDcZ3_jNhqmFrwZE7EOLG47VwKH7BMrC8lmdaQtazJqw4rKHDSA'
players_puuid['tay'] = 'UVFHubHn9zQZ_Ua-_CLCXjvMMZ2W6JkUEOLrxJh_-nnbNBgyhexCErrv6-PBFCsHKXN4kfzM8_QsDQ'
players_puuid['ninjakiwi'] = 'GS1QsEoXcPLk5SI_CxTWFl-EsbrGAlTHLNJtPPRDGSKjVr0d99IpPxjV_TtN_22-xq6xVews39cTJg'
players_puuid['guigo'] = 'f_50s5FE-Df1CqeTAEzpT80B_n5uUtScIj7B6I5zqbRUcne4mg4xzAni8mtbnx2K2AU8Zq70bRWCdg'

save_file = path + "ping_overview_"+player_alias+".json"

# count_matches = save_data_file(puuid_akaashi,save_file)

# player_match_info = get_player_match_info_by_player_puuid(raw_matches_data[0],puuid_akaashi)
# print(player_match_info)

save_pings_overview(raw_matches_data, match_settings, players_puuid[player_alias], save_file)

# save_pings_overview(raw_matches_data,puuid_tinows,save_file)

# save_json_to_csv(overview, "match_overview_akaashi.csv")


# with open(save_file, "w") as outfile:
#     data = json.dumps(raw_matches_data[0], indent=4)
#     outfile.write(data)
