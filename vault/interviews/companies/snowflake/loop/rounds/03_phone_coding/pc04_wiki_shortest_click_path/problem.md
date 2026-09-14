# pc04 · Wiki Shortest Click Path — BFS distance, lexicographically smallest reconstruction, lazy crawl with failures

**类型：** phone screen（40 min）· 3 part 递进 · 图 BFS + 路径重建
**最近：** 2026-09 · **置信度：** MED（Part1，见文末）/ 重建（Part2/3 的具体机制）

## 背景
"维基百科最短点击路径"是图 BFS 题里最经典的框架之一，Snowflake 电面池里两个聚合站都把它标记为
"BFS + 路径重建"（而不只是要距离）。本题在这个骨架上递进：Part1 只要最短距离，Part2 要求**在
所有最短路径里选字典序最小的那一条**——这比看起来更难：贪心地"每一步都选字典序最小的邻居"会在
死胡同前失败，必须先算出"每个节点到终点的最短距离"才能安全地贪心。Part3（重建）把"整张图已知"
换成"边要靠一个可能失败的 `fetch` 函数现抓"，模拟真实爬虫场景：抓取失败的页面当作死路跳过，但
要记录失败次数。

## API 契约（英文签名）
```python
def shortest_path_length(graph: dict[str, list[str]], start: str, end: str) -> int: ...

def shortest_path(graph: dict[str, list[str]], start: str, end: str) -> list[str]: ...

def crawl_shortest_path(
    fetch: Callable[[str], list[str]], start: str, end: str
) -> tuple[list[str], int]: ...
```
`graph[u]` 是页面 `u` 上的出链列表（**有向边**，"页面 A 链接到页面 B" 不代表 B 链接回 A）。

## 规则

### Part 1 — BFS 距离
`shortest_path_length(graph, start, end)`：从 `start` 到 `end` 的最短点击数（每次点击沿一条
有向边前进）。`start == end` → `0`；不可达 → `-1`。

### Part 2 — 重建路径，且要字典序最小
`shortest_path(graph, start, end)`：返回**所有**长度等于最短距离的路径里，把页面名依次拼起来
**字典序最小**的那一条（比较方式：逐个元素比较，`["A","B","D"]` 比 `["A","C","D"]` 小，因为
第二个元素 `"B" < "C"`）。**朴素贪心"每一步都选当前节点里字典序最小的邻居走"是错的**——它可能
一开始就贪心选中一个字典序更小、但通向死胡同（到不了 `end`，或要绕更远路）的邻居，需要走到头才
发现选错，而已经没有回头路（BFS 距离已定，不能简单回溯重选）。正确做法：先从 `end` 反着跑一次
BFS（沿反向边）算出**每个节点到 `end` 的最短距离**，再从 `start` 正向走，每一步只在"距终点的
距离恰好比当前节点少 1"的邻居里选字典序最小的——这样选中的邻居保证仍然在某条最短路径上。
不可达 → 空列表 `[]`。

### Part 3 — 现抓边的爬虫，抓取可能失败（重建）
`crawl_shortest_path(fetch, start, end)`：不再直接给整张图，而是给一个 `fetch(page) ->
list[str]` 函数——调用它才能拿到 `page` 的出链列表，且**这次调用可能抛异常**（模拟一次真实的
网络抓取失败）。BFS 爬取时：
- 一个页面的 `fetch` 失败，就把它当作**没有任何出链的死路**处理，**记一次失败次数**，但不能
  让整个爬取停下来——继续处理队列里其它已经发现、还没抓取的页面。
- 因为链接是现抓的、**没有整张图可以反向 BFS**，Part3 **不再保证**像 Part2 那样"全局字典序
  最小"——它只保证给出**某一条**最短路径（同一层里按字典序排序展开新页面、每个页面第一次被
  发现时就确定它的前驱，确定性可复现，但不是"通盘比较所有候选路径后选最小"的强保证）。这是一个
  刻意的、需要在面试里讲清楚的取舍：懒加载爬虫拿不到反向图，就没法用 Part2 的技巧。
- 返回 `(path, failure_count)`；`end` 在已成功抓取到的部分图里够不到时 `path` 是 `[]`
  （`failure_count` 仍然要正确统计）。

## Worked examples（全部由 `solution.py` 实际运行得出）

**例 1（Part1，基础 BFS 距离）**
```python
graph = {"A": ["B", "C"], "B": ["D"], "C": ["D"]}
shortest_path_length(graph, "A", "D")   # -> 2
shortest_path_length(graph, "D", "A")   # -> -1（有向边，反向不可达）
shortest_path_length(graph, "A", "A")   # -> 0
```

**例 2（Part2，死胡同陷阱：朴素贪心会先选错）**
```python
graph = {"A": ["B", "C"], "B": ["E"], "C": ["D", "F"], "F": ["D"], "E": []}
shortest_path(graph, "A", "D")
```
→ `["A", "C", "D"]`（最短距离是 2；如果贪心一开始就选字典序更小的 `B`（`B < C`），会走进
`B -> E` 这条死路——`E` 没有任何出链，到不了 `D`。正确算法先算出 `dist_to_end`：
`D=0, C=1, F=1, A=2`（`B`、`E` 都不在这张"到 D 的距离表"里，因为它们到不了 `D`），从 `A` 出发
时只有 `C` 满足"距终点距离比 A 少 1"，`B` 从一开始就被排除，不需要真的走进死路再回头）。

**例 3（Part2，真正的并列：两条等长路径，取字典序更小的）**
```python
graph = {"A": ["C", "B"], "B": ["D"], "C": ["D"]}
shortest_path(graph, "A", "D")
```
→ `["A", "B", "D"]`（`A->B->D` 和 `A->C->D` 都是长度 2 的最短路径，`"B" < "C"`，取前者——
即使 `graph["A"]` 里 `"C"` 排在 `"B"` 前面，输出顺序也不受输入邻接表顺序影响）。

**例 4（Part3，抓取失败逼出更长路径，且要计入失败次数）**
```python
graph = {"A": ["B", "C"], "B": ["D"], "C": ["E"], "E": ["D"]}

def fetch(page):
    if page == "B":
        raise RuntimeError("network error")
    return graph.get(page, [])

crawl_shortest_path(fetch, "A", "D")
```
→ `(["A", "C", "E", "D"], 1)`（如果 `B` 抓取成功，`A->B->D` 是长度 2 的最短路径；但 `B` 抓取
失败，被当成死路跳过，记 1 次失败，爬虫改走 `A->C->E->D`，长度 3）。**没有任何失败**（同一张图，
`fetch` 永不抛异常）时：`crawl_shortest_path(fetch_ok, "A", "D") -> (["A","B","D"], 0)`。

## `main()` 命令流
**Part1 / Part2** 首行之后：`e` / `e` 行 `"u v"` 有向边 / `"start end"`。Part1 输出一行整数
距离；Part2 输出一行逗号拼接的路径（不可达则输出空行）。

**Part3** 首行之后：`e` / `e` 行 `"u v"` 边（构成完整的图，`main()` 用它现造一个会失败的
`fetch`） / `f` / `f` 行页面名（这些页面的 `fetch` 会失败） / `"start end"`。输出两行：第一行
逗号拼接的路径（不可达输出 `"-"`），第二行失败次数。

## 边界清单
- `start == end` → Part1 输出 `0`，Part2/Part3 输出只含这一个页面的路径（`[start]`），即使
  `start` 在图里没有任何出边也是如此
- `end` 不可达 → Part1 `-1`，Part2 `[]`（空行），Part3 `[]`（输出 `"-"`），Part3 仍要正确统计
  期间发生的失败次数
- 死胡同陷阱（例2）：图里存在一个字典序更小、但通向死路的邻居，必须验证实现没有"贪心走一步就
  定终身"
- 真并列（例3）：两条不同的最短路径长度相同，必须按整条路径的字典序比较，不是"只看第一步"
  （构造一个"第一步字典序更大但整条路径更小"的反例：`A->["Bz","Ca"]`，`Bz->["Z"]`,
  `Ca->["D"]`——如果 `Z != end` 而 `D == end`，第一步选 `Bz`（更小）反而进了死路，必须选 `Ca`）
- Part3：`start` 自己 `fetch` 失败——`start==end` 时不应该需要 `fetch` 就能返回（边界：
  `start==end` 的检查必须在尝试 `fetch(start)` 之前）
- Part3：同一个页面在 BFS 里只应该被 `fetch` 一次（多条路径都指向同一个未访问页面时，不能重复
  抓取，既浪费也可能重复计入失败）
- 图为空、或 `start`/`end` 不在 `graph` 的任何 key/value 里出现过（视为孤立节点，不可达，除非
  `start==end`）

## 追问
1. "Part2 的反向 BFS 需要提前知道完整的反向图，如果图有 10 万个节点、边很稠密，构建反向图的
   内存开销你会怎么估计？"——期望候选人说清楚反向图和正向图的边数完全一样，只是方向反了，内存
   开销是 `O(V + E)`，不是额外的量级问题，但如果图本身就大到装不下，这条路径就走不通了，需要
   换成"不预建反向图、每次查询现场跑一次双向 BFS"之类的权衡。
2. "Part3 你说做不到全局字典序最小，那如果面试官坚持要这个保证，你会怎么做？"——期望候选人提出
   "先完整爬完可达的子图（把 fetch 的结果缓存下来），再对这个已知子图跑 Part2 的算法"，并指出
   代价是必须先把所有可达页面都抓一遍（不能中途因为找到一条路径就提前退出），爬取成本从
   "找到最短路径为止"变成"探索完整个连通分量"。
3. "生产环境里页面链接会变化，你会不会缓存 `fetch` 的结果？缓存多久算过期？"——开放式延伸，
   联系爬虫/缓存失效的常见讨论（TTL、按需失效、后台重新验证），不要求现场实现。

## 变体
- 来源明确点出"OA 与电面池都复用同一道 Wiki 点击路径题"（`catalog/raw/coding_phone_onsite.md`
  格式事实段），本题面向电面场景，Part2/Part3 的具体递进（字典序重建、带失败的懒爬取）是本题
  自行设计的延伸，原文只给出"BFS + 路径重建"这一层描述。

## 来源与置信度
- https://www.fastprep.io/problems/snowflake-web-crawler-shortest-path （Phone Screen,
  Graph/BFS，最近 2026-09）
- https://www.linkjob.ai/interview-questions/snowflake-software-engineer-interview/ ——独立提及
  "Web Crawler (BFS-based)" 作为电面编码例子（单独来看 LOW，与上一条合并为 MED）
- `catalog/raw/coding_phone_onsite.md` #5、`catalog/CATALOG.md` Table A pc04 行；置信度
  **MED**：两个来源仅给出标题级 + 标签级描述（"BFS over a crawled-page graph, then reconstruct
  the shortest path"），没有具体输入输出例子——本题的四个 worked example 均为按这条描述自行
  设计并用 `solution.py` 验证，Part2 的字典序重建技巧和 Part3 的失败模拟是本题在这条描述之上的
  具体化，标注为重建。

## 考什么
S05 图：BFS、最短路径重建、拓扑排序同族 · S08 复杂度/正确性权衡（贪心陷阱 vs 反向 BFS 预处理）
