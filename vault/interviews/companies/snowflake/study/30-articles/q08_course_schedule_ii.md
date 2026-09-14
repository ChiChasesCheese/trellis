# q08 · Course Schedule II：拓扑排序 + 按层 BFS 求最少学期，练的是"确定性 tie-break"

> [!tldr]
> - 这题考的是：LC 210 原题（Kahn 算法拓扑排序，最小堆保证输出唯一）+ 一个原创追问（按 BFS 分层求最少并行学期数，取自 LC1136 的题意）
> - 三步套路：建邻接表 + 入度数组 → Part 1 用最小堆代替普通队列做 Kahn 算法 → Part 2 把"逐个出队"改成"逐层出队"计数层数
> - 最值得带走的一个模式：**两个 part 故意用不同的编号方向和 0/1-indexed 约定**——这是本题设计上刻意保留的坑，写代码前先把两套约定分开写清楚

## 1. 题目在说什么（人话版）
Part 1 是 LeetCode 210 原题：给课程依赖关系，找一个可行的选课顺序（0-indexed，`[a,b]` 表示"a 需要
先修 b"），存在环就返回空列表；为了让输出唯一，规定"任意时刻能选的课里，永远选编号最小的"。

Part 2 是一个追问：每个学期能并行修任意多门课，只要它们的先修课都在更早的学期修完，求最少几个学期能
修完所有课（1-indexed，`[a,b]` 表示"a 必须先于 b"——方向和 Part 1 刚好相反）。

三行小例子（Part 1）：
```
num_courses=4, prerequisites=[[1,0],[2,0],[3,1],[3,2]]
course0先修完 -> 解锁1,2(入度都归0) -> 堆里{1,2}弹出最小1 -> course3减到差2 -> 弹出2 -> course3归0 -> 弹出3
答案：[0,1,2,3]
```

## 2. 读题：把文字变成模型
- **实体**：课程（节点）、先修关系（有向边）。
- **输入长什么样**：`PART <1|2>` + `num_courses` + 边数 + 若干行 `a b`。
- **输出要什么**：Part 1 是一行课程 id（空格分隔，不可行输出空行）；Part 2 是一个整数（不可行输出 `-1`）。
- **状态**：入度数组 `indeg`、邻接表 `adj`；Part 1 额外需要一个最小堆维护"当前可选课程"；Part 2 需要
  按 BFS 层处理，每层的节点数就是这个学期能修的课数。
- **一句话建模**：两个 part 都是 **Kahn 算法拓扑排序**，区别是 Part 1 用最小堆做确定性 tie-break、
  逐个出队；Part 2 用普通队列、逐层出队计数层数。

> [!note] 为什么选这个数据结构
> Part 1 要保证输出唯一，"入度为 0 的课程"不能用普通队列（FIFO 顺序依赖插入顺序，不确定），必须用
> 最小堆保证"永远选编号最小的"。Part 2 不关心具体顺序，只关心"能并行修多少门"，所以按 BFS 层处理更
>直接——每次把当前队列里的所有节点都出队算作同一学期，学期数就是 BFS 的层数。

## 3. 下笔顺序（面试里就按这个顺序敲）
1. **骨架先行**：`main()` 解析 `PART`/`num_courses`/边表，调 `part1`/`part2`，按格式打印。
2. **Part 1 最小可用**：建邻接表 `adj[b].append(a)`（b 先修 a）、入度数组；把入度为 0 的课程放进最小堆；
   每次弹出最小的、加入结果、给它的后继减入度，归零就入堆；最后比较结果长度和 `num_courses` 判环。
3. **Part 2 叠加**：换成 1-indexed，边方向反过来（`adj[a].append(b)`，a 先于 b）；用普通队列，每轮
   把当前队列里所有节点都处理完算一个学期，`semesters+=1`；同样最后判断处理数量是否等于总课程数。
4. **收尾**：`num_courses=0`（两个 part 都要优雅返回，Part 2 是 `0` 不是 `-1`）、自环、多个不连通分量、
   `relations=[]` 但 `num_courses>0`（Part 2 答案恒为 1）逐一过一遍。

## 4. 代码怎么组织
```
part1(num_courses, prerequisites) -> list[int]   # 0-indexed，最小堆 Kahn，逐个出队
part2(num_courses, relations) -> int             # 1-indexed，普通队列 Kahn，逐层计数
main(stdin, stdout)                               # 解析，按 PART 分派两套不同编号约定
```
两个函数完全独立，字段命名（`num_courses`/`prerequisites` vs `num_courses`/`relations`）和边的方向
在各自的 docstring 里写清楚，防止面试官（或未来的自己）把两套约定搞混。

## 5. 核心代码（骨架，≤ 40 行，带注释）
```python
def part1(num_courses, prerequisites):        # 0-indexed，[a,b]: a 需要先修 b
    adj = [[] for _ in range(num_courses)]
    indeg = [0] * num_courses
    for a, b in prerequisites:
        adj[b].append(a)
        indeg[a] += 1
    heap = [c for c in range(num_courses) if indeg[c] == 0]
    heapq.heapify(heap)                        # 最小堆保证确定性输出
    order = []
    while heap:
        course = heapq.heappop(heap)
        order.append(course)
        for nxt in adj[course]:
            indeg[nxt] -= 1
            if indeg[nxt] == 0:
                heapq.heappush(heap, nxt)
    return order if len(order) == num_courses else []

def part2(num_courses, relations):            # 1-indexed，[a,b]: a 必须先于 b
    adj = [[] for _ in range(num_courses + 1)]
    indeg = [0] * (num_courses + 1)
    for a, b in relations:
        adj[a].append(b)
        indeg[b] += 1
    queue = deque(c for c in range(1, num_courses + 1) if indeg[c] == 0)
    taken, semesters = 0, 0
    while queue:
        semesters += 1
        for _ in range(len(queue)):           # 当前队列 = 这一学期能并行修的课
            course = queue.popleft()
            taken += 1
            for nxt in adj[course]:
                indeg[nxt] -= 1
                if indeg[nxt] == 0:
                    queue.append(nxt)
    return semesters if taken == num_courses else -1
```

## 6. 面试里怎么说（边写边讲）
- 开始前：「Part 1 是标准 LC 210，我会用最小堆而不是普通队列来处理入度为 0 的课程，保证输出确定；
  Part 2 是按层 BFS 求最少学期，编号和边的方向我会按题面单独约定，不跟 Part 1 混用。」
- 写 Part 1 时：「每次从堆里弹出编号最小的可选课程，这保证了在存在多个合法拓扑序时输出总是同一个。」
- 写 Part 2 时：「这里不需要具体顺序，只需要按 BFS 的『层』来数——每一层就是一个学期，所以我在处理
  队列时用 `len(queue)` 先固定住这一层的节点数，再逐个出队。」
- 交付时：「Part 1/Part 2 的官方样例和环检测都过了；`num_courses=0`、自环、不连通分量这些边界单独
  测了；两套编号约定我在各自函数的 docstring 里写清楚了，不会混用。」

## 7. 常见跑偏（方法层面，3 条）
- **Part 1 用普通队列而不是最小堆**：语义上依然是合法的拓扑排序，但输出顺序依赖插入顺序，和题目要求
  的"编号最小优先"不一致，隐藏测试会直接判错。
- **把 Part 1 的 0-indexed、"a 需要先修 b"和 Part 2 的 1-indexed、"a 先于 b"搞混**：边的方向建反、
  下标越界，是这题最容易出现的低级错误。
- **Part 2 忘记按层处理，逐个节点处理却错误地把每个节点都当一个学期**：必须用 `len(queue)` 先固定
  当前层的节点数，再在这一轮内逐个出队，否则学期数会算多。

## 8. 同族题 / 延伸
- 同族：LC 207（布尔版本，只问能不能修完）是本题 Part 1 的子集。
- 延伸思考：如果 tie-break 规则从"编号最小"换成"输入顺序里最早出现"，只需要把最小堆换成一个按
  首次出现顺序排序的结构（比如维护一个"出现顺序"映射再排序）。
- 与图论同族题 `q10_wiki_min_clicks` 共享"BFS + 确定性遍历顺序"的方法论，但那题是无权最短路，不是
  拓扑排序。
- 练习命令：`python3 loop/mock.py start q08`
