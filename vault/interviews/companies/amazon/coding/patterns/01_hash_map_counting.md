# 01 · Hash map 计数 / 前缀和（Hash map counting & prefix sums）

> 本讲覆盖：LC 1 Two Sum · 49 Group Anagrams · 128 Longest Consecutive Sequence · 560 Subarray Sum Equals K · 41 First Missing Positive（Hard）
> 前置知识：会写 Python 的 `for` / `dict` / `set`。其余从零讲。
> 读完你应该能：(1) 一眼认出「我在反复问：之前见过 X 吗？」这类题；(2) 在三种哈希模板里选对一种；(3) 对每道题说出规模 ×1000、流式、内存受限时怎么改。

## 1. 这个模式是什么，为什么存在

### 1.1 从最笨的解法开始

Two Sum：给一个数组 `nums` 和 `target`，找两个下标，使对应的数加起来等于 `target`。

最笨的做法：对每个 `i`，再扫一遍所有 `j > i`，看 `nums[i] + nums[j] == target`。

```text
for i in range(n):
    for j in range(i + 1, n):
        if nums[i] + nums[j] == target: ...
```

复杂度 O(n²)（n = 数组长度）。n = 10⁵ 时是 5×10⁹ 次比较。Python 解释器每秒大约做 10⁷ 级别的简单操作（估算，视机器而定），所以要跑几分钟——面试里等于「超时」。

### 1.2 慢在哪里

看内层循环：对每个 `x = nums[i]`，我们其实只在问一个问题——**「数组里有没有一个值等于 `target - x`？」**
这个问题的答案对「同一个值」永远一样，却被我们用「再扫一遍数组」这种 O(n) 的方式重复回答了 n 次。

> 因果链：重复回答同一类「某个值存在吗 / 出现过几次」的问题 → 需要一个能 O(1) 回答它的结构 → 哈希表（hash table）。

### 1.3 哈希表是什么（从零讲）

- **是什么**：一个「键（key）→ 值（value）」的映射。Python 里就是 `dict`（键值对）、`set`（只有键）、`collections.Counter`（值是计数的 dict）。
- **为什么快**：内部是一个数组（桶，bucket）。存取 `key` 时先算 `hash(key)`，用它对数组长度取余，直接跳到那个格子——不用从头找。所以平均 O(1)。
- **碰撞（collision）**：两个不同的 key 算到同一个格子。Python 的 dict 用「开放寻址」：这个格子被占了就按固定规则探测下一个。装得太满（load factor 高）就整体扩容并重新放置——所以 `d[k] = v` 是**均摊（amortized）O(1)**，偶尔一次 O(n)。
- **代价**：O(n) 额外空间；key 必须可哈希（hashable）——`int/str/tuple` 可以，`list/dict/set` 不行（可变，哈希会变）。最坏情况（恶意构造碰撞）会退化到 O(n)，面试里一般不用提，但资深面试官可能追问，见下文各题。
- **没有它会怎样**：上面的 O(n²)。**有了它**：一遍扫描，每个元素问一次「`target - x` 见过吗」，O(n) 时间、O(n) 空间——**用空间换时间**。

### 1.4 三种常用形态

| 形态 | 一句话 | 典型题 |
|---|---|---|
| A. 查补数（lookup） | 边扫边存，问「我需要的那个值之前出现过吗」 | 1 Two Sum |
| B. 规范键分组 / 计数（canonical key） | 把「等价」的东西映射成同一个可哈希的键，再分组或计数 | 49 Group Anagrams、128（集合判断「是否是序列起点」） |
| C. 前缀状态 + 计数（prefix + count） | 前缀和 `P[j]`，子数组和 = `P[j] - P[i]`；把「之前出现过几次某前缀」存进哈希表 | 560 |

## 2. 模板与逐行讲解

```python
from collections import Counter, defaultdict

# Template 1: "have I already seen what I need?"  (one pass, look BEFORE you insert)
def find_pair(items, need_of):
    seen = {}                                   # value -> index
    for i, x in enumerate(items):
        want = need_of(x)
        if want in seen:
            return seen[want], i
        seen[x] = i
    return None

# Template 2: group by a canonical key (anything that is equal for "equivalent" items)
def group_by(items, key):
    groups = defaultdict(list)
    for it in items:
        groups[key(it)].append(it)              # the key must be hashable: use tuple/str/int, never list
    return dict(groups)

# Template 3: running state + how many times each state has been seen
def count_prefix_pairs(nums, k):
    seen = Counter({0: 1})                      # the empty prefix
    state = pairs = 0
    for x in nums:
        state += x                              # prefix sum so far
        pairs += seen[state - k]                # earlier prefixes that make a window with sum k
        seen[state] += 1
    return pairs

assert find_pair([2, 7, 11, 15], lambda x: 9 - x) == (0, 1)
assert group_by(["eat", "tea", "tan"], lambda w: "".join(sorted(w))) == {"aet": ["eat", "tea"], "ant": ["tan"]}
assert count_prefix_pairs([1, 1, 1], 2) == 2
```

逐行讲解（对照上面的代码）：

1. `find_pair` 里的 `seen = {}`：值 → 下标。这是整个模板的「记忆」。
2. `want = need_of(x)`：对当前元素 `x`，我**需要**什么？Two Sum 里是 `target - x`。模板化之后，换题只需要换这个函数。
3. `if want in seen`：**先查再存**。如果先 `seen[x] = i` 再查，`target = 2x` 时会把 `x` 自己当成答案（同一个元素用了两次）。这是最常见的 bug。
4. `group_by`：`key(it)` 是「规范形式」。字母异位词的规范形式是排序后的字符串或 26 位计数元组；键必须不可变（`tuple` 不是 `list`）。
5. `count_prefix_pairs`：`seen = Counter({0: 1})` 表示「空前缀出现过 1 次」——没有它，从下标 0 开始的子数组会被漏掉。
6. `pairs += seen[state - k]`：之前有多少个前缀 `p`，满足 `state - p == k`，每一个都对应一个以当前位置结尾、和为 `k` 的子数组。
7. `seen[state] += 1`：**查完再存**（和模板 A 同一条纪律：先存的话，`k == 0` 时当前前缀会和自己配对，多算出一个空子数组）。

## 3. 完整手算（Worked trace）

输入 `nums = [1, 1, 1]`，`k = 2`（LC 560）。前缀和依次是 1, 2, 3。我们用代码把每一步打印出来：

```python
def subarray_sum_trace(nums, k):
    seen = {0: 1}
    prefix = ans = 0
    print(f"k={k}  start: seen={seen}")
    for x in nums:
        prefix += x
        hit = seen.get(prefix - k, 0)
        ans += hit
        seen[prefix] = seen.get(prefix, 0) + 1
        print(f"x={x:>2} prefix={prefix:>2} look up {prefix}-{k}={prefix - k:>2} -> +{hit}  ans={ans}  seen={seen}")
    return ans

assert subarray_sum_trace([1, 1, 1], 2) == 2
```

输出：

```text
k=2  start: seen={0: 1}
x= 1 prefix= 1 look up 1-2=-1 -> +0  ans=0  seen={0: 1, 1: 1}
x= 1 prefix= 2 look up 2-2= 0 -> +1  ans=1  seen={0: 1, 1: 1, 2: 1}
x= 1 prefix= 3 look up 3-2= 1 -> +1  ans=2  seen={0: 1, 1: 1, 2: 1, 3: 1}
```

怎么读这张表：

- 第 1 行：前缀 = 1，要找 `1 - 2 = -1`，没见过，+0。
- 第 2 行：前缀 = 2，要找 `2 - 2 = 0`，见过 1 次（空前缀）→ 子数组 `[1, 1]`（下标 0..1），ans = 1。
- 第 3 行：前缀 = 3，要找 `3 - 2 = 1`，见过 1 次（第 1 个前缀）→ 子数组 `[1, 1]`（下标 1..2），ans = 2。
- 为什么能这样：`sum(nums[i+1..j]) = P[j] - P[i] = k`，所以「以 j 结尾的合法子数组个数」= 「之前等于 `P[j] - k` 的前缀个数」。

## 4. 题目

先放本讲所有解法需要的 import：

```python
from collections import Counter, defaultdict
```

### 4.1 LC 1 · Two Sum（Easy，频率 100）

```python
# solutions/1_two_sum.py
def two_sum(nums, target):
    seen = {}                       # value -> index where we saw it
    for i, x in enumerate(nums):
        need = target - x
        if need in seen:            # look BEFORE inserting x: no element is used twice
            return [seen[need], i]
        seen[x] = i
    return []
```

- **一句话洞见**：对每个 `x` 要找的只是 `target - x`，用哈希表把「之前见过的值 → 下标」存起来，一遍扫描。
- **复杂度**：时间 O(n)，空间 O(n)。

**资深追问（Senior follow-ups）**

- **规模 ×1000**（10⁵ → 10⁸ 个数）：dict 装不下（CPython 中每个条目连同 int 对象大约几十到上百字节，10⁸ 个就是 GB 级——估算）。方案：按 `min(x, target - x)` 做哈希分区（shuffle）把可能配对的数落到同一个分区/文件，再在每个分区内用内存 dict 解决；或排序后双指针（外排序）。要点是「配对的两个数必须落在同一个分区」。
- **流式输入**：数据一个个来，边来边查 `seen`，O(1)/元素；如果只要「是否存在」且允许误判，可以用 Bloom filter 先挡一层；如果只关心最近 W 个元素，要配一个队列做过期（TTL），否则内存无限增长。
- **内存受限**：排序 + 双指针只需 O(1) 额外空间，但丢了原下标（需要带着下标一起排序，空间又回到 O(n)）；说清楚这个权衡。
- **并发**：CPython 里单次 `dict` 读写在 GIL 下是原子的，但「`in seen` 然后 `seen[x] = i`」两步不是——多线程共享同一个 dict 需要锁，或者按 key 分片（sharding）各自加锁；更好的做法是数据并行：每个线程处理一段，局部 dict，最后合并时再配对。
- **接口 / 边界契约**：返回下标还是值？多组答案返回哪一组？无解返回 `[]`、`None` 还是抛异常？是否保证恰好一解？能否有重复值（`[3,3]`）、负数、0？输入会不会被修改？先问清楚再写——这是资深面试官看的「澄清」环节。
- **测试策略**：表驱动用例（重复值、负数、无解、两个元素、同一元素不能用两次）+ 与 O(n²) 暴力解随机对拍；性质：返回的两个下标不同且和等于 `target`。

### 4.2 LC 49 · Group Anagrams（Medium，频率 81）

```python
# solutions/49_group_anagrams.py
def group_anagrams(strs):
    groups = defaultdict(list)
    for s in strs:
        count = [0] * 26                       # letter histogram is the canonical form
        for ch in s:
            count[ord(ch) - ord("a")] += 1
        groups[tuple(count)].append(s)         # tuple: hashable, a list is not
    return list(groups.values())
```

- **一句话洞见**：字母异位词的「规范形式」是 26 位字母计数（或排序后的字符串），用它当 dict 的键。
- **复杂度**：时间 O(n·k)（n 个单词、最长 k），用排序当键则是 O(n·k log k)；空间 O(n·k)。

**资深追问**

- **规模 ×1000**：单机放不下时，map 阶段算出规范键，按键哈希分区到不同机器（shuffle），各机内分组——就是 MapReduce 的 word-count 形状。数据倾斜（某个键特别大）要提：对热点键加盐（salting）二次聚合。
- **流式输入**：新单词来了算键、追加到 `groups[key]`；如果分组本身无限增长，要设上限或只保留计数。
- **内存**：键用 26 个计数的 `tuple` 比排序字符串多占内存（26 个 int）；超长单词时用排序键更省，短单词时计数键更快——给出取舍。Unicode 输入怎么办（不能再假设 26 个小写字母）：用 `Counter` 的 `frozenset(items())` 或排序字符。
- **并发**：每个线程处理一个分块得到局部 `dict`，最后合并（`dict` 合并是 O(总分组数)）；避免多线程同时写同一个 `defaultdict`。
- **接口**：输出顺序是否有要求？组内顺序？大小写是否区分？空字符串算不算？（`[""]` → `[[""]]`）
- **测试**：随机生成单词 + 洗牌得到已知异位词，验证同组；与「排序键」版本对拍；空串、单字符、全相同。

### 4.3 LC 128 · Longest Consecutive Sequence（Medium，频率 75）

```python
# solutions/128_longest_consecutive_sequence.py
def longest_consecutive(nums):
    present = set(nums)
    best = 0
    for x in present:
        if x - 1 in present:        # x is not the start of a run: skip, someone else counts it
            continue
        length = 1
        while x + length in present:
            length += 1
        best = max(best, length)
    return best
```

- **一句话洞见**：只有「没有前驱 `x-1` 的数」才是序列起点，只从起点向右数——每个数最多被数一次，整体 O(n)。
- **复杂度**：时间 O(n)（`while` 内层总共只会被各起点触发，加起来不超过 n 次），空间 O(n)。
- **为什么不排序**：排序是 O(n log n)，题目要求 O(n)；也别忘了去重。

**资深追问**

- **规模 ×1000**：集合放不下时，可以排序（外排序）后线性扫描，用 O(n log n) 换内存；或者用并查集（Union-Find）把相邻值合并。分布式：按值范围分区（range partition），每个分区内求局部最长，再合并**跨分区边界**的两段（边界是关键细节）。
- **流式**：插入一个数 `x` 时，看 `x-1` 和 `x+1` 所在序列的长度，用字典 `length_at_endpoint[value]` 只维护端点上的长度，O(1) 更新，随时能回答当前最长——这是在线版本。
- **内存**：Bitmap（值域小且稠密时），空间 = 值域/8 字节。
- **并发**：只读的静态数据可以并行：各线程处理不同的起点，因为每个序列只有一个起点，不会重复计算。
- **接口**：空数组返回 0；重复元素不重复计数；返回长度还是序列本身？
- **测试**：重复、负数、全相同、单元素、乱序；对拍排序版本。

### 4.4 LC 560 · Subarray Sum Equals K（Medium，频率 75）

```python
# solutions/560_subarray_sum_equals_k.py
def subarray_sum(nums, k):
    seen = {0: 1}                   # prefix sum 0 occurred once (the empty prefix)
    prefix = 0
    ans = 0
    for x in nums:
        prefix += x
        ans += seen.get(prefix - k, 0)   # earlier prefixes p with prefix - p == k
        seen[prefix] = seen.get(prefix, 0) + 1
    return ans
```

- **一句话洞见**：子数组和 = 两个前缀和之差，把「前缀和 → 出现次数」存进哈希表。
- **为什么不能用滑动窗口**：数组里可以有负数 / 0，窗口和不再随右扩单调增加，「和太大就收左边」的前提不成立。
- **复杂度**：时间 O(n)，空间 O(n)。

**资深追问**

- **规模 ×1000**：哈希表大小与「不同前缀和的个数」成正比，最坏 O(n)。大数据下可以分块：对每块先算局部前缀和计数，跨块的子数组用「块边界前缀」处理（分治 + 合并）；或把前缀和取值哈希分桶。
- **流式**：在线版本——不断更新 `prefix` 和 `seen`，每个新元素 O(1) 回答「以它结尾的、和为 k 的子数组个数」；只想要「最近 W 个元素内」就得用带过期的计数。
- **内存**：如果只需要「是否存在」而不是个数，`set` 即可；个数要 `dict`。若 `k` 是区间（≥ k）则哈希不再适用，需要平衡树 / 树状数组。
- **并发**：前缀和是顺序依赖，但可以分块并行：各块独立算块内前缀，再用块总和做偏移（并行前缀和 / parallel scan）。
- **接口**：值域会不会溢出（Python 不会，Java/C++ 要用 `long`）？`k` 可负吗？是否要返回子数组本身而不是个数？
- **测试**：含负数和 0 的用例（滑动窗口会错）、`k = 0`、全 0、空数组、与 O(n²) 暴力对拍（文件里已有 300 组随机用例）。

### 4.5 LC 41 · First Missing Positive（Hard，频率 62）

```python
# solutions/41_first_missing_positive.py
def first_missing_positive(nums):
    n = len(nums)
    for i in range(n):
        # put value v at index v-1, as long as v is in range and not already there
        while 1 <= nums[i] <= n and nums[nums[i] - 1] != nums[i]:
            j = nums[i] - 1
            nums[i], nums[j] = nums[j], nums[i]
    for i in range(n):
        if nums[i] != i + 1:
            return i + 1
    return n + 1


def first_missing_positive_set(nums):          # O(n) space baseline; say this one first
    present = set(nums)
    ans = 1
    while ans in present:
        ans += 1
    return ans
```

- **一句话洞见**：答案一定在 `1..n+1` 里，所以把数组本身当哈希表——值 `v` 应该待在下标 `v-1`；归位之后第一个「下标和值对不上」的位置就是答案。
- **先说基线**：`set` 版本 O(n) 时间 O(n) 空间，先把它说出来（`first_missing_positive_set`），再说「题目要 O(1) 空间」→ 原地归位。
- **复杂度**：时间 O(n)（每次交换至少把一个数放到最终位置，总交换 ≤ n），空间 O(1)。

**资深追问**

- **规模 ×1000**：原地方法不需要额外内存，但会修改输入；数据在磁盘上时，一遍扫描标记「出现过」到一个 bitmap（n 位），再找第一个没有设置的位——O(n/8) 字节。
- **流式**：流里数据只能看一遍时，维护一个 bitmap + 当前最小缺失值指针，指针只增不减，均摊 O(1)。
- **内存**：对比 `set`（O(n)）、bitmap（n/8 字节）、原地归位（O(1) 但破坏输入）——说出各自的代价，让面试官选。
- **并发**：原地交换不是线程安全的；若要并行，用 bitmap（每个线程设置不同的位，用原子 OR），最后顺序找首个 0。
- **接口**：「是否允许修改输入」必须先问；重复元素（`[1,1]`）会让归位循环卡死，除非检查 `nums[nums[i]-1] != nums[i]`；元素范围是否超过 `n`、是否有负数。
- **测试**：`[1,1]`、全负数、已经是 `1..n` 的排列、空数组、含超大值；与 `set` 版本随机对拍。

## 5. 常见 bug

1. **先存后查**（Two Sum）：`target = 2x` 时把同一个元素用了两次。纪律：先查再存。
2. **忘记 `{0: 1}`**（560）：从下标 0 开始的子数组被漏掉。
3. **用 list 当 dict 的键**：`TypeError: unhashable type`。转成 `tuple` / `str`。
4. **用滑动窗口做 560**：有负数时窗口和不单调，答案错。
5. **128 对每个数都向右数**：退化成 O(n²)（例如 `1..n` 每个数都向右数一遍）。必须先判断 `x - 1 not in set`。
6. **`dict.get(k)` 返回 `None` 后直接加法**：用 `get(k, 0)` 或 `Counter`。
7. **遍历 dict 的同时修改它**：`RuntimeError: dictionary changed size during iteration`。先 `list(d)` 再改。

## 6. 自测题

1. 为什么 Two Sum 的哈希版本是「用空间换时间」？具体换了什么？
   <details><summary>答案</summary>多用了 O(n) 的哈希表，把内层「扫一遍找补数」的 O(n) 变成 O(1) 查找，总时间 O(n²) → O(n)。</details>
2. `seen = {0: 1}` 在 560 里代表什么？去掉会错在哪？
   <details><summary>答案</summary>代表「空前缀出现过一次」，使得从下标 0 开始、和恰为 k 的子数组被计数。去掉后，例如 `[2]`、`k=2` 会得到 0。</details>
3. 为什么 `x - 1 in present` 时可以直接 `continue`（LC 128）？
   <details><summary>答案</summary>`x` 不是某个连续序列的起点，它会被该序列的起点数到；跳过它保证每个数只被数一次，总时间 O(n)。</details>
4. 「字符串排序后当键」和「26 位计数元组当键」各什么时候更好？
   <details><summary>答案</summary>单词很长、字母表很小：计数元组 O(k) 建键更快；单词很短或字母表很大（Unicode）：排序键更省空间，实现更简单。</details>
5. 小编程：写一个函数判断数组中是否存在两个不同下标 `i != j` 使 `nums[i] - nums[j] == k`（`k > 0`）。
   <details><summary>答案</summary>用 `set`：`present = set(nums)`；`any(x + k in present for x in present)`。注意 `k = 0` 时需要某值出现至少两次（用 `Counter`）。复杂度 O(n)。</details>
6. 资深追问：Two Sum 的数据有 10¹⁰ 个数，你怎么做？
   <details><summary>答案</summary>按 `min(x, target - x)` 对数据做哈希分区（shuffle），让互为补数的两个数进入同一个分区；每个分区放得下内存时用 dict 求解，放不下就递归再分区或外排序 + 双指针。可以并行处理各分区。</details>
