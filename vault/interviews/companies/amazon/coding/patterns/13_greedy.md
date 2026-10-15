# 13 · 贪心：局部最优为什么能推出全局最优（Greedy）

> 本讲覆盖：LC 55 Jump Game（附 45）· 621 Task Scheduler · 134 Gas Station · 179 Largest Number · 135 Candy（Hard）· 871 Minimum Number of Refueling Stops（Hard）
> 前置：第 03 讲（区间：按右端点排序的贪心已经出现过）、第 05 讲（`heapq` 最小堆 / 取负）、第 10 讲（DP，用来对比「贪心失败」的情形）。
> 读完你应该能：(1) 说出贪心成立的两个条件，并为一道新题写出两句话的**交换论证（exchange argument）**；(2) 认出三种贪心骨架：排序再扫描 / 维护一个运行中的最优值 / 带「后悔药」的堆；(3) 举出一个贪心**失败**的反例（硬币问题）并说明该换 DP；(4) 对每道题回答「为什么这个贪心是对的」，而不只是「代码长这样」。
> 贪心题的代码通常很短，难点全在**证明**。面试里写完代码以后，面试官最常问的是「你怎么知道这是最优的」，所以本讲每道题都带一个证明草图。

## 1. 这个模式是什么，为什么存在

### 1.1 从最笨的解法开始

LC 55 Jump Game：`nums[i]` 是在位置 `i` 最多能向前跳的步数，问能否从下标 0 到达最后一格。`[2,3,1,1,4]` 可以（`0→1→4`），`[3,2,1,0,4]` 不行（所有路线都会卡在下标 3，那里 `nums[3] = 0`）。

最笨的做法：递归地尝试每一种跳法——在位置 `i` 对 `1 … nums[i]` 里每个步长都递归下去。最坏情况是指数级。稍好一点是 DP：`reach[i]` 表示能否到达 `i`，对每个 `i` 看前面是否有一个可达的 `j` 满足 `j + nums[j] >= i`，O(n²)。

### 1.2 慢在哪里 / 错在哪里

两种做法都在**比较很多本来不需要比较的选择**。比如在 `[2,3,1,1,4]` 的位置 0，你可以跳 1 步或 2 步；但只要你知道「能到达的位置恰好是从 0 开始的一段连续区间」，就没必要区分是怎么到的。

> 因果链：如果能证明「某个局部选择**一定**出现在某个最优解里」，就可以立刻做出这个选择、永不回头，问题规模缩小一格 → 不再需要比较所有分支。这样的证明有两种常见写法：
> - **交换论证（exchange argument）**：假设有一个最优解 `OPT` 没做我们的选择，把 `OPT` 里的某一步换成我们的选择，结果**不会变差**，于是存在一个包含我们选择的最优解。
> - **保持领先（stays ahead）**：证明贪心在每一步之后的状态都不比任何其他策略差（例如「到目前为止能到达的最远位置」始终最大）。

### 1.3 贪心是什么（从零讲）

- **贪心算法（greedy algorithm）**：每一步都做当前看起来最好的选择，选定后不再改变。
- 它成立需要两个性质：
  1. **贪心选择性质（greedy-choice property）**：存在一个最优解，包含贪心的第一步选择。
  2. **最优子结构（optimal substructure）**：做完第一步之后，剩下的问题是同类的更小问题，它的最优解加上第一步就是整体最优。
- **和 DP 的关系**：DP 对所有选择都算一遍然后取最好；贪心靠证明只留下一个。所以贪心**更快、更省**，但**更容易错**。一个很好的纪律：写贪心之前，先在脑子里（或测试里）用**暴力**验证它——本讲所有 `solutions/` 里的贪心都和暴力做了随机对拍。
- **三种常见骨架**：
  1. **排序后扫描**：按某个键排序，再一遍扫描做决定（区间调度按右端点；Largest Number 按拼接比较）。
  2. **运行中的最优值 / 重置**：一遍扫描维护一个量（能到的最远位置；油箱余量，为负就重置起点）。
  3. **带后悔药的堆（regret heap）**：先"贪心地接受"，以后发现不行了，就从堆里**撤销最差的一个**（871 加油站、LC 630 课程表 III）。
- **怎么证明（面试可说的版本）**：先陈述贪心规则，然后选一个反设「如果最优解不这么做」，写出**交换后不变差**的两句话。例如区间调度："设最优解里第一个区间不是最早结束的那个 `a`，把它换成 `a`：`a` 结束得更早，不会和后面的区间冲突，数量不变。"
- **贪心失败的经典反例**：硬币面值 `[1,3,4]` 凑 6。贪心（每次拿最大的）得到 `4+1+1`（3 枚），最优是 `3+3`（2 枚）。因为「拿最大的」不满足贪心选择性质——这类题必须用 DP（第 10 讲 LC 322）。

## 2. 模板与逐行讲解

```python
import heapq
from itertools import combinations
from random import Random

# Template G1: sort by the right endpoint, then sweep (interval scheduling: the most non-overlapping intervals)
def max_non_overlapping(intervals):
    count, last_end = 0, float("-inf")
    for start, end in sorted(intervals, key=lambda iv: iv[1]):    # earliest finish first
        if start >= last_end:                                     # touching ([1,2], [2,3]) is allowed
            count += 1
            last_end = end
    return count


# Template G3: regret heap -- LC 630 Course Schedule III. Take every course, and when the deadline is
# missed, drop the LONGEST course taken so far (it frees the most time).
def max_courses(courses):                      # courses: (duration, last_day)
    total, taken = 0, []                       # `taken`: max-heap of durations (negated)
    for duration, last_day in sorted(courses, key=lambda c: c[1]):
        heapq.heappush(taken, -duration)
        total += duration
        if total > last_day:
            total += heapq.heappop(taken)      # the popped value is negative: this removes the longest course
    return len(taken)


def _brute_intervals(iv):
    best = 0
    for k in range(len(iv) + 1):
        for subset in combinations(sorted(iv), k):
            if all(subset[i][1] <= subset[i + 1][0] for i in range(k - 1)):
                best = max(best, k)
    return best

def _brute_courses(courses):
    best = 0
    for k in range(len(courses) + 1):
        for subset in combinations(courses, k):
            t, ok = 0, True
            for d, last in sorted(subset, key=lambda c: c[1]):
                t += d
                ok = ok and t <= last
            if ok:
                best = max(best, k)
    return best

assert max_non_overlapping([[1, 2], [2, 3], [3, 4], [1, 3]]) == 3
assert max_courses([(100, 200), (200, 1300), (1000, 1250), (2000, 3200)]) == 3
rng = Random(5)
for _ in range(300):
    iv = [(s, s + rng.randint(1, 4)) for s in (rng.randint(0, 8) for _ in range(rng.randint(0, 7)))]
    assert max_non_overlapping(iv) == _brute_intervals(iv), iv
    cs = [(rng.randint(1, 5), rng.randint(1, 12)) for _ in range(rng.randint(0, 7))]
    assert max_courses(cs) == _brute_courses(cs), cs
```

（骨架 2「运行中的最优值」在 4.1 Jump Game 和 4.3 Gas Station 里。）

逐行讲解：

1. **G1 `key=lambda iv: iv[1]`**：按**右端点**排序，不是左端点。这是整个贪心的核心：结束得越早，留给后面的空间越大（交换论证见 1.3）。按左端点排序会在 `[1,100]`, `[2,3]`, `[4,5]` 上选错。
2. **G1 `start >= last_end`**：`>=` 表示首尾相接的区间（`[1,2]` 和 `[2,3]`）不算重叠。这是**契约**，必须先问面试官。
3. **G3 为什么先接受再撤销**：按截止日期排序后，我们总是先"都接受"。如果总时长超过了当前截止日，必须去掉**一**门课，去掉最长的那门能腾出最多时间，而且课数少 1 的代价一样。这就是「后悔药」：贪心的决定不是不可逆的，而是能被**局部修正**，修正由堆在 O(log n) 内完成。
4. **G3 的 `total += heapq.heappop(taken)`**：堆里存的是**负数**（`heapq` 是最小堆，取负模拟最大堆），弹出的是 `-最大时长`，加到 `total` 上等价于减去最大时长。
5. **对拍**：`_brute_*` 枚举所有子集；随机小输入上贪心必须和暴力一致，这是你在白板上"证明"之外的第二道保险。

## 3. 完整手算（Worked trace）

下面是两个真实运行：一个是 Gas Station 的"重置起点"如何一步步工作；另一个是 1.3 里说的**贪心失败**的反例（硬币问题）：

```python
def gas_trace(gas, cost):
    print("gas  =", gas)
    print("cost =", cost, "  total gas - total cost =", sum(gas) - sum(cost))
    start = tank = 0
    for i in range(len(gas)):
        tank += gas[i] - cost[i]
        note = ""
        if tank < 0:
            note = f"<- stuck: no start in [{start}..{i}] works, restart at {i + 1}"
            start, tank = i + 1, 0
        print(f"station {i}: gain {gas[i] - cost[i]:+d}  tank={tank}  candidate start={start} {note}")
    return start

assert gas_trace([2, 1, 1, 4, 2, 1], [1, 3, 2, 1, 1, 1]) == 3
print()

def greedy_coins(coins, amount):
    count = 0
    for c in sorted(coins, reverse=True):
        count += amount // c
        amount %= c
    return count if amount == 0 else None

def best_coins(coins, amount):
    INF = float("inf")
    dp = [0] + [INF] * amount
    for a in range(1, amount + 1):
        dp[a] = min((dp[a - c] + 1 for c in coins if c <= a), default=INF)
    return dp[amount]

print("coins [1,3,4], amount 6: greedy =", greedy_coins([1, 3, 4], 6), " optimal (DP) =", best_coins([1, 3, 4], 6))
print("coins [1,5,10,25], amount 63: greedy =", greedy_coins([1, 5, 10, 25], 63), " optimal (DP) =", best_coins([1, 5, 10, 25], 63))
assert greedy_coins([1, 3, 4], 6) == 3 and best_coins([1, 3, 4], 6) == 2
assert greedy_coins([1, 5, 10, 25], 63) == best_coins([1, 5, 10, 25], 63)
```

```text
gas  = [2, 1, 1, 4, 2, 1]
cost = [1, 3, 2, 1, 1, 1]   total gas - total cost = 2
station 0: gain +1  tank=1  candidate start=0 
station 1: gain -2  tank=0  candidate start=2 <- stuck: no start in [0..1] works, restart at 2
station 2: gain -1  tank=0  candidate start=3 <- stuck: no start in [2..2] works, restart at 3
station 3: gain +3  tank=3  candidate start=3 
station 4: gain +1  tank=4  candidate start=3 
station 5: gain +0  tank=4  candidate start=3 

coins [1,3,4], amount 6: greedy = 3  optimal (DP) = 2
coins [1,5,10,25], amount 63: greedy = 6  optimal (DP) = 6
```

怎么读：

- **Gas Station**：每一站累计 `tank`，一旦为负，就说明从当前候选起点 `start` 出发到这一站之前，没有任何一个起点能活下来，于是把候选起点推到下一站，`tank` 清零。总的 `sum(gas) - sum(cost) = 2 >= 0`，所以最后留下的候选 `3` 一定可行。整个过程只扫一遍。
- **硬币**：`[1,3,4]` 凑 6，贪心 3 枚、最优 2 枚——贪心的第一步（拿 4）就不在任何最优解里。`[1,5,10,25]`（美元硬币）凑 63，贪心和 DP 一致，因为这套面值恰好满足贪心选择性质。**同一个"拿最大的"规则，换一套面值就从对变成错**：这就是为什么必须证明或对拍，不能凭感觉。

## 4. 题目

```python
import heapq
from collections import Counter, deque
from functools import cmp_to_key
```

### 4.1 LC 55 · Jump Game（Medium，频率 68）；附 LC 45

```python
# solutions/55_jump_game.py
def can_jump(nums):
    farthest = 0
    for i, step in enumerate(nums):
        if i > farthest:                      # index i is unreachable, and so is everything after it
            return False
        farthest = max(farthest, i + step)
    return True


def min_jumps(nums):                          # LC 45 (answer exists): BFS by levels, without a queue
    jumps = cur_end = farthest = 0
    for i in range(len(nums) - 1):            # stop BEFORE the last index: we only need to reach it
        farthest = max(farthest, i + nums[i])
        if i == cur_end:                      # the current jump's range is exhausted: we must jump again
            jumps += 1
            cur_end = farthest
    return jumps
```

- **一句话洞见**：能到达的下标一定是从 0 开始的一段连续前缀 `[0, farthest]`；扫描时只维护 `farthest`，一旦当前下标 `i` 超过它，后面所有位置都不可达。
- **证明草图（stays ahead）**：设 `farthest` 是用前 `i` 个格子能到达的最远位置。位置 `i+1` 能被到达当且仅当 `i+1 <= farthest`（前缀里所有位置都可达，任何一个能覆盖它的跳点都在前缀里）。
- **LC 45（最少跳数）**：同样的区间视角——把"第 k 次跳能到达的范围"看成 BFS 的第 k 层；`cur_end` 是本层的边界，`farthest` 是下一层的边界；到边界必须再跳一次。循环只到 `len(nums) - 2`，因为到达最后一格不需要再起跳。
- **复杂度**：时间 O(n)，空间 O(1)。

**资深追问**

- **规模 ×1000**：线性扫描已经是最优；数据在磁盘 / 分片上时，每个分片只需要把「进入时的 farthest」传给下一个分片，输出新的 farthest（可以流水线处理）。
- **流式**：`nums` 以流的形式到达：只需要保存 `(i, farthest)` 两个整数，O(1) 内存。
- **内存**：O(1)；对比 DP 的 O(n)。
- **并发**：前缀最大值 `max(i + nums[i])` 是可结合的（associative），分块并行求每块的 `(块内最大值)`，再串行合并——和并行前缀和同一个思路。
- **接口**：空数组？`nums[i]` 允许负数吗？返回布尔值还是路径（路径需要记录父指针，贪心不够，用 BFS）？45 是否保证可达？
- **测试**：`[0]`（长度 1，True）、`[0,1]`（False）、卡在中间的 0（`[3,2,1,0,4]`）、与 O(n²) DP 对拍（我们做了），45 与 DP 对拍。

### 4.2 LC 621 · Task Scheduler（Medium，频率 63）

```python
# solutions/621_task_scheduler.py
def least_interval(tasks, n):
    counts = Counter(tasks).values()
    top = max(counts)                                    # the busiest task fixes the frame count
    how_many_top = sum(1 for c in counts if c == top)    # tasks tied for busiest share the last frame
    frames_len = (top - 1) * (n + 1) + how_many_top      # (top-1) full frames of n+1 slots, then the tail
    return max(len(tasks), frames_len)                   # if there are plenty of tasks, no idle is needed


def least_interval_simulated(tasks, n):                  # the same answer by running the schedule (max-heap + cooldown queue)
    heap = [-c for c in Counter(tasks).values()]
    heapq.heapify(heap)
    cooling = deque()                                    # (time_ready, remaining_count)
    time = 0
    while heap or cooling:
        time += 1
        if heap:
            left = -heapq.heappop(heap) - 1              # run the task with the most work left
            if left:
                cooling.append((time + n, left))
        if cooling and cooling[0][0] == time:            # cooldown over: eligible again
            heapq.heappush(heap, -cooling.popleft()[1])
    return time
```

- **一句话洞见**：出现次数最多的任务（次数 `top`）决定了下限：它需要 `top - 1` 个完整的"冷却帧"（每帧 `n + 1` 个槽），最后一帧只放"和它并列最多的那些任务"；其他任务可以填进帧里的空位。如果任务多到把空位都填满，就不需要空闲，答案是 `len(tasks)`。
- **证明草图**：下限——最忙的任务两次执行之间至少隔 `n` 个槽，所以至少占用 `(top - 1)(n + 1) + 1` 个槽；并列最多的 `m` 个任务在最后一帧各占一个，所以是 `+ m`。可达——按次数从多到少轮流填帧，空位不够时帧会被撑大，此时没有空闲，总长就是任务数。
- **复杂度**：公式版本时间 O(N)（N 为任务数），空间 O(字母表)；模拟版本（堆 + 冷却队列）O(N log 字母表)，好处是能输出**真实的调度序列**。

**资深追问**

- **规模 ×1000**：公式版仍然是线性；真实调度器需要实际的顺序，用模拟版（堆 + 冷却队列），每一步 O(log k)（k 是任务种类数）。
- **流式**：任务不断到达、必须在线调度：每个时刻从"当前冷却完毕、剩余次数最多"的任务里选——就是模拟版的堆；没有全局公式，因为未来不可知。
- **内存**：O(种类数)。
- **并发**：多个 worker 共享冷却约束 → 变成"带资源约束的调度"（NP-hard 的一般形式）；每个 worker 用独立冷却，或用一个线程安全的优先队列加"下一次可用时间"。
- **接口**：返回总时间还是具体的调度序列（空闲用 `idle` 标记）？`n = 0` 时答案就是任务数。
- **测试**：`n = 0`、只有一种任务、所有任务一样多（并列 `m` 个）、任务多到不需要空闲。我们用**穷举 BFS**（状态 = 剩余次数 + 每个任务上次执行时间）作为独立的暴力解，同时验证公式版和模拟版。

### 4.3 LC 134 · Gas Station（Medium，频率 54）

```python
# solutions/134_gas_station.py
def can_complete_circuit(gas, cost):
    if sum(gas) < sum(cost):
        return -1                              # not enough fuel in total: impossible from anywhere
    start = tank = 0
    for i in range(len(gas)):
        tank += gas[i] - cost[i]
        if tank < 0:                           # stuck at i: every start in [start, i] would be stuck too
            start, tank = i + 1, 0
    return start                               # the total is >= 0, so the last surviving candidate works
```

- **一句话洞见**：两个事实——(1) 总油量 `>=` 总消耗才可能有解（并且此时一定有解）；(2) 从 `start` 出发在 `i` 站油箱变负，则 `[start, i]` 里任何起点都不可能成功（它们到达 `i` 时的余量不会比 `start` 的更多），所以直接把候选起点跳到 `i + 1`。
- **证明草图**：设从 `start` 出发，到 `k - 1` 站时余量 `>= 0`（否则早就重置了）。若从 `k` 出发，相当于去掉了这段非负余量，到 `i` 站时余量只会更少，也会为负。
- **复杂度**：时间 O(n)，空间 O(1)。

**资深追问**

- **规模 ×1000**：线性、O(1) 内存；环形分片：每个分片输出 `(净增益, 前缀最小值)`，合并时用这两个值决定起点（类似线段树的合并）。
- **流式**：站点流式到达时只能判断"目前最好的候选起点"，最终答案要等总和已知。
- **内存**：O(1)。
- **并发**：同上，分块汇总再合并。
- **接口**：解是否唯一（LeetCode 保证唯一；一般情况下可能有多个，返回任意一个即可）；总量刚好相等时的行为；`-1` 表示无解。
- **测试**：油量等于消耗（`tank` 恰好为 0 仍然可以走）、单站、无解、起点在末尾；与「尝试所有起点」的 O(n²) 暴力对拍（我们做了，只断言返回的起点**有效**）。

### 4.4 LC 179 · Largest Number（Medium，频率 51）

```python
# solutions/179_largest_number.py
def largest_number(nums):
    strs = [str(x) for x in nums]

    def cmp(a, b):                             # a goes first iff the concatenation a+b is larger
        return -1 if a + b > b + a else (1 if a + b < b + a else 0)

    strs.sort(key=cmp_to_key(cmp))
    out = "".join(strs)
    return "0" if out[0] == "0" else out       # [0, 0] must give "0", not "00"
```

- **一句话洞见**：把整数当字符串排序，规则是 `a` 排在 `b` 前面当且仅当 `a + b > b + a`（字符串拼接）。例如 `"3"` 和 `"30"`：`"330" > "303"`，所以 3 在前。
- **证明草图**：(1) 相邻交换论证——如果最优排列里 `b` 紧挨着排在 `a` 前面但 `a + b > b + a`，交换后数值变大，矛盾；(2) 这个比较是**全序**（传递），因为 `a + b > b + a` 等价于 `a / (10^|a| − 1) > b / (10^|b| − 1)`——它等价于比较一个实数键，所以可以放心用排序。
- **复杂度**：时间 O(n log n · L)（L 是数字的最大位数，每次比较 O(L)），空间 O(n · L)。
- **坑**：全是 0 的时候返回 `"0"` 而不是 `"00"`。

**资深追问**

- **规模 ×1000**：排序是 O(n log n)；数据放不下内存时用外排序（external sort）+ 同一个比较器；Python 里 `cmp_to_key` 比 `key=` 慢，可以改成「每个数字重复到固定长度再比较」得到一个真正的键（`str * k` 的技巧需要证明正确，面试里先说比较器版本）。
- **流式**：不可能在线给出最终答案（后来的数可能排到最前面）；可以维护一个有序结构（平衡树 / 跳表）按比较器插入。
- **内存**：O(n · L)。
- **并发**：分块各自排序，再用同一个比较器做 k 路归并（第 05 讲 LC 23）。
- **接口**：输入是整数还是字符串（超大数字）？可能出现负数吗（题目保证非负）？返回字符串（因为结果超过 64 位）。
- **测试**：`[0,0]`、前缀关系（`[121, 12]`，`12121 > 12112`）、重复数、单元素；我们用**全排列取最大**做暴力对拍。

### 4.5 LC 135 · Candy（Hard，频率 53）

```python
# solutions/135_candy.py
def candy(ratings):
    n = len(ratings)
    give = [1] * n                              # everyone gets at least one
    for i in range(1, n):                       # pass 1: satisfy "higher than the LEFT neighbour"
        if ratings[i] > ratings[i - 1]:
            give[i] = give[i - 1] + 1
    for i in range(n - 2, -1, -1):              # pass 2: satisfy "higher than the RIGHT neighbour"
        if ratings[i] > ratings[i + 1]:
            give[i] = max(give[i], give[i + 1] + 1)   # max keeps pass 1's result
    return sum(give)


def candy_o1(ratings):                          # one pass, O(1) extra space: count up-slopes and down-slopes
    n = len(ratings)
    total, up, down, peak = 1, 0, 0, 0
    for i in range(1, n):
        if ratings[i] > ratings[i - 1]:
            up += 1; peak = up; down = 0
            total += 1 + up
        elif ratings[i] == ratings[i - 1]:
            up = peak = down = 0
            total += 1
        else:
            up = 0; down += 1
            total += 1 + down - (1 if peak >= down else 0)   # a long enough descent must lift the peak by one
    return total
```

- **一句话洞见**：约束是"评分比左邻居高就要比左邻居多"和"评分比右邻居高就要比右邻居多"。分别从左到右、从右到左各扫一遍，每遍只满足一个方向，**取两遍的最大值**同时满足两个约束，而且是最小的。
- **证明草图**：每个孩子的最小糖果数等于"以他结尾的严格上升段长度"与"以他开头的严格下降段长度"中的较大者，两遍扫描恰好各算出一个。
- **O(1) 空间版本**（`candy_o1`）：把评分序列看成一座座山；上坡累加 1, 2, 3…，下坡也累加 1, 2, 3…，如果下坡长度超过了山峰已有的糖果数，就给山峰补 1（代码里的 `peak >= down` 判断）。
- **复杂度**：两遍版本时间 O(n)、空间 O(n)；一遍版本时间 O(n)、空间 O(1)。

**资深追问**

- **规模 ×1000**：线性；分块并行时每块输出 `(开头的上升 / 下降段长度, 结尾的…, 块内糖果和)`，块边界处需要修正山峰（和 Gas Station 一样的"分块汇总再合并"）。
- **流式**：只用 O(1) 版本，维护 `up / down / peak`，每来一个评分增量更新总和；注意下坡补峰的修正是**回溯式地加 1**，已经输出的分配不能直接改，所以需要延迟确认（缓冲一整段下坡）。
- **内存**：O(1) 版本 vs O(n)。
- **并发**：同上，分块 + 合并边界。
- **接口**：评分相等的相邻孩子没有约束（可以得到不同数量的糖）；是返回总数还是每个孩子的具体分配（后者需要两遍版本）？评分是环形排列的变体（更难，需要找最低点切开）。
- **测试**：全相等、严格递增、严格递减、山峰 / 山谷、平台（`[1,2,2]`）；我们用"从全 1 开始不断修复违反约束"的**最小不动点**做暴力对拍，并验证两种实现一致。

### 4.6 LC 871 · Minimum Number of Refueling Stops（Hard，频率 38）

```python
# solutions/871_minimum_number_of_refueling_stops.py
def min_refuel_stops(target, start_fuel, stations):
    heap = []                                    # max-heap (negated) of fuel at stations we already drove past
    stops, i = 0, 0
    reach = start_fuel                           # farthest position we can reach with the fuel we have taken so far
    while reach < target:
        while i < len(stations) and stations[i][0] <= reach:
            heapq.heappush(heap, -stations[i][1])    # we COULD have stopped here: remember it
            i += 1
        if not heap:
            return -1                            # stuck: nothing passed can extend the range
        reach += -heapq.heappop(heap)            # greedy: the largest tank gives the farthest range
        stops += 1
    return stops
```

- **一句话洞见**：不要在路过加油站时决定要不要加；先把它们**记在堆里**，一直开到没油为止，再**回头**在已经路过的加油站里挑油量最大的那个加（等价于当时就在那里停了一次）。每次加油都选最大的，用最少的次数把航程推得最远。
- **证明草图（交换论证）**：设最优解停了 `k` 次。把这 `k` 次的加油站换成"到当前为止所有路过的站里油量最大的 `k` 个"，航程不会变短（更大的油量只会让可达范围更远，且这些站都在可达范围内）。贪心恰好按这个顺序延伸。
- **复杂度**：时间 O(n log n)，空间 O(n)。DP 解法是 O(n²)（`dp[i]` = 停 `i` 次能到的最远距离）。

**资深追问**

- **规模 ×1000**：n 很大时堆版本 O(n log n) 仍然可行；路线数据在磁盘上，按位置有序流式读取，堆里只保留已经路过的站。
- **流式**：车一边开一边知道前方的站——这正是本算法的"在线"形态（只用到已经路过的站）。
- **内存**：堆的大小 ≤ 已经路过的站数；可以限制堆大小（只保留最大的 K 个，K 为最多允许停靠次数）。
- **并发**：路线本身是串行的；多辆车 / 多个查询共享同一份排好序的站点列表，各自一个堆，互不影响。
- **接口**：站点是否已经按位置排序（不能假设）；`target` 就在某个站上；起始油量足够时返回 0；到不了返回 `-1`；油耗是否恒定（一升一公里，题目的设定）。
- **测试**：无站点、起始油量足够、第一站就够不到（`-1`）、需要连续使用多个站；暴力对拍用**枚举所有站点子集**（按位置顺序模拟）——这是真正独立的暴力解，不依赖贪心的任何假设。

## 5. 常见 bug

1. **没证明就写贪心**：硬币 `[1,3,4]` 是教科书反例。写完先用 5 分钟随机对拍小输入。
2. **区间排序的键错了**：区间调度要按**右端点**排序；按左端点或长度排序都会错。
3. **`>` 和 `>=` 的契约**：首尾相接的区间算不算冲突，必须在写代码前确认。
4. **Jump Game II 的循环范围**：`range(len(nums) - 1)`；多算一次最后一格会多跳一次。
5. **Task Scheduler 漏了 `max(len(tasks), …)`**：任务很多时公式会算出小于任务数的值（冷却间隔被填满，不需要空闲）。同时漏掉"并列最多的任务个数"会少算最后一帧。
6. **Gas Station 漏了总量判断**：只看局部重置会在"总量不够"时返回一个无效起点。
7. **Largest Number 的比较器**：Python 3 的 `cmp_to_key` 需要返回负 / 零 / 正的**整数**，返回布尔会让排序行为不确定；全零的特判（`"0"`）不能漏。
8. **Candy 的第二遍写成赋值而不是 `max`**：会覆盖第一遍的结果，丢掉左边的约束。
9. **Refueling 里对"可达站"的判断**：站点位置 `<= reach`（等于也可达）；弹出堆时 `reach` 增加的是油量，不是位置差。
10. **堆里存的是正数**：`heapq` 是最小堆，要最大值必须取负。

## 6. 自测题

1. 贪心算法成立的两个条件是什么？各用一句话说明。
   <details><summary>答案</summary>贪心选择性质：存在一个最优解包含当前的局部最优选择；最优子结构：做完这个选择后剩下的子问题的最优解加上这个选择就是整体最优。证明常用交换论证或保持领先。</details>
2. 给出一个贪心失败的例子，并说明应该用什么替代。
   <details><summary>答案</summary>硬币面值 `[1,3,4]` 凑 6：贪心 `4+1+1`（3 枚），最优 `3+3`（2 枚）。第一步选最大面值并不在任何最优解里，需要 DP（LC 322）。</details>
3. 区间调度（选最多不重叠区间）为什么按右端点排序？
   <details><summary>答案</summary>设最优解的第一个区间不是最早结束的 `a`；把它换成 `a`，`a` 结束得不晚于它，所以仍然不会和后面的区间冲突，数量不变。因此存在包含 `a` 的最优解，删掉 `a` 以及与 `a` 冲突的区间后递归。</details>
4. 小编程：不用 `sort`，只用一遍扫描判断 Jump Game 是否可达，并说明为什么只需要 `farthest` 一个变量。
   <details><summary>答案</summary>见 4.1：`farthest = 0; for i, s in enumerate(nums): if i > farthest: return False; farthest = max(farthest, i + s)`。可达位置是 `[0, farthest]` 的前缀，所以一个变量足够描述全部可达集合。</details>
5. Largest Number 的比较器 `a + b > b + a` 为什么可以用来排序（为什么是全序）？
   <details><summary>答案</summary>`a + b > b + a` 等价于 `a·10^|b| + b > b·10^|a| + a`，整理得 `a / (10^|a| − 1) > b / (10^|b| − 1)`。这等价于比较每个数的一个实数键，所以满足传递性和反对称性，是一个合法的（弱）全序。</details>
6. Refueling Stops 里为什么要"先不选、没油了再回头选最大的"？
   <details><summary>答案</summary>在路过某站时无法知道以后是否需要它；延迟决策可以把"是否在这里停"推迟到真正没油的时刻，此时已经知道所有路过的站，选油量最大的最优（交换论证）。这就是「后悔药」模式：先接受，以后撤销最差的一个。</details>
7. 资深追问：同事提交了一个贪心解，你怎么在 code review 里判断它是否正确？
   <details><summary>答案</summary>要求作者写出规则和一两句交换 / 保持领先论证；同时要求有**暴力对拍**测试（小输入随机，覆盖相等值、边界和空输入）；找反例时优先构造"局部最优与全局最优冲突"的输入（例如面值非规范的硬币系统、并列的最大值、相等元素）。没有论证也没有对拍的贪心不应该合入。</details>
