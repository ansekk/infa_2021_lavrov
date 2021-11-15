def f(x):
    return 1/(x**10)+x


x = 2
n = 1024
for i in range(n):
    print(x)
    x = f(x)

print("=============")
print((2 * n) ** 0.5)
