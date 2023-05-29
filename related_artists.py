#Importació de les llibreries
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd

#Codi d'autenticació
client_id = 'clau-client'
client_secret = 'clau-secret'
client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

#Establim les variables necessàries
source_artist_id = '4F4pp8NUW08JuXwnoxglpN'
source_artist_name = sp.artist(source_artist_id)['name']
count = 0
relacions = []
relacionats2n = []

#executem el codi per extreure els artistes relacionats amb Bad Gyal
related_artists = sp.artist_related_artists(source_artist_id)  #obtenim els artistes
relacionats = related_artists["artists"]  #agafem només la llista d'artistes

for l in relacionats: #iterem per a cada artista
    relacionats2n.append(l["id"]) #afegim a la llista per explotar-los en segon nivell
    related_artist_name = l["name"] #agafem només el nom
    tupla = (source_artist_name,related_artist_name) #Afegim en tuples totes les relacions
    relacions.append(tupla) #ho afegim a la llista final


#print(relacionats2n) #printem per comprobar que s'estan afegint bé els de 2n nivell

#per a cada artista relacionat amb BadGyal busquem els seus artistes relacionats també (2n nivell)
for e in relacionats2n:
    related_artists = sp.artist_related_artists(e) #obtenim els relacionats de cada artista
    relacionats = related_artists["artists"] #filtrem les dades
    source_artist_name = sp.artist(e)['name'] #posem el nom d'origen
    for l in relacionats:
        related_artist_name = l["name"]  #afegim el nom del relacionat
        tupla = (source_artist_name, related_artist_name)  #creem la tupla
        relacions.append(tupla)  #ho afegim a la llista final


df = pd.DataFrame.from_records(relacions, columns=['source','target']) #creem el df amb "relacions" i (source - target)

#Imprimim el df
print(df)

#Exportem el df a un arxiu .csv
df.to_csv('bad_gyal_related2nivell.csv', index=False)

