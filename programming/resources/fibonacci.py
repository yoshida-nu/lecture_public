# 第n項のフィボナッチ数列を返す
def fib(n):
    a, b, count = 0, 1, 1
    while count <= n:
        a, b = b, a + b
        count += 1
    return a
