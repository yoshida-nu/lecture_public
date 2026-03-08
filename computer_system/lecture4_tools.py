from __future__ import annotations
import math
import matplotlib.pyplot as plt
from dataclasses import dataclass
from typing import Dict, Optional, Tuple, List

def log_2(x):
    print(math.log2(x))

def ceil_log_2(x):
    print(math.ceil(math.log2(x)))

def self_information1(p):
    if p < 0 or p > 1:
        print("確率は0以上1以下である必要があります。")
        return

    if p == 0:
        print(f"確率: {p} -> 自己情報量: ∞")
        return

    if p == 1:
        I = 0.0
    else:
        I = -math.log2(p)

    print(f"確率: {p} -> 自己情報量: {I}")

def plot_self_information():
    # 確率の値を生成（0は対数が計算できないので避ける）
    p_values = [i / 100 for i in range(1, 101)]

    # 自己情報量を計算
    I_values = [-math.log2(p) for p in p_values]

    # グラフ描画
    plt.figure()
    plt.plot(p_values, I_values)

    plt.xlabel("Probability p")
    plt.ylabel("Self-information I(p)")
    plt.title("Self-information")

    plt.grid(True)
    plt.show()

def entropy(prob_list):
    # 空リストチェック
    if not prob_list:
        raise ValueError("確率リストが空です")

    # 各確率が 0～1 の範囲か確認
    for p in prob_list:
        if p < 0 or p > 1:
            raise ValueError("確率は 0 以上 1 以下でなければなりません")

    # 確率の合計が 1 か確認（数値誤差を考慮）
    if not math.isclose(sum(prob_list), 1.0, rel_tol=1e-9, abs_tol=1e-12):
        raise ValueError("確率の合計が 1 ではありません")

    # エントロピー計算
    H = 0
    for p in prob_list:
        if p > 0:
            H += -p * math.log2(p)

    print(f"確率分布 P: {prob_list}")
    print(f"エントロピー H(P): {H}")
    print()

def plot_binary_entropy():
    # p1 の値（0 と 1 は log が計算できないので避ける）
    p_values = [i / 1000 for i in range(1, 1000)]

    # 2値エントロピー
    H_values = [
        -p * math.log2(p) - (1 - p) * math.log2(1 - p)
        for p in p_values
    ]

    plt.figure()

    # エントロピー曲線
    plt.plot(p_values, H_values, label="Entropy")

    # 最大エントロピー H=1 の線
    plt.axhline(y=1, linestyle="--", label="Max entropy (H(0.5)=1)")

    plt.xlabel("$p_1$")
    plt.ylabel("$H(P)$")

    plt.grid(True)
    plt.legend()

    plt.show()

@dataclass
class Node:
    prob: float
    symbol: Optional[str] = None      # 葉なら記号，統合ノードなら None
    left: Optional["Node"] = None     # 0
    right: Optional["Node"] = None    # 1
    rep: str = ""                     # 部分木に含まれる最小アルファベット（タイブレーク用）


def huffman(source: Dict[str, float]) -> None:
    """
    2元ハフマン符号（授業用・完全決定版）
    ルール：
      - 最小確率の2つを選ぶ
      - 同確率ならアルファベット順（葉でも統合ノードでも rep で比較）
      - 0/1 は（確率，rep）が小さい方を 0，大きい方を 1
    入力：
      source = {symbol: probability}
    出力：
      codebook = {symbol: codeword}, avg_len
    """
    if not source:
        raise ValueError("空の情報源は扱えません．")
    if any(p < 0 for p in source.values()):
        raise ValueError("確率に負の値があります．")
    s = sum(source.values())
    if not math.isclose(s, 1.0, rel_tol=1e-9, abs_tol=1e-12):
        raise ValueError(f"確率の総和が1ではありません（sum={s}）．")

    # 初期ノード（葉）をアルファベット順で作る
    nodes: List[Node] = []
    for sym in sorted(source.keys()):
        nodes.append(Node(prob=float(source[sym]), symbol=sym, rep=sym))

    # 記号が1個だけのとき：慣例的に "0" を付与（空語を避ける）
    if len(nodes) == 1:
        only = nodes[0].symbol
        assert only is not None
        return {only: "0"}, 1.0

    def key(n: Node):
        # ここが授業用の決定規則：確率→代表記号（最小アルファベット）
        return (n.prob, n.rep)

    # ハフマン木の構築
    while len(nodes) > 1:
        nodes.sort(key=key)
        a = nodes.pop(0)
        b = nodes.pop(0)

        # 0/1 の割当も同じ規則で決定（小さい方が 0）
        if key(a) <= key(b):
            left, right = a, b
        else:
            left, right = b, a

        merged = Node(
            prob=a.prob + b.prob,
            symbol=None,
            left=left,
            right=right,
            rep=min(left.rep, right.rep)  # 統合ノードの代表記号
        )
        nodes.append(merged)

    root = nodes[0]

    # 符号語の生成
    codebook: Dict[str, str] = {}

    def dfs(n: Node, prefix: str) -> None:
        if n.symbol is not None:
            codebook[n.symbol] = prefix
            return
        assert n.left is not None and n.right is not None
        dfs(n.left, prefix + "0")
        dfs(n.right, prefix + "1")

    dfs(root, "")

    # 平均符号長
    avg_len = sum(source[sym] * len(codebook[sym]) for sym in source.keys())
    
    print("符号語:", codebook)
    print("平均符号長:", avg_len)






