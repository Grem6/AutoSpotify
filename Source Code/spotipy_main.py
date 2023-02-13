import spotipy
from spotipy.oauth2 import SpotifyOAuth
from csv import reader
from csv import writer
import webbrowser
import time
import configparser
import os.path
config = configparser.ConfigParser()
from colorama import init
init(autoreset=False)
YELLOW = "\x1b[1;33;40m"
RED = "\x1b[1;31;40m"


def auto_spotify():
    

    print('\x1b[0;32;40m' + 'Running autospotify...' + '\x1b[0m')

    scope = "playlist-modify-public playlist-modify-private playlist-read-private playlist-read-collaborative"
    
    config.read(r'auth.conf')

    client_id = config['credentials']['client_id']
    client_secret = config['credentials']['client_secret']
    

    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id,
                                                   client_secret=client_secret,
                                                   redirect_uri='http://localhost:5000/callback/',
                                                   scope=scope))

    current_user = sp.current_user()
    user_id = current_user['id']
    print('\n')
    print('Hi', current_user['display_name'])
    print('\n')

    playlist_exists = os.path.exists('playlists_auto.conf')

    if playlist_exists:
        
        #if playlist created by autospotify already exists locally;

        config.read(r'playlists_auto.conf')

        playlist_id = config['playlist']['id']
        playlist_name = config['playlist']['name']
        print(f'playlist : {playlist_name} found! ')
        
        #user choice to add to locally found playlist
        # if yes, run this;
        print(f"\n{YELLOW}Do you want to add to this existing playlist? | (yes/no): ",end='')
        user_choice = input(RED).lower()
        if user_choice == 'yes':
            url = f'https://open.spotify.com/playlist/{playlist_id}'
            webbrowser.open(url)

            with open('spotify.csv', 'r') as f_r:
                csv_reader = reader(f_r)
                for index, row in enumerate(csv_reader):
                    if index == 0:
                        continue
                    q = row[1]
                    output = sp.search(q, limit=1, offset=0,
                                    type='track', market=None)
                    for track in output['tracks']['items']:
                        tracks = [track['uri']]
                        
                        sp.user_playlist_remove_all_occurrences_of_tracks(
                            user_id, playlist_id, tracks)
                        sp.user_playlist_add_tracks(
                            user_id, playlist_id, tracks, position=None)
            print('\x1b[0;32;40m' + 'All tracks added!' + '\x1b[0m')
            print('\x1b[0;32;40m' + '**removed duplicate entries**' + '\x1b[0m')
            
        else:
        #user choice to add to locally found playlist
        #if no, run this;
            
            print(f"\n{YELLOW}paste your playlist id here: ",end='')
            playlist_id_user = input(RED)
            config['playlist'] = {"id": playlist_id_user}
            
            with open('playlists_user.conf', 'w') as configfile:
                config.write(configfile)
                
            config.read(r'playlists_user.conf')

            playlist_id_user = config['playlist']['id']
            url = f'https://open.spotify.com/playlist/{playlist_id_user}'
            webbrowser.open(url)

            with open('spotify.csv', 'r') as f_r:
                csv_reader = reader(f_r)
                for index, row in enumerate(csv_reader):
                    if index == 0:
                        continue
                    q = row[1]
                    output = sp.search(q, limit=1, offset=0,
                                    type='track', market=None)
                    for track in output['tracks']['items']:
                        tracks = [track['uri']]
                        
                        sp.user_playlist_remove_all_occurrences_of_tracks(
                            user_id, playlist_id_user, tracks)
                        sp.user_playlist_add_tracks(
                            user_id, playlist_id_user, tracks, position=None)
            print('\x1b[0;32;40m' + 'All tracks added!' + '\x1b[0m')
            print('\x1b[0;32;40m' + '**removed duplicate entries**' + '\x1b[0m')
                
                    

    else:

        print('\x1b[0;31;40m' + 'No playlists found!' + '\x1b[0m')
        print('\n')
        print('Autospotify is creating one for you...')
        print(f"\n{YELLOW}Add a name to this playlist: ",end='')
        name = input(RED)
        print(f"\n{YELLOW}Add a description to this playlist: ",end='')
        description = input(RED)
        print(f"\n{YELLOW}Make it public? | (yes/no): ",end='')
        public = input(RED).lower()
        print(f"\n{YELLOW}Make it collaborative? | (yes/no): ",end='')
        collaborative = input(RED).lower()
        if public and collaborative != 'yes':
            public = False
            collaborative = False

        playlist = sp.user_playlist_create(user_id, name, public=public, collaborative=collaborative, description=description)
        id = playlist['id']
        url = f'https://open.spotify.com/playlist/{id}'
        webbrowser.open(url)
        time.sleep(10)

        config['playlist'] = {"name": name, "id": id}

        with open('playlists_auto.conf', 'w') as configfile:
            config.write(configfile)

        print('\n')
        print(f'Playlist: {name} with id: {id} created!')
        
        with open('spotify.csv', 'r') as f_r:
                csv_reader = reader(f_r)
                for index, row in enumerate(csv_reader):
                    if index == 0:
                        continue
                    q = row[1]
                    output = sp.search(q, limit=1, offset=0,
                                    type='track', market=None)
                    for track in output['tracks']['items']:
                        tracks = [track['uri']]
                        
                        sp.user_playlist_remove_all_occurrences_of_tracks(user_id, id, tracks)
                        sp.user_playlist_add_tracks(user_id, id, tracks, position=None)
        print('\x1b[0;32;40m' + 'All tracks added!' + '\x1b[0m')
        print('\x1b[0;32;40m' + '**removed duplicate entries**' + '\x1b[0m')

