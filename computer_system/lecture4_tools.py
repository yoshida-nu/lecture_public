from __future__ import annotations
import math
from dataclasses import dataclass
from typing import Dict, Optional, Tuple, List


def entropy(prob_list):
    H = 0
    for p in prob_list:
        if p > 0:
            H += -p * math.log2(p)
    return H

@dataclass
class Node:
    prob: float
    symbol: Optional[str] = None      # 葉なら記号，統合ノードなら None
    left: Optional["Node"] = None     # 0
    right: Optional["Node"] = None    # 1
    rep: str = ""                     # 部分木に含まれる最小アルファベット（タイブレーク用）


def huffman(source: Dict[str, float]) -> Tuple[Dict[str, str], float]:
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
    return codebook, avg_len






