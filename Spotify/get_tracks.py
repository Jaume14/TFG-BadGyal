# Importació de les llibreries
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd
import json

# Codi d'autenticació
client_id = 'clau-client'
client_secret = 'clau-secret'
client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

# Establim les variables necessàries
artist_id = '4F4pp8NUW08JuXwnoxglpN'
count = 0
llista_pistesf = []
ll_tipus_albums = []
ll_release_date = []

# Agafem els tipus de recopilatoris que volem analitzar
tipus_albums = ['album']

# Iterem per obtenir una llista amb les cançons de tots els tipus de recopilatoris
for element in tipus_albums:  # Iterem per recopilatori
    llista_albums = sp.artist_albums(artist_id, album_type=element)

    for album in llista_albums['items']:  # Iterem per album
        llista_pistes = sp.album_tracks(album['id'])
        tipus_album = album['album_type']
        with open(f'data_album_{album["id"]}.json', 'w', encoding='utf-8') as f:
            json.dump(llista_pistes, f, ensure_ascii=False, indent=4)

        for pista in llista_pistes['items']:  # Iterem per cançó i afegim a la llista
            
            llista_pistesf.append(pista['name'])
            ll_tipus_albums.append(tipus_album)
            ll_release_date.append(album['release_date'])
            #ll_features = sp.features

        count += 1  # Utilitzem count com a codi de control
        print(count)

print('creem df')
# Creem el df a partir de la llista
df = pd.DataFrame(llista_pistesf, columns=['pista'])
df = pd.DataFrame({'Pista': llista_pistesf, 'Tipus': ll_tipus_albums, 'Data_Publicacio': ll_release_date})

# Imprimim el df
print(df)

# Exportem el df a un arxiu .csv
#df.to_csv('bad_gyal_pistes_info.csv', index=False)'''