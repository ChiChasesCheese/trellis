# hc01 · 解法与原理

买卖股票是一族题，规则一条条加，但解法都是同一个想法：每天结束时，你要么手里有股，要么没有，对这两种情况各记一个「到目前为止最多赚了多少」，第二天只用这两个数就能算出新的两个数。下面先说开场 3 分钟怎么做，然后每个 Part 给出思路、原理和两种语言的完整代码，最后是口头追问的答案。

## 开场 3 分钟：先把问题问清楚

你可以这样说：

> "I'll scan the prices once. For one transaction I track the lowest price so far and the best profit so far. Questions: can I buy and sell on the same day? If prices only fall, do I return 0? Is the input sorted by day, and can it be empty?"

面试官通常会说：不赚钱就返回 0，同一天只做一个动作，数组可能为空。

## Part 1 · 一次交易和次数不限

**一次交易的思路**：从左到右扫，记住「到今天为止的最低价」。把今天当作卖出日，利润是今天的价格减最低价，取最大值。

**原理：为什么不是「全局最小值和全局最大值相减」**

买必须在卖之前。`[2,10,0,1]` 里最低价 0 在最高价 10 之后，直接相减会得到 10，但实际能做到的最好是 2 买、10 卖，赚 8。边扫边更新最低价，保证了最低价一定在今天之前（或就是今天，利润 0）。

**次数不限的思路**：每一段上涨都能吃到。把相邻两天的差为正的部分全加起来。

**原理：为什么相邻差之和是对的**

1→5→6 这样连续上涨，从 1 买到 6 卖赚 5，和 1→5 赚 4、5→6 赚 1 加起来一样。遇到下跌就不持有，把下跌那一天的差记为 0。所以最优解就是所有正差之和，不用找具体的买卖点。

**Java**

```java
public static long maxProfitOnce(long[] prices) {
    long minPrice = Long.MAX_VALUE, best = 0;
    for (long p : prices) {
        minPrice = Math.min(minPrice, p);
        best = Math.max(best, p - minPrice);
    }
    return best;
}

public static long maxProfitUnlimited(long[] prices) {
    long profit = 0;
    for (int i = 1; i < prices.length; i++) profit += Math.max(0, prices[i] - prices[i - 1]);
    return profit;
}
```

**C++**

```cpp
inline long long max_profit_once(const std::vector<long long>& prices) {
    long long min_price = LLONG_MAX, best = 0;
    for (long long p : prices) {
        min_price = std::min(min_price, p);
        best = std::max(best, p - min_price);
    }
    return best;
}

inline long long max_profit_unlimited(const std::vector<long long>& prices) {
    long long profit = 0;
    for (size_t i = 1; i < prices.size(); ++i) profit += std::max(0LL, prices[i] - prices[i - 1]);
    return profit;
}
```

复杂度：时间 O(n)，空间 O(1)。

## Part 2 · 最多 k 笔

**思路**：先写出状态。`free[j]` 是「手里没股，已经做完 j 笔」时的最大利润，`hold[j]` 是「手里有股，已经买入 j 次」时的最大利润。每天看一个价格 p，对每个 j 做两步：

- 买：从「做完 j-1 笔、没股」买入，`hold[j] = max(hold[j], free[j-1] - p)`。
- 卖：从「持有」卖出，`free[j] = max(free[j], hold[j] + p)`。

初始 `free` 全是 0，`hold` 是负无穷（还没买过，不可能持有）。答案是 `free[k]`。

**原理：为什么 j 要倒着循环**

买入用到的是「昨天」的 `free[j-1]`。如果 j 从小到大，`free[j-1]` 在今天已经被更新过，等于允许同一天先卖再买。这样答案仍然正确（同一天卖出再买入，利润等于什么都没做），但倒着循环能让每一步都对应「今天只做一个动作」，更好解释。

**原理：为什么 k 要先压到 n/2**

一笔交易至少占两天，n 天最多完成 n/2 笔。`k` 比这个大时，限制已经不起作用，答案和「次数不限」一样。不压的话，`k = Integer.MAX_VALUE` 会让数组大到内存放不下，并且 O(n·k) 的循环也跑不完。压到 n/2 之后，时间 O(n·min(k, n/2))，空间 O(min(k, n/2))。

**Java**

```java
public static long maxProfitAtMost(int k, long[] prices) {
    k = Math.min(k, prices.length / 2);  // n 天最多完成 n/2 笔
    if (k <= 0) return 0;
    long[] hold = new long[k + 1], free = new long[k + 1];
    Arrays.fill(hold, Long.MIN_VALUE / 2);
    for (long p : prices) {
        for (int j = k; j >= 1; j--) {  // 倒着更新：free[j - 1] 还是昨天的值
            hold[j] = Math.max(hold[j], free[j - 1] - p);
            free[j] = Math.max(free[j], hold[j] + p);
        }
    }
    return free[k];
}
```

**C++**

```cpp
inline long long max_profit_at_most(int k, const std::vector<long long>& prices) {
    k = static_cast<int>(std::min<long long>(k, prices.size() / 2));
    if (k <= 0) return 0;
    std::vector<long long> hold(k + 1, LLONG_MIN / 2), free(k + 1, 0);
    for (long long p : prices)
        for (int j = k; j >= 1; --j) {
            hold[j] = std::max(hold[j], free[j - 1] - p);
            free[j] = std::max(free[j], hold[j] + p);
        }
    return free[k];
}
```

初始的 `hold` 用 `Long.MIN_VALUE / 2` 而不是 `Long.MIN_VALUE`：后者再减一个价格就会溢出。

## Part 3 · 口头追问和回答

**1. 卖出后冷却一天才能再买（LeetCode 309），怎么改？**

状态从两个变成三个：`FREE`（没股，可以买）、`HOLD`（有股）、`COOL`（刚卖出，今天不能买）。多出来的转移只有两条：卖出之后进入 `COOL` 而不是 `FREE`，`COOL` 过一天变回 `FREE`。代码是下面五行，每天用旧值同时更新三个变量：

```java
long hold = -prices[0], free = 0, cool = 0;
for (int i = 1; i < prices.length; i++) {
    long p = prices[i];
    long newHold = Math.max(hold, free - p);  // 继续持有，或者从 FREE 买入
    long newCool = hold + p;                  // 今天卖出
    long newFree = Math.max(free, cool);      // 继续空仓，或者冷却结束
    hold = newHold; cool = newCool; free = newFree;
}
// 答案：Math.max(free, cool)
```

例子：`[1,2,3,0,2]` 得 3（1 买、2 卖，冷却，0 买、2 卖）。

**2. 每笔卖出要付手续费（LeetCode 714），怎么改？**

状态不变，只在卖出那条转移上减去手续费：`free = max(free, hold + p - fee)`，`hold = max(hold, free - p)`。手续费只在卖出时扣一次（也可以只在买入时扣，结果相同）。例子：`fee=2, [1,3,2,8,4,9]` 得 8。

**3. 这几个变体是不是同一个东西？**

是。都是「每天一个状态，用箭头画出今天能怎么走到明天」。一次、不限、k 笔、冷却、手续费，区别只是状态里多记不记「已用几笔」和「是否在冷却」，以及卖出那条箭头是否带一个费用或延迟。先画状态机，再把每条箭头写成一行 `max`，不容易漏。

**4. 除了利润，还要报出具体哪天买、哪天卖，怎么做？**

对每一天、每个状态，多记「这个最大值是从哪个状态来的」（前驱）。扫完之后从终点状态倒着沿前驱走回去，状态从 `FREE` 变成 `HOLD` 的那天是买入日，从 `HOLD` 变回来的那天是卖出日。代价是要保存整张表，空间从 O(k) 变成 O(n·k)。次数不限时更简单：每段上涨的起点和终点就是一笔交易。

**5. n 非常大（装不进内存）时怎么办？**

只求利润的话，上面的写法每天只用昨天的状态，是流式的：读一天处理一天，空间 O(k)，不需要把价格全部放进内存。要还原交易就比较麻烦，因为倒着走需要整张表。一种办法是只存每隔 B 天的状态（检查点，每个是长度 k 的一行），回溯时从后往前对每一块重新算一遍、只保留这一块的决策，用大约两倍的时间换 O((n/B + B)·k) 的空间；B 取 √n 时是 O(√n·k)。

## 常见错误

1. 一次交易用「全局最小值和全局最大值相减」：最低价可能出现在最高价之后。
2. 次数不限时找每一段的起点和终点：容易漏掉边界，直接累加正差更简单。
3. `k` 很大时 `new long[k + 1]`：内存放不下。
4. 初始 `hold` 填 0：等于「免费拥有一股」，利润偏大；必须是负无穷。
5. 初始 `hold` 填 `Long.MIN_VALUE`：再减一个价格就溢出。
6. 冷却期用「卖完直接回到 `FREE`」：冷却那一天就能再买，答案偏大。
