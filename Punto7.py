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


# 7. Produrre una visualizzazione interattiva con PyVis dei due grafi con colorazioni di
# nodi ed archi a piacimento. Salvare i due output in formato HTML nella cartella
# /visualizations .

# read_gpickle()
with open("graphs/coauthorship_graph.pkl", 'rb') as f:  # notice the r instead of w
    coauthorship_graph = pickle.load(f)

# read_gpickle()
with open("graphs/extended_coauthorship_graph.pkl", 'rb') as f:  # notice the r instead of w
    extended_coauthorship_graph = pickle.load(f)


nt = Network(
    height="100%",
    width="100%",
    bgcolor="#222222",
    font_color="white",
    heading="Game of Graphs"
)
nt.barnes_hut()
nt.from_nx(coauthorship_graph)
neighbor_map = nt.get_adj_list()
for node in nt.nodes:
    node["value"] = len(neighbor_map[node["id"]])
nt.show("visualizations/interactive_first_graphs.html", notebook=False)


nt.barnes_hut()
nt.from_nx(extended_coauthorship_graph)
neighbor_map = nt.get_adj_list()
for node in nt.nodes:
    node["value"] = len(neighbor_map[node["id"]])
nt.show("visualizations/interactive_extended_graphs.html", notebook=False)