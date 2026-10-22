"""
Testes de funcionamento e de propriedades das duas árvores.
Os mesmos dados e as mesmas operações são aplicados à AVL e à Rubro-Negra.

Uso: python3 -m unittest -v test_trees.py
"""

import random
import unittest

from trees import AVLTree, RBTree

N = 1000


def datasets():
    rnd = random.Random(42)
    shuffled = list(range(1, N + 1))
    rnd.shuffle(shuffled)
    return {
        "crescente": list(range(1, N + 1)),
        "decrescente": list(range(N, 0, -1)),
        "nao_ordenada": shuffled,
    }


class TreeContract:
    """Testes comuns; cada subclasse define make()."""

    def make(self):
        raise NotImplementedError

    # árvore vazia
    def test_empty_tree(self):
        t = self.make()
        self.assertFalse(t.search(1))
        self.assertFalse(t.remove(1))
        self.assertEqual(t.inorder(), [])
        self.assertEqual(t.height(), 0)
        self.assertEqual(t.render(), "(árvore vazia)")
        t.check()

    # um elemento
    def test_single_element(self):
        t = self.make()
        self.assertTrue(t.insert(7))
        self.assertTrue(t.search(7))
        self.assertEqual(t.height(), 1)
        t.check()
        self.assertTrue(t.remove(7))
        self.assertEqual(t.inorder(), [])
        t.check()

    def test_duplicate_rejected(self):
        t = self.make()
        self.assertTrue(t.insert(5))
        self.assertFalse(t.insert(5))
        self.assertEqual(t.inorder(), [5])
        self.assertEqual(t.size, 1)

    def test_insert_orders_keep_balance(self):
        for name, data in datasets().items():
            with self.subTest(ordem=name):
                t = self.make()
                for k in data:
                    t.insert(k)
                    t.check()
                self.assertEqual(t.inorder(), sorted(data))

    def test_search_existing_and_missing(self):
        t = self.make()
        for k in datasets()["nao_ordenada"]:
            t.insert(k)
        for k in (1, N // 2, N):
            self.assertTrue(t.search(k))
        for k in (0, -5, N + 1, 10 ** 9):
            self.assertFalse(t.search(k))

    def test_remove_leaf_one_child_two_children(self):
        t = self.make()
        for k in (50, 30, 70, 20, 40, 60, 80, 10):
            t.insert(k)
        # 10 é folha; 20 tem só um filho (10); 50 tem dois filhos
        for k in (10, 20, 50):
            with self.subTest(remover=k):
                self.assertTrue(t.remove(k))
                self.assertFalse(t.search(k))
                t.check()
        self.assertEqual(t.inorder(), [30, 40, 60, 70, 80])

    def test_remove_missing(self):
        t = self.make()
        for k in (1, 2, 3):
            t.insert(k)
        before = t.inorder()
        self.assertFalse(t.remove(99))
        self.assertEqual(t.inorder(), before)
        t.check()

    def test_remove_keeps_balance(self):
        for name, data in datasets().items():
            with self.subTest(ordem=name):
                t = self.make()
                for k in data:
                    t.insert(k)
                rnd = random.Random(7)
                to_remove = data[:]
                rnd.shuffle(to_remove)
                for i, k in enumerate(to_remove):
                    self.assertTrue(t.remove(k))
                    if i % 25 == 0:
                        t.check()
                self.assertEqual(t.inorder(), [])
                t.check()

    def test_random_mixed_operations(self):
        rnd = random.Random(123)
        t, ref = self.make(), set()
        for _ in range(5000):
            k = rnd.randint(0, 300)
            if rnd.random() < 0.6:
                self.assertEqual(t.insert(k), k not in ref)
                ref.add(k)
            else:
                self.assertEqual(t.remove(k), k in ref)
                ref.discard(k)
        t.check()
        self.assertEqual(t.inorder(), sorted(ref))


class TestAVL(TreeContract, unittest.TestCase):
    def make(self):
        return AVLTree()

    def test_rotation_example(self):
        # 10, 20, 30 em linha -> uma rotação à esquerda, 20 vira raiz
        t = self.make()
        for k in (10, 20, 30):
            t.insert(k)
        self.assertEqual(t.root.key, 20)
        self.assertEqual(t.stats["rotacoes"], 1)


class TestRB(TreeContract, unittest.TestCase):
    def make(self):
        return RBTree()

    def test_colors_visible(self):
        t = self.make()
        for k in (10, 20, 30, 15):
            t.insert(k)
        out = t.render(color=False)
        self.assertIn("20(P)", out)
        self.assertIn("15(V)", out)


if __name__ == "__main__":
    unittest.main()
