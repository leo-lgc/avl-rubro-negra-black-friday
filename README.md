# AVL vs Rubro-Negra: índice de encomendas da Black Friday

Protótipo para IMD0039 (Estruturas de Dados Básicas II). Um sistema de logística
registra, localiza e remove IDs de encomendas usando uma árvore de busca balanceada,
escolhida na hora da execução: **AVL** ou **Rubro-Negra**. Todo o balanceamento
(rotações e recolorações) foi implementado à mão, sem bibliotecas de árvore.

**Autor:** Leonardo Guimarães Castro

## Requisitos

- Python 3.8 ou mais recente. Nenhuma dependência externa.
- Python é interpretado: não há versão compilada. Os arquivos `.py` são o programa
  pronto para rodar.

## Como executar

```bash
python3 main.py                        # programa interativo
python3 -m unittest -v test_trees.py   # testes
python3 benchmark.py                   # comparação AVL x RB com N = 10000
python3 benchmark.py 100000            # mesmo experimento com outro N
```

No Windows, use `python` no lugar de `python3`.

## Arquivos

| Arquivo | Conteúdo |
|---|---|
| `trees.py` | `AVLTree` e `RBTree`, com a mesma interface |
| `main.py` | menu interativo |
| `test_trees.py` | testes de funcionamento e de propriedades (os mesmos para as duas árvores) |
| `benchmark.py` | experimento comparativo: altura, rotações, recolorações e tempo |
| `apresentacao/` | slides da apresentação (HTML e PDF) |

## Funcionalidades

Ao iniciar, o usuário escolhe a árvore. O menu oferece:

1. Inserir ID
2. Remover ID
3. Buscar ID
4. Percurso em ordem (IDs em ordem crescente)
5. Visualizar a árvore (na AVL, com o fator de balanceamento de cada nó; na
   Rubro-Negra, com a cor: `(P)` preto, `(V)` vermelho, também em vermelho no terminal)
6. Inserir vários IDs de uma vez
7. Estatísticas: tamanho, altura, rotações (e recolorações e altura negra na RB)

## Exemplo de uso

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

A árvore é desenhada de lado: a raiz fica à esquerda, os filhos da direita aparecem
acima e os da esquerda abaixo.

## Decisões de projeto

- **IDs repetidos:** a inserção é recusada com aviso e a árvore não muda. O ID de
  uma encomenda é único, então um repetido indica erro de entrada.
- **Busca ou remoção de ID inexistente:** o sistema informa "não encontrado" e a
  árvore não muda.
- **Árvore vazia:** todas as operações funcionam; a visualização mostra `(árvore vazia)`.
- **Remoção de nó com dois filhos:** o nó é substituído pelo sucessor em ordem
  (o menor da subárvore direita), nas duas árvores.
- **Entrada que não é inteiro:** mensagem de erro, e o programa continua.
- **Contagem de rotações:** uma rotação dupla (casos LR/RL da AVL, caso 2 da RB)
  conta como duas rotações simples. Na RB, só conta como recoloração quando a cor
  de um nó muda de fato.
- **Rubro-Negra:** segue o CLRS (cap. 13), com um nó sentinela `NIL` preto
  representando todas as folhas.

## Como funciona

**AVL.** Cada nó guarda sua altura. Depois de inserir ou remover, o caminho até a
raiz é refeito, e cada nó tem o fator de balanceamento (altura esquerda menos altura
direita) verificado. Se ele sair de {-1, 0, 1}, aplica-se uma de quatro correções:
LL (rotação à direita), RR (rotação à esquerda), LR e RL (rotações duplas).

**Rubro-Negra.** Cada nó é vermelho ou preto. As regras são: a raiz é preta, as
folhas NIL são pretas, um nó vermelho não tem filho vermelho, e todo caminho de um
nó até as folhas tem o mesmo número de pretos. O nó novo entra vermelho. Se o pai
também for vermelho, a correção depende da cor do tio: tio vermelho resolve com
recoloração, e tio preto resolve com uma ou duas rotações. Na remoção, quando sai
um nó preto, a correção olha o irmão (4 casos).

`check()` confere todas essas propriedades e é chamado pelos testes e pelo benchmark
depois das operações.

## Resultados (N = 10.000, `python3 benchmark.py`)

Mesmos IDs e mesma sequência nas duas árvores; depois de inserir tudo, metade das
chaves é removida.

| Ordem | Árvore | Altura após inserir | Rotações ao inserir | Recolorações ao inserir | Altura após remover | Rotações no total |
|---|---|---|---|---|---|---|
| Crescente | AVL | 14 | 9.986 | — | 13 | 9.991 |
| Crescente | RB | 24 | 9.976 | 49.877 | 13 | 9.987 |
| Decrescente | AVL | 14 | 9.986 | — | 13 | 9.991 |
| Decrescente | RB | 24 | 9.976 | 49.877 | 13 | 9.987 |
| Aleatória | AVL | 16 | 6.946 | — | 15 | 8.938 |
| Aleatória | RB | 16 | 5.806 | 23.230 | 15 | 7.806 |

Os tempos em milissegundos variam de máquina para máquina e aparecem na saída do
`benchmark.py`.
