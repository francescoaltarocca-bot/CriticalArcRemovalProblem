import networkx as nx
import matplotlib.pyplot as plt
import random
import pickle

# Esempio
# n = 20 #Numero dei nodi
# l = 1  # Limite inferiore
# u = 100  # Limite superiore
# k = 2
# M = 1000
# h = 5 # Numero di archi deboli >= k
# p = 0.65 # Probabilità di creare un arco
# seed = 5123467

# con n 5000 e k>10 l'algoritmo si satura e AMPL esce senza soluzioni trovate (>300 secondi)

instances = [
    {"n": 50, "l": 1, "u": 100, "k": 5,  "M": None,  "h": 10, "p": 0.75, "seed": 147257},
    {"n": 50, "l": 1, "u": 100, "k": 10,  "M": None,  "h": 15, "p": 0.75, "seed": 147256},
    {"n": 50, "l": 1, "u": 100, "k": 15,  "M": None,  "h": 20, "p": 0.75, "seed": 147255},
    {"n": 500, "l": 1, "u": 100, "k": 5, "M": None, "h": 10, "p": 0.75, "seed": 147254},
    {"n": 500, "l": 1, "u": 100, "k": 10, "M": None, "h": 15, "p": 0.75, "seed": 147253},
    {"n": 500, "l": 1, "u": 100, "k": 15, "M": None, "h": 20, "p": 0.75, "seed": 147252},
    {"n": 1000, "l": 1, "u": 100, "k": 5, "M": None, "h": 10, "p": 0.75, "seed": 147251},
    {"n": 1000, "l": 1, "u": 100, "k": 10, "M": None, "h": 15, "p": 0.75, "seed": 147250},
    {"n": 1000, "l": 1, "u": 100, "k": 15, "M": None, "h": 20, "p": 0.75, "seed": 147274},
    {"n": 1500, "l": 1, "u": 100, "k": 5,  "M": None,  "h": 10, "p": 0.75, "seed": 147258},
    {"n": 1500, "l": 1, "u": 100, "k": 10,  "M": None,  "h": 15, "p": 0.75, "seed": 258147},
    {"n": 1500, "l": 1, "u": 100, "k": 15,  "M": None,  "h": 20, "p": 0.75, "seed": 852741},
    {"n": 2000, "l": 1, "u": 100, "k": 5,  "M": None,  "h": 10, "p": 0.75, "seed": 963852},
    {"n": 2000, "l": 1, "u": 100, "k": 10,  "M": None,  "h": 15, "p": 0.75, "seed": 285147},
    {"n": 2000, "l": 1, "u": 100, "k": 15,  "M": None,  "h": 20, "p": 0.75, "seed": 852963},
    {"n": 2500, "l": 1, "u": 100, "k": 5,  "M": None,  "h": 10, "p": 0.75, "seed": 357159},
    {"n": 2500, "l": 1, "u": 100, "k": 10,  "M": None,  "h": 15, "p": 0.75, "seed": 951753},
    {"n": 2500, "l": 1, "u": 100, "k": 15,  "M": None,  "h": 20, "p": 0.75, "seed": 951357},
    {"n": 3000, "l": 1, "u": 100, "k": 5, "M": None, "h": 10, "p": 0.75, "seed": 159357},
    {"n": 3000, "l": 1, "u": 100, "k": 10, "M": None, "h": 15, "p": 0.75, "seed": 159753},
    {"n": 3000, "l": 1, "u": 100, "k": 15, "M": None, "h": 20, "p": 0.75, "seed": 268431},
    {"n": 4000, "l": 1, "u": 100, "k": 5, "M": None, "h": 10, "p": 0.75, "seed": 268497},
    {"n": 4000, "l": 1, "u": 100, "k": 10, "M": None, "h": 15, "p": 0.75, "seed": 315974},
    {"n": 4000, "l": 1, "u": 100, "k": 15, "M": None, "h": 20, "p": 0.75, "seed": 369741},
    {"n": 5000, "l": 1, "u": 100, "k": 5, "M": None, "h": 10, "p": 0.75, "seed": 147273},
    {"n": 5000, "l": 1, "u": 100, "k": 10, "M": None, "h": 15, "p": 0.75, "seed": 147276},
    {"n": 5000, "l": 1, "u": 100, "k": 15, "M": None, "h": 20, "p": 0.75, "seed": 147271},

]


def genera_lista(n, l, u, seed):
    """
    Genera una lista di n numeri interi (compresi tra l e u)
    :param n: Numero dei pesi da generare
    :param l: Limite inferiore
    :param u: Limite superiore
    :param seed: Seed per numeri pseudocasuali

    :return: Lista di h archi estratti
    """
    random.seed(seed)
    return {i: random.randint(l, u) for i in range(1, n+1)}
def extract_h_edges(G, h, seed):
    """
    Estrae h archi casuali dal grafo G.
    :param G: Grafo NetworkX (DiGraph)
    :param h: Numero di archi da estrarre
    :param seed: Seed per numeri pseudocasuali

    :return: Lista di h archi estratti
    """
    if h > len(G.edges):
        raise ValueError("h è maggiore del numero totale di archi nel grafo!")

    random.seed(seed)
    return random.sample(list(G.edges), h)

def plotDag(G, w_edges, title_txt, fig_size_x, fig_size_y):
    """
    Disegna il grafo G.
    :param G: Grafo NetworkX (DiGraph)
    :param w_edges: Lista archi deboli
    :param title_txt: Titolo del grafico
    :param fig_size_x: Larghezza del grafico
    :param fig_size_y: Altezza del grafico
    """
    plt.figure(figsize=(fig_size_x, fig_size_y))
    for layer, nodes in enumerate(nx.topological_generations(G)):
        for node in nodes:
            G.nodes[node]["layer"] = layer
    pos = nx.multipartite_layout(G, subset_key="layer")

    # Modifica del colore degli archi
    for u, v in G.edges():
        G[u][v]['color'] = 'green' if (u, v) in w_edges else 'gray'

    colors = nx.get_edge_attributes(G, 'color').values()

    nx.draw(G, pos, with_labels=True, node_color="lightblue", edge_color=colors, node_size=2000, font_size=12)

    edge_labels = {(u, v): G[u][v]['weight'] for u, v in G.edges()}
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color="red")
    plt.title(title_txt)
    plt.show()
def exportFileDatAMPL(DAG, weak_edges, lista_casuale, n, k, M, instanceFilename):
    """
    Esporta il grafo G in un file dat di AMPL
    :param DAG: Grafo NetworkX (DiGraph)
    :param weak_edges: Lista archi deboli
    :param lista_casuale: Pesi dei nodi
    :param n: Numero dei nodi
    :param k: Numero massimo di archi deboli da eliminare
    :param M: Costante grande
    :param instanceFilename: Nome del file di destinazione
    """
    contenuto = f"data; \nparam n := {n}; \nparam k := {k}; \nparam M := {M};\n"
    nodes = list(DAG.nodes)
    nodes.sort(reverse=False)
    edges = list(DAG.edges)
    A2 = list(DAG.edges() - weak_edges)

    fileDatAMPL = f"{instanceFilename}.ampl.dat"
    with open(fileDatAMPL, "w") as file:
        file.write(contenuto)

        # esporta gli archi, nominati con A
        file.write("set A:= ")
        for ee in range(len(edges) - 1):
            file.write(f"{edges[ee]} ")
        file.write(f"{edges[-1]};\n")

        # esporta archi deboli A1
        file.write("set A1:= ")
        for ee in range(len(weak_edges) - 1):
            file.write(f"{weak_edges[ee]} ")
        file.write(f"{weak_edges[-1]};\n")

        # esporta archi A2
        file.write("set A2:= ")
        for aa in range(len(A2) - 1):
            file.write(f"{A2[aa]} ")
        file.write(f"{A2[-1]};\n")

        file.write("param d := \n")
        for nodo, peso in (lista_casuale.items()):
            file.write(f'{nodo} {peso}\n')
        file.write(";")

def generateInstance(n, l, u, k, M, h, p, seed):
    """
    Genera il grafo DAG Grafo NetworkX (DiGraph)
    :param n: Numero dei nodi
    :param l: Limite inferiore peso nodo
    :param u: Limite superiore peso nodo
    :param k: Numero massimo di archi deboli da eliminare
    :param M: Costante grande
    :param h: numero degli archi deboli h > k
    :param p: probabilità di creare un arco
    :param seed: Seed per numeri pseudocasuali

    """

    upper=u
    if M is None:
        M=n*u
    if h<k:
        h=k

    # genera la lista dei pesi associati ai nodi
    lista_casuale_pesi_nodi = genera_lista(n, l, u, seed)
    print(lista_casuale_pesi_nodi)
    G = nx.gnp_random_graph(n, p, directed=True, seed=seed)
    DAG = nx.DiGraph([(u, v, {'weight': 0}) for (u, v) in G.edges() if u < v])
    nx.is_directed_acyclic_graph(DAG)
    # Dizionario per la rinominazione dei nodi (n → n+1)
    mapping = {node: node + 1 for node in DAG.nodes}
    # Creazione di un nuovo grafo con i nodi rinominati
    DAG = nx.relabel_nodes(DAG, mapping)
    # Copia DAG
    dagOrig = DAG.copy()
    # Correggi i nodi trovati
    print(f"Lista archi aggiunti a nodi che non hanno successori")
    # Aggiunge n-> n+1 ai nodi che non hanno successori
    for node in DAG.nodes:
        if ((node not in {n}) and (DAG.out_degree(node) == 0)):
            next_node = (node + 1)
            DAG.add_edge(node, next_node, weight=0)
            print(f"{node}->{next_node}")
    print(f"Lista archi aggiunti a nodi che non hanno predecessori")
    # Aggiunge n-> n+1 ai nodi che non hanno predecessori
    for node in DAG.nodes:
        if ((node not in {1}) and (DAG.in_degree(node) == 0)):
            prev_node = (node - 1)
            DAG.add_edge(prev_node, node, weight=0)
            print(f"{prev_node}->{node}")
    for u, v in dagOrig.edges():
        dagOrig[u][v]['weight'] = lista_casuale_pesi_nodi[u]
    for u, v in DAG.edges():
        DAG[u][v]['weight'] = lista_casuale_pesi_nodi[u]
    weak_edges = extract_h_edges(DAG, h, seed)
    # plotDag(dagOrig, weak_edges, "dagOrig generato automaticamente", 8, 6)
    # plotDag(DAG, weak_edges, "DAG generato automaticamente", 8, 6)
    instanceFilename = f"n{n}l{l}u{upper}k{k}M{M}h{h}p{p}seed{seed}"
    # Salvataggio su file del grafo nx e dei parametri
    with open(f"{instanceFilename}.pkl", "wb") as f:
        pickle.dump((DAG, weak_edges, n, l, upper, k, M, h, p, seed), f)
    exportFileDatAMPL(DAG, weak_edges, lista_casuale_pesi_nodi, n, k, M, instanceFilename)


"""
MAIN
Genera i grafi contenuti nella lista instances
"""
for i in instances:
    generateInstance(i['n'], i['l'], i['u'], i['k'], i['M'], i['h'], i['p'], i['seed'])

