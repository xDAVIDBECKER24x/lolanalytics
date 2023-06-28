import json

def save_data_file(puuid):
    with open("temp.json", "w") as outfile:
        
        for match in data :

            print("Getting Match => "+match['metadata']['matchId'])
            
            participants_info = match['metadata']['participants']
            player_idx =  participants_info.index(puuid_akaashi)


            player_info = match['info']['participants'][player_idx]
            player_info = json.dumps(player_info, indent=4)
            outfile.write(player_info)
            

#Load data from exported matches json
file = open('matchs_metada_example.json')
data = json.load(file)
file.close()


puuid_akaashi= 'jkgVko75HkHz9kHMYrVKYuPPC60s59vKct4Dj2djr0ETBLd52pqBO6xERuqLPsL7VbNR8sHHh7cFNg'

save_data_file()

print("Finished player data => " + puuid_akaashi)





    
