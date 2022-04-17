# importing the module 
import imdb 
from pyarr import RadarrAPI
import argparse
import traceback
import os

parser = argparse.ArgumentParser()
parser.add_argument("IMDBActorID")
args = parser.parse_args()

host_url = 'http://127.0.0.1:7878'
api_key = os.getenv('RADARR_KEY')

radarr = RadarrAPI(host_url, api_key)
ia = imdb.IMDb() 
  
code = args.IMDBActorID
print(ia.get_person(code)) 
   
actor_results = ia.get_person_filmography(code) 
  
for movie in actor_results['data']['filmography']['actor']:
    try:
        title = movie.get('title')
        year = movie.get('year')
        print(str(title) + " " + str(year))
        result = radarr.lookup_movie(str(title) + " " + str(year))
        if len(result) == 0:
            continue

        #pprint(result)
        title = result[0]['title']
        dbid = result[0]['tmdbId']
        print(title)
        print(dbid)
        radarr.add_movie(dbid, 1, "/movies")
    except Exception as e:
        #print("fail ...")
        #print(e)
        traceback.print_exc()
