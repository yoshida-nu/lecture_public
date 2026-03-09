def AND(A, B):
    return A & B

def OR(A, B):
    return A | B

def XOR(A, B):
    return A ^ B


def NOT(A):
    return 1 - A

def NAND(A, B):
    return 1 - (A & B)

def NOR(A, B):
    return 1 - (A | B)

def truth_table(f):
    for A in [0, 1]:
        for B in [0, 1]:
            print(A, B, f(A, B))

def bit_op(a, b, op):
    n = max(len(a), len(b))
    a = a.zfill(n)
    b = b.zfill(n)

    result = ""

    for i in range(n):
        A = int(a[i])
        B = int(b[i])

        if op == "AND":
            r = A & B
        elif op == "OR":
            r = A | B
        elif op == "XOR":
            r = A ^ B
        elif op == "NAND":
            r = 1 - (A & B)
        elif op == "NOR":
            r = 1 - (A | B)
        else:
            raise ValueError("Unknown operation")

        result += str(r)

    return result


def show_bits(s):
    s = s.lstrip("0")
    if s == "":
        return "0"
    return s


def shift_left_with_overflow(bits):
    if bits[0] == "1":
        return "1" + bits[1:] + "0"
    else:
        return bits[1:] + "0"


def add_by_logic(a, b):

    print("加算するビット列:")
    print("  a =", a)
    print("  b =", b)
    print()

    step = 1

    while int(b) != 0:

        n = max(len(a), len(b))
        a = a.zfill(n)
        b = b.zfill(n)

        # XOR
        sum_ = ""
        for i in range(n):
            sum_ += str(int(a[i]) ^ int(b[i]))

        # AND
        carry = ""
        for i in range(n):
            carry += str(int(a[i]) & int(b[i]))

        carry = shift_left_with_overflow(carry)

        m = max(len(sum_), len(carry))
        a_disp = a.zfill(m)
        b_disp = b.zfill(m)
        sum_disp = sum_.zfill(m)
        carry_disp = carry.zfill(m)

        print("Step", step)
        print("   ", a_disp)
        print("+  ", b_disp)
        print("   " + "-" * m)
        print("XOR ", sum_disp)
        print("CAR ", carry_disp)
        print()

        a = sum_
        b = carry
        step += 1

    print("結果:")
    print("   ", show_bits(a))


def add_by_logic_old(a, b):

    print("加算するビット列:")
    print("a =", a)
    print("b =", b)
    print()

    while int(b) != 0:

        # 桁数を揃える
        n = max(len(a), len(b))
        a = a.zfill(n)
        b = b.zfill(n)

        # XOR（桁上がりを無視した和）
        sum_ = ""
        for i in range(n):
            sum_ += str(int(a[i]) ^ int(b[i]))

        # AND（桁上がりが発生した場所）
        carry = ""
        for i in range(n):
            carry += str(int(a[i]) & int(b[i]))

        # 左シフト（必要なときだけ1桁増やす）
        carry = shift_left_with_overflow(carry)

        # 表示用に長さを揃える
        m = max(len(sum_), len(carry))
        sum_disp = sum_.zfill(m)
        carry_disp = carry.zfill(m)

        print("桁上りを無視した和（XOR）:", sum_disp)
        print("桁上りした場所（AND → 左シフト）:", carry_disp)
        print()

        a = sum_
        b = carry

    print("結果: a+b =", show_bits(a))

    