# hc19 · 解法与原理

打家劫舍的核心只有一句话：对每个位置，要么选它，要么不选它，两种情况各留一个最好成绩。后面的追问都是在这个骨架上换形状：环、树、返回方案、负数。下面先说开场 3 分钟，然后每个 Part 给出思路、原理和两种语言的完整代码，最后是口头追问的答案。

## 开场 3 分钟：先把问题问清楚

你可以这样说：

> "For each position I either take it or skip it. If I take it, the previous one must have been skipped. Can amounts be negative? Can the array be empty? Could the total exceed 32 bits?"

面试官通常会说：金额非负，可能为空，总和用 `long`。

## Part 1 · 两个滚动变量

**思路**：用 `take` 表示「选了当前位置」时前面所有位置的最好成绩，`skip` 表示「没选当前位置」时的最好成绩，从左到右扫一遍。

**原理**：

- 选当前位置 `x`，上一个位置就一定没选，所以新的 `take = 旧 skip + x`。
- 不选当前位置，上一个位置选不选都可以，所以新的 `skip = max(旧 skip, 旧 take)`。
- 每一步只依赖上一步的两个值，所以不用数组，空间 O(1)。更新 `take` 要用旧的 `skip`，所以先把 `skip + x` 存到临时变量，再更新 `skip`。
- 最后答案是 `max(take, skip)`。空数组两个变量都是 0，自然返回 0。

**Java**

```java
public static long maxLoot(long[] nums) {
    long take = 0, skip = 0;
    for (long x : nums) {
        long nextTake = skip + x;
        skip = Math.max(skip, take);
        take = nextTake;
    }
    return Math.max(take, skip);
}
```

**C++**

```cpp
inline long long max_loot(const std::vector<long long>& nums) {
    long long take = 0, skip = 0;
    for (long long x : nums) {
        long long next_take = skip + x;
        skip = std::max(skip, take);
        take = next_take;
    }
    return std::max(take, skip);
}
```

复杂度：时间 O(n)，空间 O(1)。

## Part 2 · 返回选中的下标

**思路**：这次保留整个数组 `best`，`best[i]` 表示只看前 `i` 个位置的最大总金额，`best[0] = 0`。再从 `i = n` 往回走，一边走一边记下选了谁。

**原理**：

- `best[i] = max(best[i-1], best[i-2] + nums[i-1])`，其中 `best[-1]` 当作 0。第一项是不选第 `i-1` 号位置，第二项是选它。
- 往回走时看 `best[i]` 和 `best[i-1]` 是否相等。相等说明不选最后一个位置也能达到同样的总金额，按规则**优先不选**，`i` 减 1；不相等说明一定选了它，记下 `i-1`，然后跳过它左边的相邻位置，`i` 减 2。
- 这样走出来的下标是倒序的，最后反转。
- 平局规则必须写死，否则同一个输入可以有几个都对的答案，测试没法判。`[5,5]` 里 `best = [0,5,5]`，`best[2] == best[1]`，不选下标 1，再看 `best[1] != best[0]`，选下标 0，得到 `[0]`。

**Java**

```java
public static List<Integer> chosenIndices(long[] nums) {
    int n = nums.length;
    long[] best = new long[n + 1];
    for (int i = 1; i <= n; i++) {
        long withLast = (i >= 2 ? best[i - 2] : 0) + nums[i - 1];
        best[i] = Math.max(best[i - 1], withLast);
    }
    List<Integer> picked = new ArrayList<>();
    int i = n;
    while (i > 0) {
        if (best[i] == best[i - 1]) {
            i--;
        } else {
            picked.add(i - 1);
            i -= 2;
        }
    }
    Collections.reverse(picked);
    return picked;
}
```

**C++**

```cpp
inline std::vector<int> chosen_indices(const std::vector<long long>& nums) {
    const int n = static_cast<int>(nums.size());
    std::vector<long long> best(n + 1, 0);
    for (int i = 1; i <= n; ++i)
        best[i] = std::max(best[i - 1], (i >= 2 ? best[i - 2] : 0) + nums[i - 1]);
    std::vector<int> picked;
    for (int i = n; i > 0;) {
        if (best[i] == best[i - 1]) {
            --i;
        } else {
            picked.push_back(i - 1);
            i -= 2;
        }
    }
    std::reverse(picked.begin(), picked.end());
    return picked;
}
```

复杂度：时间 O(n)，空间 O(n)。

## Part 3 · 口头追问和回答

**1. 环形街怎么办？**

首尾相邻，所以第一个和最后一个位置不能同时选。把它拆成两个直线问题：只在下标 `0..n-2` 上做一遍，只在 `1..n-1` 上做一遍，取较大的。这两个范围覆盖了「不选最后一个」和「不选第一个」两种情况，任何合法方案必然落在其中一种里。`n == 1` 要单独处理，直接返回 `nums[0]`，否则两个范围都是空的。时间仍是 O(n)，空间 O(1)。

**2. 位置组成一棵树怎么办？**

做一次深度优先搜索（DFS），每个节点返回一对值 `(take, skip)`：`take = 节点金额 + 所有孩子的 skip 之和`，`skip = 所有孩子的 max(take, skip) 之和`，根节点的答案是 `max(take, skip)`。思路和直线完全一样，「上一个」变成了「孩子」。每个节点只访问一次，时间 O(n)，递归栈深度等于树高，退化成一条链时是 O(n)。

**3. 为什么贪心不行？**

「每次拿最大的」会把两边的邻居一起封死。`[2,3,2]`：先拿 3 之后两边都不能拿，总共 3；而拿两个 2 得 4。再看 `[4,5,4,1,4]`：先拿 5 之后只剩下标 3 和 4 里的一个，最多 5 + 4 = 9，而选下标 0、2、4 得 12。局部最大不能保证全局最大，因为一次选择会影响后面哪些位置还能选，DP 把两种情况都留着，所以才对。

**4. 金额可以是负数时，Part 1 还对吗？**

对，前提是允许一个都不选，此时答案至少是 0。`skip` 从 0 开始并且不会变小，所以负数金额永远不会让答案低于 0，选不选负数位置由 `max` 自然决定。如果规定「必须至少选一个」，全是负数时答案应该是最大的那个负数，初始值就不能再用 0，要用第一个元素来初始化，并且特别处理。Part 2 的往回走同样成立：选上负数位置只会让总额变小，`best[i]` 等于 `best[i-1]`，按平局规则就不会选它。

**5. 为什么返回下标不能只用两个变量？**

两个变量只记得「到目前为止的最好成绩」，不记得是怎么得到的。要还原方案，要么每一步都记下做了哪个选择（O(n) 空间），要么像 Part 2 这样保留 `best` 数组，从后往前比较相邻两项来推出选择。所以 O(1) 空间的写法只能求金额，不能求方案。

## 常见错误

1. 更新 `skip` 之后再用它算 `take`：`take` 用到的是已经更新过的 `skip`，结果偏大。先算临时变量再更新。
2. 用 `int` 存金额或总和：超过约 21 亿时静默回绕成负数。
3. 往回走时选中后只把 `i` 减 1：会选到相邻的位置，应该减 2。
4. 平局规则没有固定：同一个输入两次运行结果不同，或者和测试期望的方案不同。
5. 环形街忘了 `n == 1`：两个范围都为空，返回 0，而不是 `nums[0]`。
