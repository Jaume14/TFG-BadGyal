import glob  # permet agafar tots els fitxers
import pandas as pd
from tqdm import tqdm
import openpyxl

count=0
llista_prov=[]

#file = pd.read_excel('datasets/dataset-Bad Gyal-lang-es-cat.xlsx')
#df = pd.DataFrame(file)
#print(df)
#total = 404748
total = 500000
chunksize = 100000
for skip in tqdm(range(0, total, chunksize)):
    df = pd.read_excel('datasets/dataset-Bad Gyal-lang-es-cat(3).xlsx', skiprows=skip, nrows=chunksize, usecols="K,X,C")
    for a, tweet in df.iterrows():
        try:
            username = tweet['username']
            created_at = tweet['tweet_created_at']
            #print(username)
        except KeyError:
            pass

        try:  # agafem les mencions
            txt = tweet['in_reply_to_name'].split(';')
            llista_mencions = txt
            for element in llista_mencions:
                if element == 'false' or element == 'FALS':
                    pass
                else:
                    rel = (element, username, created_at)
                    llista_prov.append(rel)

        except KeyError:
            pass
        count +=1
        #print(count)


# creem el df i l'exportem a csv
df_final = pd.DataFrame(llista_prov, columns=['Source', 'Target', 'Timestamp'])
#print(df_final)
df_final.to_csv('datasets/respostes.csv', index=False)
