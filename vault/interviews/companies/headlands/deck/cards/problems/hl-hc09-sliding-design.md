---
id: hl-hc09-sliding-design
node: problems.hc09-top-trades-by-notional
type: qa
step: 9
---
## Q
`SlidingTopK` 的数据结构设计和窗口语义是什么？写出 `add` 与过期的核心代码，为什么操作顺序是正确性的一部分？

## A
**语义**：`SlidingTopK(window, k)`；`now - time < window` 的成交是活的，`now - time >= window` 过期，即活跃区间 `(now - window, now]`，**恰好差 `window` 就过期**。时间 ≥ 0，`window ≥ 1`，`k ≥ 0`；时间倒退抛 `IllegalArgumentException`（相等允许）；`add` 里总额溢出 → `ArithmeticException`，**ticker 状态保持原样**（原子性）。

**结构**：
- `ArrayDeque<Fill> live`：按时间顺序的活跃成交，队头最老（FIFO 过期，每个事件进一次出一次，过期总代价 O(n)，摊还每个事件 O(1) 次出队）；
- `HashMap<String, Acc> totals`：ticker → (窗口内总额, 活跃笔数 count)；
- `TreeSet<TickerTotal> ranking`：按 (总额降序, ticker 升序)，与 `totals` 一一对应。

`Acc.count` 必要：总额可能为 0（价格或数量为 0），不能用「总额 == 0」判断有没有活跃成交；count 减到 0 才从两张表删掉。`Acc` 是可变类而非 record（每个成交都要更新，建新 record 产生垃圾），局限在 private static 类。

```java
public void add(Fill f) {
    advanceTo(f.time());
    var acc = totals.get(f.ticker());
    long oldTotal = acc == null ? 0 : acc.total;
    long newTotal = Math.addExact(oldTotal, f.notional());     // 先算：溢出就抛，还没动结构
    if (acc == null) { acc = new Acc(); totals.put(f.ticker(), acc); }
    else ranking.remove(new TickerTotal(f.ticker(), oldTotal)); // 先按旧值删
    acc.total = newTotal; acc.count++;
    ranking.add(new TickerTotal(f.ticker(), newTotal));
    live.addLast(f);
}
// 过期
while ((f = live.peekFirst()) != null && now - f.time() >= window) {
    live.removeFirst();
    var acc = totals.get(f.ticker());
    ranking.remove(new TickerTotal(f.ticker(), acc.total));
    acc.total -= f.notional(); acc.count--;
    if (acc.count == 0) totals.remove(f.ticker());
    else ranking.add(new TickerTotal(f.ticker(), acc.total));
}
```
- `ranking.remove` 必须在改 `acc.total` **之前**，否则用新值找不到旧键，旧键残留、同一 ticker 出现两次；
- 溢出检查在改状态之前；
- 过期条件用 `now - time >= window`，不用 `time + window <= now`（时间很大时后者溢出）；
- `acc.total -= notional` 不会溢出（非负数之和减去其中一个）。

`top()` = `ranking.stream().limit(k).toList()`，O(log m + k)。
