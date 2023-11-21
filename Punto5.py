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

def get_Info(grafo):

    # a. Coefficiente di clustering medio
    #nx.average_clustering(grafo)

    # b. Centro del grafo
    #nx.center(grafo)

    # c. Raggio
    #nx.radius(grafo)

    # d. Distanza Media
    #nx.average_shortest_path_length(grafo)

    # e. Transitività
    #nx.transitivity(grafo)

    # f. Coefficienti Omega e Sigma, per stimare la “small-world-ness”
    #nx.omega(grafo)
    #nx.sigma(grafo)
    #print("test2")

    #print(nx.average_clustering(grafo))
    #print(nx.center(grafo))
    #print(nx.radius(grafo))
    #print(nx.average_shortest_path_length(grafo))
    #print(nx.transitivity(grafo))
    #print(nx.omega(grafo))
    #print(nx.sigma(grafo))

    new_row = {'coefficiente di clustering medio': nx.average_clustering(grafo), 'centro del grafo': nx.center(grafo), 'raggio': nx.radius(grafo), 'distanza media': nx.average_shortest_path_length(grafo), 'transitività': nx.transitivity(grafo), 'coefficiente omega': nx.omega(grafo), 'coefficiente sigma': nx.sigma(grafo)}

    #print("test3")

    return new_row

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
df_first_graph_centralities = pd.DataFrame(get_Info(coauthorship_graph))
print(df_first_graph_centralities)
df_extended_graph_centralities = pd.DataFrame(get_Info(extended_coauthorship_graph))
print(df_extended_graph_centralities)

df_overall_measures = pd.concat([df_first_graph_centralities, df_extended_graph_centralities], ignore_index=True)
df_overall_measures.to_csv("results/overall_measures.csv", index=False)