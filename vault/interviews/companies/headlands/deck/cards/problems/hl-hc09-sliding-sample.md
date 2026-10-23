---
id: hl-hc09-sliding-sample
node: problems.hc09-top-trades-by-notional
type: qa
step: 10
---
## Q
手跑滑动窗口样例（窗口 W=10，k=2）：`F 1 AAPL 100 2`、`F 3 MSFT 50 10`、`F 5 AAPL 100 3`、`Q 5`、`F 12 TSLA 10 10`、`Q 12`、`Q 15`、`Q 40`。

## A
成交 `F time ticker price volume`，查询 `Q time`。

- `Q 5`：AAPL = 200 + 300 = 500，MSFT = 500 → `[AAPL 500, MSFT 500]`（并列按 ticker 升序）；
- `F 12 TSLA 10 10` 加入 TSLA 100；`Q 12`：t=1 的 AAPL 200 已过期（12 − 1 = 11 ≥ 10），AAPL 剩 300 → `[MSFT 500, AAPL 300]`；
- `Q 15`：MSFT(t=3)：15 − 3 = 12 ≥ 10 过期；AAPL(t=5)：15 − 5 = 10 ≥ 10，**边界算过期** → `[TSLA 100]`；
- `Q 40`：全部过期 → `[]`。

`replay(window, k, List<Feed>)` 回放一串 `Fill / Tick(time) / Ask(time)`，返回每个 `Ask` 的 `Answer(time, top)`。`Ask(t)` 也先推进时钟，所以「在 t 时刻问」等价于「先 Tick(t) 再问」：

```java
switch (f) {
    case Fill fill -> w.add(fill);
    case Tick(var t) when t == w.now() -> { }
    case Tick(var t) -> w.advanceTo(t);
    case Ask(var t) -> { w.advanceTo(t); answers.add(new Answer(t, w.top())); }
}
```
`Feed` 是 `sealed interface ... permits Fill, Tick, Ask`，不需要 `default`；带守卫的 `case Tick(var t) when …` 必须在不带守卫的 `case Tick(var t)` **之前**，否则被遮蔽，编译器报 `dominated`。

边界：恰好 `window` 的边界；同一时间戳多笔；ticker 因过期被别人反超；总额溢出后状态不变；窗口 0；时间倒退。

复杂度：每个事件 O(log m) 摊还（m = 窗口内不同 ticker 数），查询 O(log m + k)。1e6 笔成交 + 1e4 次查询、窗口 5000、m=2000 约 430–480 ms。最笨的做法是每次查询重算 O(窗口大小)，但它是最好的对拍基线。
