# hc18 · 解法与原理

持仓是「某个时刻的完整状态」加上「那之后发生的变化」。快照给出状态，成交给出变化。Part 1 里事件按顺序到，直接覆盖和累加就行；Part 2 事件乱序，关键是知道每笔成交到底在不在某个快照里，这只能靠序号。下面先说开场 3 分钟怎么做，再给出每个 Part 的思路、原理和两种语言的完整代码。

## 开场 3 分钟：先把问题问清楚

你可以这样说：

> "A snapshot replaces the position for its symbol, a fill adds for BUY and subtracts for SELL. I'll return a sorted map and keep symbols whose net is zero. Are the sequence numbers per symbol, and can events arrive out of order or twice?"

面试官通常会说：先按顺序处理；序号在标的内比较；之后会问乱序。先把 Part 1 写完，再谈序号。

## Part 1 · 按到达顺序处理

**思路**：用一个有序映射（Java `TreeMap`，C++ `std::map`）保存标的到持仓。快照直接 `put`，成交按方向加或减。

**原理**：有序映射让结果自然按标的排序。成交用「加 qty 或减 qty」，不需要先知道标的有没有出现过：Java 的 `merge` 和 C++ 的 `operator[]` 都会从 0 开始。数量为 0 的标的留在结果里，因为它表示「我们知道这个标的，现在是平的」，和「没有出现过」不同。

**Java**

```java
public static Map<String, Long> positionsInOrder(List<Event> events) {
    Map<String, Long> pos = new TreeMap<>();
    for (Event e : events) {
        if (e.isSnapshot()) pos.put(e.symbol(), e.qty());
        else pos.merge(e.symbol(), signed(e), Long::sum);
    }
    return pos;
}
```

`signed(e)` 对 `BUY` 返回 `qty`，对 `SELL` 返回 `-qty`，其他方向抛 `IllegalArgumentException`。

**C++**

```cpp
inline std::map<std::string, long long> positions_in_order(const std::vector<Event>& events) {
    std::map<std::string, long long> pos;
    for (const Event& e : events) {
        if (e.is_snapshot) pos[e.symbol] = e.qty;
        else pos[e.symbol] += signed_qty(e);
    }
    return pos;
}
```

复杂度：时间 O(n log s)（s 是标的个数），空间 O(s)。

## Part 2 · 乱序到达

**思路**：每个标的保存三样东西：最新采用的快照的 `snapSeq` 和 `snapQty`，以及一个 `seq → 带符号数量` 的有序映射 `fills`，只放 seq 大于 `snapSeq` 的成交。

- 来了快照：`seq <= snapSeq` 就丢掉；否则采用它，并从 `fills` 里删掉所有 `seq <=` 它的成交。
- 来了成交：`seq <= snapSeq` 就丢掉；否则放进 `fills`，已经有同一个 seq 就不覆盖。
- 最后，持仓 = `snapQty` + `fills` 里所有数量之和。

**原理**：快照 seq 的意思是「序号 ≤ seq 的成交都已经算进去了」，所以这些成交再加一次就是重复计算；序号更大的成交没算进去，必须加上。成交可能比快照先到，所以不能一来就加到一个数上，否则后到的快照一覆盖，这笔成交就丢了。把成交按 seq 存下来，快照到的时候再裁剪，顺序就无关紧要了。用 seq 做键同时解决了重复投递：同一个 seq 只会留一份。

**Java**

```java
private static final class State {
    long snapSeq = 0, snapQty = 0;
    final TreeMap<Long, Long> fills = new TreeMap<>();
}

public static Map<String, Long> positions(List<Event> events) {
    Map<String, State> states = new HashMap<>();
    for (Event e : events) {
        State s = states.computeIfAbsent(e.symbol(), k -> new State());
        if (e.isSnapshot()) {
            if (e.seq() <= s.snapSeq) continue;
            s.snapSeq = e.seq();
            s.snapQty = e.qty();
            s.fills.headMap(e.seq(), true).clear();
        } else if (e.seq() > s.snapSeq) {
            s.fills.putIfAbsent(e.seq(), signed(e));
        }
    }
    Map<String, Long> out = new TreeMap<>();
    for (var en : states.entrySet()) {
        long total = en.getValue().snapQty;
        for (long d : en.getValue().fills.values()) total += d;
        out.put(en.getKey(), total);
    }
    return out;
}
```

参考解里还有一行 `else signed(e);`，只是为了让被忽略的成交也检查方向是否合法；面试里可以省略。

**C++**

```cpp
struct State {
    long long snap_seq = 0, snap_qty = 0;
    std::map<long long, long long> fills;
};

inline std::map<std::string, long long> positions(const std::vector<Event>& events) {
    std::unordered_map<std::string, State> states;
    for (const Event& e : events) {
        State& s = states[e.symbol];
        if (e.is_snapshot) {
            if (e.seq <= s.snap_seq) continue;
            s.snap_seq = e.seq;
            s.snap_qty = e.qty;
            s.fills.erase(s.fills.begin(), s.fills.upper_bound(e.seq));
        } else {
            const long long d = signed_qty(e);
            if (e.seq > s.snap_seq) s.fills.emplace(e.seq, d);
        }
    }
    std::map<std::string, long long> out;
    for (const auto& [symbol, s] : states) {
        long long total = s.snap_qty;
        for (const auto& [seq, d] : s.fills) total += d;
        out[symbol] = total;
    }
    return out;
}
```

复杂度：设 n 个事件，每个事件对有序映射一次插入或区间删除，每个成交最多被删一次，总时间 O(n log n)；空间 O(尚未被快照吸收的成交数 + 标的数)。

## Part 3 · 口头追问和回答

**1. 为什么用序号而不是时间戳？**

时间戳来自不同的机器，时钟有偏差，同一毫秒里还会有多个事件，用它们排序会把顺序排错。序号由同一个来源按顺序分配，是一个严格的全序，直接比较就行。序号还能暴露丢包：如果收到了 11 和 13 却没有 12，就知道少了一笔，时间戳做不到这一点。

**2. 怎么和我们自己记录的成交对账，不一致时怎么办？**

我们自己也记着每笔成交。快照 seq 到的时候，计算「上一个快照的 qty + 我们记录的、seq 在两个快照之间的成交」，和新快照的 qty 比较。相等就是对上了；不相等就报警，说明我们漏了成交、重复了成交，或者券商那边有我们不知道的调整。对账完成后以券商快照为准，因为它是持仓的权威记录，但要留下差额和相关事件供排查。做这件事需要把 seq ≤ 新快照的成交保留到对账完成，而不是在快照到达时立刻删掉。

**3. 持仓数量用 `long` 会溢出吗？**

`long` 的最大值是 9223372036854775807，真实的股数离它很远，但持仓是很多笔成交的累加，输入有错（比如数量被错误地放大）时，静默回绕会把持仓变成一个错误的负数。稳妥的做法是用 `Math.addExact`，溢出时抛 `ArithmeticException` 并报警。C++ 里有符号溢出是未定义行为，要用 `__builtin_add_overflow` 之类的检查，不能先加再看结果是不是变负。

**4. 很多标的同时进来怎么并行？**

标的之间互不影响，seq 也只在标的内比较，所以可以按标的哈希分片：同一个标的的事件总是交给同一个线程，每个线程只改自己那几个标的的 `State`，不需要加锁。同一个标的内部不并行，因为顺序（至少是 seq）对它重要。

**5. 要保存的状态会不会越积越多？**

每个标的的 `fills` 只存 seq 大于最新快照的成交，快照一到就被裁掉。券商定期给快照，状态就有上界；如果快照很久不来，`fills` 会一直变长，可以报警，或者在已经收到连续 seq 的前提下把前缀合并成一个数。

## 常见错误

1. 成交一来就加到一个数上：成交先于快照到达时，快照一覆盖，这笔成交就丢了。
2. 把 seq 等于快照 seq 的成交也加上：快照已经包含了它，重复计算。
3. 过期快照也采用：持仓退回到旧值。
4. 重复的成交不去重：同一笔成交被算两次。
5. 用到达顺序或时间戳代替 seq 判断新旧。
