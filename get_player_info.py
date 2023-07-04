import requests

api_key = "RGAPI-efa5eded-699e-42d9-a19b-af8603501d14"

def get_player_data_by_name(name):

    url = f"https://br1.api.riotgames.com/lol/summoner/v4/summoners/by-name/{username}?api_key={api_key}"
    
    return requests.get(url).json()


def get_match_data_by_player_id(id):

    url = f"https://br1.api.riotgames.com/lol/spectator/v4/active-games/by-summoner/{id}?api_key={api_key}"

    return  requests.get(url).json()



username = 'Beckynho'

player = get_player_data_by_name(username)
print(f"Gettng {player['name']} data statistics => {player['puuid']}")
# match = get_match_data_by_player_id(player['id'])
# user = res.json()
# id = user['id']
# print(match)
