# pc11 · 字符频率统计：练的是"迭代展开任意深度结构，别让递归撞栈"

> [!tldr]
> - fastprep.io 结构化来源（两道 Easy 电面暖场题合并，2026-06 报告）；**Part 2 的"合并成一题"与 Part 3 top-k 打平均为 (reconstructed)**
> - 这题考的是：跨字符串 / 跨任意深度嵌套列表的字符计数与排序 tie-break，以及"深嵌套不能用递归展开"
> - 三步套路：字典累加 + `(-count, char)` 排序 → 把展开逻辑从递归换成显式栈迭代 → 在排序结果上做"打平全带上"的 top-k
> - 最值得带走的一个模式：**任意深度嵌套结构（来自不受信任的输入）绝不能用递归展开——用一个显式栈 + `iter()` 存"当前遍历到哪一层的哪个位置"，栈深度不受 Python 调用栈限制**

## 1. 题目在说什么（人话版）

统计若干字符串里每个字符出现的次数（含空格、标点，区分大小写），按次数降序、次数相同
按字符升序排序。追问把输入换成任意深度嵌套的列表（叶子是字符串），还要支持"取前 k 名，
但打平的全带上"。

```
char_frequencies(["abb", "bcc"]) -> [("b",3), ("c",2), ("a",1)]
char_frequencies(["a a!", "a!"]) -> [("a",3), ("!",2), (" ",1)]   # 空格标点也算
```

## 2. 读题：把文字变成模型

- **实体**：字符（Unicode code point）、扁平/嵌套的字符串容器。
- **输出**：`(char, count)` 列表，`(-count, char)` 排序。
- **状态**：一个计数字典；Part 2 额外需要"当前展开到哪一层"的显式栈。
- **一句话建模**：这是一个 **计数哈希 + 确定性排序 tie-break** 问题，Part 2 叠加"迭代展开任意深度容器"。

> [!note] 为什么不能用递归展开嵌套列表
> Python 默认递归深度限制约 1000。嵌套列表如果来自不受信任的输入（比如日志里递归的
> 结构），几万层嵌套会直接撞 `RecursionError`。用一个显式栈（`list` 当栈、每层存一个
> `iter()`）代替函数调用栈，栈的深度就是普通 Python 对象的列表长度，不受调用栈限制。

## 3. 下笔顺序（面试里就按这个顺序敲）

1. **Part 1 最小可用**：用字典累加每个字符出现次数，按 `(-count, char)` 排序。
2. **Part 2 叠加**：把"遍历字符串列表"换成"迭代展开任意深度列表"——写一个显式栈的生成器，只改变输入怎么变成字符流，计数/排序逻辑原样复用。
3. **Part 3 叠加**：在 Part 2 的排序结果上找第 `k` 名的次数作为阈值，向后扫描把所有等于阈值的都纳入。
4. **收尾**：非字符串叶子/非 list 容器要报错；`k=0`、`k` 超过总数的边界；构造一个几万层的嵌套验证不撞栈。

## 4. 代码怎么组织

```
_count(chars) -> dict                  # 通用计数
_sorted_counts(counts) -> list         # (-count, char) 排序
_iter_flat_chars(strings)              # Part 1 用的字符流
_iter_nested_chars(data)               # Part 2/3 用：显式栈迭代展开
char_frequencies / char_frequencies_nested / top_k_chars
part1 / part2 / part3
```
`_count` 和 `_sorted_counts` 被三个 part 共享；差别只在"喂给它们的字符流是怎么产生的"
——这是本题最值得在面试里强调的抽象点。

## 5. 核心代码骨架

```python
def _count(chars):
    counts = {}
    for ch in chars:
        counts[ch] = counts.get(ch, 0) + 1
    return counts

def _sorted_counts(counts):
    return sorted(counts.items(), key=lambda p: (-p[1], p[0]))

def _iter_nested_chars(data):
    # Part 2：显式栈迭代展开，不用递归——栈深度 = 嵌套深度，不受调用栈限制
    if not isinstance(data, list):
        raise ValueError("nested data must be a list")
    stack = [iter(data)]
    while stack:
        it = stack[-1]
        try:
            item = next(it)
        except StopIteration:
            stack.pop(); continue
        if isinstance(item, str):
            yield from item
        elif isinstance(item, list):
            stack.append(iter(item))
        else:
            raise ValueError(f"unexpected leaf type: {type(item).__name__}")

def top_k_chars(data, k):
    # Part 3：找第 k 名的次数作为阈值，把所有并列的都纳入
    ordered = _sorted_counts(_count(_iter_nested_chars(data)))
    if k == 0 or not ordered:
        return []
    if k >= len(ordered):
        return ordered
    cutoff = ordered[k - 1][1]
    end = k
    while end < len(ordered) and ordered[end][1] == cutoff:
        end += 1
    return ordered[:end]
```

## 6. 面试里怎么说（边写边讲）

- 开始前：「我确认一下：是统计所有字符，包括空格标点，对吗？次数相同按字符升序？」
- 写 Part 2 时：「嵌套深度可能很深，我不用递归展开，用一个显式栈存当前遍历到哪一层，这样不会撞 Python 的递归深度限制。」
- 交付时：「样例过了；如果要 top-k，我会在排序结果上找第 k 名的次数作阈值，把并列的都带上，所以结果可能比 k 长。」

## 7. 常见跑偏（方法层面，3 条）

- 以为只统计字母，忽略空格和标点——题目要求统计所有字符。
- 用递归展开嵌套列表，深度大时直接 `RecursionError`。
- Top-k 只是简单切片 `ordered[:k]`，没处理"第 k 名和后面打平"的情况。

## 8. 同族题 / 延伸

- 同一类"计数哈希 + 确定性排序 tie-break"：`pc12`（分组求和排名）、`pc03`（滑窗事件流的计数）。
- 练习命令：`python3 loop/mock.py start pc11`
