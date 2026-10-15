# 05 · 堆 / Top-K（Heap & top-k）

> 本讲覆盖：LC 347 Top K Frequent Elements · 767 Reorganize String · 23 Merge k Sorted Lists（Hard）· 295 Find Median from Data Stream（Hard）
> 前置：`dict` / `Counter`（第 01 讲）、链表节点（第 08 讲会细讲，这里只需要知道 `node.val`、`node.next`）。
> 读完你应该能：(1) 解释堆（heap）是什么、为什么 push/pop 是 O(log n)；(2) 在 Python 里正确使用只有最小堆的 `heapq`（取负、元组、tie-breaker）；(3) 判断「大小为 k 的堆」与「全排序」何时划算。

## 1. 这个模式是什么，为什么存在

### 1.1 从最笨的解法开始

LC 347：给整数数组，返回出现次数最多的 `k` 个数。最笨的做法：统计次数，把所有 `(次数, 值)` **全部排序**，取前 k 个。排序是 O(m log m)（m = 不同值的个数）。

### 1.2 慢在哪里

我们只要 k 个，却把全部 m 个都排好了序。当 m = 10⁷、k = 10 时，99.9999% 的排序工作是浪费。更糟的是在**流式**场景里数据一直在来，没法「等全部到齐再排序」。

> 因果链：只关心「当前最大的 k 个」→ 只需要随时能知道 **这 k 个里最弱的那个**，新来的比它强就替换它 → 需要一个能 O(log k) 插入、O(1) 看最值、O(log k) 删最值的结构 → 堆（heap）。时间 O(m log k)，空间 O(k)。

### 1.3 堆是什么（从零讲）

- **是什么**：一棵「完全二叉树」，每个节点都 ≤ 它的两个孩子（最小堆，min-heap）。所以根（下标 0）永远是最小值。
- **怎么存**：不用指针，直接放进数组。下标 `i` 的父节点是 `(i-1)//2`，孩子是 `2i+1` 和 `2i+2`。
- **push**：放到数组末尾，然后和父节点比较、比父节点小就交换，一路上浮（sift-up）。树高 log n → O(log n)。
- **pop 最小值**：取走根，把数组最后一个元素放到根，然后和较小的孩子比较、比孩子大就交换，一路下沉（sift-down）。O(log n)。
- **heapify**：把任意数组原地变成堆，O(n)（不是 n log n；下层节点多但下沉距离短）。
- **Python 的 `heapq` 只有最小堆**。要最大堆就存**相反数**；要按多个字段排序就存**元组**，元组按字典序比较；元组前面的字段相等时会比较后面的字段，如果后面是不可比较的对象（链表节点）会抛 `TypeError`，所以要插入一个唯一的 tie-breaker（比如递增的序号）。

### 1.4 什么时候用堆、什么时候不用

| 场景 | 选择 |
|---|---|
| 要全部数据排好序 | `sorted` |
| 只要最大 / 最小的 k 个，k ≪ n，或数据是流 | 大小为 k 的堆，O(n log k) |
| k 很接近 n | 直接排序，或 `heapq.nlargest` 内部会选更优策略 |
| 要「持续取当前最小」+ 中途插入新元素（合并 k 路、Dijkstra、事件模拟） | 堆 |
| 要动态维护**中位数** | 两个堆：最大堆放较小的一半，最小堆放较大的一半 |
| 次数范围有限（≤ n） | 桶排序（bucket sort）O(n)——LC 347 的另一种解法 |

## 2. 模板与逐行讲解

```python
import heapq

# Template: the k LARGEST of a stream with a size-k MIN-heap (the heap's root is the weakest member)
def k_largest(nums, k):
    heap = []
    for x in nums:
        if len(heap) < k:
            heapq.heappush(heap, x)
        elif x > heap[0]:
            heapq.heapreplace(heap, x)          # pop root + push x in one O(log k) step
    return sorted(heap, reverse=True)

# Template: max-heap in Python = store negatives
def pop_largest_first(nums):
    heap = [-x for x in nums]
    heapq.heapify(heap)                          # O(n), cheaper than n pushes
    return [-heapq.heappop(heap) for _ in range(len(heap))]

# Template: tuples compare element by element -> add a tiebreaker when the payload is not comparable
def merge_sorted(*lists):
    heap = [(lst[0], i, 0) for i, lst in enumerate(lists) if lst]     # (value, which list, position)
    heapq.heapify(heap)
    out = []
    while heap:
        v, i, j = heapq.heappop(heap)
        out.append(v)
        if j + 1 < len(lists[i]):
            heapq.heappush(heap, (lists[i][j + 1], i, j + 1))
    return out

assert k_largest([5, 1, 9, 3, 7], 3) == [9, 7, 5]
assert pop_largest_first([3, 1, 2]) == [3, 2, 1]
assert merge_sorted([1, 4], [2, 3], []) == [1, 2, 3, 4]
```

逐行讲解：

1. `k_largest` 里用**最小堆**求**最大的 k 个**：堆顶是这 k 个里最小的（门槛）；新元素 `x > heap[0]` 才有资格进来，替换门槛。很多人以为「最大的 k 个要用最大堆」，那样反而要放全部 n 个。
2. `heapq.heapreplace(heap, x)`：先弹出堆顶再压入 `x`，比 `heappop` + `heappush` 快；还有 `heappushpop`（先压后弹）。
3. `pop_largest_first`：把值取负压入，弹出时再取负；`heapify` 是 O(n)，比逐个 `heappush` 的 O(n log n) 好。
4. `merge_sorted`：堆里放 `(值, 来自第几个列表, 在该列表中的位置)`。弹出一个后，把**同一个列表的下一个**压进来——堆的大小始终 ≤ 列表个数 k，所以每次操作 O(log k)，总共 O(N log k)。
5. 元组的第二项 `i` 既告诉我们怎么取下一个，也是 tie-breaker——即使值相同也不会去比较第三项。

## 3. 完整手算（Worked trace）

LC 347，`nums = [1,1,1,2,2,3]`，`k = 2`。先统计 `{1: 3, 2: 2, 3: 1}`，堆里放 `(次数, 值)`，超过 k 个就弹出最小的（次数最少的）。

```python
import heapq
from collections import Counter

def topk_trace(nums, k):
    freq = Counter(nums)
    print("counts:", dict(freq))
    heap = []
    for value, count in freq.items():
        heapq.heappush(heap, (count, value))
        evicted = heapq.heappop(heap) if len(heap) > k else None
        print(f"push ({count},{value})  evicted={evicted}  heap={sorted(heap)}")
    return [v for _, v in heap]

assert sorted(topk_trace([1, 1, 1, 2, 2, 3], 2)) == [1, 2]
```

```text
counts: {1: 3, 2: 2, 3: 1}
push (3,1)  evicted=None  heap=[(3, 1)]
push (2,2)  evicted=None  heap=[(2, 2), (3, 1)]
push (1,3)  evicted=(1, 3)  heap=[(2, 2), (3, 1)]
```

第三行：压入 `(1, 3)` 后堆里有 3 个，弹出最小的 `(1, 3)`——次数最少的 3 被淘汰，留下 `{1, 2}`。

再看 LC 295 的两个堆（流 `5, 2, 8, 1`）：

```python
import heapq

def median_trace(stream):
    low, high = [], []          # low: max-heap (negated), high: min-heap
    for x in stream:
        heapq.heappush(low, -x)
        heapq.heappush(high, -heapq.heappop(low))
        if len(high) > len(low):
            heapq.heappush(low, -heapq.heappop(high))
        med = float(-low[0]) if len(low) > len(high) else (-low[0] + high[0]) / 2
        print(f"add {x}: low(max-heap)={sorted((-v for v in low), reverse=True)} high(min-heap)={sorted(high)} median={med}")

median_trace([5, 2, 8, 1])
```

```text
add 5: low(max-heap)=[5] high(min-heap)=[] median=5.0
add 2: low(max-heap)=[2] high(min-heap)=[5] median=3.5
add 8: low(max-heap)=[5, 2] high(min-heap)=[8] median=5.0
add 1: low(max-heap)=[2, 1] high(min-heap)=[5, 8] median=3.5
```

不变量：`len(low)` 等于 `len(high)` 或多 1；`low` 里所有数 ≤ `high` 里所有数。所以奇数个时中位数是 `low` 的堆顶，偶数个时是两个堆顶的平均。`add_num` 的写法「先压进 low、再把 low 的最大弹到 high、不平衡再弹回来」可以不用分情况就保持第二条性质。

## 4. 题目

```python
import heapq
from collections import Counter


class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next
```

### 4.1 LC 347 · Top K Frequent Elements（Medium，频率 75）

```python
# solutions/347_top_k_frequent_elements.py
def top_k_frequent(nums, k):
    freq = Counter(nums)
    heap = []                                   # min-heap of (count, value), never more than k items
    for value, count in freq.items():
        heapq.heappush(heap, (count, value))
        if len(heap) > k:
            heapq.heappop(heap)                 # evict the least frequent of the k+1
    return [value for _, value in heap]


def top_k_frequent_buckets(nums, k):
    freq = Counter(nums)
    buckets = [[] for _ in range(len(nums) + 1)]   # buckets[c] = values that appear c times
    for value, count in freq.items():
        buckets[count].append(value)
    out = []
    for count in range(len(nums), 0, -1):
        for value in buckets[count]:
            out.append(value)
            if len(out) == k:
                return out
    return out
```

- **一句话洞见**：大小为 k 的最小堆，以次数为键；桶排序版本利用「次数 ≤ n」做到 O(n)。
- **复杂度**：堆版本 O(n + m log k)，空间 O(m)；桶版本 O(n)。

**资深追问**

- **规模 ×1000**：`Counter` 要 O(distinct) 内存。分布式**必须先按 key 分区再统计**：每台机器的「局部 top-k」合并**不是**全局 top-k（一个全局热门的 key 可能在每台机器上都排不进前 k）。正确做法：shuffle 到同一个 key 的机器上算出精确次数，再各自取局部 top-k，最后合并 k·P 个候选。
- **流式输入**：key 种类无限时用近似算法：Count-Min Sketch + 堆，或 Misra-Gries / Space-Saving（保证出现频率 > n/k 的元素一定被找出来），内存 O(k)。
- **内存**：精确答案必须记录所有 key 的计数；近似答案可以 O(k) 内存。
- **并发**：多线程写同一个 `Counter` 要加锁；更好的做法是线程本地计数 + 最后合并（或分片锁）。
- **接口**：并列怎么处理（返回任意 k 个还是需要稳定排序规则）？`k > 不同元素数` 返回全部；返回顺序是否要求按次数降序？
- **测试**：并列、`k` 等于不同值个数、全相同、负数；与「按次数排序取前 k」的暴力对比时要注意并列的顺序不确定，比较**次数的多重集**而不是值的顺序。

### 4.2 LC 767 · Reorganize String（Medium，频率 78）

```python
# solutions/767_reorganize_string.py
def reorganize_string(s):
    heap = [(-c, ch) for ch, c in Counter(s).items()]      # max-heap via negated counts
    heapq.heapify(heap)
    out = []
    held = None                                            # (neg_count, ch) used last step, not yet reusable
    while heap or held:
        if not heap:                                       # only the held char is left -> would be adjacent
            return ""
        neg, ch = heapq.heappop(heap)
        out.append(ch)
        if held:
            heapq.heappush(heap, held)                     # now it's no longer adjacent to itself
            held = None
        if neg + 1 < 0:                                    # still has copies left
            held = (neg + 1, ch)
    return "".join(out)
```

- **一句话洞见**：每一步放当前剩余次数最多、且不等于上一个放的字符；用最大堆取最多的，刚用过的字符先「扣留」一步再放回。不可行当且仅当某字符次数 > `(n+1)//2`。
- **复杂度**：时间 O(n log a)（a = 字符集大小，常数很小），空间 O(a)。
- **另一种解法**：先按次数降序，把字符依次填入偶数下标 0, 2, 4…，再填奇数下标，O(n)。

**资深追问**

- **规模 ×1000**：字符集小，堆操作近似 O(1)，整体 O(n)；用填偶数 / 奇数下标法完全没有堆。
- **流式**：全局排列需要知道所有字符的频率，无法在纯流式中做；可以做滑动窗口版（任务调度，LC 621 的冷却时间）。
- **内存**：O(a) 计数 + 输出 O(n)。
- **并发**：串行贪心；多个独立字符串可并行。
- **接口**：多个合法答案时返回哪一个（任意 / 字典序最小）？不可能时返回 `""`。如果要求字典序最小，堆的键要改为 `(−count, ch)` 并重新证明正确性。
- **测试**：**不要比较具体输出**，用性质检验——相邻字符不同、多重集与原串一致；不可行的用例 `aaab`、`aaaaabbc`；刚好可行的边界 `aaaabbc`（a 占 4/7）；单字符。

### 4.3 LC 23 · Merge k Sorted Lists（Hard，频率 75）

```python
# solutions/23_merge_k_sorted_lists.py
def merge_k_lists(lists):
    heap = []
    for i, node in enumerate(lists):
        if node:
            heapq.heappush(heap, (node.val, i, node))    # i breaks ties: ListNode is not comparable
    dummy = tail = ListNode()
    while heap:
        _, i, node = heapq.heappop(heap)
        tail.next = node
        tail = node
        if node.next:
            heapq.heappush(heap, (node.next.val, i, node.next))
    return dummy.next
```

- **一句话洞见**：堆里永远放 k 个链表各自的「当前头」，弹出最小的，把它的 `next` 压进去。
- **tie-breaker**：`(val, i, node)` 里的 `i` 是必须的——值相同时 Python 会去比较 `node`，而 `ListNode` 不可比较，抛 `TypeError`。
- **复杂度**：时间 O(N log k)（N 为总节点数），空间 O(k)。
- **替代**：两两分治合并（merge sort 的合并树）同样 O(N log k)，并且不需要堆，空间 O(1)（链表），见第 08 讲的 LC 21。

**资深追问**

- **规模 ×1000**：k 个有序文件各自 GB 级：这就是外排序的归并阶段——每个文件一个读缓冲，堆里只放当前头，内存 O(k · 缓冲区)。k 太大（一次打不开那么多文件）则多趟归并，每趟合并 100 路。
- **流式**：k 个流在线合并，输出也是流；要处理「某个流暂时没有数据」——阻塞等待还是跳过取决于有序性语义（水位线 watermark）。
- **内存**：链表版本复用原节点（不拷贝），额外内存只有堆。
- **并发**：并行归并树——把 k 个列表分成多组并行两两合并；堆版本是串行的。
- **接口**：节点是复用还是拷贝（是否允许改输入）？允许 `None` 元素和空列表；值相同时是否要求稳定（先出现的列表先出）——`i` 作为 tie-breaker 恰好保证稳定。
- **测试**：空列表、全 `None`、含 `None`、重复值（测试 tie-breaker）、一条很长其他很短；与排序所有节点的暴力对拍。

### 4.4 LC 295 · Find Median from Data Stream（Hard，频率 63）

```python
# solutions/295_find_median_from_data_stream.py
class MedianFinder:
    def __init__(self):
        self.low = []     # max-heap (store negatives): the smaller half
        self.high = []    # min-heap: the larger half; invariant len(low) in {len(high), len(high)+1}

    def add_num(self, num):
        heapq.heappush(self.low, -num)
        heapq.heappush(self.high, -heapq.heappop(self.low))   # push through low so ordering low <= high holds
        if len(self.high) > len(self.low):                    # rebalance: low may hold one extra
            heapq.heappush(self.low, -heapq.heappop(self.high))

    def find_median(self):
        if len(self.low) > len(self.high):
            return float(-self.low[0])
        return (-self.low[0] + self.high[0]) / 2
```

- **一句话洞见**：中位数把数据分成「较小一半」和「较大一半」；最大堆装前者、最小堆装后者，中位数就在两个堆顶。
- **复杂度**：`add_num` O(log n)，`find_median` O(1)，空间 O(n)。

**资深追问**

- **规模 ×1000**：存全部数据 O(n) 内存不可行时：值域小（例如 0..100 的整数）→ 计数数组，O(1) 内存、O(值域) 查询（这是原题的官方追问；99% 的数在 0..100，其余放两个溢出计数器）；一般情况用分位数草图（quantile sketch：GK、t-digest），可合并、近似。
- **流式**：这题本身就是流式；加上「删除」或「滑动窗口中位数」（LC 480）需要懒删除（lazy deletion）或有序结构（`SortedList`）。
- **内存**：精确中位数必须保留全部数据（信息论下界）；近似可以 O(1/ε)。
- **并发**：多个生产者线程写入：加锁，或每个线程一个本地结构、定期合并（草图可合并，两个堆合并要重新插入）。
- **接口**：偶数个时返回 `float`（均值）；空流调用 `find_median` 要抛异常还是返回 `None`（本题保证非空，面试中要问）；数据类型整数 / 浮点？
- **测试**：每次插入后与 `sorted` 列表的中位数对拍（文件里已有）；重复值、负数、单个元素、递增 / 递减输入。

## 5. 常见 bug

1. **以为 `heapq` 是最大堆**：它是最小堆；最大堆存 `-x`。弹出后别忘了再取负。
2. **堆里放不可比较对象**：`(val, node)` 值相同时比较 `node` 报 `TypeError`；加唯一序号。
3. **求最大的 k 个却用最大堆**：要放全部 n 个；应该用大小为 k 的最小堆。
4. **`heappush` 后再 `heappop` 想弹出刚压入的**：`heappop` 弹的是最小值，不是刚压入的那个。
5. **堆里的元素被外部修改**：堆不会重新排序。需要「改优先级」就用懒删除（再压一个新的，弹出时丢弃过期的）。
6. **对 `heap` 列表直接排序或切片当作有序序列**：堆数组只保证父 ≤ 孩子，不是有序的；只有 `heap[0]` 是最小值。
7. **在两个堆的中位数里忘记平衡**：`len(low) - len(high)` 必须在 {0, 1}。

## 6. 自测题

1. `heapify` 为什么是 O(n) 而不是 O(n log n)？
   <details><summary>答案</summary>叶子占一半，不需要下沉；倒数第二层最多下沉 1 层……下沉距离越远的节点越少，求和 ∑ (层高 × 该层节点数) 收敛为 O(n)。</details>
2. 为什么求「最大的 k 个」要用最小堆？
   <details><summary>答案</summary>堆顶表示这 k 个里最弱的一个（门槛）；新元素只需与门槛比较，不够强直接丢弃；用最大堆就得存全部元素。</details>
3. LC 23 的堆元组 `(val, i, node)` 里去掉 `i` 会怎样？
   <details><summary>答案</summary>当两个节点值相同，Python 会比较第三项 `node`，`ListNode` 没有 `__lt__`，抛 `TypeError`。</details>
4. 小编程：返回数组中第 k 大的元素（LC 215）。
   <details><summary>答案</summary>`heap = []`；`for x in nums: heappush(heap, x); if len(heap) > k: heappop(heap)`；返回 `heap[0]`。O(n log k)。（面试官也可能追问 Quickselect，平均 O(n)、最坏 O(n²)。）</details>
5. 两个堆求中位数时，如果新来的数比 `low` 的堆顶还小，应该放哪个堆？
   <details><summary>答案</summary>放 `low`（较小的一半）。题解中「先压 low、再弹到 high、再平衡」的写法让这个判断自动完成。</details>
6. 资深追问：1000 台机器各自有一个日志文件，找全局出现次数最多的 10 个 URL。
   <details><summary>答案</summary>先按 URL 哈希分区（shuffle），让相同 URL 落到同一台机器并汇总成精确次数；每台机器用大小 10 的堆取局部 top-10；最后合并 1000×10 个候选再取 top-10。直接让每台机器先取本地 top-10 再合并是错的。可选：先 Count-Min Sketch 估计，找候选再精确计数。</details>
