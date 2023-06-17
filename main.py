import requests

api_key = "RGAPI-c29ff9d4-7749-47e3-846b-b161d1eb25eb"

def get_player_data_by_name(name):

    url = f"https://br1.api.riotgames.com/lol/summoner/v4/summoners/by-name/{username}?api_key={api_key}"
    
    return requests.get(url).json()


def get_match_data_by_player_id(id):

    url = f"https://br1.api.riotgames.com/lol/spectator/v4/active-games/by-summoner/{id}?api_key={api_key}"

    return  requests.get(url).json()



username = 'Koi Panda'

player = get_player_data_by_name(username)
print(f"Gettng {player['name']} data statistics => {player['id']}")
match = get_match_data_by_player_id(player['id'])
# user = res.json()
# id = user['id']
print(match)
