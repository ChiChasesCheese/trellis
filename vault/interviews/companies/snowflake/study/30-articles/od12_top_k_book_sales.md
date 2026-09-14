# od12 · Top K Book Sales：懒失效堆——原生不支持删除时的标准解法

> [!tldr]
> - 这题考的是：一个实时累计销量 Top-K 榜单的类设计，`heapq` 天生不支持高效删除任意元素时的标
>   准应对方式——懒失效（lazy invalidation），外加退货批量原子性和 `rank()` 的取舍判断
> - 三步套路：先写正确性版本（每次查询整体排序）→ 换成懒失效最大堆维持高频调用下的效率 → 加退
>   货（负数增量）的批量 all-or-nothing 校验，`rank()` 走独立简单路径
> - 最值得带走的一个模式：**当数据结构原生不支持某个操作时（`heapq` 不能高效删除任意元素），
>   不必换数据结构——让"过期"的记录留着，查询时验证有效性、丢弃无效的、塞回有效的，均摊成本几
>   乎不变**

## 1. 题目在说什么（人话版）

一个实时销量榜：每次调用同时提交一批"书名 + 本次销量增量"，先把增量累加进每本书的总销量，再
返回当前总销量最高的 `k` 本书。要求这个查询在调用次数很多之后仍然高效，而不是每次都对全部书
重新排序。

三行小例子：
```
best_sellers(["a","b","c"], [5,7,7], 2)  -> [b, c]   (b、c 并列 7，字母序 b 在前；a 排不进前 2)
best_sellers(["a"], [10], 2)             -> [a, b]   (a 累加到 15，跃升第一)
```

## 2. 读题：把文字变成模型

- **实体**：书、每本书的运行总销量。
- **输入长什么样**：`books: list[str]`、`counts: list[int]`（Part 3 允许负数）、`k: int`。
- **输出要什么**：总销量降序、书名升序排序后的前 `k` 个书名；`rank(book)` 返回从 1 开始的名
  次。
- **状态**：`name -> 总销量` 字典，外加一个可能含**过期记录**的最大堆（`(-total, name)`）。
- **一句话建模**：这是一个**支持高频更新、需要高效 Top-K 查询、但不需要高效任意删除**的场景，
  懒失效堆是这类问题的标准解法。

> [!note] 为什么不能每次查询都整体排序
> `best_sellers` 被调用的量级远大于书籍规模，如果每次查询都 `sorted(全部书)`，复杂度是
> `O(调用次数 × 书籍数 × log 书籍数)`，大数据量下会超时。懒失效堆把"删除旧记录"这件 `heapq`
> 做不到的事，改成"允许旧记录留着、查询时才验证"，均摊下来每条记录一生只被验证一次。

## 3. 下笔顺序（面试里就按这个顺序敲）

1. **骨架先行**：`BookSalesTracker.__init__` 定义 `_totals` 字典；`best_sellers` 先只做累加，
   查询用 `sorted(self._totals.items(), key=(-total, name))` 取前 `k`——正确性优先。
2. **Part 1 最小可用**：确认排序 key（总销量降序、书名升序）、`k<=0`/超量的边界都对。
3. **Part 2 叠加**：把查询换成懒失效最大堆——每次更新只管 `heappush` 一条新记录，不去堆里删旧
   记录；查询时不断 `heappop`，用 `_totals` 校验记录是否仍然有效，无效永久丢弃，有效的（凑够
   k 个）原样塞回堆里。
4. **Part 3 叠加**：`best_sellers` 先把本次调用里同一本书的多次增量合并成一个净变化量，**预校
   验**——任何一本书会变负就整批拒绝，不留副作用；`rank(book)` 走独立的简单全量排序路径。
5. **收尾**：用随机操作序列跟"每次都整体排序"的朴素实现交叉验证懒失效堆的结果完全一致。

## 4. 代码怎么组织

```
BookSalesTracker.__init__               # _totals 字典 + 懒失效最大堆 self._heap
best_sellers(books, counts, k)          # 合并 delta -> 预校验(Part3) -> 应用 -> push 堆 -> _top_k
_top_k(k)                                # 懒失效弹出 + 校验 + 塞回
rank(book)                               # 独立简单路径：全量排序找位置，不复用堆
```

## 5. 核心代码（骨架，≤ 40 行，带注释）

```python
def best_sellers(self, books, counts, k):
    # 合并同一次调用里对同一本书的多次增量，避免重复 push、避免批量校验漏判
    deltas = {}
    for name, delta in zip(books, counts):
        deltas[name] = deltas.get(name, 0) + delta
    for name, delta in deltas.items():           # Part3：预校验，任何一本会变负就整批拒绝
        if self._totals.get(name, 0) + delta < 0:
            raise ValueError(f"refund would take {name!r} below zero")
    for name, delta in deltas.items():
        new_total = self._totals.get(name, 0) + delta
        self._totals[name] = new_total
        heapq.heappush(self._heap, (-new_total, name))   # 只 push，从不去堆里删旧记录
    return self._top_k(k)

def _top_k(self, k):
    if k <= 0:
        return []
    result, popped, seen = [], [], set()
    while self._heap and len(result) < k:
        neg_total, name = heapq.heappop(self._heap)
        if name in seen or self._totals.get(name) != -neg_total:
            continue                              # 名字重复或总量对不上：过期记录，永久丢弃
        popped.append((neg_total, name))
        seen.add(name)
        result.append(name)
    for entry in popped:                          # 验证过的有效记录塞回堆里，后面查询还用得上
        heapq.heappush(self._heap, entry)
    return result
```

## 6. 面试里怎么说（边写边讲）

- 开始前：「确认一下并列排序按书名升序打平；`k<=0` 返回空、`k` 超过书籍数返回全部。」
- 写 Part 2 时：「`heapq` 不支持高效删除任意元素，我不换数据结构，而是让旧记录留在堆里，查询
  时用 `_totals` 字典校验是否还有效，无效就永久丢弃，有效的塞回去——均摊下来还是
  `O((更新数+查询数·k)·log n)`。」
- 交付时：「样例过了；我用随机操作序列跟'每次都整体排序'的朴素实现交叉验证，结果完全一致。如
  果面试官追问并发批量提交的原子性，我会展开讲。」
- **如果被追问并发**：「如果多个客户端同时提交批量退货，`best_sellers` 里'预校验 + 应用'这两
  步不是原子的——两个并发批次可能各自校验通过（分别看到的都是'减完还非负'），但两个都应用之后
  总销量却变成了负数，这是先检查再执行模式在并发下的经典 TOCTOU 陷阱，需要把这一整段包进一把
  锁，或者用乐观并发（读时带版本号，提交时 CAS，冲突则重试）。」

## 7. 常见跑偏（方法层面，含并发一条）

- 每次更新都对全部书重新排序——正确但没有解决"高频调用"这个约束，退化成
  `O(调用次数 × n log n)`。
- 忘记合并同一次调用里对同一本书的多次增量，导致退货批量校验漏判（分开看每次都非负，合并起来
  却会变负）。
- **并发相关**：把"预校验 + 应用"这两步当成天然原子的，没意识到并发批量提交时这是经典的
  TOCTOU（check-then-act）竞态，需要额外加锁或乐观并发保护。

## 8. 同族题 / 延伸

- 与 LeetCode 1244（Design A Leaderboard）/2349 同族，懒失效堆是"支持高效 Top-K 但不支持高效
  任意删除"这类问题的标准解法。
- `rank()` vs `best_sellers()` 是"先测哪条路径热、再决定往哪投入优化"的工程判断，与
  `od08_lru_ttl_cache` 里"哪条路径值得为 O(1) 投入更复杂的数据结构"是同一种权衡。
- 练习命令：`python3 loop/mock.py start od12`
