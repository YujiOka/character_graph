# print(type(1) == type(list()))

def tmp(test):
    test.append(["c", 3])

test = [["a", 1]]
test.append(["b",2])
tmp(test)
print(test)