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
GoogleScholarSearch.SERP_API_KEY = "ce9dffa0dfa0822e54e9008226d1dbbe92165f4ae7096b2c46734945c466fba5"


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
    # 2. Per ciascuno dei 7 autori, utilizzare il suo ID per accedere al relativo profilo Google
    # Scholar e scaricare l’elenco dei suoi coautori, sempre via SerpAPI. Con tale elenco di nomi:

    df_nodes = pd.read_csv("data/nodes.csv")
    df_coauthor = pd.DataFrame(columns=["name", "affiliations", "author_id", "cited_by", "interests"])

    for author_id in df_nodes["author_id"]:
        #print(author_id)
        params = {
            "engine": "google_scholar_author",
            "hl": "en",
            "author_id": author_id
        }

        search = GoogleScholarSearch(params)
        results_author_id = search.get_dict() # elenco di coautori per ciascun autore

        # a. Utilizzare le SerpAPI per cercare su Google Scholar un ricercatore che
        # corrisponde a tale nome. Per ciascuno, salvare name, affiliations,
        # author_id, cited_by e interests in un nuovo DataFrame contenente tutte
        # queste informazioni relative ai coautori dei 7 autori originari.


        for coauthor in results_author_id["co_authors"]:

            coauthor_name = {coauthor['name']}

            # trova ricercatore che corrisponde a tale nome

            # Ricerco name tra i profili presenti su Google Scholar
            params = {
                "engine": "google_scholar_profiles",
                "hl": "en",
                "mauthors": coauthor_name
            }

            search = GoogleScholarSearch(params)

            # prendo primo profilo
            results_author_id_profile = search.get_dict()["profiles"][0]
            results_author_id_profile1 = results_author_id_profile
            #print(results_author_id_profile1)
            # Per ciascuno, salvare name, affiliations, author_id, cited_by e interests
            # in un nuovo DataFrame contenente tutte queste informazioni relative ai coautori
            # dei 7 autori originari.
            print(results_author_id_profile1)
            # Creo DataFrame
            coauthor_affiliations = results_author_id_profile1.get('affiliations')
            #print(coauthor_affilations)
            coauthor_id = results_author_id_profile1.get('author_id')
            #print(coauthor_id)
            coauthor_cited_by = results_author_id_profile1.get('cited_by', 'value')
            #print(coauthor_cited_by)
            coauthor_interests = results_author_id_profile1.get('interests')
            #print(coauthor_interests)
            coauthor_title = None

            try:
                for interest in coauthor_interests:
                    coauthor_title = interest.get('title', '')
            except:
                coauthor_title = ""

            # non funziona append!
            new_row = {'coauthor_name': coauthor_name, 'coauthor_affiliations': coauthor_affiliations, 'coauthor_author_id': coauthor_id, 'coauthor_cited_by': coauthor_cited_by, 'coauthor_interests': coauthor_title}
            df_coauthor.loc[len(df_coauthor)] = new_row
            print(new_row)
            # esco dal for
    display(df_coauthor)
    # b. Concatenare il DataFrame con i 7 autori originari e quello dei coautori
    # generato al punto 2a in un unico DataFrame.
    # NOTA BENE: è sufficiente effettuare la ricerca dei profili per nome, non
    # accedere al loro profilo tramite id.
    # ASSUNZIONE: in questo caso non potete identificare il profilo corretto tramite
    # il valore di affiliations, quindi assumete che quello corretto sia il primo
    # ritornato nella lista di authors.

    df_coauthor.to_csv("data/coauthor.csv", index=False)
    # salvataggio non neccessario -> eseguito solo per velocizzare il programma


    # c. Creare un terzo DataFrame con le colonne author1, author2 che
    # rappresenta le co-authorship. In tale DataFrame, una riga rappresenta un
    # arco di coauthorship tra due autori.
    # ESEMPIO: David La Barbera, Michael Soprano è una riga del DataFrame
    # creato al punto 2c se Michael Soprano è coautore di David La Barbera. La
    # co-authorship è binaria, non pesata.

    #->df_edges = pd.DataFrame()
    #->df_edges = pd.concat([df_nodes[""], df_coauthor], axis=1)


Punto2()
