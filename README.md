
# README

This code is a Python script that uses the Plex API to delete movies from a Plex library based on their audience rating.

  

## Dependencies

Python 3.x
tqdm
plexapi

To install the required dependencies, use the following command:
 
shell
>pip install -r requirements.txt

### Usage

Before running the script, you need to set up a configuration file called config.ini. An example file is provided, which you can modify to suit your needs. The config.ini file should contain the following parameters:

 ' base_url: The URL of your Plex server.'

token: Your Plex authentication token.

Once you have set up the configuration file, you can run the script with the following command:

  

shell
>python delete_low_rated_movies.py

When prompted, enter the minimum audience rating below which you want to delete movies. If you want to delete the movies from your Plex library, enter y when prompted.

  

### Functionality

The script performs the following functions:

  

Reads the configuration file to get the Plex server URL and authentication token.

Connects to the Plex server and scans the movie library for movies with an audience rating below the specified threshold.

Asks for confirmation before deleting the movies.

Deletes the selected movies from the Plex library and outputs a log file of the deleted movies.

License

This code is licensed under the MIT License. Probably.