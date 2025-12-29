import math
import os
import subprocess
import pickle
import networkx as nx
from itertools import combinations
import re
import time

global time_limit
time_limit=300

def output_box(testo, larghezza=40, linea_vuotaTF=True, c="#"):
    """
    Genera un box di testoil grafo DAG Grafo NetworkX (DiGraph)
    :param testo: Testo da inserire nel box
    :param larghezza: Larghezza del box
    :param linea_vuotaTF: Se True inserisce una linea vuota prima e una dopo
    :param c: Carattere da usare per il box

    """

    testo_centrato = testo.center(larghezza - 2)
    bordo = c + c * (larghezza - 2) + c
    linea_vuota = c + " " * (larghezza - 2) + c
    contenuto = f"{c}{testo_centrato}{c}"
    bordo_basso = c + c * (larghezza - 2) + c
    if linea_vuotaTF:
        return f"{bordo}\n{linea_vuota}\n{contenuto}\n{linea_vuota}\n{bordo_basso}\n"
    else:
        return f"{bordo}\n{contenuto}\n{bordo_basso}\n"
def sostituisci_riga_data(nomefile, nuova_stringa):
    """
    Sostituisce il file dat all'interno del file run di  AMPL
    :param nomefile: File nel quale sostituire il file dat
    :param nuova_stringa: Testo da sostituire nel file

    """
    try:
        # Apri il file in modalità lettura
        with open(nomefile, 'r') as file:
            file_data = file.read()

        # Regex per trovare una riga che inizia con "data" e finisce con ";"
        pattern = r'^data .*?dat;$'

        # Sostituisci la riga con la nuova stringa
        file_data = re.sub(pattern, nuova_stringa, file_data, flags=re.MULTILINE)

        # Apri il file in modalità scrittura per sovrascrivere il contenuto modificato
        with open(nomefile, 'w') as file:
            file.write(file_data)

    except FileNotFoundError:
        print(f"Errore: Il file '{nomefile}' non è stato trovato.")
    except Exception as e:
        print(f"Si è verificato un errore: {e}")

def longest_path(graph):
    """
    Calcola il LP di un grafo
    :param graph: Grafo di input

    :return: LP
    """
    if not nx.is_directed_acyclic_graph(graph):
        return float('inf')

    topological_order = list(nx.topological_sort(graph))
    longest_dist = {node: float('-inf') for node in graph}
    longest_dist[topological_order[0]] = 0

    for node in topological_order:
        for successor in graph.successors(node):
            weight = graph[node][successor]['weight']
            longest_dist[successor] = max(longest_dist[successor], longest_dist[node] + weight)

    return max(longest_dist.values())
def get_subsets(arr, k):
    """
    Calcola i sottoinsiemi di cardianlità al più k di arr
    :param arr: Lista degli elementi dell'insieme
    :param k: Cardinalità massima

    :return: lista di sottoinsiemi di arr
    """
    subsets = []
    for i in range(k + 1):  # Include anche il sottoinsieme vuoto
        subsets.extend(combinations(arr, i))
    return [list(subset) for subset in subsets]
def solve_dag(DAGraph, w_edges, kappa, percTry, file, debug=False, minTries = 25):
    """
    Funzione euristica che risolve il problema della rimozione degli archi deboli
    :param DAGraph: Grafo DAG
    :param w_edges: Insieme degli archi deboli
    :param kappa: Numero massimo di archi da rimuovere
    :param percTry: Percentuale di sottoinsiemi da provare
    :param file: File dei risultati
    :param debug: Inserisce informazioni di dettaglio per debug
    :param minTries: Numero minimo di tentativi se si eccede tempo massimo (stima del tempo massimo > tempo massimo consentito)
    """

    outFile.write(output_box(f"Solve method: LP eu (limit {percTry} of subsets)", 50, False, "*"))

    start = time.perf_counter()

    # Generazione dei sottoinsiemi
    ss = get_subsets(w_edges, kappa)
    # Calcolo della somma dei pesi per ogni sottoinsieme
    ssres = {str(s): sum(DAGraph[u][v]['weight'] for (u, v) in s) for s in ss}
    # Ordinamento dei sottoinsiemi per peso decrescente
    sssres = dict(sorted(ssres.items(), key=lambda item: item[1], reverse=True))
    # Calcolare il numero di elementi da estrarre
    num_elementi = max(1, int(len(sssres) * percTry ))
    # Estrarre i primi 'num_elementi'
    primi_elementi = dict(list(sssres.items())[:num_elementi])


    # Calcolo del LP per ogni sottoinsieme e selezione del minimo
    lp_results = {}
    counter=0
    start_n_try = time.perf_counter()
    for s in primi_elementi:
        counter += 1
        subset_keys = eval(s)  # Converte la stringa in una lista
        grafo_A_star = DAGraph.copy()
        grafo_A_star.remove_edges_from(subset_keys)
        lp_results[s] = longest_path(grafo_A_star)

        end_n_try = time.perf_counter()
        # Se si sono calcolati il numero minimo di LP stima il tempo di completamento
        if(counter>=(minTries*percTry)):
            stima_completamento=math.floor((((end_n_try - start_n_try)/counter)*num_elementi))
            #Se si eccede tempo massimo (stima del tempo massimo > tempo massimo consentito) termina
            if(stima_completamento > time_limit):
                print(f"Calcolo LP interrotto (stima del tempo di completamento {stima_completamento} > {time_limit}): sottoinsiemi testati {counter} di {num_elementi}")
                file.write(f"Calcolo LP interrotto (stima del tempo di completamento {stima_completamento} > {time_limit}): sottoinsiemi testati {counter} di {num_elementi}\n")
                break

    # Selezione del valore minimo
    min_LP_subset = min(lp_results, key=lp_results.get)
    min_value = lp_results[min_LP_subset]
    if debug:
        print(f"Archi deboli ({h}): {w_edges}")
        print(f"Sottoinsiemi generati ({len(ss)}): {ss}")
        print("Somme dei pesi:", ssres)
        print("Sottoinsiemi ordinati secondo la somma dei pesi degli archi:", primi_elementi)
        print("Risultati LP:", lp_results)

        file.write(f"Archi deboli ({h}): {w_edges}\n")
        file.write(f"Sottoinsiemi generati ({len(ss)}): {ss}\n")
        file.write(f"Somme dei pesi: {ssres}\n")
        file.write(f"Sottoinsiemi ordinati secondo la somma dei pesi degli archi: {sssres}\n")
        file.write(f"Risultati LP: {lp_results}\n")


    # Estrai tutte le chiavi con il valore minimo
    min_LP_subset = [(key, value) for key, value in lp_results.items() if value == min_value]
    # Ordinare per numero di archi rimossi
    min_LP_subset_ordered = dict(sorted(min_LP_subset, key=lambda x: len(x[0])))

    # Stampa il primo (se debug=True li stampa tutti in ordimne crescente in base al numero degli archi rimossi)
    for key, v in min_LP_subset_ordered.items():
        print(f"Sottoinsieme che minimizza il LP ({len(eval(key))} archi rimossi): {key} con valore {v}")
        file.write(f"Sottoinsieme che minimizza il LP ({len(eval(key))} archi rimossi): {key} con valore {v}\n")
        if not debug:
            break

    end = time.perf_counter()
    print(f"Tempo di esecuzione: {end - start:.5f} secondi")
    file.write(f"Tempo di esecuzione: {end - start:.5f} secondi\n")

def runAmpl(runSolverPrototype, instance, title, outFile, amplPath):
    """
    Invoca AMPL per risolvere il problema della rimozione degli archi deboli
        * versione nuormale
        * versione ottimizzata con minor numero di archi rimossi

    :param runSolverPrototype: File run di AMPL da invocare
    :param instance: Istanza del problema
    :param title: Testo da scrivere nel file di risultati
    :param outFile: File dove scrivere i risultati
    :param file: File dei risultati
    :param amplPath: Path di AMPL
    """
    # Genara il file .run customizzato con l'istanza
    sostituisci_riga_data(runSolverPrototype, "data " + instance + ".ampl.dat;")
    # Costruisce il comando per eseguire AMPL con il file .dat
    command = [amplPath, runSolverPrototype]
    # Esegue AMPL e aspetta che termini
    process = subprocess.run(command, capture_output=True, text=True)
    # Stampa e registra l'output
    print(process.stdout)
    print(process.stderr)
    # salva risultati nel file
    outFile.write(output_box(title, 40, False, "*"))
    outFile.write(process.stdout.replace("\b", ""))
    outFile.write(process.stderr.replace("\b", ""))


"""
MAIN
Risolve il problema della rimozione degli archi deboli utilizzando l'approccio euristico e PLI (AMPL)
sugli esempi della directory corrente
"""
# Imposta la cartella contenente i file .dat
folder_path = "./"          # Modifica con il percorso reale
output_file = "output_H4000.ter.txt"  # File dove salvare i risultati
# Trova tutti i file .dat nella cartella
dat_files = sorted([f for f in os.listdir(folder_path) if f.endswith(".dat")])

# Percorso dell'eseguibile AMPL
ampl_executable = "C:/Users/francesco/AMPL/ampl"  # Modifica con il percorso corretto

# Controlla se ci siano file .dat
if not dat_files:
    print("Nessun file .dat trovato nella cartella.")
    exit()


with open(output_file, "w") as outFile:

    # Esegui ogni file .dat uno alla volta
    for dat_file in dat_files:
        dat_file = dat_file[:-9]
        outTxt = f"Instance: {dat_file}"

        print(outTxt)
        outFile.write(output_box(outTxt, 60, True, "#"))

        # Caricamento da file
        with open(f"{dat_file}.pkl", "rb") as f:
            DAG, weak_edges, n, l, u, k, M, h, p, seed = pickle.load(f)

        #Heuristic
        solve_dag(DAG, weak_edges, k, 1.0, outFile)
    #    solve_dag(DAG, weak_edges, k, 0.7, outFile)
        solve_dag(DAG, weak_edges, k, 0.5, outFile)
    #    solve_dag(DAG, weak_edges, k, 0.3, outFile)
        solve_dag(DAG, weak_edges, k, 0.1, outFile)

        #AMPL
        runAmpl("LP.run", dat_file , f"Solve method: LP AMPL normal", outFile, ampl_executable)
        runAmpl("LP_opt.run", dat_file , f"Solve method: LP AMPL opt", outFile, ampl_executable)
