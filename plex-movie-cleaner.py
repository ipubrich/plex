import csv
import sys
import os
from tqdm.auto import tqdm
from plexapi.server import PlexServer
from plexapi.exceptions import BadRequest
from plexapi.exceptions import NotFound
import logging
import configparser

# Check if variables are set 
config = configparser.ConfigParser()
config.read('config.ini')

if not config.has_section('plex'):
    raise ValueError('Configuration file does not have the required section "plex"')

PLEX_BASE_URL = config.get('plex', 'base_url')
PLEX_TOKEN = config.get('plex', 'token')

print(PLEX_BASE_URL, PLEX_TOKEN)  # should output http://192.168.1.55:32400 LKG1YxmLEVWfDe6xFAvx

PLEX_TIMEOUT = 30
LIBRARY_SECTION = 15

plex = PlexServer(PLEX_BASE_URL, PLEX_TOKEN, timeout=PLEX_TIMEOUT)
CSV_FILE = 'movies.csv'

logging.basicConfig(filename='deleted_movie.log', level=logging.INFO)


def delete_movie(movie):
    logger = logging.getLogger(__name__)
    try:
        # loop through all media files and delete them
        for media in movie.media:
            media.delete()

        # delete the library item
        movie.delete()
        logger.info(f"{movie.title} deleted from Plex library")
    except NotFound as e:
        logger.error(f'NotFound Error deleting {movie.title}: {e}')
    except BadRequest as e:
        logger.error(f'BadRequest Error deleting {movie.title}: {e}')

        
def get_movies_to_delete(min_score):
    movies_to_delete = []
    with open(CSV_FILE, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            movie_name = row['movie_name']
            audience_rating = row['audience_rating'].strip()
            year = row['year'].strip()
            try:
                audience_rating = float(audience_rating)
            except ValueError:
                print(f"Skipping movie '{movie_name}' with invalid audience rating '{audience_rating}'")
                continue
            if not year:
                print(f"Skipping movie '{movie_name}' with invalid year '{year}'")
                continue
            try:
                year = int(year)
            except ValueError:
                print(f"Skipping movie '{movie_name}' with invalid year '{year}'")
                continue
            if audience_rating < min_score:
                movies_to_delete.append({'movie_name': movie_name, 'rating_key': row['rating_key'], 'year': year, 'rating': audience_rating})

    # print the movies to delete
    print("Movies to delete:")
    for i, movie in enumerate(movies_to_delete):
        print(f"{i+1}. {movie['movie_name']} ({movie['year']}) - Rating: {movie['rating']}")
    return movies_to_delete


def delete_movies_confirm(min_score, delete_from_plex):
    # Get the list of movies to delete
    movies_to_delete = get_movies_to_delete(min_score)

    # Display the list of movies to delete
    print(f"Movies to delete:")
    for index, movie in enumerate(movies_to_delete):
        print(f"{index+1}. {movie['movie_name']} ({movie['year']}) - Rating: {movie['rating']}")

    # Prompt the user for confirmation
    confirmation = input(f"\nAre you sure you want to delete {len(movies_to_delete)} movies below the minimum score? (y/n): ")
    if confirmation.lower() == "y":
        # Delete the movies
        for movie in movies_to_delete:
            movie_name = movie['movie_name']
            rating_key = movie['rating_key']
            url = f"/library/metadata/{rating_key}?checkFiles=1&includeAllConcerts=1&includeBandwidths=1&includeChapters=1&includeChildren=1&includeConcerts=1&includeExtras=1&includeFields=1&includeGeolocation=1&includeLoudnessRamps=1&includeMarkers=1&includeOnDeck=1&includePopularLeaves=1&includePreferences=1&includeRelated=1&includeRelatedCount=1&includeReviews=1&includeStations=1&Plex-Token={PLEX_TOKEN}"

            # delete from Plex library
            if delete_from_plex:
                movie = plex.fetchItem(url)
                if movie:
                    delete_choice = input(f"Do you want to delete '{movie_name}' from Plex library? (y/n): ")
                    if delete_choice.lower() == 'y':
                        delete_movie(movie)
                        print(f"Deleted '{movie_name}' from Plex library.")
                    else:
                        print(f"Not deleting '{movie_name}' from Plex library.")
            else:
                movie = plex.fetchItem(url)
                delete_movie(movie)
                print(f"Deleted '{movie_name}' from Plex library.")

        print(f"\nDeleted {len(movies_to_delete)} movies from Plex library.")
    else:
        print("\nMovies not deleted.")
        
    return

def scan_library():
    # Connect to the Plex server
    plex = PlexServer(PLEX_BASE_URL, PLEX_TOKEN)

    # Get the movie library
    movies = plex.library.sectionByID(LIBRARY_SECTION).search(libtype='movie')

    # Create a set to keep track of processed movie titles
    processed_movies = set()

    # Create a CSV file and write headers
    with open(CSV_FILE, 'w', newline='') as csvfile:
        fieldnames = ['file_name', 'movie_name', 'audience_rating', 'rating_key', 'year']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        # Loop through each movie and write data to CSV file
        for movie in tqdm(movies, desc='Processing movies'):
            try:
                # Check for duplicates before processing the movie
                if movie.title in processed_movies:
                    continue

                # Add the processed movie to the set of processed movies
                processed_movies.add(movie.title)

                # Loop through each movie file and write data to CSV file
                for media in movie.media:
                    for part in media.parts:
                        # Get the movie file name and path
                        file_name = part.file

                        # Get the movie name, audience rating, rating key, and year
                        movie_name = movie.title
                        try:
                            audience_rating = float(movie.audienceRating) if hasattr(movie, 'audienceRating') and isinstance(movie.audienceRating, float) else '0.0'
                        except (ValueError, TypeError):
                            audience_rating = 0.0
                        rating_key = movie.ratingKey
                        year = movie.year

                        # Write data to CSV file
                        writer.writerow({'file_name': file_name, 'movie_name': movie_name, 'audience_rating': audience_rating,
                                         'rating_key': rating_key, 'year': year})
            except Exception as e:
                # Handle any errors and continue processing movies
                print(f'Error processing {movie.title}: {e}')
                continue



def main_menu():
    while True:
        print("Main Menu")
        print("---------")
        print("1. Scan Movies - Create CSV before running operations")
        print("2. Delete Movies below minimum score with manual confirmation")
        print("3. Delete Movies below minimum score with without confirmation")
        print("4. Delete CSV file")
        print("5. Exit")
        choice = input("Enter your choice (1-5): ")
        if choice == "1":
            scan_library()
        elif choice == "2":
            min_score = float(input("Enter the minimum score: "))
            delete_movies_confirm(min_score, True)
        elif choice == "3":
            min_score = float(input("Enter the minimum score: "))
            delete_movies_confirm(min_score, False)
        elif choice == "4":
            os.remove(CSV_FILE)
            print(f"Deleted {CSV_FILE}")
        elif choice == "5":
            sys.exit()
        else:
            print("Invalid choice. Please enter a number between 1 and 5.")


if __name__ == "__main__":
    main_menu()
