# q20 · Sequential String：练的是"排列覆盖 = 计数问题，不是子序列问题"

> [!tldr]
> - 2024 年 OA 一手转述（`JoeBao22/SDE-OA-2024`）；**Part 2 的 O(1) 索引写法是 (reconstructed)**
> - 这题考的是：磁带只能顺序读，求最短前缀长度使其数字多重集合能拼出查询串的某个排列
> - 三步套路：识破"这不是子序列匹配" → 每个数字建前缀计数表二分 → 出现位置表直接索引去掉 log
> - 最值得带走的一个模式：**"能不能拼出某个排列"永远是计数问题、跟顺序无关——把它当子序列匹配去找，会系统性地把答案判得更小甚至判成不可能**

## 1. 题目在说什么（人话版）

有一台只能往右走的磁带 `s`（数字字符串）。对每个查询串，问：磁带最少要读多长的前缀，
这段前缀里的数字才够"重新拼"出查询串（不要求顺序，只要求每个数字出现的次数够）？
凑不出来就是 `-1`。

```
s = "064819848398"
查询 "088" -> 前缀读到下标 7（"0648198"）才凑齐两个 0、一个 8 -> 答案 7
查询 "071" -> "7" 这个数字在 s 里从没出现过 -> 答案 -1
```

## 2. 读题：把文字变成模型

- **实体**：磁带 `s`、若干查询串，每个查询串对应一个"需求向量" `need[d]`（数字 `d` 需要几个）。
- **输入长什么样**：`s` 和查询都是纯数字字符串；真正有用的信息是每个查询里每个数字出现了几次，顺序完全不重要。
- **输出要什么**：每个查询一个整数（最短前缀长度）或 `-1`。
- **状态**：要能快速回答"数字 `d` 在 `s[:L]` 里出现了几次"或者反过来"数字 `d` 第 `k` 次出现在哪"。
- **一句话建模**：这是一个 **按数字维度做前缀计数、取各维度需求的最晚满足点** 的问题。

> [!note] 为什么不是子序列匹配
> 题面里"顺序读"很容易让人联想到"在 `s` 里顺着找一个子序列"。但"能否拼出排列"只关心
> 集合的计数是否够，不关心顺序：`s="21"`、查询`"12"`，前缀 `"21"` 里有一个 1 一个 2，
> 答案是 2；如果按子序列去找（先找 `'1'` 在下标 1，再从下标 2 往后找 `'2'`——找不到），
> 会误判为 `-1`。来源仓库自带的参考实现正是这么错的。

## 3. 下笔顺序（面试里就按这个顺序敲）

1. **先讲清楚模型**：口头举 `"21"` vs `"12"` 的反例，说明这是计数题不是子序列题，防止面试官以为你要写子序列匹配。
2. **Part 1 最小可用**：对每个数字建前缀计数列 `counts[d][i]`；查询里每个数字在对应列上二分找第一个 `≥ need[d]` 的下标，取所有数字里的最大值。
3. **Part 2 叠加**：把"二分搜索"换成"直接索引"——每个数字记出现位置列表 `occ[d]`，需要第 `need[d]` 个就是 `occ[d][need[d]-1]`。
4. **收尾**：空查询答案是 0；某数字从未出现是 `-1`；两个 Part 在同一批随机输入上必须给出相同答案。

## 4. 代码怎么组织

```
_validate(s, queries)
sequential_prefix_lengths_binary(s, queries)   # Part 1：前缀计数表 + 二分
sequential_prefix_lengths_fast(s, queries)     # Part 2：出现位置表 + 直接索引
part1 / part2                                  # 命令流包装
```
两个函数共享"对查询算 `need`（Counter）→ 逐数字算所需前缀长度 → 取最大值"的骨架，
差别只在"给定 `need[d]`，怎么求出所需前缀长度"这一步用二分还是直接索引，面试里可以先写
一个共享的小 helper 占位，再决定要不要抽出来。

## 5. 核心代码骨架

```python
from collections import Counter
import bisect

# Part 1：每个数字一张前缀计数列，查询时二分
def sequential_prefix_lengths_binary(s, queries):
    n = len(s)
    counts = [[0] * (n + 1) for _ in range(10)]
    for i, ch in enumerate(s):
        for d in range(10):
            counts[d][i + 1] = counts[d][i]
        counts[int(ch)][i + 1] += 1

    out = []
    for q in queries:
        need = Counter(int(c) for c in q)
        best = 0
        for d, cnt in need.items():
            idx = bisect.bisect_left(counts[d], cnt)
            if idx > n:
                best = None; break
            best = max(best, idx)
        out.append(-1 if best is None else best)
    return out

# Part 2：每个数字一张出现位置表，O(1) 索引
def sequential_prefix_lengths_fast(s, queries):
    occ = [[] for _ in range(10)]
    for i, ch in enumerate(s):
        occ[int(ch)].append(i)
    out = []
    for q in queries:
        need = Counter(int(c) for c in q)
        best = 0
        for d, cnt in need.items():
            if len(occ[d]) < cnt:
                best = None; break
            best = max(best, occ[d][cnt - 1] + 1)
        out.append(-1 if best is None else best)
    return out
```

## 6. 面试里怎么说（边写边讲）

- 开始前：「我先确认一下：这是要前缀的数字多重集合覆盖查询，跟顺序无关，对吗？我举个反例——`s="21"`，查询`"12"`，如果按子序列找会判不可能，但实际前缀`"21"`就够了。」
- 写 Part 1 时：「我给每个数字建一张前缀计数表，查询里每个数字所需的前缀长度用二分求，取所有数字里的最大值，因为前缀必须同时满足所有数字的需求。」
- 交付时：「样例过了；如果时间允许，我可以把二分换成直接对出现位置表索引，去掉 log 因子。」

## 7. 常见跑偏（方法层面，3 条）

- 把题目读成子序列匹配，写出一个完全不同的算法（来源仓库参考实现的原始错误）。
- 只判断"数字是否出现过"，忘了要凑够**次数**（重复计数）。
- 忘了空查询要单独处理（`need` 为空时答案恒为 0，不能落入"所有数字都满足"的循环判断出问题）。

## 8. 同族题 / 延伸

- 同样是"多重集合覆盖/计数正确性"的贪心陷阱：`q19`（翻倍哪个元素才是最优贪心）、`q21`（只挑收益率最高的类型不是正确贪心）——都是"看起来直觉对、实际要论证"的套路。
- 练习命令：`python3 drill.py start q20`

## 索引行

| [q20_sequential_string](q20_sequential_string.md) | `../../problems/q20_sequential_string/` | OA | "能不能拼出某个排列"永远是计数问题、跟顺序无关——把它当子序列匹配去找，会系统性地把答案判得更小甚至判成不可能 |
