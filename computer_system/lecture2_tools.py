# lecture2_tools.py
# 第2回「数の表現（整数・負の数・小数）」 配布用ツール集（IDLE向け）
#
# ─────────────────────────────────────────────
# 受講生向け：最短の使い方（重要）
#
# 1) この lecture2_tools.py をダウンロードして保存
# 2) IDLE → File → New File で新規ファイルを作る
# 3) その新規ファイルを lecture2_tools.py と「同じフォルダ」に保存（例：practice.py）
# 4) practice.py に以下を書いて F5（Run Module）
#
#   from lecture2_tools import (
#       show_signed_nbit_repr, show_bits_to_signed_int,
#       show_ieee754, show_sum_demo
#   )
#
#   show_signed_nbit_repr(-5, 8)                  # 整数→nビット（範囲内）
#   show_signed_nbit_repr(130, 8, overflow=True)  # 整数→nビット（桁あふれ）
#   show_bits_to_signed_int("11111011")           # ビット列→整数（2の補数）
#
#   show_ieee754(0.1, 64, frac_head=24)           # 倍精度の符号・指数・仮数
#   show_ieee754(0.1, 32, frac_head=24)           # 単精度に丸めた結果（重要）
#   show_sum_demo()                               # 0.1 + 0.2 デモ
#
# よくあるエラー：
# ・ModuleNotFoundError：このファイルと practice.py が同じフォルダにありません．
# ─────────────────────────────────────────────

from __future__ import annotations

from fractions import Fraction
import struct
from typing import Tuple, Dict, Any, Optional

# ============================================================
# 1) nビット符号付き整数（2の補数）
# ============================================================
def signed_nbit_repr(x: int, n: int, *, overflow: bool = False) -> str:
    """
    整数 x を nビット符号付き整数（2の補数）として表したビット列を返す．

    overflow=False：
      範囲外なら ValueError（「表せない」を明確にしたいとき向け）
      表現可能範囲：-2^(n-1) ～ 2^(n-1)-1

    overflow=True：
      mod 2^n による桁あふれ（循環）を許す（実機の整数型っぽい挙動）
    """
    if not isinstance(x, int) or not isinstance(n, int):
        raise TypeError("x and n must be integers")
    if n <= 0:
        raise ValueError("n must be positive")

    mod = 1 << n

    if overflow:
        u = x % mod
    else:
        minv = -(1 << (n - 1))
        maxv = (1 << (n - 1)) - 1
        if x < minv or x > maxv:
            raise ValueError(f"x out of range for {n}-bit signed integer: [{minv}, {maxv}]")
        # 2の補数：負なら 2^n を足して nビットに収める
        u = x if x >= 0 else mod + x # この条件下では u = x % mod と同じ意味

    return format(u, f"0{n}b")

def show_signed_nbit_repr(x: int, n: int, *, overflow: bool = False) -> None:
    """
    signed_nbit_repr の結果を表示する（printまで含む）．
    """
    minv = -(1 << (n - 1))
    maxv = (1 << (n - 1)) - 1
    bits = signed_nbit_repr(x, n, overflow=overflow)
    if (x < minv or x > maxv) and overflow:
        tag = " ！誤差発生"
    else:
        tag = ""
    print(f"n={n}, x={x:>4} -> {bits}{tag}")

# ============================================================
# 1-b) ビット列 → 符号付き整数（2の補数）【逆変換】
# ============================================================

def bits_to_signed_int(bits: str) -> int:
    """
    '0'/'1' からなるビット列 bits を，2の補数の符号付き整数として解釈して返す．
    例：
      "00000101" ->  5
      "11111011" -> -5
      "10000000" -> -128（8ビットの場合）
    """
    if not isinstance(bits, str):
        raise TypeError("bits must be a string")
    if len(bits) == 0:
        raise ValueError("bits must be non-empty")
    if any(c not in "01" for c in bits):
        raise ValueError("bits must contain only '0' and '1'")

    n = len(bits)
    u = int(bits, 2)
    sign_bit = 1 << (n - 1)

    # 符号ビットが 0 ならそのまま，1 なら u - 2^n
    return u if (u & sign_bit) == 0 else u - (1 << n)


def show_bits_to_signed_int(bits: str) -> None:
    """
    bits_to_signed_int の結果を表示する（printまで含む）．
    """
    x = bits_to_signed_int(bits)
    print(f"{bits} -> {x}")

# ============================================================
# 2) IEEE 754（単精度／倍精度）ビット取り出し
# ============================================================

def ieee754_bits(x: float, precision: int = 64) -> Tuple[str, str, str]:
    """
    IEEE 754 のビット表現を (sign, exponent, fraction) で返す．

    precision=64：倍精度（1/11/52）
    precision=32：単精度（1/8/23）
      ※ここで binary32 への「丸め」が起きる（重要）
    """
    if precision == 64:
        u = struct.unpack(">Q", struct.pack(">d", x))[0]
        b = format(u, "064b")
        return b[0], b[1:12], b[12:]
    elif precision == 32:
        u = struct.unpack(">I", struct.pack(">f", float(x)))[0]
        b = format(u, "032b")
        return b[0], b[1:9], b[9:]
    else:
        raise ValueError("precision must be 64 or 32")


def show_ieee754(x: float, precision: int = 64, *, frac_head: Optional[int] = None) -> None:
    """
    IEEE 754 表現を表示する（printまで含む）．

    frac_head：
      仮数部を先頭何ビット表示するか．
      None を指定すると仮数部を全部表示（52bit/23bit）．
    """
    s, e, f = ieee754_bits(x, precision)

    if frac_head is None:
        f_disp = f
    else:
        f_disp = f[:frac_head] + ("..." if frac_head < len(f) else "")

    print(f"精度  : {precision}ビット")
    print(f"符号  : {s}")
    print(f"指数部: {e}")
    print(f"仮数部: {f_disp}")
    print()

# ============================================================
# 3) 0.1 + 0.2 デモ（Fractionで「内部の値」を見る）
# ============================================================

def stored_fraction(x: float) -> Fraction:
    """
    float x が内部に保持している値を Fraction で正確に返す．
    例：0.1 は「1/10」ではなく，ある分数として保持されている．
    """
    return Fraction.from_float(x)


def demo_data(a: float = 0.1, b: float = 0.2) -> Dict[str, Any]:
    """
    デモに必要な情報を辞書で返す（printしない）．
    """
    fa = stored_fraction(a)
    fb = stored_fraction(b)
    exact_sum = fa + fb
    rounded = float(exact_sum)

    return {
        "a": a,
        "b": b,
        "stored_a": fa,
        "stored_b": fb,
        "exact_sum_of_stored": exact_sum,
        "rounded_float": rounded,
        "bits_0_3": ieee754_bits(0.3, 64),
        "bits_a_plus_b": ieee754_bits(a + b, 64),
        "bits_rounded_float": ieee754_bits(rounded, 64),
    }


def show_sum_demo(a: float = 0.1, b: float = 0.2, *, frac_head: int = 53) -> None:
    """
    0.1 + 0.2 問題の可視化（printまで含む）．
    frac_head：仮数部を先頭何ビット表示するか
    """
    d = demo_data(a, b)

    print(f"(1) {a}の分数表現: {d['stored_a']}")
    print(f"(2) {b}の分数表現: {d['stored_b']}")
    print()

    print(f"(1) + (2): {d['exact_sum_of_stored']}")
    print()

    print(f"(1) + (2) の小数表現: {d['rounded_float']}")
    print()

    def _show_bits(title: str, parts: Tuple[str, str, str]) -> None:
        s, e, f = parts
        f_disp = f[:frac_head] + ("..." if frac_head < len(f) else "")
        print(title)
        print(" 符号:", s, " 指数部:", e, " 仮数部:", f_disp)
        print()

    _show_bits(f"{a+b:g} のIEEE754（倍精度）表現:", d["bits_0_3"])
    _show_bits(f"{a} + {b} のIEEE754（倍精度）表現:", d["bits_a_plus_b"])

# ============================================================
# 4) 簡易セルフテスト（このファイルを直接実行したときだけ動く）
# ============================================================

if __name__ == "__main__":
    print("=== signed_nbit_repr demo ===")
    show_signed_nbit_repr(-5, 8)
    show_signed_nbit_repr(130, 8, overflow=True)
    print()

    print("=== bits_to_signed_int demo ===")
    show_bits_to_signed_int("00000101")
    show_bits_to_signed_int("11111011")
    print()

    print("=== ieee754 demo ===")
    show_ieee754(0.1, 64, frac_head=24)
    show_ieee754(0.1, 32, frac_head=24)
    print()

    print("=== 0.1 + 0.2 demo ===")
    show_sum_demo()