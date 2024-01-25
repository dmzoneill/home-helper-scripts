#!/usr/bin/python3
import requests
from pprint import pprint
import argparse


api_key = "80d9fdfbc543445db90c5d53037651b8"
base_url = "http://localhost:7878/api/v3"
headers = {"X-Api-Key": api_key}


# Create an argument parser
parser = argparse.ArgumentParser(
    description="Show movies in the range based on IMDb and Rotten Tomatoes ratings",
    epilog="python3 radarr_rating_delete.py -imdb 0.0 3.0 -rotten 0 20 -delete"                
)

# Add IMDb rating filter arguments
parser.add_argument("-imdb", nargs="*", type=float, help="IMDb rating filter range (low high)")

# Add Rotten Tomatoes rating filter arguments
parser.add_argument("-rotten", nargs="*", type=int, help="Rotten Tomatoes rating filter range (low high)")

# Whether to delete from radarr or not
parser.add_argument("-delete", action="store_true", help="Whether to delete the movies in the range")

# Parse the command-line arguments
args = parser.parse_args()

# Extract the IMDb and Rotten Tomatoes rating filter values
if args.imdb:
    if len(args.imdb) == 1:
        low_imdb_filter = int(args.imdb[0] * 10)
        high_imdb_filter = 100
    elif len(args.imdb) == 2:
        low_imdb_filter = int(args.imdb[0] * 10)
        high_imdb_filter = int(args.imdb[1] * 10)
    else:
        raise ValueError("Invalid number of arguments for IMDb rating filter")
else:
    low_imdb_filter = 0
    high_imdb_filter = 100

if args.rotten:
    if len(args.rotten) == 1:
        low_rotten_filter = int(args.rotten[0])
        high_rotten_filter = 100
    elif len(args.rotten) == 2:
        low_rotten_filter = int(args.rotten[0])
        high_rotten_filter = int(args.rotten[1])
    else:
        raise ValueError("Invalid number of arguments for Rotten Tomatoes rating filter")
else:
    low_rotten_filter = 0
    high_rotten_filter = 100

# Query all movies
response = requests.get(f"{base_url}/movie", headers=headers)
movies = response.json()
in_range_imdb = 0
in_range_rotten = 0
both_in_range = 0 

movies = sorted(
    movies,
    key=lambda movie: (
        bool(movie.get("ratings", {}).get("imdb")),  # True if IMDb ratings exist, False otherwise
        movie.get("ratings", {}).get("imdb", {}).get("value", -9999)  # IMDb rating value or fallback value
    )
)

def delete(movie_id):
    global api_key, base_url, args
    if args.delete:
        delete_url = f"{base_url}/movie/{movie_id}?deleteFiles=true&apikey={api_key}"
        response = requests.delete(delete_url)

        if response.status_code == requests.codes.ok:
            print("Movie deleted successfully.")
        else:
            print("Failed to delete the movie.")

# Iterate through movies and retrieve IMDb ID and file path
for movie in movies:
    if "imdbId" in movie and "path" in movie:
        imdb_id = movie["imdbId"]
        file_path = movie["path"]
        movie_id = movie["id"]
        ratings = movie.get("ratings", {})
        imdb_rating = ratings.get("imdb", {}).get("value")
        rotten_rating = ratings.get("rottenTomatoes", {}).get("value")
        # pprint(movie)

        lines = []
        lines.append(f"Movie ID: {movie_id}")
        lines.append(f"IMDb ID: {imdb_id}")
        lines.append(f"File Path: {file_path}")
                
        if imdb_rating is not None:
            imdb_rating_int = int(imdb_rating * 10)
            
            if low_imdb_filter <= imdb_rating_int <= high_imdb_filter:
                lines.append(f"IMDb Rating: {imdb_rating}")
                in_range_imdb += 1

        if rotten_rating is not None:
            rotten_rating_int = int(rotten_rating)
            
            if low_rotten_filter <= rotten_rating_int <= high_rotten_filter:
                lines.append(f"Rotten Tomatoes Rating: {rotten_rating}")
                in_range_rotten += 1

        if args.rotten and args.imdb and len(lines) == 5:
            both_in_range += 1
            for line in lines:
                print(line)
            delete(movie_id)
            continue

        if args.rotten and not args.imdb and len(lines) == 4 and 'Rotten' in lines[3]:
            for line in lines:
                print(line)
            delete(movie_id)
            continue

        if not args.rotten and args.imdb and len(lines) == 4 and 'IMDb' in lines[3]:
            for line in lines:
                print(line)
            delete(movie_id)
            continue


# Print the total number of movies within the IMDb and Rotten Tomatoes rating range
print(f"Total movies within IMDb rating range: {in_range_imdb}")
print(f"Total movies within Rotten Tomatoes rating range: {in_range_rotten}")
print(f"Total movies in both ranges: {both_in_range}")