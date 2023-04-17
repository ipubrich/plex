# Connects to local plex server and produces a CSV of path\file, title and audience rating
#
import csv
from plexapi.server import PlexServer
from tqdm import tqdm

# Update these to your local requirements
PLEX_BASE_URL = 'http://ip:port'
MOVIE_URL = PLEX_BASE_URL + '/library/sections/****/all'
CSV_FILENAME = 'movies.csv'
PLEX_TOKEN = 'add-personal-token-here'

# Connect to the Plex server
plex = PlexServer(PLEX_BASE_URL, PLEX_TOKEN)

# Get the movie library
movies = plex.library.sectionByID(15).all()

# Create a CSV file and write headers
with open(CSV_FILENAME, 'w', newline='') as csvfile:
    fieldnames = ['file_name', 'movie_name', 'audience_rating']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    # Loop through each movie and write data to CSV file
    for movie in tqdm(movies, desc='Processing movies'):
        try:
            # Get the movie file name and path
            file_name = movie.media[0].parts[0].file

            # Get the movie name and audience rating
            movie_name = movie.title
            audience_rating = movie.audienceRating if hasattr(movie, 'audienceRating') else None

            # Write data to CSV file
            writer.writerow({'file_name': file_name, 'movie_name': movie_name, 'audience_rating': audience_rating})
        except Exception as e:
            # Handle any errors and continue processing movies
            print(f'Error processing {movie.title}: {e}')
            continue
