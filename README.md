# Strongly Connected Components — Tarjan's Algorithm

[![CI](https://github.com/BernardoFerrazG/componentes_fconexas/actions/workflows/ci.yml/badge.svg)](https://github.com/BernardoFerrazG/componentes_fconexas/actions/workflows/ci.yml)

Finds the **strongly connected components** (*componentes fortemente conexas*) of a directed graph: the maximal groups of vertices in which every vertex can reach every other. It uses a from-scratch, **iterative implementation of Tarjan's algorithm** and draws the graph with one colour per component.

Code and CLI messages are in Portuguese; this README is in English.

## How it works

Tarjan's algorithm finds every component in a single depth-first search:

- Each vertex gets a **discovery index** and a **lowlink**: the smallest index reachable from it through the DFS tree plus at most one back edge to a vertex still on the stack.
- Vertices are pushed onto a stack as they are discovered.
- When a vertex finishes and its `lowlink` equals its own index, it is the **root of a component**. That component is the root plus every vertex above it on the stack.

The DFS uses an explicit stack instead of recursion, so it handles very deep graphs: the test suite runs it on a 20,000-vertex cycle, beyond Python's default recursion limit.

| | |
| --- | --- |
| Time | `O(V + E)` |
| Space | `O(V)` |

## Usage

```bash
pip install -r requirements.txt
python grafo.py                  # uses grafo.txt and opens the plot
python grafo.py --sem-grafico    # text output only
python grafo.py -g outro.txt
```

The input has one directed edge `origin destination` per line (see [`grafo.txt`](grafo.txt)).

Example output:

```
3 componente(s) fortemente conexa(s):
  C1: {F, G, H}
  C2: {A, B, C, D, E}
  C3: {I}
```

## Tests

```bash
pip install pytest
pytest
```

The suite compares the result with `networkx.strongly_connected_components` on the sample graph and on 30 random graphs, and includes the deep-graph check. CI runs it on every push.
