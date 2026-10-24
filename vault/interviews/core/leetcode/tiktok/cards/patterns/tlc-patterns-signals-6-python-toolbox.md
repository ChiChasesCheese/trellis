---
id: tlc-patterns-signals-6-python-toolbox
node: patterns.signals
type: qa
step: 6
---
## Q
**模式识别｜每个模式对应的 Python 工具**

确定了模式之后，Python 标准库里有哪些现成工具，能把模板写短而且不容易出错？

## A
| 模式 | 工具 | 一句话 |
|---|---|---|
| 计数、查找、分组 | `Counter`、`defaultdict(list)`、`set` | 缺失键不用手判；`Counter` 可相减 / 比较 |
| 前缀和 | `itertools.accumulate(nums, initial=0)` | 一行得到 `n+1` 长度的前缀数组 |
| 滑动窗口 | `Counter`、`deque` | 窗口内计数；单调队列求窗口最值 |
| 二分 | `bisect_left/right`，`bisect_left(range(...), True, key=ok)` | 不手写边界；对答案二分一行 |
| 堆 / Top-K | `heapq`（`heappush`、`heappushpop`、`nlargest`、`merge`） | 最大堆存负数；元组带序号避免比较对象 |
| BFS | `deque` + `popleft` | 队列 `O(1)` 出队 |
| DFS / DP 递归 | `functools.cache`、显式栈 | 记忆化一行；深度大时改栈 |
| 区间 | `sorted(key=...)`、`pairwise` | 先按左端点排序，再比较相邻 |
| 排列 / 组合 | `itertools.permutations/combinations/product` | 暴力基准；小规模直接用 |
| 并查集 / Trie / 设计 | 自己写类，`dict` 当节点，`__slots__` 省内存 | 没有现成库 |
| 有序容器 | `sortedcontainers.SortedList`（可用时） | 增删查约 `O(log n)` |
| 数学 / 位 | `divmod`、`math.gcd`、`pow(a, b, mod)`、`int.bit_count()` | 内置函数代替手写循环 |

- 内置的 C 实现比手写 Python 循环快 10 倍以上；能用 `sum`、`max`、`sorted` 就用。
- 关键判断：**工具是否隐藏了面试要考的技术**。`bisect` 可以用，但被要求时能手写二分；`permutations` 不能代替回溯。
- 类型注解、清楚的变量名、局部函数 `def dfs(...)`，比一行写完的炫技更得分。
