# 前置课 01 · Java 程序员的 Python 面试写法

> 目标：你会 Java/Kotlin，Python 语法不是问题，但**面试节奏下最快的写法**和你的肌肉记忆不一样。这篇只讲"电面/OA 40 分钟内你会用到的那 20%"，不是 Python 教程。例子尽量对照 `../../problems/`、`../../loop/rounds/04_ood/` 里的真实 solution.py 写法。

---

## 1. `collections`：别用 Java 的思维手写计数器/队列

| Java 你会写 | Python 面试里直接用 |
|---|---|
| `Map<K,Integer>` 手动 `getOrDefault` 累加 | `collections.Counter(iterable)` |
| `Map<K,List<V>>` 手动 `computeIfAbsent` | `collections.defaultdict(list)` |
| `LinkedList` 当双端队列 | `collections.deque`（`popleft()`/`append()` 都是 O(1)，普通 `list.pop(0)` 是 O(n)——**这是电面里最容易犯的性能错误**）|
| `LinkedHashMap` 做 LRU | `collections.OrderedDict`（`move_to_end`/`popitem(last=False)`，见 `../00-essentials/04-class-design-and-concurrency.md` §4）|

```python
from collections import defaultdict, deque, Counter

adj = defaultdict(list)          # 图的邻接表，不用先判断 key 存不存在
adj["a"].append("b")

dq = deque([1, 2, 3])
dq.appendleft(0); dq.popleft()   # O(1)，不要用 list

freq = Counter(["a", "b", "a"])  # Counter({'a': 2, 'b': 1})
```

**易错**：`Counter` 的 `.most_common(k)` 平手顺序是"先出现的先返回"，不是字典序——需要字典序 tie-break 时要自己 `sorted(freq.items(), key=lambda kv: (-kv[1], kv[0]))`。

---

## 2. `heapq`：只有最小堆，没有 comparator

Java 的 `PriorityQueue<>(comparator)` 在 Python 里没有直接等价物——`heapq` 只维护**元组的字典序最小值**，想要"最大堆"或"自定义比较"都是**把比较键编码进元组**。

```python
import heapq

heap = []
heapq.heappush(heap, (-priority, timestamp, task_id))   # 取负数模拟最大堆
neg_priority, ts, tid = heapq.heappop(heap)              # 弹出优先级最高的

# 惰性删除（懒删除堆，见 04-class-design-and-concurrency.md §2）：
# 不物理删除过期条目，弹出时检查是否仍然有效，无效就继续弹
```

**易错**：
- 元组比较是逐位比较，第一位相同才看第二位——这正是 tie-break 链的实现方式（先按 `-priority`，再按 `timestamp`，再按 `task_id`），不需要写 comparator 函数。
- `heapq` 不支持 decrease-key；要更新优先级，标准做法是懒删除（推新条目 + 弹出时判过期），不是 Java 里 `PriorityQueue.remove()` 那种物理删除再插入。

---

## 3. `bisect`：有序数组上的二分，别手写 `while lo < hi`

Java 你可能会手写二分或用 `Collections.binarySearch`。Python 标准库直接给你三个函数，**面试里手写二分反而是减分项**（除非题目是"在答案空间上二分"，见 `../00-essentials/02-dp-patterns.md` 或 Stripe 的 `08-algorithm-patterns.md` §3）。

```python
from bisect import bisect_left, bisect_right, insort

a = [1, 3, 3, 5]
bisect_left(a, 3)     # 2 -- 第一个 >= 3 的位置
bisect_right(a, 3)    # 4 -- 第一个 > 3 的位置（也是"3 出现次数"的右边界）
insort(a, 4)          # 原地插入并保持有序：a == [1, 3, 3, 4, 5]
```

**本 kit 的真实用法**：
- `q04`（加权区间调度）：`bisect_right(ends, starts[i-1], 0, i-1)` 找最晚的不冲突前驱。
- `q05`（Paint the Ceiling）：`bisect_right(sides, a // x)` 数满足 `x*y <= a` 的 `y` 的个数。
- `od06`（审计日志）：`bisect.insort` 处理**乱序到达**的访问事件，`bisect_left` 做时间范围查询的双指针。

**易错**：`bisect_left`/`bisect_right` 只在**已排序**数组上有意义，插入新元素后数组仍保持有序才能继续用（`insort` 保证这一点，普通 `append` 不保证）。

---

## 4. `dataclass`：比手写 `__init__` 快，比裸 tuple 可读

Java 的 record / POJO 对应 Python 的 `dataclass`。面试里权衡：**tuple 更快打，dataclass 更可读**——40 分钟的题用 tuple 也够，OOD 题（类设计本身就是考点）应该用 dataclass 或普通类。

```python
from dataclasses import dataclass, field

@dataclass
class Task:
    task_id: str
    priority: int
    timestamp: int
    version: int = 0            # 默认值，可变默认值要用 field(default_factory=list)
```

**易错**：`@dataclass` 默认生成的 `__eq__` 按字段值比较，不是按对象身份——如果要把 `Task` 放进 `set`/当 `dict` 的 key，要么保证它 `frozen=True`（不可变才能 hash），要么改用元组当 key。

---

## 5. `itertools`：小范围枚举/分组，别手写嵌套循环

```python
from itertools import product, combinations, groupby

list(product("01", repeat=3))          # 长度 3 的 0/1 全排列，n <= ~20 时可用
list(combinations([1,2,3], 2))         # [(1,2),(1,3),(2,3)]

for key, group in groupby(sorted(items, key=f), key=f):   # 必须先按同一个 key 排序
    ...
```

**易错**：`groupby` **不会**自动分组不连续的相同 key——它只把"连续"出现的相同 key 分到一组，用之前必须先按同一个 key 排序，这是 Java 的 `Collectors.groupingBy` 不需要操心但 Python 的 `groupby` 会踩的坑。

---

## 6. 递归限制：Python 默认 1000 层，Java 的调用栈默认深得多

Java 默认栈大小是 MB 级别，递归几千层通常没事；Python 的 `sys.setrecursionlimit()` 默认 1000，**树/链表题输入规模大时会直接 `RecursionError`**。

```python
import sys
sys.setrecursionlimit(20000)     # q03 part3 的做法：链状树最深可能到几千层
```

**更稳的做法是改写成迭代**（`q03` part3 的 `_compute_height` 用显式栈做后序遍历，不递归）：

```python
stack = [(root, False)]
while stack:
    node, processed = stack.pop()
    if processed:
        # 后序处理 node
        ...
    else:
        stack.append((node, True))
        for child in children[node]:
            stack.append((child, False))
```

**面试里的判断标准**：n ≤ 数百，递归写起来更快、更清楚，直接写；n 可能上万或题面暗示"链状/退化树"，主动说"我会改写成迭代版本避免栈溢出"，即使不写也要说出口（对应 `../00-essentials/01-solving-framework.md` §5① 压复杂度类 follow-up）。

---

## 7. 读 stdin：本 kit 所有题目共用的解析纪律

Snowflake 的 OA/电面题不是 LeetCode 式"函数签名已经写好"，是**从 stdin 读文本自己解析**——这是 Java 选手最容易在"业务逻辑都对但输出格式错"上丢分的地方。本 kit 每个 `solution.py` 的 `main()` 都遵循同一套模式：

```python
def main(stdin=sys.stdin, stdout=sys.stdout) -> None:
    lines = stdin.read().splitlines()          # 一次性读完，不用逐行 input()
    idx = 0
    while idx < len(lines) and not lines[idx].strip():   # 跳过空白分隔行
        idx += 1
    n = int(lines[idx].strip()); idx += 1
    values = [int(x) for x in lines[idx].split()] if idx < len(lines) else []
    idx += 1
    # ... 处理 ...
    stdout.write(f"{result}\n")                 # 显式换行，不依赖 print 的默认行为
```

**四条纪律**（对齐 Stripe `01-solving-framework.md` §4 的六件事，这里是 Python 实现层面）：
1. **`stdin.read().splitlines()` 一次性读完**，不要 `for line in sys.stdin` 和 `input()` 混用——后者在某些 judge 环境下缓冲行为不一致。
2. **每次取值前跳过空白行**（`while ... not lines[idx].strip(): idx += 1`），因为"n == 0 时数组行可能被省略"是本 kit 题面反复出现的坑（`q01`、`q03` 的 stdin 格式注释都写明了这一点）。
3. `main(stdin=sys.stdin, stdout=sys.stdout)` **接受参数而不是硬编码全局 `sys.stdin`**——这样测试代码可以传入 `io.StringIO` 直接断言输出，不需要真的起子进程。
4. 输出用 `stdout.write(... + "\n")`，**不要**用 `print()` 和 `write()` 混用在同一个函数里——容易在某一条分支上漏加换行符，Stripe 框架 §7 的交卷清单第一条就是这个。

**函数式测试的好处**：本 kit 的测试文件（`test_qNN.py`）都是直接调用 `part1(...)`/`part2(...)` 这些纯函数，不经过 stdin/stdout——**面试现场如果时间紧，先保证纯函数正确，`main()` 的 stdin 解析放最后写**，这也是 `01-solving-framework.md` §1 四段式骨架（parse/build/compute/render）的具体体现。

---

## 8. 自测

- [ ] 不看这篇，写出"惰性删除堆"的 push/pop 骨架（≤ 10 行）
- [ ] 说出 `bisect_left` 和 `bisect_right` 在等值元素场景下的区别
- [ ] 解释为什么 `groupby` 必须先排序
- [ ] 挑一道 `q0X` 题，只看它的 stdin 格式注释，自己写一遍 parse 函数
