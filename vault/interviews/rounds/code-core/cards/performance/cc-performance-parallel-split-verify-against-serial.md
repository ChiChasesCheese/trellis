---
id: cc-performance-parallel-split-verify-against-serial
node: performance.parallel-split
type: qa
---
## Q
You have a parallel version of a numeric function and the simple serial version. How do you convince yourself, and the interviewer, that the parallel one is right?

## A
**The serial version is the oracle. Run a seeded random differential test over sizes where chunking breaks; ints must match exactly, floats within a tolerance.**

```python
import math, random

def check_against_serial(par, ser, trials=200, seed=0):
    rng = random.Random(seed)                 # replayable failures
    sizes = [0, 1, 2, 3, 7, 8, 9]             # around the worker count
    for t in range(trials):
        n = sizes[t] if t < len(sizes) else rng.randint(0, 50)
        w = rng.choice([1, 2, 3, 4, 8, 64])   # 64: more workers than items
        if t % 2:                             # ints: exact
            a = [rng.randint(-10**12, 10**12) for _ in range(n)]
            assert par(a, w) == ser(a), (seed, t, n, w)
            continue
        a = [rng.uniform(-1, 1) * 10.0 ** rng.randint(-8, 8)
             for _ in range(n)]
        got, want = par(a, w), ser(a)         # floats: order moves bits
        tol = 1e-12 * (sum(map(abs, a)) or 1.0)
        assert len(got) == len(want) and all(
            math.isclose(g, s, rel_tol=1e-9, abs_tol=tol)
            for g, s in zip(got, want)), (seed, t, n, w)
```

- **Bug-catching sizes.** 0, 1, around the worker count, more workers than items.
- **Floats.** Parallel code adds in another order and float addition is not associative, so compare with `rel_tol` plus an input-scaled `abs_tol`.
- **Replayable.** Each assertion carries `(seed, t, n, w)`.
- **It works.** A prefix sum that forgets chunk offsets fails on trial 3 (n = 2).
- **Cheap invariants.** Last prefix equals `sum(a)`; lengths match.

**Follow-up: "is it faster?"** Measure separately: large input, warm-up, repeats, speedup at 1, 2, 4, 8 workers.

## Q zh
你有一个数值函数的并行版本和一个简单的串行版本。怎么让自己、也让面试官相信并行版本是对的？

## A zh
**串行版本就是判定标准（oracle）。跑一个带种子的随机差分测试，覆盖切块容易出错的尺寸；整数必须完全相等，浮点在容差内相等。**

```python
import math, random

def check_against_serial(par, ser, trials=200, seed=0):
    rng = random.Random(seed)                 # replayable failures
    sizes = [0, 1, 2, 3, 7, 8, 9]             # around the worker count
    for t in range(trials):
        n = sizes[t] if t < len(sizes) else rng.randint(0, 50)
        w = rng.choice([1, 2, 3, 4, 8, 64])   # 64: more workers than items
        if t % 2:                             # ints: exact
            a = [rng.randint(-10**12, 10**12) for _ in range(n)]
            assert par(a, w) == ser(a), (seed, t, n, w)
            continue
        a = [rng.uniform(-1, 1) * 10.0 ** rng.randint(-8, 8)
             for _ in range(n)]
        got, want = par(a, w), ser(a)         # floats: order moves bits
        tol = 1e-12 * (sum(map(abs, a)) or 1.0)
        assert len(got) == len(want) and all(
            math.isclose(g, s, rel_tol=1e-9, abs_tol=tol)
            for g, s in zip(got, want)), (seed, t, n, w)
```

- **能抓 bug 的尺寸。** 0、1、worker 数附近、worker 比元素多。
- **浮点。** 并行代码的加法顺序不同，浮点加法不满足结合律，所以用 `rel_tol` 加一个按输入缩放的 `abs_tol` 比较。
- **可重放。** 每条断言都带着 `(seed, t, n, w)`。
- **真能抓到。** 一个忘了加块偏移量的前缀和，在第 3 次试验（n = 2）就失败。
- **廉价不变量。** 最后一个前缀等于 `sum(a)`；长度一致。

**追问：「那它更快吗？」** 单独测：大输入、预热、重复多次，报告 1、2、4、8 个 worker 的加速比。
