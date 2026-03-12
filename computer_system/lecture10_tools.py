plain_space = 'abcdefghijklmnopqrstuvwxyz'
cipher_space = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

def caesar_encrypt(plaintext, k=3):
    print("平文:", plaintext)
    print(f"鍵 k = {k}")
    print()

    print("平文文字  →  番号  →  番号 + k  →  暗号文字")
    print("--------------------------------")

    ciphertext = ""

    for i in plaintext:
        number = ord(i) - ord("a")
        shifted = (number + k) % 26
        cipher_char = chr(shifted + ord("a"))

        print(f"{i}  →  {number:2}  →  {shifted:2}  →  {cipher_char.upper()}")

        ciphertext += cipher_char.upper()

    print("--------------------------------")
    print("暗号文:", ciphertext)


def caesar_decrypt(ciphertext, k=3):
    print("暗号文:", ciphertext)
    print(f"鍵 k = {k}")
    print()

    print("暗号文文字  →  番号  →  番号 - k  →  復号文文字")
    print("--------------------------------")

    plaintext = ""

    for i in ciphertext:
        number = ord(i) - ord("A")
        shifted = (number - k) % 26
        plain_char = chr(shifted + ord("A"))

        print(f"{i}  →  {number:2}  →  {shifted:2}  →  {plain_char.lower()}")

        plaintext += plain_char.lower()

    print("--------------------------------")
    print("復号文:", plaintext)

# シーザー暗号の復号
def caesar_dec(c, k):
    n = len(c)
    k = 26 - k
    p = ''
    
    for i in range(n):
        j = cipher_space.find(c[i])
        j = (j + k) % 26
        p = p + plain_space[j]
        
    return p


# 総当たりで復号する関数
def brute_force(ciphertext):
    keys = range(1, 26)
    
    for key in keys:
        plaintext = caesar_dec(ciphertext, key)
        print(f'鍵k={key:>2}： {plaintext}')


        