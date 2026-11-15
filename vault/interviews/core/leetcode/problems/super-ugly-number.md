---
slug: super-ugly-number
---
## Q
**LC 313 超级丑数**｜Medium

超级丑数是所有质因数都在给定质数数组 `primes` 中的正整数（1 也是）。返回第 `n` 个超级丑数。

## A
**一句话。** 每个质数一个指针，指向它要乘的已生成的丑数；每一步取各指针候选值的最小者作为下一个丑数，并让所有产生这个值的指针前进（顺便去重）。

```python
def nth_super_ugly_number(n, primes):
    ugly = [1]
    idx = [0] * len(primes)      # 每个质数当前要乘的丑数下标
    for _ in range(n - 1):
        nxt = min(ugly[idx[j]] * p
                  for j, p in enumerate(primes))
        ugly.append(nxt)
        for j, p in enumerate(primes):
            if ugly[idx[j]] * p == nxt:
                idx[j] += 1      # 所有产生 nxt 的指针都前进
    return ugly[-1]
```

**复杂度。** 时间 `O(n · k)`（`k = len(primes)`），空间 `O(n + k)`。

**易错点。**
- 只让一个指针前进：不同质数可能产生同一个值（如 `2 × 3 = 3 × 2`），不一起前进会重复。
- 用集合加堆但不去重：同一个丑数被多次弹出。
- 第一个丑数忘了是 1：`n = 1` 时返回 1。

**追问。**
- 为什么指针法正确？：每个丑数都是某个更小丑数乘一个质数，每个质数对应的候选序列是递增的，各取当前最小的候选即可按序生成。
- 用堆行不行？：行，每次弹出最小值并压入它乘各质数的结果，要去重，`O(nk log (nk))`。

**同模式。** LC 264 丑数 II、LC 263 丑数、LC 1201 丑数 III、LC 373 查找和最小的 K 对数字
