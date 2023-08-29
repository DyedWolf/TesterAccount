a = [1, 2, 3, 4, 5]
print(a[1:2])
print(a[-1:])
print(a.reverse())
print(a.sort())
print(a[::-1])
b = []
for i in range(len(a)):
    b.append(a[-1])
    a.remove(a[-1])
print(b)
