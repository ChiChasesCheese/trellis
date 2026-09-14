# pc25 · Grep With Context Lines：练的是"区间标记合并 + 流式的延迟定案"

> [!tldr]
> - 这题考的是：实现 `grep -C`，从窗口合并到 GNU 风格分组（`--`、`-B/-A`）再到流式 O(1) 内存版本；一手预览只给函数签名，Part 2/3 **(reconstructed)**
> - 三步套路：给每个命中标记 `[i-around, i+around]` 的区间 → 标记数组天然去重合并 → 流式版本用固定大小的环形缓冲延迟决定一行是否输出
> - 最值得带走的一个模式：**区间标记 + 并集是滑窗合并的通用技巧；流式版本用"延迟定案"模式（固定大小环形缓冲）替代无界累积状态**

## 1. 题目在说什么（人话版）

`grep(lines, search_target, lines_around)` 返回命中行以及前后各 `N` 行；多个命中的上下文窗口
重叠或相邻时要合并成一段连续区间，不能重复输出同一行。Part 2 加上 GNU 风格的 `--` 分组和不对称
的 `-B/-A`；Part 3 把 `lines` 换成只能遍历一次的迭代器，要求用固定的内存量完成同样的事。

小例子：
```python
lines = ["a","b","ERR_x","c","d","e","ERR_y","f","g"]
grep(lines, "ERR", 1)          -> ["b","ERR_x","c","e","ERR_y","f"]
grep_grouped(lines, "ERR", 0, 0) -> ["ERR_x", "--", "ERR_y"]   # 两段不相邻，中间插 --
```

## 2. 读题：把文字变成模型

- **实体**：文本行、命中位置、上下文窗口、保留标记。
- **输入**：Part 1/2 是列表；Part 3 是一次性迭代器。
- **输出**：保留下来的行（按原序，无重复）。
- **状态**：Part 1/2 用一个布尔数组标记"保留"；Part 3 用一个固定大小的环形缓冲区。
- **一句话建模**：这是一个 **"区间标记 + 合并"** 问题；流式版本的核心困难是"看到一行的那一刻
  还不知道它算不算某个命中的后文"，需要延迟判定。

> [!note] 为什么流式版本要延迟定案，而不是边读边输出
> 一行是否要保留，取决于它自己是否命中，或者它是否落在后面某个命中的"前文"窗口里——而后面还有
> 没有命中，读到当前这行时并不知道。所以必须把这一行暂存起来，等再往后多看 `lines_around` 行、
> 确认期间没有新的命中需要更长的前文窗口，才能确定它到底要不要输出。

## 3. 下笔顺序

1. **问清**：命中行本身算不算自己窗口的一部分？`lines_around=0` 时只留命中行本身吗？
2. **Part 1 最小可用**：对每个命中位置 `i`，把 `[i-around, i+around]`（截断到边界）标记为
   "保留"到一个布尔数组，最后按原序输出被标记的行——标记数组天然去重、天然合并重叠窗口。
3. **Part 2 叠加**：同样的标记逻辑，`before`/`after` 分开；输出时跟踪"上一个被保留行的下标"，
   下标不连续就插入一行 `"--"`（第一段前、最后一段后都不加）。
4. **Part 3 叠加**：用一个容量为 `lines_around+1` 的环形缓冲，新行入队时如果自己是命中，就地把
   缓冲区里已有的最近 `lines_around` 行标记为保留，并设一个"接下来 `lines_around` 行也保留"的
   计数器；缓冲区超过容量时弹出最老一行，按标记决定是否输出。
5. **收尾**：负数 `lines_around`/`before`/`after` 报错；空输入返回空；Part 3 用真正的一次性
   生成器测试，防止偷懒把迭代器先转成 list 再复用 Part 1。

## 4. 代码怎么组织

```
grep(lines, target, around)                    # Part 1：标记数组
grep_grouped(lines, target, before, after)     # Part 2：标记数组 + '--' 分组
grep_stream(lines: Iterable, target, around)   # Part 3：环形缓冲，生成器
```
Part 1、Part 2 共享"标记数组"的思路；Part 3 是完全不同的实现（不能建索引数组），但保证结果与
批量版本一致。

## 5. 核心代码（骨架）

```python
# Part 1：标记 + 合并
def grep(lines, search_target, lines_around):
    n = len(lines)
    keep = [False] * n
    for i, line in enumerate(lines):
        if search_target in line:
            lo, hi = max(0, i - lines_around), min(n - 1, i + lines_around)
            for j in range(lo, hi + 1):
                keep[j] = True
    return [line for i, line in enumerate(lines) if keep[i]]

# Part 3：环形缓冲，延迟定案
def grep_stream(lines, search_target, lines_around):
    window, after_remaining, cap = deque(), 0, lines_around + 1
    for line in lines:
        is_match = search_target in line
        window.append([line, False])
        if is_match:
            lo = max(0, len(window) - 1 - lines_around)
            for k in range(lo, len(window)):
                window[k][1] = True
            after_remaining = lines_around
        elif after_remaining > 0:
            window[-1][1] = True
            after_remaining -= 1
        while len(window) > cap:
            line, keep = window.popleft()
            if keep: yield line
    while window:
        line, keep = window.popleft()
        if keep: yield line
```

## 6. 面试里怎么说

- 开始前：「命中行本身算不算自己窗口的一部分？我假设算，`lines_around=0` 时只留命中行本身。」
- 写 Part 1 时：「我给每个命中标记一个区间，标记数组天然去重、天然合并重叠或相邻的窗口，不需要
  单独写合并逻辑。」
- 到 Part 3 时：「迭代器只能遍历一次，看到一行的那一刻还不知道它是不是某个后面命中的前文——我
  用一个固定大小的环形缓冲延迟定案，缓冲区大小只跟 `lines_around` 有关，跟总行数无关。」
- 交付时：「我用 500 组随机数据把流式版本和批量版本交叉验证，结果完全一致。」

## 7. 常见跑偏

- 每个命中各自输出自己的窗口，事后再去重拼接——比直接标记再统一输出复杂得多，也容易在窗口
  重叠处漏掉或重复。
- Part 2 的 `--` 在第一段前面或最后一段后面也加了一个，没有正确处理"只在两段之间才插入"的
  条件。
- Part 3 偷懒先把迭代器耗尽成一个 list 再复用 Part 1 的实现——这违反了"O(lines_around) 辅助
  内存、不随输入行数增长"的要求，用真正的一次性生成器测试就能抓出来。

## 8. 同族题 / 延伸

- 与 `pc03`（Recent Event Stream）同属"滑动窗口 + 增量维护"的考法，但 pc03 是按条数/时间的
  事件窗口，pc25 是按行号的上下文窗口。
- 与 `pc05`（Max Events II）同样用区间标记思维，但 pc05 是区间调度计数，pc25 是区间合并去重。
- 练习命令：`python3 loop/mock.py start pc25`
