"""
Experimento comparativo: aplica os mesmos dados e as mesmas operações às duas
árvores e mede altura, rotações e recolorações.

Uso: python3 benchmark.py [N]   (padrão N = 10000)
"""

import random
import sys
import time

from trees import AVLTree, RBTree


def run(tree_cls, data, removals, lookups):
    t = tree_cls()
    t0 = time.perf_counter()
    for k in data:
        t.insert(k)
    t_ins = time.perf_counter() - t0
    t.check()
    h_ins = t.height()
    rot_ins = t.stats["rotacoes"]
    rec_ins = t.stats.get("recoloracoes", 0)

    t0 = time.perf_counter()
    for k in lookups:
        t.search(k)
    t_busca = time.perf_counter() - t0

    t0 = time.perf_counter()
    for k in removals:
        t.remove(k)
    t_rem = time.perf_counter() - t0
    t.check()
    return {
        "h_ins": h_ins, "rot_ins": rot_ins, "rec_ins": rec_ins,
        "h_rem": t.height(), "rot_tot": t.stats["rotacoes"],
        "rec_tot": t.stats.get("recoloracoes", 0),
        "t_ins": t_ins, "t_busca": t_busca, "t_rem": t_rem,
    }


def main():
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 10000
    rnd = random.Random(42)
    shuffled = list(range(1, n + 1))
    rnd.shuffle(shuffled)
    sets = {
        "crescente": list(range(1, n + 1)),
        "decrescente": list(range(n, 0, -1)),
        "aleatoria": shuffled,
    }
    lookups = [rnd.randint(1, 2 * n) for _ in range(n)]  # ~50% inexistentes
    print(f"N = {n}; remoção de metade das chaves (uma sim, uma não, na ordem de inserção)\n")
    hdr = f"{'ordem':<12}{'arvore':<13}{'h_ins':>6}{'rot_ins':>9}{'recol_ins':>10}" \
          f"{'h_rem':>6}{'rot_tot':>9}{'recol_tot':>10}{'ins(ms)':>9}{'busca(ms)':>10}{'rem(ms)':>9}"
    print(hdr)
    print("-" * len(hdr))
    for name, data in sets.items():
        removals = data[::2]
        for cls in (AVLTree, RBTree):
            r = run(cls, data, removals, lookups)
            print(f"{name:<12}{cls.name:<13}{r['h_ins']:>6}{r['rot_ins']:>9}{r['rec_ins']:>10}"
                  f"{r['h_rem']:>6}{r['rot_tot']:>9}{r['rec_tot']:>10}"
                  f"{r['t_ins']*1000:>9.1f}{r['t_busca']*1000:>10.1f}{r['t_rem']*1000:>9.1f}")


if __name__ == "__main__":
    main()
