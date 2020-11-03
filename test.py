def f():
    import random
    return random.random()
for i in range(1000000):
    f()
