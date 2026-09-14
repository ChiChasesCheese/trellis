# q22 · Dropped Requests：练的是"主动澄清题面没说清楚的计数口径"

> [!tldr]
> - TrueInterview 同步清单 #68（2025-11 报告，题名对应经典 HackerRank "Dropped Requests"）；**三条阈值数字与 Part 2 语义均为 (reconstructed)**
> - 这题考的是：三条并行滑动窗口限流规则判断请求是否被拒，以及"窗口计数要不要含被拒请求"这个隐藏假设
> - 三步套路：三个窗口各自摊还 O(1) 判定 → 意识到"算不算被拒的"是个未言明的选择 → 用两套自洽实现分别验证
> - 最值得带走的一个模式：**滑动窗口限流题里，"窗口计数是否包含被自己拒绝的请求"是一个题面经常不说、但答案会分叉的隐藏假设——写代码前先问出来**

## 1. 题目在说什么（人话版）

请求按时间到达（非降序）。一个请求被拒绝，当且仅当满足以下任一条件：同一秒内是第 4
个或更晚到达；过去 10 秒窗口内是第 21 个或更晚到达；过去 60 秒窗口内是第 61 个或更晚
到达。返回所有被拒绝请求的时间戳。

```
requestTimes = [5, 5, 5, 5]
前 3 个请求（同秒）被接受，第 4 个触发"同秒 > 3" -> 被拒 -> [5]
```

## 2. 读题：把文字变成模型

- **实体**：按时间到达的请求；三条并行的滑动窗口规则（1 秒 / 10 秒 / 60 秒）。
- **状态**：同秒计数器 + 两个滑动窗口（`deque`），随时间推进入队、按过期规则出队。
- **一句话建模**：这是一个 **多条并行滑动窗口限流** 问题，核心动作是"摊还 O(1) 地维护窗口计数、判断新请求是否超限"。

> [!note] 为什么要单独澄清"窗口算不算被拒的请求"
> 题面从没说清楚：一个被拒绝的请求，算不算占用了后续请求视角里"这 10 秒/这 60 秒"的
> 一个名额？两种读法都自洽——像 nginx 的 `limit_req` 只统计通过的请求，而某些审计式限流
> 把所有到达（含被拒）都算作配额消耗。两者在"从未连续拒绝"的输入上结果相同，一旦出现
> **连续拒绝**就会分叉：被拒请求算不算数，直接决定后面请求看到的窗口计数是大是小。

## 3. 下笔顺序（面试里就按这个顺序敲）

1. **先问清楚**：「窗口计数是否包含被拒绝的请求本身？」如果面试官没有明确答案，说明你会先实现"计入全部"（更常见的读法），并提出另一种读法作为备选。
2. **Part 1 最小可用**：三个滑动窗口（同秒计数器 + 两个 `deque`），每个请求无条件入队，再弹出过期项，检查是否超限。
3. **Part 2 叠加**：同样的三个窗口结构，但判定时用"如果接受它，窗口会变多大"跟阈值比较；一旦拒绝就不让它进任何窗口。
4. **收尾**：构造一个"连续拒绝"的输入，验证两种读法确实会给出不同答案。

## 4. 代码怎么组织

```
_validate(request_times)                          # 非降序、非负
dropped_requests_count_all(request_times)          # Part 1：窗口计入全部到达
dropped_requests_count_accepted_only(request_times) # Part 2：窗口只计入被接受的
part1 / part2
```
两个函数的窗口结构（同秒计数器 + 两个 `deque`）完全一样，差别集中在"新请求要不要真的
入队"这一步——面试里可以先写 Part 1，再指出 Part 2 只是把"先入队再判断"改成"先判断
再决定要不要入队"。

## 5. 核心代码骨架

```python
from collections import deque

def dropped_requests_count_all(request_times):
    # Part 1：窗口计入所有到达（含被拒的）
    dropped = []
    win10, win60 = deque(), deque()
    last_time, same = None, 0
    for t in request_times:
        win10.append(t)
        while win10[0] < t - 9:
            win10.popleft()
        win60.append(t)
        while win60[0] < t - 59:
            win60.popleft()
        same = same + 1 if t == last_time else 1
        last_time = t
        if same > 3 or len(win10) > 20 or len(win60) > 60:
            dropped.append(t)
    return dropped

def dropped_requests_count_accepted_only(request_times):
    # Part 2：窗口只计入被接受的到达——判断时先看"如果接受会变多大"
    dropped = []
    win10, win60 = deque(), deque()
    last_time, same = None, 0
    for t in request_times:
        while win10 and win10[0] < t - 9:
            win10.popleft()
        while win60 and win60[0] < t - 59:
            win60.popleft()
        tentative = (same + 1) if t == last_time else 1
        if tentative > 3 or len(win10) + 1 > 20 or len(win60) + 1 > 60:
            dropped.append(t)
            continue
        win10.append(t); win60.append(t)
        same, last_time = tentative, t
    return dropped
```

## 6. 面试里怎么说（边写边讲）

- 开始前：「三条规则我理解了；有一个假设需要澄清——窗口计数要不要含被拒绝的请求本身？我先按'含'来实现，因为这是更常见的版本。」
- 写 Part 1 时：「三个窗口都是摊还 O(1)，每个时间戳最多入队出队各一次。」
- 交付时：「样例过了；如果按'只计入被接受的'来读，结果会在连续拒绝的场景下不一样，我可以另写一版对比。」

## 7. 常见跑偏（方法层面，3 条）

- 没有意识到"窗口算不算被拒的请求"是个需要澄清的假设，闷头写一种然后被隐藏测试打脸。
- 用 `O(n²)` 的暴力重新扫描窗口而不是用 `deque` 摊还，导致大输入超时。
- 恰好卡在阈值上（`==3`、`==20`、`==60`）判断成拒绝——应该是"超过"阈值才拒绝，不是"达到"。

## 8. 同族题 / 延伸

- 同一类"滑动窗口 + 计数"套路：`pc03` Recent Event Stream（deque 管窗口、Counter 管查询）。
- 练习命令：`python3 drill.py start q22`

## 索引行

| [q22_dropped_requests](q22_dropped_requests.md) | `../../problems/q22_dropped_requests/` | OA | 滑动窗口限流题里，"窗口计数是否包含被自己拒绝的请求"是一个题面经常不说、但答案会分叉的隐藏假设——写代码前先问出来 |
