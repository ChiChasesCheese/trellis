---
id: tlc-minimum-operations-to-make-character-frequencies-equal-4-followup
node: b.minimum-operations-to-make-character-frequencies-equal
type: qa
step: 4
---
## Q
**LC 3389 使字符频率相等的最少操作次数**｜追问

面试官接着问：（1）没有第三种操作，只能删和补，怎么做？（2）允许 `'z'` 变成 `'a'` 呢？（3）要输出具体的操作方案？

## A
1. **只有删和补。** 每个字母独立决定：清零花 `c`，保留花 `|c - t|`，取小。答案是 `min over t of Σ min(c, |c - t|)`：

```python
from collections import Counter


def make_good_delete_add_only(s: str) -> int:
    freq = list(Counter(s).values())
    return min(sum(min(c, abs(c - t)) for c in freq) for t in range(1, max(freq) + 1))
```

`"aaaaabbb"` 得 `2`，而允许变成下一个字母时是 `1`。
2. **字母表成环。** 'z' 到 'a' 多出一对相邻关系。先固定 'a' 的去向（`0` 或 `t`），沿 `a → z` 跑线性 DP，最后补上 'z' 到 'a' 的那一对节省 `min(z 的富余, a 的缺口)`；两种固定各跑一次取小，复杂度不变。
3. **输出方案。** DP 时为每个字母记下取到最小值的前驱状态，对最优的 `t` 回溯，就得到每个字母的去向，以及每对相邻字母之间推送的个数。

**Python 提醒**：`Counter(s).values()` 只含出现过的字母，适合上面「每个字母独立」的写法；但主解法要按 `a..z` 的顺序依赖相邻关系，必须用 `[cnt[ch] for ch in ascii_lowercase]` 把缺席的字母补成 `0` 保持位置，不能直接用 `values()`。
