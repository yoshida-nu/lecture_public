plain_space = 'abcdefghijklmnopqrstuvwxyz'
cipher_space = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

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


        