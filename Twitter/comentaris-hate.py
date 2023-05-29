import glob
from tqdm import tqdm
import pandas as pd
from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline
import openpyxl

# Models que s'utilitzaran extrets de Hugging Face
models = ["MMG/xlm-roberta-base-sa-spanish",
          "francisco-perez-sorrosal/distilbert-base-uncased-finetuned-with-spanish-tweets-clf",
          "jorgeortizfuentes/spanish_hate_speech"]
# El dataset en el que estan tots els tweets amb les dades
dataset = "datasets/dataset-BadGyal-lang-es-dataset.xlsx"


# es defineix el procés que es farà per obtenir els resultats
def proc(dataset):
    for model in models:  # S'itera per a cada model
        model_name = model.split("/")[1]
        print(model_name)
        dataset_new_name = f"datasets/procesado-{model_name}.xlsx"  # Es crea el nom del fitxer amb les respostes del model
        tup_list = []
        df = pd.read_excel(dataset, usecols='E,M')  # Per optimitzar les dades s'agafa només les columnes necessàries
        tweets = df["text"].to_list()
        tweet_id = df["tweet_id"].to_list()

        t = AutoTokenizer.from_pretrained(model)
        m = AutoModelForSequenceClassification.from_pretrained(model)

        for tweet, tid in tqdm(zip(tweets, tweet_id)):  # Per a cada tweet s'nalitza amb el codi següent
            try:
                pipe = pipeline("text-classification", model=m, tokenizer=t)
                result = pipe(tweet)
                content = result[0]
                label = content["label"]
                score = content["score"]
                tupla = (str(tid), tweet, label, score)  # Es desa la resposta en una tupla
                tup_list.append(tupla)  # S'uneix a la llista
            except:  # Es crea una excepció per tal que no s'aturi el procés si hi ha cap error
                label = 'null'
                score = 0
                tupla = (str(tid), tweet, label, score)
                tup_list.append(tupla)  # S'afegeix el valor a la llista igualment per tenir-lo en compte

        # Es crea el data frame a partir de la llista de tuples
        data = pd.DataFrame.from_records(tup_list, columns=[f"tweet_id", "text", f"label-{model}", f"score-{model}"])
        # S'exporta la resposta del model
        data.to_excel(dataset_new_name, index=False)


# S'executa el procediment definit anteriorment
proc(dataset)

# Es recull la resposta de cada model
datasets = glob.glob("datasets/procesado-*.xlsx")
print(datasets)
dataset_madre = pd.read_excel(datasets[0])

# Per a cada model s'uneixen les respostes al dataset final "dataset_madre"
for d in datasets[1:]:
    df = pd.read_excel(d)
    dataset_madre = dataset_madre.merge(df, on=["tweet_id", "text"])
    print(dataset_madre)

# S'exporta el dataset final amb tots els valors en un document d'Excel
dataset_madre.to_excel('final.xlsx', index=False)
