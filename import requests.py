import requests
import pandas as pd
from serpapi import GoogleScholarSearch
import re
import random
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from IPython.display import display
import pickle
from pyvis.network import Network
import json

# SerpAPI key can be set globally or per search
GoogleScholarSearch.SERP_API_KEY = "0f658d785e1b46d0e868c0d1c59a141db0d89601aff55ba06c2d55d77016348e"


def Punto1():
    # 1. A partire da nodes.csv, utilizzare la libreria Python SerpAPI per scaricare, per
    # ciascuno dei 7 autori elencati:
    # - author_id: ID identificativo del profilo Google Scholar
    # - cited_by: numero totale di citazioni ricevute
    # - interests: elenco degli interessi di ciascun autore
    # Sfruttando la libreria Python Pandas, usare la struttura dati DataFrame per
    # aggiornare il file originale con apposite colonne e memorizzarlo nella cartella /data.

    # Leggo file csv e carico dataframe
    df_nodes = pd.read_csv("data/nodes.csv")
    # display(df_nodes)
    df_nodes_aux = pd.DataFrame(columns=["author_id", "cited_by", "interests"])

    # itero per la coppia name e affilations
    for name, affilations in zip(df_nodes["name"], df_nodes["affiliations"]):

        # Ricerco name tra i profili presenti su Google Scholar
        params = {
            "engine": "google_scholar_profiles",
            "hl": "en",
            "mauthors": name
            }

        search = GoogleScholarSearch(params)
        results = search.get_dict()["profiles"]

        # So che posso avere più profili possibili, ma cerco affilations
        correct_affilations = None

        for result in results:
            if result["affiliations"] == affilations:
                correct_affilations = result

        # display("correct_affilations: ", correct_affilations)

        # -> Trovato profilo corretto !

        # per ciascuno dei 7 autori elencati:
        # - author_id: ID identificativo del profilo Google Scholar
        # - cited_by: numero totale di citazioni ricevute
        # - interests: elenco degli interessi di ciascun autore

        # Creo DataFrame
        author_id = correct_affilations.get('author_id')
        cited_by = correct_affilations.get('cited_by', 'value')
        interests = correct_affilations.get('interests')
        title = None
        for interest in interests:
            title = interest.get('title', '')

        # print(author_id)
        # print(cited_by)
        # print(title)

        # non funziona append!
        new_row = {'author_id': author_id, 'cited_by': cited_by, 'interests': title}
        df_nodes_aux.loc[len(df_nodes_aux)] = new_row

        # esco dal for

    df = pd.concat([df_nodes, df_nodes_aux], axis=1)
    # display(df)

    # scarico dataframe
    df.to_csv("data/nodes.csv", index=False)

def Punto2():


Punto2()
