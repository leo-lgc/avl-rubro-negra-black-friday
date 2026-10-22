"""
Árvores de busca balanceadas: AVL e Rubro-Negra.

Autor: Leonardo Guimarães Castro
Disciplina: IMD0039 - Estruturas de Dados Básicas II

Ambas as classes expõem a mesma interface:
    insert(key) -> bool     True se inseriu, False se a chave já existia
    remove(key) -> bool     True se removeu, False se a chave não existia
    search(key) -> bool     True se a chave existe
    inorder()   -> list     chaves em ordem crescente
    height()    -> int      altura em nós (vazia = 0, só a raiz = 1)
    render()    -> str      desenho da árvore (de lado, raiz à esquerda)
    check()     -> None     levanta AssertionError se alguma propriedade falhar
    stats       -> dict     contadores de rotações (e recolorações na RB)

Nenhuma biblioteca de árvore é usada: todo o balanceamento está aqui.
"""


# ---------------------------------------------------------------------------
# Árvore AVL
# ---------------------------------------------------------------------------

class AVLNode:
    __slots__ = ("key", "left", "right", "h")

    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None
        self.h = 1  # altura do nó (folha = 1)


def _h(node):
    return node.h if node else 0


class AVLTree:
    name = "AVL"

    def __init__(self):
        self.root = None
        self.size = 0
        self.stats = {"rotacoes": 0}

    # --- utilidades -------------------------------------------------------

    def _update(self, n):
        n.h = 1 + max(_h(n.left), _h(n.right))

    def _balance_factor(self, n):
        # fator = altura(esq) - altura(dir); a AVL exige que fique em {-1, 0, 1}
        return _h(n.left) - _h(n.right)

    def _rot_right(self, y):
        #       y            x
        #      / \          / \
        #     x   C  -->   A   y
        #    / \              / \
        #   A   B            B   C
        x = y.left
        y.left = x.right
        x.right = y
        self._update(y)
        self._update(x)
        self.stats["rotacoes"] += 1
        return x

    def _rot_left(self, x):
        y = x.right
        x.right = y.left
        y.left = x
        self._update(x)
        self._update(y)
        self.stats["rotacoes"] += 1
        return y

    def _rebalance(self, n):
        """Recalcula a altura de n e aplica uma das 4 rotações se preciso."""
        self._update(n)
        bf = self._balance_factor(n)
        if bf > 1:                                   # pesado à esquerda
            if self._balance_factor(n.left) < 0:     # caso LR: rotação dupla
                n.left = self._rot_left(n.left)
            return self._rot_right(n)                # caso LL
        if bf < -1:                                  # pesado à direita
            if self._balance_factor(n.right) > 0:    # caso RL: rotação dupla
                n.right = self._rot_right(n.right)
            return self._rot_left(n)                 # caso RR
        return n

    # --- operações --------------------------------------------------------

    def insert(self, key):
        self._inserted = False
        self.root = self._insert(self.root, key)
        if self._inserted:
            self.size += 1
        return self._inserted

    def _insert(self, n, key):
        if n is None:
            self._inserted = True
            return AVLNode(key)
        if key < n.key:
            n.left = self._insert(n.left, key)
        elif key > n.key:
            n.right = self._insert(n.right, key)
        else:
            return n  # duplicata: ignora, árvore não muda
        return self._rebalance(n)

    def remove(self, key):
        self._removed = False
        self.root = self._remove(self.root, key)
        if self._removed:
            self.size -= 1
        return self._removed

    def _remove(self, n, key):
        if n is None:
            return None  # chave não existe
        if key < n.key:
            n.left = self._remove(n.left, key)
        elif key > n.key:
            n.right = self._remove(n.right, key)
        else:
            self._removed = True
            if n.left is None:           # folha ou só filho direito
                return n.right
            if n.right is None:          # só filho esquerdo
                return n.left
            # dois filhos: copia o sucessor (menor da subárvore direita)
            # e remove o sucessor da subárvore direita
            succ = n.right
            while succ.left:
                succ = succ.left
            n.key = succ.key
            n.right = self._remove(n.right, succ.key)
        return self._rebalance(n)

    def search(self, key):
        n = self.root
        while n:
            if key == n.key:
                return True
            n = n.left if key < n.key else n.right
        return False

    def inorder(self):
        out, stack, n = [], [], self.root
        while stack or n:
            while n:
                stack.append(n)
                n = n.left
            n = stack.pop()
            out.append(n.key)
            n = n.right
        return out

    def height(self):
        return _h(self.root)

    def render(self):
        if self.root is None:
            return "(árvore vazia)"
        lines = []

        def walk(n, prefix, is_left):
            if n.right:
                walk(n.right, prefix + ("│   " if is_left else "    "), False)
            label = f"{n.key} [fb={self._balance_factor(n):+d}]"
            lines.append(prefix + ("└── " if is_left else "┌── ") + label)
            if n.left:
                walk(n.left, prefix + ("    " if is_left else "│   "), True)

        if self.root.right:
            walk(self.root.right, "", False)
        lines.append(f"{self.root.key} [fb={self._balance_factor(self.root):+d}]  (raiz)")
        if self.root.left:
            walk(self.root.left, "", True)
        return "\n".join(lines)

    def check(self):
        """Confere ordem de BST, alturas guardadas e fator de balanceamento."""
        def rec(n, lo, hi):
            if n is None:
                return 0
            assert (lo is None or n.key > lo) and (hi is None or n.key < hi), "ordem BST violada"
            hl = rec(n.left, lo, n.key)
            hr = rec(n.right, n.key, hi)
            assert abs(hl - hr) <= 1, f"nó {n.key} desbalanceado (fb={hl - hr})"
            assert n.h == 1 + max(hl, hr), f"altura guardada errada no nó {n.key}"
            return 1 + max(hl, hr)
        rec(self.root, None, None)


# ---------------------------------------------------------------------------
# Árvore Rubro-Negra (segue Cormen et al., cap. 13, com sentinela NIL)
# ---------------------------------------------------------------------------

RED, BLACK = "V", "P"  # vermelho / preto


class RBNode:
    __slots__ = ("key", "color", "left", "right", "parent")

    def __init__(self, key, color, nil):
        self.key = key
        self.color = color
        self.left = nil
        self.right = nil
        self.parent = nil


class RBTree:
    name = "Rubro-Negra"

    def __init__(self):
        # sentinela única: representa todas as folhas NIL (sempre pretas)
        self.NIL = RBNode(None, BLACK, None)
        self.NIL.left = self.NIL.right = self.NIL.parent = self.NIL
        self.root = self.NIL
        self.size = 0
        self.stats = {"rotacoes": 0, "recoloracoes": 0}

    # --- utilidades -------------------------------------------------------

    def _paint(self, n, color):
        # só conta como recoloração quando a cor muda de fato
        if n is not self.NIL and n.color != color:
            n.color = color
            self.stats["recoloracoes"] += 1

    def _rot_left(self, x):
        y = x.right
        x.right = y.left
        if y.left is not self.NIL:
            y.left.parent = x
        y.parent = x.parent
        if x.parent is self.NIL:
            self.root = y
        elif x is x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y
        y.left = x
        x.parent = y
        self.stats["rotacoes"] += 1

    def _rot_right(self, x):
        y = x.left
        x.left = y.right
        if y.right is not self.NIL:
            y.right.parent = x
        y.parent = x.parent
        if x.parent is self.NIL:
            self.root = y
        elif x is x.parent.right:
            x.parent.right = y
        else:
            x.parent.left = y
        y.right = x
        x.parent = y
        self.stats["rotacoes"] += 1

    def _find(self, key):
        n = self.root
        while n is not self.NIL:
            if key == n.key:
                return n
            n = n.left if key < n.key else n.right
        return None

    # --- inserção ---------------------------------------------------------

    def insert(self, key):
        parent, cur = self.NIL, self.root
        while cur is not self.NIL:
            parent = cur
            if key == cur.key:
                return False  # duplicata: ignora
            cur = cur.left if key < cur.key else cur.right
        z = RBNode(key, RED, self.NIL)  # nó novo sempre entra vermelho
        z.parent = parent
        if parent is self.NIL:
            self.root = z
        elif key < parent.key:
            parent.left = z
        else:
            parent.right = z
        self.size += 1
        self._insert_fixup(z)
        return True

    def _insert_fixup(self, z):
        # enquanto houver vermelho-vermelho (z e o pai)
        while z.parent.color == RED:
            gp = z.parent.parent
            if z.parent is gp.left:
                uncle = gp.right
                if uncle.color == RED:
                    # caso 1: tio vermelho -> só recolore e sobe
                    self._paint(z.parent, BLACK)
                    self._paint(uncle, BLACK)
                    self._paint(gp, RED)
                    z = gp
                else:
                    if z is z.parent.right:
                        # caso 2: z é filho "de dentro" -> rotação vira caso 3
                        z = z.parent
                        self._rot_left(z)
                    # caso 3: recolore e gira o avô
                    self._paint(z.parent, BLACK)
                    self._paint(z.parent.parent, RED)
                    self._rot_right(z.parent.parent)
            else:  # espelho
                uncle = gp.left
                if uncle.color == RED:
                    self._paint(z.parent, BLACK)
                    self._paint(uncle, BLACK)
                    self._paint(gp, RED)
                    z = gp
                else:
                    if z is z.parent.left:
                        z = z.parent
                        self._rot_right(z)
                    self._paint(z.parent, BLACK)
                    self._paint(z.parent.parent, RED)
                    self._rot_left(z.parent.parent)
        self._paint(self.root, BLACK)  # propriedade 2: raiz preta

    # --- remoção ----------------------------------------------------------

    def _transplant(self, u, v):
        if u.parent is self.NIL:
            self.root = v
        elif u is u.parent.left:
            u.parent.left = v
        else:
            u.parent.right = v
        v.parent = u.parent

    def remove(self, key):
        z = self._find(key)
        if z is None:
            return False  # chave não existe
        y = z
        y_color = y.color
        if z.left is self.NIL:                 # folha ou só filho direito
            x = z.right
            self._transplant(z, z.right)
        elif z.right is self.NIL:              # só filho esquerdo
            x = z.left
            self._transplant(z, z.left)
        else:                                  # dois filhos: usa o sucessor
            y = z.right
            while y.left is not self.NIL:
                y = y.left
            y_color = y.color
            x = y.right
            if y.parent is z:
                x.parent = y
            else:
                self._transplant(y, y.right)
                y.right = z.right
                y.right.parent = y
            self._transplant(z, y)
            y.left = z.left
            y.left.parent = y
            y.color = z.color  # sucessor herda a cor (não é recoloração de ajuste)
        self.size -= 1
        if y_color == BLACK:
            # saiu um nó preto: algum caminho ficou com um preto a menos
            self._remove_fixup(x)
        self.NIL.parent = self.NIL
        return True

    def _remove_fixup(self, x):
        while x is not self.root and x.color == BLACK:
            if x is x.parent.left:
                w = x.parent.right  # irmão
                if w.color == RED:
                    # caso 1: irmão vermelho -> vira caso 2, 3 ou 4
                    self._paint(w, BLACK)
                    self._paint(x.parent, RED)
                    self._rot_left(x.parent)
                    w = x.parent.right
                if w.left.color == BLACK and w.right.color == BLACK:
                    # caso 2: irmão preto com filhos pretos -> recolore e sobe
                    self._paint(w, RED)
                    x = x.parent
                else:
                    if w.right.color == BLACK:
                        # caso 3: sobrinho de dentro vermelho -> vira caso 4
                        self._paint(w.left, BLACK)
                        self._paint(w, RED)
                        self._rot_right(w)
                        w = x.parent.right
                    # caso 4: sobrinho de fora vermelho -> resolve
                    self._paint(w, x.parent.color)
                    self._paint(x.parent, BLACK)
                    self._paint(w.right, BLACK)
                    self._rot_left(x.parent)
                    x = self.root
            else:  # espelho
                w = x.parent.left
                if w.color == RED:
                    self._paint(w, BLACK)
                    self._paint(x.parent, RED)
                    self._rot_right(x.parent)
                    w = x.parent.left
                if w.right.color == BLACK and w.left.color == BLACK:
                    self._paint(w, RED)
                    x = x.parent
                else:
                    if w.left.color == BLACK:
                        self._paint(w.right, BLACK)
                        self._paint(w, RED)
                        self._rot_left(w)
                        w = x.parent.left
                    self._paint(w, x.parent.color)
                    self._paint(x.parent, BLACK)
                    self._paint(w.left, BLACK)
                    self._rot_right(x.parent)
                    x = self.root
        self._paint(x, BLACK)

    # --- consultas --------------------------------------------------------

    def search(self, key):
        return self._find(key) is not None

    def inorder(self):
        out, stack, n = [], [], self.root
        while stack or n is not self.NIL:
            while n is not self.NIL:
                stack.append(n)
                n = n.left
            n = stack.pop()
            out.append(n.key)
            n = n.right
        return out

    def height(self):
        def rec(n):
            return 0 if n is self.NIL else 1 + max(rec(n.left), rec(n.right))
        return rec(self.root)

    def black_height(self):
        h, n = 0, self.root
        while n is not self.NIL:
            if n.color == BLACK:
                h += 1
            n = n.left
        return h

    def render(self, color=True):
        if self.root is self.NIL:
            return "(árvore vazia)"
        red = "\033[91m" if color else ""
        reset = "\033[0m" if color else ""

        def label(n):
            if n.color == RED:
                return f"{red}{n.key}(V){reset}"
            return f"{n.key}(P)"

        lines = []

        def walk(n, prefix, is_left):
            if n.right is not self.NIL:
                walk(n.right, prefix + ("│   " if is_left else "    "), False)
            lines.append(prefix + ("└── " if is_left else "┌── ") + label(n))
            if n.left is not self.NIL:
                walk(n.left, prefix + ("    " if is_left else "│   "), True)

        if self.root.right is not self.NIL:
            walk(self.root.right, "", False)
        lines.append(label(self.root) + "  (raiz)")
        if self.root.left is not self.NIL:
            walk(self.root.left, "", True)
        return "\n".join(lines)

    def check(self):
        """Confere ordem de BST e as 5 propriedades da Rubro-Negra."""
        assert self.NIL.color == BLACK, "NIL deve ser preto"
        assert self.root.color == BLACK, "raiz deve ser preta"

        def rec(n, lo, hi):
            if n is self.NIL:
                return 1  # folhas NIL contam como preto
            assert n.color in (RED, BLACK)
            assert (lo is None or n.key > lo) and (hi is None or n.key < hi), "ordem BST violada"
            if n.color == RED:
                assert n.left.color == BLACK and n.right.color == BLACK, \
                    f"nó vermelho {n.key} com filho vermelho"
            bl = rec(n.left, lo, n.key)
            br = rec(n.right, n.key, hi)
            assert bl == br, f"altura negra diferente abaixo de {n.key}"
            return bl + (1 if n.color == BLACK else 0)
        rec(self.root, None, None)


TREES = {"1": AVLTree, "2": RBTree}
