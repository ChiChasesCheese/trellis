# q40 · 邻近词查询（k 词内 · 最小窗口 · 归一化 · 文档排序）

> `problems/q40_query_words_within_k/` · 4 个 part
> **主题：词级（不是字符级）的滑动窗口 + 一次预处理支撑多次查询。**

## 一句话题意

在一段文本里找：查询的**第一个词**出现在下标 `i`，且其余每个查询词都出现在 `i < p <= i + k` 的位置。
Part 2 换成"包含全部查询词的最短连续区间"（LC 76 的词版本）。

## 核心考点

`S02` 解析 · `S08` 确定性 tie-break · **`S13` 闭/开区间边界** · **`S14` 字符串归一化** ·
**`S16` 滑动窗口** · `S19` 增量

## 解题思路

### Part 1 — `find_starts(text, query, k)`

返回所有满足条件的**第一个查询词的下标 `i`**：其余每个查询词都在 `(i, i + k]` 内出现过。
位置是 **0-based 的词下标**。单词查询返回它的全部位置。

**预处理成 `word -> 有序位置列表`，然后用 `bisect`**（这也是面试官问的 follow-up）：

```python
pos = defaultdict(list)
for idx, w in enumerate(tokens): pos[w].append(idx)

def ok(i, w, k):
    lst = pos.get(w, [])
    j = bisect_right(lst, i)          # 第一个 > i 的位置
    return j < len(lst) and lst[j] <= i + k
```

这样重复查询不用重新扫全文。

### Part 2 — `min_window(text, query)`

包含**所有**查询词（**任意顺序**）的最短连续词区间；长度相同时取**起点最早**的；
有词从未出现 → `None`。用词列表上的滑动窗口，O(n)。

### Part 3 — 归一化

`tokenize(text, normalize=True)`：先转小写，token 是 `[a-z0-9]+` 的极大连续段
（标点被丢弃，`Quick-fox` 变成 `quick`、`fox`）。**查询用同样的方式归一化。**

### Part 4 — `rank(docs, query)`

归一化后对每个 `(name, text)` 算 Part 2 的窗口；
只保留包含全部词的文档；按 `(length, 输入顺序)` 排序；`length = end - start + 1`。

## 坑

1. **`k` 边界**：距离**恰好等于 `k`** 算数（`quick fox|2` 包含距离 1），`k - 1` 不算；
   **`k = 0` 时只有单词查询能匹配**。
2. **另一个词出现在起点之前不算**（`fox quick` 和 `quick fox` 结果不同）——
   条件是 `i < p <= i + k`，**左端严格大于**。
3. 查询词不存在 → `[]` / `None` / `-1`；空文本；单词查询；**查询里有重复词**。
4. 最小窗口平手 → **起点最早**；窗口里同一个词重复（`quick quick fox`）。
5. Part 3：`Quick-fox.` 切成两个 token；查询大小写不敏感。
6. Part 4：平手保持**输入顺序**；缺词的文档**直接省略**，不是打印 `-1`。

## 变体

- 返回布尔（"所有词是否都在彼此 k 词之内？"）而不是下标。
- LC 76（字符级最小窗口子串）；LC 243/244（两个词的最短距离）。

## Code Core 节点

**`algorithms.sliding-window`** · **`toolbox.sorted`**（`bisect` 预处理） · `input.normalization` ·
`model.index`（倒排位置表） · `output.ordering` · `performance.amortized`

## 自测清单

- [ ] 距离 `== k` / `k - 1` / `k = 0`
- [ ] 另一个词在起点之前
- [ ] 查询词不存在 / 空文本 / 单词查询 / 重复查询词
- [ ] 最小窗口平手取最早；窗口内重复词
- [ ] `Quick-fox.` 的切分；查询大小写
- [ ] Part 4 的平手顺序；缺词文档被省略
- [ ] 多次查询同一文档（确认没有重复扫全文）
