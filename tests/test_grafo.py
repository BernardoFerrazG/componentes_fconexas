from pathlib import Path

import networkx as nx
import pytest

from grafo import cria_grafo, encontrar_componentes_f_conexas

ARQUIVO = Path(__file__).resolve().parent.parent / "grafo.txt"


def como_conjunto(componentes):
    return {frozenset(c) for c in componentes}


def test_grafo_de_exemplo():
    grafo = cria_grafo(ARQUIVO)
    esperado = como_conjunto(nx.strongly_connected_components(grafo))
    assert como_conjunto(encontrar_componentes_f_conexas(grafo)) == esperado


@pytest.mark.parametrize("seed", range(30))
def test_grafos_aleatorios(seed):
    grafo = nx.gnp_random_graph(40, 0.06, seed=seed, directed=True)
    esperado = como_conjunto(nx.strongly_connected_components(grafo))
    assert como_conjunto(encontrar_componentes_f_conexas(grafo)) == esperado


def test_caminho_longo_nao_estoura_recursao():
    grafo = nx.DiGraph(nx.path_graph(20_000, create_using=nx.DiGraph))
    grafo.add_edge(19_999, 0)  # fecha o ciclo: tudo vira uma única componente
    componentes = encontrar_componentes_f_conexas(grafo)
    assert len(componentes) == 1 and len(componentes[0]) == 20_000
