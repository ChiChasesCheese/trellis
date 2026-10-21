import time

def collatz_total(limit):
    steps = 0
    for n in range(1, limit + 1):
        x = n
        while x != 1:
            x = 3 * x + 1 if x & 1 else x // 2
            steps += 1
    return steps

t0 = time.perf_counter()
total = collatz_total(300000)
print(f"collatz total steps (1..300000) = {total} in {(time.perf_counter() - t0) * 1000:.0f} ms")
