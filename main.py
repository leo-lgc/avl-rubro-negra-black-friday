"""
Protótipo do sistema de logística: registra, localiza e remove IDs de encomendas.

Autor: Leonardo Guimarães Castro
Uso: python3 main.py
"""

from trees import AVLTree, RBTree

MENU = """
[1] Inserir ID          [5] Visualizar árvore
[2] Remover ID          [6] Inserir vários IDs (separados por espaço)
[3] Buscar ID           [7] Estatísticas (altura, rotações)
[4] Percurso em ordem   [0] Sair
"""


def read_int(prompt):
    """Lê um inteiro; devolve None se a entrada for inválida."""
    raw = input(prompt).strip()
    try:
        return int(raw)
    except ValueError:
        print(f"  ✗ '{raw}' não é um número inteiro.")
        return None


def choose_tree():
    while True:
        op = input("Escolha a árvore: [1] AVL  [2] Rubro-Negra > ").strip()
        if op == "1":
            return AVLTree()
        if op == "2":
            return RBTree()
        print("  Opção inválida.")


def show_stats(tree):
    print(f"  Árvore: {tree.name}")
    print(f"  Elementos: {tree.size}")
    print(f"  Altura: {tree.height()}")
    for k, v in tree.stats.items():
        print(f"  {k.capitalize()}: {v}")
    if isinstance(tree, RBTree):
        print(f"  Altura negra: {tree.black_height()}")


def main():
    print("=== Logística Black Friday: índice de encomendas ===")
    tree = choose_tree()
    print(f"Usando árvore {tree.name}.")
    while True:
        print(MENU)
        op = input("> ").strip()
        if op == "0":
            break
        elif op == "1":
            k = read_int("ID a inserir: ")
            if k is not None:
                print("  ✓ inserido." if tree.insert(k) else f"  ✗ ID {k} já existe (duplicata ignorada).")
        elif op == "2":
            k = read_int("ID a remover: ")
            if k is not None:
                print("  ✓ removido." if tree.remove(k) else f"  ✗ ID {k} não encontrado.")
        elif op == "3":
            k = read_int("ID a buscar: ")
            if k is not None:
                print(f"  ✓ ID {k} encontrado." if tree.search(k) else f"  ✗ ID {k} não encontrado.")
        elif op == "4":
            keys = tree.inorder()
            print("  " + (" ".join(map(str, keys)) if keys else "(árvore vazia)"))
        elif op == "5":
            print(tree.render())
        elif op == "6":
            ok = dup = bad = 0
            for tok in input("IDs: ").split():
                try:
                    if tree.insert(int(tok)):
                        ok += 1
                    else:
                        dup += 1
                except ValueError:
                    bad += 1
            print(f"  {ok} inseridos, {dup} duplicatas ignoradas, {bad} entradas inválidas.")
        elif op == "7":
            show_stats(tree)
        else:
            print("  Opção inválida.")


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print()
