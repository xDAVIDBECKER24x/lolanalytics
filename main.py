import json

file = open('matchs_metada_example.json')

data = json.load(file)

file.close()

puuid_akaashi= 'jkgVko75HkHz9kHMYrVKYuPPC60s59vKct4Dj2djr0ETBLd52pqBO6xERuqLPsL7VbNR8sHHh7cFNg'

participants_info = data[1]['metadata']['participants']
player_idx =  participants_info.index(puuid_akaashi)

player_info = data[1]['info']['participants'][player_idx]

# print(player_idx)

player_info = json.dumps(player_info, indent=4)
 
with open("temp.json", "w") as outfile:
    outfile.write(player_info)
