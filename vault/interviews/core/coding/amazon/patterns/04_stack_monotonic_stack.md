# 04 · 栈 / 单调栈（Stack & monotonic stack）

栈（stack）处理「最近的」「下一个更大的」「成对匹配」这三类问题：后进先出正好对应「离我最近的未解决项」。单调栈（monotonic stack）让栈内元素保持有序，每个元素最多进栈出栈各一次，所以整体 O(n)；单调队列（monotonic deque）把同一思路用到滑动窗口的最大值。严格 `<` 还是 `<=` 决定相等元素怎么处理，是这类题最常见的 bug 来源。

覆盖的题目：LC 20 Valid Parentheses · 739 Daily Temperatures · 84 Largest Rectangle in Histogram（Hard）· 239 Sliding Window Maximum（Hard，单调队列）


## 1. 这个模式是什么，为什么存在

### 1.1 从最笨的解法开始

LC 739：给每天的气温，求每一天要等几天才会遇到更高的气温。最笨的做法：对每一天 `i`，向右一天天扫，直到找到更高的温度。

```text
for i in range(n):
    for j in range(i + 1, n):
        if temps[j] > temps[i]: ans[i] = j - i; break
```

最坏情况（气温一路下降）每天都要扫到末尾，O(n²)；n = 10⁵ 时 5×10⁹。

### 1.2 慢在哪里

在温度下降的段落里，「`i` 在等一个更热的日子」和「`i+1` 在等一个更热的日子」是**同一个等待**——但我们为每个 `i` 分别重新扫了一遍。

> 因果链：很多天在**同时等待**；一个新来的更热的日子会**一次性**结束所有比它冷、且还在等待的天。 → 把「还在等待的天」按顺序放进一个栈；新来的 `t` 从栈顶开始，只要栈顶比 `t` 冷就弹出并结算。栈里的温度因此**从底到顶不增**（monotonic，单调）。每个下标至多入栈 1 次、出栈 1 次 → O(n)。

### 1.3 栈是什么（从零讲）

- **是什么**：后进先出（LIFO, last-in-first-out）的容器。Python 里 `stack = []`，`stack.append(x)` 压栈，`stack.pop()` 弹栈，`stack[-1]` 看栈顶，都是 O(1)。
- **为什么需要它**：当问题里有「最近的未完成的东西」时——最近没配对的左括号、最近还在等答案的元素——栈正好把它放在顶上。
- **三种用法**：
  1. **配对 / 嵌套**（LC 20）：遇到左括号压栈，遇到右括号和栈顶比较。
  2. **单调栈**（LC 739、84）：栈里保持单调，弹出时结算「等待」。
  3. **单调队列**（LC 239，用 `deque`）：两端都能弹出；队首是当前窗口最大值，队尾维护单调。

## 2. 模板与逐行讲解

```python
# Template: monotonic stack of INDICES, "next greater element" version
def next_greater(nums):
    ans = [-1] * len(nums)                      # -1 = no greater element to the right
    stack = []                                  # indices still waiting for their answer; values non-increasing
    for i, x in enumerate(nums):
        while stack and nums[stack[-1]] < x:    # x answers every waiting smaller element
            ans[stack.pop()] = x
        stack.append(i)
    return ans                                  # whatever is still on the stack has no answer

# Template: plain stack for nested structure (match the most recent opener)
def balanced(s):
    stack = []
    for ch in s:
        if ch == "(":
            stack.append(ch)
        elif ch == ")":
            if not stack:
                return False
            stack.pop()
    return not stack

assert next_greater([2, 1, 2, 4, 3]) == [4, 2, 4, -1, -1]
assert balanced("(()())") and not balanced("(()")
```

逐行讲解：

1. `ans = [-1] * len(nums)`：先填默认值「没有答案」，因为扫描结束后栈里剩下的就是没等到答案的元素，什么都不用做。
2. 栈里存**下标**而不是值：知道下标就能取值，也能算距离（739 要 `i - j`）、算宽度（84 要 `i - left - 1`）。**经验法则：存下标，需要值时 `nums[idx]`。**
3. `while stack and nums[stack[-1]] < x`：只要当前 `x` 比栈顶大，就说明栈顶找到了「下一个更大」，弹出并结算。是 `while` 不是 `if`——一个 `x` 可能结束很多个等待。
4. 严格 `<` 还是 `<=`：决定相等元素是否算「更大」。LC 739 要「更热」（严格），所以相等不弹；LC 84 对相等高度用 `>=` 弹出，因为相等的柱子宽度要合并算。**这是栈题最常见的 bug 来源，每次都要想一遍。**
5. `balanced` 里的 `return not stack`：循环结束后栈非空 = 有未配对的左括号。

## 3. 完整手算（Worked trace）

LC 739 输入 `[73, 74, 75, 71, 69, 72, 76, 73]`，每一行：当前下标 `i`、温度 `t`、被它结算的弹出项、以及栈（只写温度）。

```python
def temps_trace(temps):
    ans, stack = [0] * len(temps), []
    for i, t in enumerate(temps):
        popped = []
        while stack and temps[stack[-1]] < t:
            j = stack.pop()
            ans[j] = i - j
            popped.append(f"day{j}({temps[j]})->{i - j}")
        stack.append(i)
        print(f"i={i} t={t}  pops: {', '.join(popped) or '-':<28} stack(values)={[temps[k] for k in stack]}")
    return ans

assert temps_trace([73, 74, 75, 71, 69, 72, 76, 73]) == [1, 1, 4, 2, 1, 1, 0, 0]
```

```text
i=0 t=73  pops: -                            stack(values)=[73]
i=1 t=74  pops: day0(73)->1                  stack(values)=[74]
i=2 t=75  pops: day1(74)->1                  stack(values)=[75]
i=3 t=71  pops: -                            stack(values)=[75, 71]
i=4 t=69  pops: -                            stack(values)=[75, 71, 69]
i=5 t=72  pops: day4(69)->1, day3(71)->2     stack(values)=[75, 72]
i=6 t=76  pops: day5(72)->1, day2(75)->4     stack(values)=[76]
i=7 t=73  pops: -                            stack(values)=[76, 73]
```

重点看 `i=5`（72）：它先弹出 69（隔 1 天），再弹出 71（隔 2 天），遇到 75 停——75 比 72 热，75 还要继续等。栈里的温度始终是 `[75, 71, 69]` → `[75, 72]` 这样**不增**。最后栈里剩 `[76, 73]`，它们永远等不到，答案保持 0。

## 4. 题目

```python
from collections import deque
```

### 4.1 LC 20 · Valid Parentheses（Easy）

```python
# solutions/20_valid_parentheses.py
def is_valid(s):
    pairs = {")": "(", "]": "[", "}": "{"}
    stack = []
    for ch in s:
        if ch in pairs:                              # a closer: must match the latest opener
            if not stack or stack.pop() != pairs[ch]:
                return False
        else:
            stack.append(ch)
    return not stack                                 # leftover openers -> invalid
```

- **一句话洞见**：右括号必须匹配**最近**的未匹配左括号——这就是栈顶。
- **复杂度**：时间 O(n)，空间 O(n)（全是左括号时）。

**资深追问**

- **规模 ×1000**：线性不变；流式读取，栈只与「嵌套深度」成正比。
- **流式输入**：天然在线；一旦出现栈空时的右括号，可以立刻判定失败（fail-fast）而不用读完。
- **内存**：只有一种括号时，栈退化成**计数器**，O(1) 空间；多种括号才需要真栈，空间 = 最大嵌套深度。
- **并发**：括号匹配可以并行归约：每一段文本归约成「(多余的右括号序列, 多余的左括号序列)」，两段合并时左段的多余左括号和右段的多余右括号相消——这个合并是结合律的，所以可以树形并行（parallel reduce）。
- **接口 / 边界**：非括号字符是忽略还是非法？只返回 `bool`，还是返回第一个出错的位置（IDE 报错体验）？空串是否有效（这里有效）？
- **测试**：`")("`、`"(("`、`"([)]"`、空串、深嵌套；用文法随机生成合法串再随机改一个字符，检查是否被识别为非法。

### 4.2 LC 739 · Daily Temperatures（Medium）

```python
# solutions/739_daily_temperatures.py
def daily_temperatures(temps):
    ans = [0] * len(temps)
    stack = []                                   # indices whose answer is still unknown; temps decreasing
    for i, t in enumerate(temps):
        while stack and temps[stack[-1]] < t:    # t is the next warmer day for everything it beats
            j = stack.pop()
            ans[j] = i - j
        stack.append(i)
    return ans
```

- **一句话洞见**：栈里放「还在等更热日子的天」，新来的一天结算所有比它冷的。
- **复杂度**：时间 O(n)（每个下标最多入栈 / 出栈各一次），空间 O(n)。

**资深追问**

- **规模 ×1000**：线性，分块处理：每块算完后把**栈里剩余的元素**（一个单调递减序列）传给下一块继续结算，所以块间只需要传递一个很小的状态。
- **流式输入**：online，但注意答案是**延迟产生的**：第 j 天的答案要等到更热的那天才知道。需要设计成「回调 / 事件」接口，或者允许一个窗口上限（超过 N 天还没等到就返回 0）。
- **内存**：最坏（一路下降）栈大小 O(n)；设窗口上限 W 就可以丢弃过老的项，O(W)。
- **并发**：块间有依赖；用上面「传递剩余栈」的方式串行流水，块内并行不划算。
- **接口**：「更热」是严格更大；未来没有更热返回 0；输入为整数还是浮点？返回天数还是目标日期？
- **测试**：全相等、严格递增、严格递减、空、单个；暴力 O(n²) 对拍。

### 4.3 LC 84 · Largest Rectangle in Histogram（Hard）

```python
# solutions/84_largest_rectangle_in_histogram.py
def largest_rectangle_area(heights):
    stack = []                                   # indices with increasing heights
    best = 0
    for i, h in enumerate(heights + [0]):        # sentinel 0 flushes the stack at the end
        while stack and heights[stack[-1]] >= h:
            height = heights[stack.pop()]        # this bar can't extend past i
            left = stack[-1] if stack else -1    # first smaller bar on the left
            best = max(best, height * (i - left - 1))
        stack.append(i)
    return best
```

- **一句话洞见**：以第 `h` 号柱子为高的最大矩形，左右边界是它**左右两侧第一个更矮的柱子**。单调栈（高度递增）在弹出某根柱子时，同时知道了「右边第一个更矮」（当前 `i`）和「左边第一个更矮」（弹出后的新栈顶）。
- **末尾加哨兵 0**：保证最后栈里所有柱子都被弹出并结算。
- **复杂度**：时间 O(n)，空间 O(n)。
- **延伸**：LC 85 Maximal Rectangle = 逐行累计高度后，每行调用 LC 84，O(R·C)。

**资深追问**

- **规模 ×1000**：线性；分治 / 并行：分成两半，答案 = max(左半, 右半, 跨中线)，跨中线用双指针向外扩（取较高一侧），可以并行。
- **流式**：柱子逐根到来时，栈在线维护，随时能给出「已确认」的最大矩形（弹出时结算），但还在栈里的柱子的矩形只有看到后面才定。
- **内存**：最坏递增序列栈大小 O(n)。
- **并发**：栈是串行的；并行用上面的分治。
- **接口**：高度 ≥ 0；宽度恒为 1；空数组返回 0；高度可以是浮点吗（可以，算法不变）？
- **测试**：全相等（`>=` vs `>` 的 bug）、单调递增、单调递减、含 0、单个、空；暴力 O(n²) 对拍。

### 4.4 LC 239 · Sliding Window Maximum（Hard）

```python
# solutions/239_sliding_window_maximum.py
def max_sliding_window(nums, k):
    dq = deque()                         # indices; nums[dq[0]] > nums[dq[1]] > ...
    out = []
    for i, x in enumerate(nums):
        while dq and nums[dq[-1]] <= x:  # smaller elements before x can never be a max again
            dq.pop()
        dq.append(i)
        if dq[0] <= i - k:               # front fell out of the window
            dq.popleft()
        if i >= k - 1:
            out.append(nums[dq[0]])
    return out
```

- **一句话洞见**：用双端队列保存**下标**，值严格递减。新元素 `x` 把队尾所有 `<= x` 的下标弹掉（它们在窗口里永远没机会当最大值了——有一个更大且更晚离开窗口的 `x` 在），队首如果已出窗就弹掉，队首即窗口最大值。
- **暴力法**：每个窗口 `max(nums[i:i+k])` → O(n·k)。堆法 O(n log n)（需要「懒删除」）。单调队列 O(n)。
- **复杂度**：时间 O(n)，空间 O(k)。

**资深追问**

- **规模 ×1000**：线性；`k` 很大（10⁶）时队列最坏 O(k)；若是任意区间最大值查询而不是滑动窗口，用稀疏表（sparse table）O(n log n) 预处理 O(1) 查询。
- **流式**：天然适合——每来一个元素吐出一个窗口最大值，内存 O(k)。
- **内存**：想要 O(1) 额外内存可以用「分块前后缀最大」（van Herk / Gil-Werman）：把数组切成长度为 k 的块，预计算块内的前缀最大和后缀最大，窗口最大 = `max(suffix[left], prefix[right])`，需要两个 O(n) 数组但是对并行很友好。
- **并发**：上面的分块方法每个块独立，易于并行；单调队列本身是串行的。
- **接口**：`k > n`、`k <= 0` 怎么处理（抛错 / 返回空）；返回最大值列表还是下标列表；元素可否为浮点 / NaN。
- **测试**：`k = 1`、`k = n`、全相等（`<=` 与 `<` 的区别）、递减、递增、随机对拍。

## 5. 常见 bug

1. **栈里存值而不是下标**：算不了距离 / 宽度，也分不清重复值。
2. **`<` 与 `<=` 写反**：LC 84 相等高度必须一起弹（`>=`），否则宽度算短；LC 739 相等不算更热（`<`）。
3. **忘了哨兵 / 收尾**：LC 84 不加 `0`，栈里剩余的柱子永远没结算。
4. **弹出前没判断栈非空**：`stack[-1]` 在空栈上抛 `IndexError`。
5. **单调队列忘记弹出已出窗的队首**：`dq[0] <= i - k`。
6. **LC 20 只在循环里判断匹配，忘了最后检查栈是否为空**：`"("` 会被判为有效。
7. **用 `list.pop(0)` 当队列**：O(n)，要用 `deque.popleft()`。

## 6. 自测题

1. 为什么单调栈虽然有 `while` 嵌套，总时间仍是 O(n)？
   <details><summary>答案</summary>每个元素最多 `append` 一次、`pop` 一次；`while` 的总迭代次数 ≤ 总弹出次数 ≤ n。</details>
2. LC 84 里弹出柱子时，宽度为什么是 `i - left - 1`？
   <details><summary>答案</summary>`i` 是右侧第一个更矮柱子的下标，`left`（新栈顶，或 −1）是左侧第一个更矮的下标；两者之间（不含）都不矮于该柱子，所以宽度是 `i - left - 1`。</details>
3. 用栈实现队列（LC 232）需要几个栈？均摊复杂度？
   <details><summary>答案</summary>两个：入队栈 `in` 和出队栈 `out`；出队时若 `out` 为空，把 `in` 全部倒进 `out`。每个元素最多被搬一次，所以均摊 O(1)。</details>
4. 小编程：求每个元素右侧第一个**不小于**它的元素（LC 496 / 503 变体）。
   <details><summary>答案</summary>把 `nums[stack[-1]] < x` 保持为严格小于就是「严格更大」；改成 `<=` 就是「不小于」。其余模板完全相同。</details>
5. 为什么 LC 239 的队列里要存下标不存值？
   <details><summary>答案</summary>要判断队首是否已经滑出窗口（需要下标），而且有重复值时存值无法区分谁先离开。</details>
6. 资深追问：括号匹配要在一个 100GB 的文件上做，怎么并行？
   <details><summary>答案</summary>每个分块归约成「多余右括号数 / 多余左括号数」（单一括号）或对应序列（多种括号），相邻块合并时左块的多余左括号与右块的多余右括号相消；合并满足结合律，可以树形归约，最终只剩 0 个才有效。</details>
