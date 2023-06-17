import requests

username = 'Beckynho'

api_key = "RGAPI-c29ff9d4-7749-47e3-846b-b161d1eb25eb"
url = 'https://br1.api.riotgames.com/lol/summoner/v4/summoners/by-name/Beckynho?api_key=RGAPI-c29ff9d4-7749-47e3-846b-b161d1eb25eb'
# headers = {'X-Riot-Token': api_key}

res = requests.get(url)
user = res.json()
id = user['id']
print(id)
