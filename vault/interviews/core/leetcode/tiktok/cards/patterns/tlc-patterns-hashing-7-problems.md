---
id: tlc-patterns-hashing-7-problems
node: patterns.hashing
type: qa
step: 7
---
## Q
**哈希（Hashing）｜本组用到哈希的题**

按变形分类，这个题组里哪些题的核心是哈希？

## A
**补数 / 先查后存**
- LC 1 两数之和
- LC 560 和为 K 的子数组（前缀和 + 哈希）
- LC 974 和可被 K 整除的子数组（前缀和模 `k` 做键）

**频次 / 计数**
- LC 347 前 K 个高频元素（`Counter` + 堆或桶）
- LC 438 找到字符串中所有字母异位词（窗口计数）
- LC 76 最小覆盖子串（需求计数）
- LC 2456 最流行的视频创作者（字典聚合 + 取最大）

**签名分组**
- LC 49 字母异位词分组
- LC 694 不同岛屿的数量（形状签名）

**集合 / 存在性**
- LC 128 最长连续序列
- LC 939 最小面积矩形（点集）
- LC 3 无重复字符的最长子串（字典记最近位置）

**哈希 + 其他结构**
- LC 146 LRU 缓存（哈希 + 链表）
- LC 380 O(1) 时间插入、删除和获取随机元素（哈希 + 数组）
- LC 133 克隆图（哈希：旧节点 → 新节点）

模板提示：看到「内层在找某个值」就把它改成字典查询；看到「按某种等价分类」就想签名；看到「连续」且含负数就想前缀和 + 哈希。

**例题：** LC 1 两数之和

整数数组 `nums` 和 `target`，找出和为 `target` 的两个不同元素，返回它们的下标（保证恰有一个答案）。`2 <= nums.length <= 10^4`，`-10^9 <= nums[i], target <= 10^9`。

```python
def two_sum(nums: list[int], target: int) -> list[int]:
    seen: dict[int, int] = {}                  # 值 -> 下标
    for i, x in enumerate(nums):
        if (j := seen.get(target - x)) is not None:   # 先查：只会匹配到前面的元素
            return [j, i]
        seen[x] = i                            # 后存：自己不会和自己配对
    return []
```

**例题：** LC 560 和为 K 的子数组

整数数组 `nums` 和 `k`，统计和为 `k` 的连续非空子数组的个数。`1 <= nums.length <= 2 * 10^4`，`-1000 <= nums[i] <= 1000`，`-10^7 <= k <= 10^7`。

```python
from collections import Counter
def subarray_sum(nums: list[int], k: int) -> int:
    seen = Counter({0: 1})        # 前缀和 -> 出现次数；空前缀的和是 0
    pre = ans = 0
    for x in nums:
        pre += x
        ans += seen[pre - k]      # 以当前位置结尾、和为 k 的子数组个数
        seen[pre] += 1
    return ans
```

**例题：** LC 974 和可被 K 整除的子数组

整数数组 `nums` 和 `k`，统计和可被 `k` 整除的连续非空子数组的个数。`1 <= nums.length <= 3 * 10^4`，`-10^4 <= nums[i] <= 10^4`，`2 <= k <= 10^4`。

```python
from collections import Counter
def subarrays_div_by_k(nums: list[int], k: int) -> int:
    seen = Counter({0: 1})                  # 前缀和模 k 的出现次数；空前缀的余数是 0
    prefix = ans = 0
    for x in nums:
        prefix = (prefix + x) % k           # Python 的 % 对负数也返回 [0, k)，不用再补 + k
        ans += seen[prefix]                 # 以当前位置结尾、余数相同的前缀每个对应一个合法子数组
        seen[prefix] += 1
    return ans
```

**例题：** LC 347 前 K 个高频元素

整数数组 `nums` 和 `k`，返回出现频率前 `k` 高的元素（任意顺序，答案唯一）。`1 <= nums.length <= 10^5`，`-10^4 <= nums[i] <= 10^4`，要求优于 `O(n log n)`。

```python
from collections import Counter
def top_k_frequent(nums: list[int], k: int) -> list[int]:
    count = Counter(nums)
    buckets: list[list[int]] = [[] for _ in range(len(nums) + 1)]   # 下标 = 出现次数
    for x, c in count.items():
        buckets[c].append(x)
    ans: list[int] = []
    for bucket in reversed(buckets):          # 从高频到低频
        ans.extend(bucket)
        if len(ans) >= k:
            return ans[:k]
    return ans
```

**例题：** LC 438 找到字符串中所有字母异位词

字符串 `s` 和 `p`，返回 `s` 中所有 `p` 的异位词子串的起始下标。`1 <= s.length, p.length <= 3 * 10^4`，只含小写字母。

```python
def find_anagrams(s: str, p: str) -> list[int]:
    m = len(p)
    need = Counter(p)             # need[c]：窗口里还缺几个 c；负数表示多了
    unbalanced = len(need)        # need[c] != 0 的字母种数；为 0 就是异位词
    ans: list[int] = []
    def shift(c: str, d: int) -> int:
        """窗口增减一个 c，返回 unbalanced 的变化量。"""
        was = need[c] != 0
        need[c] += d
        return (need[c] != 0) - was
    for right, ch in enumerate(s):
        unbalanced += shift(ch, -1)               # 右端进窗口：少缺一个 ch
        if right >= m:
            unbalanced += shift(s[right - m], +1)  # 左端出窗口：多缺一个
        if unbalanced == 0:
            ans.append(right - m + 1)
    return ans
```

**例题：** LC 76 最小覆盖子串

字符串 `s` 和 `t`，返回 `s` 中包含 `t` 全部字符（含重复次数）的最短子串，没有则返回 `""`。`1 <= s.length, t.length <= 10^5`，由大小写字母组成。

```python
from collections import Counter
def min_window(s: str, t: str) -> str:
    need = Counter(t)                              # need[ch] > 0 表示还缺 ch；< 0 表示窗口里多出来
    missing = len(t)                               # 还缺的字符总数（含重复）
    best_l, best_len = 0, len(s) + 1
    left = 0
    for right, ch in enumerate(s):
        if need[ch] > 0:
            missing -= 1
        need[ch] -= 1
        if missing == 0:                           # 窗口已经覆盖 t：尽量收缩左端
            while need[s[left]] < 0:               # 左端字符是多余的，丢掉
                need[s[left]] += 1
                left += 1
            if right - left + 1 < best_len:
                best_l, best_len = left, right - left + 1
            need[s[left]] += 1                     # 再丢一个必需字符，窗口重新变得不完整
            missing += 1
            left += 1
    return "" if best_len > len(s) else s[best_l : best_l + best_len]
```

**例题：** LC 2456 最流行的视频创作者

`creators[i]`、`ids[i]`、`views[i]` 描述第 `i` 个视频。创作者的流行度是其视频播放量之和。返回流行度最高的所有创作者，以及各自播放量最高的视频 id（并列取字典序最小）。`1 <= n <= 10^5`，`0 <= views[i] <= 10^5`。

```python
from collections import defaultdict
def most_popular_creator(creators: list[str], ids: list[str], views: list[int]) -> list[list[str]]:
    popularity: defaultdict[str, int] = defaultdict(int)
    best_video: dict[str, tuple[int, str]] = {}    # 创作者 -> (-播放量, id)，元组越小越好
    for creator, vid, view in zip(creators, ids, views):
        popularity[creator] += view
        candidate = (-view, vid)                   # 播放量大优先，并列取字典序小的 id
        if creator not in best_video or candidate < best_video[creator]:
            best_video[creator] = candidate
    top = max(popularity.values())
    return [[c, best_video[c][1]] for c, total in popularity.items() if total == top]
```

**例题：** LC 49 字母异位词分组

字符串数组 `strs`，把字母异位词分到同一组，按任意顺序返回。`1 <= strs.length <= 10^4`，`0 <= strs[i].length <= 100`，只含小写字母。

```python
from collections import defaultdict
def group_anagrams(strs: list[str]) -> list[list[str]]:
    groups: defaultdict[tuple[int, ...], list[str]] = defaultdict(list)
    for s in strs:
        count = [0] * 26                       # 26 个字母的出现次数就是指纹
        for ch in s:
            count[ord(ch) - ord("a")] += 1
        groups[tuple(count)].append(s)         # list 不可哈希，转成 tuple 才能当键
    return list(groups.values())
```

**例题：** LC 694 不同岛屿的数量

0/1 网格里四连通的 `1` 构成岛屿，统计形状互不相同的岛屿数（只允许平移重合，不能旋转或翻转）。`1 <= m, n <= 50`。

```python
def num_distinct_islands(grid: list[list[int]]) -> int:
    rows, cols = len(grid), len(grid[0])
    seen = [[False] * cols for _ in range(rows)]
    shapes: set[frozenset[tuple[int, int]]] = set()
    for r0 in range(rows):
        for c0 in range(cols):
            if grid[r0][c0] != 1 or seen[r0][c0]:
                continue
            # (r0, c0) 是行优先扫描遇到的第一格，也就是这座岛最靠上、同行最靠左的格子
            seen[r0][c0] = True
            stack = [(r0, c0)]
            cells: list[tuple[int, int]] = []
            while stack:
                r, c = stack.pop()
                cells.append((r - r0, c - c0))     # 相对起点的偏移 = 平移不变量
                for nr, nc in ((r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)):
                    if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == 1 and not seen[nr][nc]:
                        seen[nr][nc] = True
                        stack.append((nr, nc))
            shapes.add(frozenset(cells))           # 无序的格子集合：与遍历顺序无关
    return len(shapes)
```

**例题：** LC 128 最长连续序列

未排序整数数组 `nums`，求数值连续的最长序列的长度，要求 `O(n)`。`0 <= nums.length <= 10^5`，`-10^9 <= nums[i] <= 10^9`。

```python
def longest_consecutive(nums: list[int]) -> int:
    seen = set(nums)                   # 去重 + O(1) 查询
    best = 0
    for x in seen:
        if x - 1 in seen:              # x 不是序列的起点：跳过，让起点去数
            continue
        end = x + 1
        while end in seen:             # 从起点向右数下去
            end += 1
        best = max(best, end - x)
    return best
```

**例题：** LC 939 最小面积矩形

平面上互不相同的点 `points`，求以这些点为顶点、边平行于坐标轴的矩形的最小面积，不存在返回 `0`。`1 <= points.length <= 500`，`0 <= xi, yi <= 4 * 10^4`。

```python
from itertools import combinations
def min_area_rect(points: list[list[int]]) -> int:
    pts = [tuple(p) for p in points]       # 列表不可哈希，转成元组
    seen = set(pts)
    areas = (
        abs(x1 - x2) * abs(y1 - y2)
        for (x1, y1), (x2, y2) in combinations(pts, 2)
        if x1 != x2 and y1 != y2 and (x1, y2) in seen and (x2, y1) in seen   # 另外两个角也在
    )
    return min(areas, default=0)           # 没有矩形时返回 0
```

**例题：** LC 3 无重复字符的最长子串

求字符串 `s` 中不含重复字符的最长子串的长度。`0 <= s.length <= 10^5`。

```python
def length_of_longest_substring(s: str) -> int:
    last: dict[str, int] = {}          # 字符 -> 它最近一次出现的下标
    best = left = 0                    # 窗口是 s[left : right + 1]
    for right, ch in enumerate(s):
        if last.get(ch, -1) >= left:   # ch 在窗口内出现过：左端直接跳过去
            left = last[ch] + 1
        last[ch] = right
        best = max(best, right - left + 1)
    return best
```

**例题：** LC 146 LRU 缓存

设计 `LRUCache(capacity)`：`get(key)` 命中返回值、否则返回 `-1`；`put(key, value)` 写入或更新，写入后键数超过 `capacity` 就逐出最久未使用的键。两个操作平均 `O(1)`。`1 <= capacity <= 3000`，最多调用 `2 * 10^5` 次。

```python
class Node:
    __slots__ = ("key", "val", "prev", "next")
    def __init__(self, key: int = 0, val: int = 0) -> None:
        self.key, self.val = key, val
        self.prev: Node | None = None
        self.next: Node | None = None
class LRUCache:
    def __init__(self, capacity: int) -> None:
        self.cap = capacity
        self.map: dict[int, Node] = {}
        self.head, self.tail = Node(), Node()      # 哨兵：head.next 是最近使用，tail.prev 是最久未使用
        self.head.next, self.tail.prev = self.tail, self.head
    def _unlink(self, node: Node) -> None:
        node.prev.next, node.next.prev = node.next, node.prev
    def _push_front(self, node: Node) -> None:
        node.prev, node.next = self.head, self.head.next
        self.head.next.prev = node
        self.head.next = node
    def get(self, key: int) -> int:
        if key not in self.map:
            return -1
        node = self.map[key]
        self._unlink(node)                         # 摘下来再放到最前面 = 标记为刚用过
        self._push_front(node)
        return node.val
    def put(self, key: int, value: int) -> None:
        if key in self.map:
            node = self.map[key]
            node.val = value
            self._unlink(node)
            self._push_front(node)
            return
        if len(self.map) == self.cap:              # 满了：逐出链表尾部（最久未使用）
            lru = self.tail.prev
            self._unlink(lru)
            del self.map[lru.key]
        node = self.map[key] = Node(key, value)
        self._push_front(node)
```

**例题：** LC 380 O(1) 时间插入、删除和获取随机元素

实现 `RandomizedSet`：`insert(val)` 不存在时插入并返回 `true`；`remove(val)` 存在时删除并返回 `true`；`getRandom()` 等概率返回现有元素之一。每个操作平均 `O(1)`，调用 `getRandom` 时集合非空，最多 `2 * 10^5` 次调用。

```python
import random
class RandomizedSet:
    def __init__(self) -> None:
        self.items: list[int] = []         # 紧凑数组：getRandom 按下标 O(1) 取
        self.pos: dict[int, int] = {}      # 值 -> 它在 items 里的下标
    def insert(self, val: int) -> bool:
        if val in self.pos:
            return False
        self.pos[val] = len(self.items)
        self.items.append(val)
        return True
    def remove(self, val: int) -> bool:
        if (i := self.pos.pop(val, None)) is None:
            return False
        last = self.items.pop()            # 先弹出末尾，数组保持紧凑
        if i < len(self.items):            # val 不在末尾：把 last 填进空出的 i
            self.items[i] = last
            self.pos[last] = i
        return True
    def getRandom(self) -> int:
        return random.choice(self.items)
```

**例题：** LC 133 克隆图

给无向连通图中一个节点的引用，返回整张图的深拷贝（每个节点有 `val` 和 `neighbors`）。节点数 `0..100`，`val` 互不相同，无重边、无自环。

```python
def clone_graph(node: Node | None) -> Node | None:
    copies: dict[Node, Node] = {}              # 原节点 -> 它的拷贝，同时充当 visited
    def dfs(cur: Node) -> Node:
        if cur in copies:
            return copies[cur]                 # 已经克隆过：直接复用，环到这里就断了
        copies[cur] = clone = Node(cur.val)    # 先登记再递归邻居，遇到环才不会死循环
        clone.neighbors = [dfs(nb) for nb in cur.neighbors]
        return clone
    return dfs(node) if node else None
```
