import pandas as pd
from tqdm import tqdm
import openpyxl

# creem els valors necessaris previs
count = 0
llista_prov = []
total = 500000
chunksize = 100000

# iterem pels valors per extreure cada dada del tweet
for skip in tqdm(range(0, total, chunksize)):  # per no sobrecarregar l'ordinador apliquem range i chunksize
    df = pd.read_excel('datasets/dataset-Bad Gyal-lang-es-cat(3).xlsx', skiprows=skip, nrows=chunksize, usecols="K,X,C")
    for a, tweet in df.iterrows():
        try:
            username = tweet['username']
            created_at = tweet['tweet_created_at']
            # print(username)
        except KeyError:
            pass

        try:  # agafem les mencions
            txt = tweet['ent_mentions'].split(';')
            llista_mencions = txt  # creem una llista amb les mencions del tweet
            for element in llista_mencions:
                if element == 'false' or element == 'FALS':  # treiem els tweets sense menció
                    pass
                else:
                    rel = (username, element, created_at)  # agrupem els tres elements
                    llista_prov.append(rel)

        except KeyError:  # per evitar que es pari el programa si no hi ha mencions
            pass
        count += 1
        # print(count)

# creem el df i l'exportem a csv
df_final = pd.DataFrame(llista_prov, columns=['Source', 'Target', 'Timestamp'])
# print(df_final)
df_final.to_csv('datasets/mencions(3).csv', index=False)
