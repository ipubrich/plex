README
Project Name
The name of this project is Plex Movie Deleter.

Description
This project provides a script that helps users delete movies with low audience ratings from their Plex libraries. The user can define a minimum score, and the script will create a CSV file containing a list of movies with scores below the minimum. Then, the user can choose whether or not to delete the movies from the Plex library.

Installation
Clone this repository to your local machine.
Install the required dependencies by running the following command in your terminal:

Copy code
pip install -r requirements.txt

Create a config.ini file in the project directory with the following content:
csharp

Copy code
[plex]
base_url = <your plex base URL>
token = <your plex token>
Replace <your plex base URL> with the URL of your Plex server and <your plex token> with your Plex authentication token.
Run the script using the following command:

Copy code
python delete_movies.py
Follow the prompts to delete movies from your Plex library.
Usage
The script provides the following functions:

delete_movie(movie): deletes a movie from the Plex library.
get_movies_to_delete(min_score): reads a CSV file containing a list of movies and returns a list of movies with audience ratings below the specified minimum score.
delete_movies_confirm(min_score, delete_from_plex): prompts the user to confirm the deletion of movies with audience ratings below the specified minimum score. If delete_from_plex is True, the script will delete the movies from the Plex library.

scan_library(): scans the Plex library and writes a CSV file containing a list of movies and their audience ratings.
Credits

This project uses the following dependencies:

csv - for reading and writing CSV files.
sys - for system-specific parameters and functions.
os - for interacting with the operating system.
tqdm - for adding progress bars to loops.
plexapi - for interacting with the Plex API.
logging - for logging error messages.
configparser - for parsing the config.ini file.
License
This project is licensed under the MIT License. See the LICENSE file for details.
