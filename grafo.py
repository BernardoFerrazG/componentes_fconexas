import networkx as nx
import matplotlib.pyplot as plt

def cria_grafo(caminho_grafo):

    grafo = nx.read_edgelist(caminho_grafo, create_using=nx.DiGraph)
    return grafo


def encontrar_componentes_f_conexas(grafo):
    
    return list(nx.strongly_connected_components(grafo))


def desenha_grafo(grafo):

    plt.figure(figsize=(8,6))
    pos = nx.spring_layout(grafo)
    nx.draw(grafo, pos, with_labels=True)
    plt.show()

def main():
    
    arquivo_grafo = "grafo.txt"

    grafo = cria_grafo(arquivo_grafo)

    componentes_f_conexas = encontrar_componentes_f_conexas(grafo)
    
    
    print("Componentes fortemente conectadas:")
    for componente in componentes_f_conexas:
        print(f"componente: {componente}")


    desenha_grafo(grafo)

if __name__ == "__main__":
    main()
