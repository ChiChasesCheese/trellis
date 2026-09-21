# pc08 · LRU Cache + TTL + Median From Stream：练的是"两套经典设计题的边界条件写死"

> [!tldr]
> - 这题考的是：能不能把两道背熟的经典题（LRU、双堆中位数）里那些"容易含糊带过"的边界条件讲清楚、写对
> - 三步套路：先跑通库函数版本（拿到分）→ 换成手写结构证明理解底层 → 叠加一个新维度（TTL）时先想清楚它和已有机制是不是独立的
> - 最值得带走的一个模式：**"两个独立机制作用在同一个数据结构上"时，第一件事是想清楚它们各自的触发条件是不是互相干扰——LRU 淘汰和 TTL 过期是两条完全不相交的规则**

## 1. 题目在说什么（人话版）

Part 1（LC 146）：一个容量固定的缓存，`get`/`put` 都要 O(1)，满了就淘汰最久没被访问的那个。Part 2（重建）：给每条记录加一个"过期时间"，过期了就当不存在。Part 3（LC 295，独立的第二道经典题）：一串数字流进来，随时能问"目前的中位数是多少"。

```
LRUCache(2): put(1,1); put(2,2); get(1)->1(标记1最近用过); put(3,3)（淘汰2）; get(2)->-1

MedianStream: add(5)->median()=5; add(15)->median()=10; add(1)->median()=5; add(3)->median()=4
```

## 2. 读题：把文字变成模型

- **Part 1 的状态**：一个"谁最近被用过"的顺序 + 一个 key→value 的查找表——`OrderedDict` 天生就是这两者的组合。
- **Part 2 新增的状态**：每个 key 一个"到期时刻"（不是"还能活多久"，是"到了哪个绝对时间点就死"）。
- **Part 3 的状态**：不是"全部数字"，而是"比中位数小的那一半"和"比中位数大的那一半"各自的极值——这正好是两个堆的职责分工。
- **一句话建模**：Part 1/2 是"顺序 + 查找表"的组合数据结构；Part 3 是"用两个堆把中位数附近的信息单独摘出来维护"。

> [!note] 为什么 TTL 和 LRU 淘汰是两套独立机制
> 容易想岔的地方：以为"过期的条目应该优先被淘汰"，于是把两套逻辑揉在一起。但淘汰是"容量满了才触发的操作"，过期是"查询时才检查的状态"——一个 TTL 还很早的条目完全可能因为容量满被淘汰掉，一个已经过期但还没被查询过的条目会一直"占着位置"直到下次被 `get` 到或者被淘汰。把这两件事分开想，代码才不会纠缠。

## 3. 下笔顺序（面试里就按这个顺序敲）

1. **Part 1 先给 `OrderedDict` 版本**：`move_to_end` 标记最近使用，`popitem(last=False)` 淘汰最老的。立刻用样例自测。
2. **被追问"不用库"时换手写双链表**：MRU 挂在尾部、LRU 挂在头部，`get`/`put` 都要"摘下来再挂到尾部"。用两个哨兵节点（`head`/`tail`）避免处理"空链表"的特殊分支。
3. **Part 2 加 TTL**：先想清楚"到期时刻在 `put` 时就算死"（`clock() + ttl`），`get` 只负责"检查有没有到，到了就当不存在并顺手清掉"——不要在 `get` 里"顺便刷新"过期时间。
4. **容量淘汰保持不变**：`put` 后超容量就按 LRU 顺序淘汰，跟 TTL 完全无关，这行代码基本从 Part 1 原样搬过来。
5. **Part 3 独立写**：两个堆（Python 没有大顶堆，负数取反模拟），每次 `add` 后调整平衡，`median` 只看堆顶。
6. **收尾**：输入校验（`capacity`/`key`/`value`/`ttl`/`num` 各自的合法范围，`bool` 要单独挡掉因为它是 `int` 子类）。

## 4. 代码怎么组织

```
LRUCache / LRUCacheLinked          # Part1：两种实现，行为必须一致
LRUCacheTTL                        # Part2：在 LRUCache 基础上加 _expiry 字典 + 注入的 clock
MedianStream                       # Part3：完全独立，两个堆
part1..part3 / main
```
`LRUCacheTTL` 不是继承 `LRUCache`，而是重新写一份（`_expiry` 需要在 `get`/`put` 里都检查，硬塞进继承关系反而更绕）；`MedianStream` 和前两个类没有任何共享状态，独立成一段。

## 5. 核心代码（骨架，≤ 40 行，带注释）

```python
class LRUCache:
    def __init__(self, capacity):
        self.capacity = capacity
        self._data = OrderedDict()

    def get(self, key):
        if key not in self._data:
            return -1
        self._data.move_to_end(key)      # 标记为最近使用
        return self._data[key]

    def put(self, key, value):
        if key in self._data:
            self._data.move_to_end(key)
        self._data[key] = value
        if len(self._data) > self.capacity:
            self._data.popitem(last=False)  # 淘汰最久未使用

class MedianStream:
    def add(self, num):
        if self._lower and num <= -self._lower[0]:
            heapq.heappush(self._lower, -num)   # 大顶堆存较小一半
        else:
            heapq.heappush(self._upper, num)    # 小顶堆存较大一半
        # 之后重新平衡到两堆大小差 <= 1
```

## 6. Talking through it in the interview

- Before starting: "I'll build the OrderedDict version first to get a correct O(1) baseline, then swap in the hand-rolled doubly linked list if you want to see the pointer mechanics."
- Writing the TTL extension: "The deadline is set once at put time as an absolute timestamp — a get() that hits an entry marks it as recently used for LRU purposes, but it never pushes the deadline out, because that's a sliding-TTL semantics I wasn't asked for."
- Writing the median stream: "I'm keeping the lower half in a max-heap and the upper half in a min-heap, rebalancing after every insert so their sizes never differ by more than one — that turns the query into an O(1) heap-top lookup."
- On delivery: "The worked examples pass; the OrderedDict and linked-list LRU implementations agree on a batch of randomized operations."

## 7. 常见跑偏（方法层面，3 条）

- 把"过期"和"淘汰"混成一套逻辑（比如让 `put` 顺便清理所有过期条目）——两者触发条件不同，混在一起会让"容量淘汰不看 TTL"这条规则很难验证。
- TTL 写成滑动窗口（`get` 时顺手刷新到期时间）——除非题目明确要求，绝对到期时间是更常见也更容易验证的默认语义，混淆的话会让"命中后还会不会过期"这类追问答错。
- 中位数用"每次插入后整体排序"——能过小样例，但复杂度是 O(n log n) 每次插入，面试官一问"如果这是个持续几十万条的流呢"就露馅；应该从一开始就用两个堆。

## 8. 同族题 / 延伸

- LRU Cache 与"限流器""滑动窗口计数"是同一类"维护一个有序/受限窗口 + O(1) 查询"的设计题，可以对照本库其它带滑窗的题一起复习。
- 双堆求中位数是"用两个堆分别维护上下界"这一模式的代表，遇到"流式 top-k""流式分位数"这类题时可以直接迁移思路。
- 练习命令：`python3 loop/mock.py start pc08`
