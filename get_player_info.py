import requests

api_key = "RGAPI-9040abe6-ba03-45bf-a7d5-ff877f741125"

def get_player_data_by_name(name):

    url = f"https://br1.api.riotgames.com/lol/summoner/v4/summoners/by-name/{username}?api_key={api_key}"
    
    return requests.get(url).json()


def get_match_data_by_player_id(id):

    url = f"https://br1.api.riotgames.com/lol/spectator/v4/active-games/by-summoner/{id}?api_key={api_key}"

    return  requests.get(url).json()



username = 'twitch nicklink'

player = get_player_data_by_name(username)
print(f"Gettng {player['name']} data statistics => {player['puuid']}")
# match = get_match_data_by_player_id(player['id'])
# user = res.json()
# id = user['id']
# print(match)
