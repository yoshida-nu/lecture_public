import ssl
import socket
from cryptography import x509
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa, ec

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

# ユークリッドの互除法
def gcd(a, b):
    if a < b:
        a, b = b, a
    while b != 0:
        a, b = b, a % b
    return a


# 乗法的逆元
def minv(n, a):
    if n < a:
        n, a = a, n

    n0 = n
    u0, u1 = 1, 0
    v0, v1 = 0, 1

    while a != 0:
        q = n // a
        n, a = a, n % a
        w0, w1 = u0 - q * v0, u1 - q * v1
        u0, u1 = v0, v1
        v0, v1 = w0, w1

    inv = u1 % n0
    return inv


# e の候補を求める
def find_e_candidates(phi_n):
    print("【e の候補を探す】")
    print(f"{phi_n} と互いに素な整数を探します．")

    es = []
    for i in range(2, phi_n):
        if gcd(phi_n, i) == 1:
            es.append(i)
    print(f"e の候補一覧: {es}")
    print()
    return es

# d を探索して求める
def find_d_by_search(e, phi_n):
    print("【d を探す】")
    print("ed = (p - 1)(q - 1)k + 1 を満たす d と k を探します．")
    print(f"今回は e = {e}, (p - 1)(q - 1) = {phi_n} です．")
    print()

    k = 1
    while True:
        value = phi_n * k + 1
        print(f"k = {k} のとき，(p - 1)(q - 1)k + 1 = {phi_n} × {k} + 1 = {value}")

        if value % e == 0:
            d = value // e
            print(f"  {value} は e = {e} で割り切れる")
            print(f"  d = {value} ÷ {e} = {d}")
            print()
            return d
        else:
            print(f"  {value} は e = {e} で割り切れない")
        k += 1


# 鍵生成
def generate_keys(p, q, e_index=0):
    print("========================================")
    print("【鍵生成】")
    print("========================================")
    print(f"素数 p = {p}")
    print(f"素数 q = {q}")

    n = p * q
    phi_n = (p - 1) * (q - 1)

    print(f"n = p × q = {p} × {q} = {n}")
    print(f"(p - 1)(q - 1) = ({p} - 1) × ({q} - 1) = {phi_n}")
    print()

    es = find_e_candidates(phi_n)

    e = es[e_index]
    print(f"今回は e の候補の {e_index + 1} 番目を使います．")
    print(f"選んだ e = {e}")
    print()

    d = find_d_by_search(e, phi_n)

    public_key = (e, n)
    private_key = (d, n)

    print("================================")
    print("生成された鍵")
    print("================================")

    print(f"公開鍵 (e, n) = {public_key}")
    print(f"秘密鍵 (d, n) = {private_key}")

    print("================================")
    print()


# 暗号化
def encrypt(plaintext, public_key):
    e, n = public_key

    print("========================================")
    print("【暗号化】")
    print("========================================")
    print(f"平文 m = {plaintext}")
    print(f"公開鍵 (e, n) = ({e}, {n})")
    print("暗号化の式: c = m^e % n")
    print(f"          = {plaintext}^{e} % {n}")

    ciphertext = pow(plaintext, e, n)

    print(f"暗号文 c = {ciphertext}")
    print()

# 復号
def decrypt(ciphertext, private_key):
    d, n = private_key

    print("========================================")
    print("【復号】")
    print("========================================")
    print(f"暗号文 c = {ciphertext}")
    print(f"秘密鍵 (d, n) = ({d}, {n})")
    print("復号の式: m = c^d % n")
    print(f"        = {ciphertext}^{d} % {n}")

    plaintext = pow(ciphertext, d, n)

    print(f"復号した平文 m = {plaintext}")
    print()


def show_certificate(hostname, port=443):
    context = ssl.create_default_context()

    with socket.create_connection((hostname, port)) as sock:
        with context.wrap_socket(sock, server_hostname=hostname) as ssock:
            cert = ssock.getpeercert()

    print("接続先:", hostname)
    print()

    if cert is None:
        print("証明書を取得できませんでした")
        return

    print("証明書情報:")
    for key, value in cert.items():
        print(f"{key}: {value}")

def show_public_key(hostname, port=443):

    context = ssl.create_default_context()

    with socket.create_connection((hostname, port)) as sock:
        with context.wrap_socket(sock, server_hostname=hostname) as ssock:
            cert_bin = ssock.getpeercert(binary_form=True)

    if cert_bin is None:
        print("証明書を取得できませんでした")
        return

    cert = x509.load_der_x509_certificate(cert_bin, default_backend())
    public_key = cert.public_key()

    print("接続先:", hostname)
    print()

    if isinstance(public_key, rsa.RSAPublicKey):
        numbers = public_key.public_numbers()
        print("公開鍵タイプ: RSA暗号")
        print("e =", numbers.e)
        print("n =", numbers.n)

    elif isinstance(public_key, ec.EllipticCurvePublicKey):
        numbers = public_key.public_numbers()
        print("公開鍵タイプ: 楕円曲線暗号")
        print("curve =", public_key.curve.name)
        print("x =", numbers.x)
        print("y =", numbers.y)

