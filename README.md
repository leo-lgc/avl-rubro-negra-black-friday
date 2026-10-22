# AVL vs Rubro-Negra: índice de encomendas da Black Friday

Oi, professora! Este é o meu projeto para IMD0039 (Estruturas de Dados Básicas II).

A ideia é um sistema de logística em plena Black Friday precisa registrar, localizar e
remover IDs de encomendas o tempo todo. Como esses IDs costumam chegar em ordem, uma
árvore de busca comum viraria uma lista enorme. Então implementei as duas árvores
balanceadas da disciplina, **AVL** e **Rubro-Negra**, e o programa deixa escolher qual
usar logo ao abrir. Todo o balanceamento (rotações e recolorações) foi escrito à mão,
sem biblioteca de árvore.

### Sobre o visual dos slides

Os slides usam o template visual da **Tess**, a empresa onde eu trabalho: cores, fonte e
logo vêm do manual de marca de lá. Usei porque já tinha o material pronto e a senhora flaou
que poderia utilizar e que seria legal, então acabei adotando.

## O que precisa para rodar

- Python 3.8

## Como executar

```bash
python3 main.py                        # o programa com menu
python3 -m unittest -v test_trees.py   # os testes
python3 benchmark.py                   # a comparação AVL x RB com 10.000 IDs
python3 benchmark.py 100000            # o mesmo experimento com outro tamanho
```

No Windows, troque `python3` por `python`.

## O que tem em cada arquivo

| Arquivo | Conteúdo |
|---|---|
| `trees.py` | as duas árvores (`AVLTree` e `RBTree`), com a mesma interface |
| `main.py` | o menu interativo |
| `test_trees.py` | os testes, que são os mesmos para as duas árvores |
| `benchmark.py` | o experimento que compara altura, rotações, recolorações e tempo |
| `apresentacao/` | os slides (HTML e PDF) |

## O que o programa faz

Quando abre, ele pergunta qual árvore usar. Depois aparece o menu:

1. Inserir um ID
2. Remover um ID
3. Buscar um ID
4. Percurso em ordem (mostra os IDs do menor para o maior)
5. Ver a árvore. Na AVL aparece o fator de balanceamento de cada nó; na Rubro-Negra
   aparece a cor, `(P)` para preto e `(V)` para vermelho (no terminal o vermelho
   aparece colorido mesmo)
6. Inserir vários IDs de uma vez
7. Estatísticas: tamanho, altura e rotações (na RB também recolorações e altura negra)

## Um exemplo rápido

```
Escolha a árvore: [1] AVL  [2] Rubro-Negra > 2
> 6
IDs: 10 20 30 15 25 5
  6 inseridos, 0 duplicatas ignoradas, 0 entradas inválidas.
> 1
ID a inserir: 20
  ✗ ID 20 já existe (duplicata ignorada).
> 3
ID a buscar: 99
  ✗ ID 99 não encontrado.
> 5
┌── 30(P)
│   └── 25(V)
20(P)  (raiz)
│   ┌── 15(V)
└── 10(P)
    └── 5(V)
```

A árvore aparece deitada: a raiz fica à esquerda, os filhos da direita ficam em cima e
os da esquerda embaixo.

## Decisões que tomei

- **ID repetido:** o programa recusa e avisa. ID de encomenda é único, então um
  repetido só pode ser erro de digitação.
- **Buscar ou remover um ID que não existe:** aparece "não encontrado" e a árvore fica
  como estava.
- **Árvore vazia:** tudo funciona normalmente, e a visualização mostra `(árvore vazia)`.
- **Remover um nó com dois filhos:** ele é trocado pelo sucessor em ordem (o menor da
  subárvore da direita). Fiz igual nas duas árvores para a comparação ser justa.
- **Digitar algo que não é número:** aparece um erro e o programa continua rodando.
- **Como contei as rotações:** uma rotação dupla (LR/RL na AVL) conta como duas. Na RB,
  só conto recoloração quando a cor do nó muda de verdade.
- **Rubro-Negra:** segui o Cormen (CLRS, cap. 13), usando um nó sentinela `NIL` preto
  no lugar de todas as folhas.

## Como as árvores funcionam

**AVL.** Cada nó guarda a própria altura. Depois de inserir ou remover, o programa
volta pelo caminho até a raiz conferindo o fator de balanceamento (altura da esquerda
menos altura da direita). Se algum sair de {-1, 0, 1}, entra uma das quatro correções:
LL (rotação à direita), RR (rotação à esquerda), LR ou RL (rotações duplas).

**Rubro-Negra.** Cada nó é vermelho ou preto, e as regras são: a raiz é preta, as
folhas NIL são pretas, nó vermelho não tem filho vermelho e todo caminho até as folhas
passa pelo mesmo número de pretos. O nó novo sempre entra vermelho. Se o pai também for
vermelho, o que resolve é olhar o tio: se o tio for vermelho, basta recolorir; se for
preto, entram uma ou duas rotações. Na remoção, quando sai um nó preto, a correção olha
o irmão (são 4 casos).

A função `check()` confere todas essas regras. Os testes e o benchmark chamam ela
depois das operações, então se alguma propriedade quebrasse eu ia ver na hora.

## Resultados (10.000 IDs, `python3 benchmark.py`)

Usei os mesmos IDs e a mesma sequência de operações nas duas árvores. Depois de
inserir tudo, removi metade das chaves.

| Ordem | Árvore | Altura após inserir | Rotações ao inserir | Recolorações ao inserir | Altura após remover | Rotações no total |
|---|---|---|---|---|---|---|
| Crescente | AVL | 14 | 9.986 | — | 13 | 9.991 |
| Crescente | RB | 24 | 9.976 | 49.877 | 13 | 9.987 |
| Decrescente | AVL | 14 | 9.986 | — | 13 | 9.991 |
| Decrescente | RB | 24 | 9.976 | 49.877 | 13 | 9.987 |
| Aleatória | AVL | 16 | 6.946 | — | 15 | 8.938 |
| Aleatória | RB | 16 | 5.806 | 23.230 | 15 | 7.806 |

Os tempos em milissegundos mudam de computador para computador, por isso deixei só na
saída do `benchmark.py`.
