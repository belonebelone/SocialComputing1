# 6. Per entrambi i grafi prodotti calcolare per ogni nodo:
# a. Degree Centrality
# b. Betweenness Centrality
# c. Closeness Centrality
# d. Pagerank
# e. HITS, per calcolare i valori di hubness e authority
# f. Riassumere le due informazioni in un DataFrame per ciascun grafo, dove
# ogni riga rappresenta le informazioni relative ad un nodo, ed ogni colonna le
# informazioni relative ad una misura calcolata per quel nodo. Salvare nella
# cartella /results tali DataFrame.

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


# 5. Per entrambi i grafi prodotti calcolare:
# a. Coefficiente di clustering medio
# b. Centro del grafo
# c. Raggio
# d. Distanza Media
# e. Transitività
# f. Coefficienti Omega e Sigma, per stimare la “small-world-ness”
# g. Riassumere le informazioni in un DataFrame, dove ogni riga rappresenta le
# informazioni relative ad un grafo, ed ogni colonna le informazioni relative ad
# una misura calcolata per quel grafo. Salvare nella cartella /results tale
# DataFrame.

def get_graphInfo(grafo):
    nodes = nx.nodes(coauthorship_graph)
    degree_centrality = nx.degree_centrality(grafo)
    betweenness_centrality = nx.betweenness_centrality(grafo)
    closeness_centrality = nx.closeness_centrality(grafo)
    pagerank = nx.pagerank(grafo)
    hits = nx.hits(grafo)

    # Creare un DataFrame
    df = pd.DataFrame({
        'Node': list(grafo.nodes()),
        'Degree Centrality': list(degree_centrality.values()),
        'Betweenness Centrality': list(betweenness_centrality.values()),
        'Closeness Centrality': list(closeness_centrality.values()),
        'Pagerank': list(pagerank.values()),
        'HITS Hubness': list(hits[0].values()),
        'HITS Authority': list(hits[1].values())
    })
    return df


# read_gpickle()
with open("graphs/coauthorship_graph.pkl", 'rb') as f:  # notice the r instead of w
    coauthorship_graph = pickle.load(f)

# read_gpickle()
with open("graphs/extended_coauthorship_graph.pkl", 'rb') as f:  # notice the r instead of w
    extended_coauthorship_graph = pickle.load(f)

# g. Riassumere le informazioni in un DataFrame, dove ogni riga rappresenta le
# informazioni relative ad un grafo, ed ogni colonna le informazioni relative ad
# una misura calcolata per quel grafo. Salvare nella cartella /results tale
# DataFrame.


print("test")


df_first_graph_centralities = pd.DataFrame(get_graphInfo(coauthorship_graph))
print(df_first_graph_centralities)


df_extended_graph_centralities = pd.DataFrame(get_graphInfo(extended_coauthorship_graph))
print(df_extended_graph_centralities)

df_first_graph_centralities.to_csv("results/first_graph_centralities.csv", index=False)

df_extended_graph_centralities.to_csv("results/extended_graph_centralities.csv", index=False)
