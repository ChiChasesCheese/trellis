---
id: performance-prof-tottime-cumtime
node: performance.profiling
type: qa
step: 1
---
## Q
`cProfile` 输出里 `tottime` 和 `cumtime` 两列有什么区别？先按哪一列排序、再按哪一列排序，才能从“哪条路径慢”追到“哪一行慢”？

## A
**`tottime` 是函数自身的时间；`cumtime` 把它调用的子函数也算进去**

- **`tottime`（自身时间）**：只算这个函数的代码，不含它调用的函数；找“真正在烧 CPU 的那一行”看它；
- **`cumtime`（累计时间）**：含所有子调用；`main` 的累计时间接近总时间，没有信息量，但它自上而下告诉你时间流向哪条路径；
- **先按 `cumulative` 排序**：从入口往下看，找出哪个分支占大头（这里 `score` 占了 `main` 的绝大部分）；
- **再按 `tottime` 排序**：在这个分支里找到自身耗时最大的函数；
- **调用次数 `ncalls` 同样重要**：一个每次只花 0.05 微秒的函数，被调用 17 万次，也是热点；
- **`20001/1`** 这种写法表示总调用数 / 原始（非递归）调用数。

```python
import cProfile, pstats

def normalize(s): return s.strip().lower()
def load(rows): return [normalize(r) for r in rows]
def score(words):
    return sum(sum(ord(c) for c in w) for w in words)

def main():
    rows = [f"  Row{i} " for i in range(20000)]
    return score(load(rows))

cProfile.run("main()", "/tmp/p.out")
pstats.Stats("/tmp/p.out").strip_dirs().sort_stats("tottime").print_stats(4)
```

本机 3.11 实际输出（节选，已略去时间戳行）：

```text
         397789 function calls (377789 primitive calls) in 0.021 seconds

   Ordered by: internal time
   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
   168890    0.008    0.000    0.011    0.000 demo.py:6(<genexpr>)
 20001/1    0.006    0.000    0.018    0.018 {built-in method builtins.sum}
   148890    0.002    0.000    0.002    0.000 {built-in method builtins.ord}
    20000    0.002    0.000    0.003    0.000 demo.py:3(normalize)
```

按 `tottime`，最大的是 `score` 里那个生成器表达式（`<genexpr>`，调用了 16.9 万次）；它的累计时间比自身时间大，因为里面又调了 `ord`。

改按 `cumulative` 排序时，`main` 累计 0.023 s，其中 `score` 占 0.018 s，`load` 只占 0.004 s：时间主要流向 `score`。

**知识点：**读懂剖析结果（Reading Profiles）
