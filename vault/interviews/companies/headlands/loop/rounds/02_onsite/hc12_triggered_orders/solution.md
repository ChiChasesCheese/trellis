# hc12 · 解法与原理

订单筛选看起来简单，其实是订单簿（order book）的最小版本：买单和卖单各一堆，新来的订单拿自己的价格去碰对手方最优的一档。Part 1 只需要两个数，Part 2 需要能随时取走最优价的数据结构。下面先说开场 3 分钟怎么做，再给出每个 Part 的思路、原理和两种语言的完整代码。

## 开场 3 分钟：先把问题问清楚

你可以这样说：

> "A BUY is triggered if its price is at least the lowest sell seen so far, and a SELL is triggered if its price is at most the highest buy seen so far. Does equal price count as a trigger? Do earlier orders stay in play after they trigger, or does a match remove them?"

面试官通常会说：相等算触发；先做最简单的版本，早先的订单一直算数；然后再问触发以后会不会吃掉对手单。先把 Part 1 的规则讲定，再去想 Part 2。

## Part 1 · 早先的订单从不被消耗

**思路**：扫一遍，只维护两个数：`minSell`（见过的最低卖价）和 `maxBuy`（见过的最高买价）。每张订单先和对手方的那个数比，再更新自己方向的那个数。

**原理**：买单能不能和某张先前的卖单成交，只取决于有没有卖价 ≤ 自己的价格，这等价于「最低卖价 ≤ 自己的价格」。所以不用保存所有订单，两个数就够了。顺序不能反：先更新再比较，订单会和自己比较。

**Java**

```java
public static List<Integer> triggeredSimple(int[] prices, String[] sides) {
    List<Integer> out = new ArrayList<>();
    int minSell = Integer.MAX_VALUE, maxBuy = Integer.MIN_VALUE;
    for (int i = 0; i < prices.length; i++) {
        if (isBuy(sides[i])) {
            if (prices[i] >= minSell) out.add(i);
            maxBuy = Math.max(maxBuy, prices[i]);
        } else {
            if (prices[i] <= maxBuy) out.add(i);
            minSell = Math.min(minSell, prices[i]);
        }
    }
    return out;
}
```

`isBuy` 对 `"BUY"` 返回 true，对 `"SELL"` 返回 false，其他字符串抛 `IllegalArgumentException`。

**C++**

```cpp
inline std::vector<int> triggered_simple(const std::vector<int>& prices, const std::vector<std::string>& sides) {
    std::vector<int> out;
    int min_sell = std::numeric_limits<int>::max(), max_buy = std::numeric_limits<int>::min();
    for (int i = 0; i < static_cast<int>(prices.size()); ++i) {
        if (is_buy(sides[i])) {
            if (prices[i] >= min_sell) out.push_back(i);
            max_buy = std::max(max_buy, prices[i]);
        } else {
            if (prices[i] <= max_buy) out.push_back(i);
            min_sell = std::min(min_sell, prices[i]);
        }
    }
    return out;
}
```

复杂度：时间 O(n)，额外空间 O(1)（不算输出）。

## Part 2 · 触发就吃掉最优挂单

**思路**：卖单放进一个小根堆（min-heap，堆顶是最低卖价），买单放进一个大根堆（max-heap，堆顶是最高买价）。来一张买单：如果卖堆非空且 `price >= 堆顶`，弹出堆顶，记下这张订单的下标；否则把它推进买堆。卖单对称。

**原理**：Part 1 里订单永远不消失，所以两个数就够；现在触发会把一张挂单拿走，拿走后「次优的那张」就变成了新的最优，你需要一个随时能取出最优、又能删除最优的结构。堆正好做这两件事：取堆顶 O(1)，弹出和插入 O(log n)。触发的订单本身不进簿子，因为它已经成交了。Java 的 `PriorityQueue` 默认是小根堆，买堆要传 `Collections.reverseOrder()`；C++ 的 `std::priority_queue` 默认是大根堆，卖堆要传 `std::greater<int>`。这是最容易写反的地方。

**Java**

```java
public static List<Integer> triggeredConsuming(int[] prices, String[] sides) {
    List<Integer> out = new ArrayList<>();
    PriorityQueue<Integer> sells = new PriorityQueue<>();
    PriorityQueue<Integer> buys = new PriorityQueue<>(Collections.reverseOrder());
    for (int i = 0; i < prices.length; i++) {
        int p = prices[i];
        if (isBuy(sides[i])) {
            if (!sells.isEmpty() && p >= sells.peek()) { sells.poll(); out.add(i); } else buys.add(p);
        } else {
            if (!buys.isEmpty() && p <= buys.peek()) { buys.poll(); out.add(i); } else sells.add(p);
        }
    }
    return out;
}
```

**C++**

```cpp
inline std::vector<int> triggered_consuming(const std::vector<int>& prices, const std::vector<std::string>& sides) {
    std::vector<int> out;
    std::priority_queue<int, std::vector<int>, std::greater<int>> sells;
    std::priority_queue<int> buys;
    for (int i = 0; i < static_cast<int>(prices.size()); ++i) {
        const int p = prices[i];
        if (is_buy(sides[i])) {
            if (!sells.empty() && p >= sells.top()) { sells.pop(); out.push_back(i); } else buys.push(p);
        } else {
            if (!buys.empty() && p <= buys.top()) { buys.pop(); out.push_back(i); } else sells.push(p);
        }
    }
    return out;
}
```

复杂度：每张订单最多一次堆插入或一次堆弹出，时间 O(n log n)，空间 O(n)（挂单都留在堆里）。

## Part 3 · 口头追问和回答

**1. Part 2 为什么要堆，Part 1 为什么不用？各自的复杂度是多少？**

Part 1 里订单从不消失，「最低卖价」只会越变越小，一个变量就能跟踪。Part 2 里堆顶被吃掉之后，要立刻知道次低的卖价是多少，只存一个数做不到，必须保留所有挂单并能高效取最小值。Part 1 是 O(n) 时间 O(1) 空间，Part 2 是 O(n log n) 时间 O(n) 空间。也可以用有序映射（Java `TreeMap`，C++ `std::map`）代替堆，复杂度相同，但还能按价格范围查询。

**2. 订单带数量，一张订单只吃掉一部分怎么办？**

这时就是真正的撮合（order matching）。触发的订单对着对手方最优价逐档吃：吃掉 `min(自己剩余数量, 挂单数量)`，两边各减去这个数；挂单减到 0 就弹出，自己还有剩余就继续吃下一档；最后剩下的部分如果是限价单就挂进簿子。堆里存的不再只是价格，而是（价格，数量）或者每个价位一个队列。一张订单可能触发多次成交，所以「返回下标」要改成「返回成交列表」。

**3. 同一个价格上有好几张挂单，先吃哪张？**

只返回下标时，价格相同的挂单谁被吃掉不影响结果，所以堆里只存价格就够了。真实的交易所用价格优先、时间优先（price-time priority）：先比价格，价格相同比到达顺序。实现上把堆的键改成（价格，到达序号），或者每个价位一个先进先出队列。

**4. 很多个标的（symbol）同时进来怎么办？**

每个标的有自己独立的一对堆，用 `Map<symbol, Book>` 按标的分发，不同标的之间互不影响。这也方便并行：按标的哈希到不同的线程，每个线程只读写自己那几个簿子，不需要加锁，同一个标的内部仍然按到达顺序处理。

**5. 真正的止损单（stop order）是按最新成交价触发的，怎么实现？**

止损单有一个触发价（stop price）。买止损单在最新成交价 ≥ 触发价时触发，卖止损单在最新成交价 ≤ 触发价时触发。把没触发的买止损单放进小根堆（堆顶是最低触发价），卖止损单放进大根堆；每次发生成交，更新最新成交价，然后只要堆顶满足条件就弹出，变成一张正常订单送进撮合。触发的止损单可能又产生新的成交，所以这是一个循环：处理到没有新的触发为止。

## 常见错误

1. 先更新 `minSell` / `maxBuy` 再比较：订单和自己比较，第一张订单就会被触发。
2. Part 1 里只在订单没触发时才更新两个数：与「早先的订单一直算数」矛盾。
3. Part 2 里触发的订单也放进堆：它已经成交了，后面的订单会再次吃到它。
4. 把大小根堆写反：Java 默认是小根堆，C++ 默认是大根堆。
5. 用 `<` 代替 `<=`：价格相等的订单漏掉。
