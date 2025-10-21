from pyvis.network import Network
import networkx as nx

def afficher_graphe(entities, relations, fichier_sortie="relation_graph.html"):
    g = nx.Graph()
    for nom, infos in entities.items():
        g.add_node(nom, **infos)
    for e1, e2, data in relations:
        g.add_edge(e1, e2, **data)
    net = Network(height='750px', width='100%', bgcolor='#222222', font_color='white')
    net.from_nx(g)
    net.show(fichier_sortie)
