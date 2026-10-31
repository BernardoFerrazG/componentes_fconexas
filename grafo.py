"""Componentes fortemente conexas (f-conexas) com o algoritmo de Tarjan.

O grafo dirigido é lido de uma lista de arestas (``origem destino`` por linha).
O algoritmo de Tarjan é implementado do zero, de forma iterativa (sem risco de
estourar o limite de recursão do Python em grafos grandes); o NetworkX é usado
apenas como estrutura do grafo e para o desenho.
"""

from __future__ import annotations

import argparse
from collections.abc import Hashable

import networkx as nx

Vertice = Hashable


def cria_grafo(caminho_grafo: str) -> nx.DiGraph:
    return nx.read_edgelist(caminho_grafo, create_using=nx.DiGraph)


def encontrar_componentes_f_conexas(grafo: nx.DiGraph) -> list[set[Vertice]]:
    """Retorna as componentes fortemente conexas do grafo (algoritmo de Tarjan, O(V + E)).

    Cada vértice recebe um índice de descoberta e um ``lowlink`` — o menor índice
    alcançável a partir dele pela árvore da DFS mais, no máximo, uma aresta de
    retorno. Um vértice com ``lowlink == indice`` é raiz de uma componente, formada
    por ele e pelos vértices acima dele na pilha.
    """
    indice: dict[Vertice, int] = {}
    lowlink: dict[Vertice, int] = {}
    na_pilha: set[Vertice] = set()
    pilha: list[Vertice] = []
    componentes: list[set[Vertice]] = []
    contador = 0

    for raiz in grafo.nodes:
        if raiz in indice:
            continue

        # Cada quadro da DFS guarda o vértice e o iterador dos seus sucessores.
        dfs = [(raiz, iter(grafo.successors(raiz)))]
        indice[raiz] = lowlink[raiz] = contador
        contador += 1
        pilha.append(raiz)
        na_pilha.add(raiz)

        while dfs:
            vertice, sucessores = dfs[-1]
            avancou = False
            for vizinho in sucessores:
                if vizinho not in indice:
                    indice[vizinho] = lowlink[vizinho] = contador
                    contador += 1
                    pilha.append(vizinho)
                    na_pilha.add(vizinho)
                    dfs.append((vizinho, iter(grafo.successors(vizinho))))
                    avancou = True
                    break
                if vizinho in na_pilha:
                    lowlink[vertice] = min(lowlink[vertice], indice[vizinho])
            if avancou:
                continue

            dfs.pop()
            if dfs:
                pai = dfs[-1][0]
                lowlink[pai] = min(lowlink[pai], lowlink[vertice])

            if lowlink[vertice] == indice[vertice]:
                componente = set()
                while True:
                    membro = pilha.pop()
                    na_pilha.discard(membro)
                    componente.add(membro)
                    if membro == vertice:
                        break
                componentes.append(componente)

    return componentes


def desenha_grafo(grafo: nx.DiGraph, componentes: list[set[Vertice]]) -> None:
    import matplotlib.pyplot as plt

    cor_por_vertice = {v: i for i, comp in enumerate(componentes) for v in comp}
    cores = [cor_por_vertice[v] for v in grafo.nodes]

    plt.figure(figsize=(8, 6))
    pos = nx.spring_layout(grafo, seed=42)
    nx.draw(grafo, pos, with_labels=True, node_color=cores, cmap=plt.cm.Set3, node_size=700, arrowsize=18)
    plt.title("Vértices da mesma cor pertencem à mesma componente")
    plt.show()


def main() -> None:
    parser = argparse.ArgumentParser(description="Componentes fortemente conexas (Tarjan).")
    parser.add_argument("-g", "--grafo", default="grafo.txt", help="arquivo com a lista de arestas (padrão: grafo.txt)")
    parser.add_argument("--sem-grafico", action="store_true", help="não abre a janela com o desenho")
    args = parser.parse_args()

    grafo = cria_grafo(args.grafo)
    componentes = encontrar_componentes_f_conexas(grafo)

    print(f"{len(componentes)} componente(s) fortemente conexa(s):")
    for i, componente in enumerate(componentes, start=1):
        print(f"  C{i}: {{{', '.join(sorted(map(str, componente)))}}}")

    if not args.sem_grafico:
        desenha_grafo(grafo, componentes)


if __name__ == "__main__":
    main()
