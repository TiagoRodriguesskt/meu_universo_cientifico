"""
This is heap's algorithm, wich is used for generating all possible permutations of n
objects. Another exemple could be the traveling Salesman Problem.
Colocando time para medir o tempo de execução
Ideia do algoritmo: Caxeiro viajante.
"""

import time
from itertools import permutations

start = time.time()
for p in permutations([1, 2, 3]):  # Move all objects
    print(p)
print("---" * 10)
for p in permutations([1, 2, 3], 2):  # Move only 2 objects
    print(p)

# Time of execution in seconds (s) and milliseconds (ms) .2f = 2 casas decimais
print(
    f"Tempo de execução: {time.time() - start:.2f}s.{int((time.time() - start) * 1000):.2f}ms"
)

print("---" * 10)

# Calculation serie of Fibonacci


def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)


print(fibonacci(30))
print(
    f"Tempo de execução: {time.time() - start:.2f}s.{int((time.time() - start) * 1000):.2f}ms"
)
