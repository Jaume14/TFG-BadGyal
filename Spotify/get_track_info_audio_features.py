import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd

# Codi d'autenticació
client_id = 'clau-client'
client_secret = 'clau-secret'
client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

# Establim les variables necessàries
artist_id = '4F4pp8NUW08JuXwnoxglpN'
count = 0
llista_dfs = []

# Agafem els tipus de recopilatoris que volem analitzar
tipus_albums = ['album', 'single', 'appears_on', 'compilation']

# Iterem per obtenir una llista amb les cançons de tots els tipus de recopilatoris
for element in tipus_albums:  # Iterem per recopilatori
    llista_albums = sp.artist_albums(artist_id, album_type=element)

    for album in llista_albums['items']:  # Iterem per album
        llista_pistes = sp.album_tracks(album['id'])

        for pista in llista_pistes['items']:  # Iterem per cançó i afegim a la llista
            llista_artistes = []
            llista_markets = []

            for artista in pista['artists']:
                if artista['name'] == 'Bad Gyal':

                    # iterem pels elements que són llistes
                    for artist in pista['artists']:
                        llista_artistes.append(artist['name'])
                    for market in pista['available_markets']:
                        llista_markets.append(market)

                    # Obtenim les audio features de la cançó
                    audio_features = sp.audio_features(pista['id'])[0]

                    # Afegim les audio features al dataframe
                    df = pd.DataFrame({
                        "track": pista['name'],
                        'duration': pista['duration_ms'],
                        "album": album['name'],
                        'position': pista['track_number'],
                        "published": album['release_date'],
                        'artistes': ','.join(llista_artistes),
                        'explicit': pista['explicit'],
                        'id': pista['id'],
                        'markets': ','.join(llista_markets),
                        'danceability': audio_features['danceability'],
                        'energy': audio_features['energy'],
                        'key': audio_features['key'],
                        'loudness': audio_features['loudness'],
                        'mode': audio_features['mode'],
                        'speechiness': audio_features['speechiness'],
                        'acousticness': audio_features['acousticness'],
                        'instrumentalness': audio_features['instrumentalness'],
                        'liveness': audio_features['liveness'],
                        'valence': audio_features['valence'],
                        'tempo': audio_features['tempo'],
                        'time_signature': audio_features['time_signature']
                    }, index=[0])
                    llista_dfs.append(df)

        #count += 1  # Utilitzem count com a codi de control
        #print(count)

# Creem el df a partir de la llista
df_final = pd.concat(llista_dfs)
print(df_final)

# Exportem el df a un arxiu .csv
df_final.to_csv('bad_gyal_pistes_info(5).csv', index=False)