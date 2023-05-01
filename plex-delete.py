import csv
from tqdm import tqdm
from plexapi.server import PlexServer

CSV_FILENAME = 'movies.csv'
LOG_FILENAME = 'delete_log.txt'

PLEX_BASE_URL = 'http://ip:port'
PLEX_TOKEN = 'YOUR_PLEX_TOKEN'

# Connect to the Plex server
plex = PlexServer(PLEX_BASE_URL, PLEX_TOKEN)

def create_deletion_log():
    # Open log file
    log_file = open(LOG_FILENAME, 'w')

    # Read CSV file and delete movies with audience rating <= 5.6
    with open(CSV_FILENAME, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in tqdm(reader, desc='Processing movies'):
            try:
                if float(row['audience_rating']) <= 5.6 or not row['audience_rating']:
                    # Log deleted movie
                    log_file.write(f"Deleted {row['file_name']} with audience rating of {row['audience_rating']}\n")
            except ValueError:
                # Handle cases where audience rating is not a number
                log_file.write(f"Unable to delete {row['file_name']} due to invalid audience rating of {row['audience_rating']}\n")
                continue

    # Close log file
    log_file.close()
    print("Deletion log created successfully.")

def delete_movies_without_approval():
    # Read log file and delete movies
    with open(LOG_FILENAME, 'r') as log_file:
        for line in tqdm(log_file.readlines(), desc='Deleting movies'):
            file_name = line.split()[1]
            try:
                plex.library.remove(file_name)
            except Exception as e:
                # Handle any errors and continue deleting movies
                print(f'Error deleting {file_name}: {e}')
                continue

    print("Movies deleted successfully.")

def delete_movies_with_approval():
    # Read log file and delete movies
    with open(LOG_FILENAME, 'r') as log_file:
        for line in tqdm(log_file.readlines(), desc='Deleting movies'):
            file_name = line.split()[1]
            user_input = input(f"Do you want to delete {file_name}? (y/n): ")
            if user_input.lower() == 'y':
                try:
                    plex.library.remove(file_name)
                except Exception as e:
                    # Handle any errors and continue deleting movies
                    print(f'Error deleting {file_name}: {e}')
                    continue
            else:
                print(f"Skipping deletion of {file_name}.")

    print("Movies deleted successfully.")

# Show menu screen
while True:
    print("Menu:")
    print("1. Create a deletion log of all movies with a score under 5.6")
    print("2. Connect to the Plex server and delete movies without approval")
    print("3. Connect to the Plex server and delete movies with approval required")
    print("4. Exit")

    user_input = input("Enter option number: ")

    if user_input == '1':
        create_deletion_log()
    elif user_input == '2':
        delete_movies_without_approval()
    elif user_input == '3':
        delete_movies_with_approval()
    elif user_input == '4':
        break
    else:
        print("Invalid input. Please enter a valid option number.")
