---
id: tlc-maximize-amount-after-two-days-of-conversions-4-followup
node: a.maximize-amount-after-two-days-of-conversions
type: qa
step: 4
---
## Q
**LC 3387 两天自由外汇交易后的最大货币数**｜追问

面试官接着问：（1）如果不保证"无矛盾、无环"（可能有套利环）怎么办？（2）扩展到 `d` 天？（3）输出时只保留 5 位小数，浮点误差怎么控制？分别怎么答。

## A
1. **图不再无环无矛盾**：换成"逐天松弛"。状态是 `best[c]`：当前手里每种货币的最大数量。每天重复遍历所有边（正向与反向各一次），能让某个货币变多就更新，直到不再变化或达到轮数上限（货币种类数）。

```python
def max_amount_relax(initial: str, pairs1: list[list[str]], rates1: list[float],
                     pairs2: list[list[str]], rates2: list[float]) -> float:
    def relax_day(best: dict[str, float], pairs: list[list[str]], rates: list[float]) -> dict[str, float]:
        best = dict(best)
        for _ in range(len(pairs) + 1):
            changed = False
            for (a, b), r in zip(pairs, rates):
                for u, v, w in ((a, b, r), (b, a, 1 / r)):
                    if u in best and best[u] * w > best.get(v, 0.0) * (1 + 1e-12):
                        best[v] = best[u] * w
                        changed = True
            if not changed:
                break
        return best

    return relax_day(relax_day({initial: 1.0}, pairs1, rates1), pairs2, rates2)[initial]
```

   示例 1、2、3 分别得到 `720.0`、`1.5`、`1.0`。若图里真的有套利环，数值会一直增大，要靠轮数上限截断；严格处理要对汇率取对数，把乘法化成加法后做 Bellman-Ford，并检测正环。`1 + 1e-12` 的门槛避免浮点误差造成无休止的"改进"。
2. **`d` 天**：第 `i` 天的初值是第 `i - 1` 天的结果 `best`，对每天的图依次调用 `relax_day`，最后读 `best[initial]`。
3. **浮点**：汇率在 `[1.0, 10.0]`，最多 `20` 次乘除，相对误差在 `1e-13` 量级，对题目要求的 `1e-5` 绰绰有余。比较两个答案时用 `math.isclose` 或容差，不要用 `==`；输出时 `round(x, 5)` 或 `f"{x:.5f}"`。

**Python 提醒**：`best.get(v, 0.0)` 对没有出现的货币给 `0.0`，任何正的数量都比它大；`dict(best)` 复制字典，避免第 1 天的结果被第 2 天原地修改。
