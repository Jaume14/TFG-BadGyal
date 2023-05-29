#Importació de les llibreries
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd

#Codi d'autenticació
client_id = 'clau-client'
client_secret = 'clau-secret'
client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

df_inicial = pd.read_csv("bad_gyal_pistes_info(5).csv", header=0)
llista_artist=[]
llista_ids=[]
llista_generes=[]
count=0

for track in df_inicial['id']:
    #print(track_id)
    track_info = sp.track(track)
    for info in track_info['artists']:
        llista_ids.append(info['id'])

    genres=[]
    for artist_id in llista_ids:
        artist = sp.artist(artist_id)
        genres.append(artist['genres'])
        for g in artist['genres']:
            tupla = (track_info['name'], g)  #creem la tupla
            llista_generes.append(tupla)
    count += 1
    print(count)

#print(llista_generes)
df = pd.DataFrame.from_records(llista_generes, columns=['source','target']) #creem el df amb "relacions" i (source - target)

#Imprimim el df
print(df)

#Exportem el df a un arxiu .csv
df.to_csv('bad_gyal_related_genres.csv', index=False)
