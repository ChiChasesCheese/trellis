---
id: cc-chrono-windows-bucket-vs-rolling
node: chrono.windows
type: qa
---
## Q
"No more than 100 events per hour." Fixed hourly buckets versus a rolling 60-minute window — where do they disagree, and which does a *per-hour band* rule need?

## A
**They disagree at the seam.** Fixed buckets (`ts // 3600`) allow 100 events at 10:59 and 100 more at 11:00 — 200 inside one real hour. A rolling window never allows more than 100 in any 60 minutes, but needs per-key event storage.

- Buckets: O(1) memory per key, trivially resettable, and the right model when the *label* matters ("transactions in hour 12", "the 2026-03-02 daily total").
- Rolling: exact "within the last hour" semantics, deque plus running sum, amortized O(1) ([[cc-toolbox-deque-window-sum]]).
- A **band** rule keyed on the clock hour (`09–11 → −1`, `12–17 → +1`, otherwise nothing) is bucket logic: extract the hour, compare against each band's endpoints, and state whether each end is inclusive — hour 11 and hour 12 land in different bands and both are graded.
- Bucket keys must be derived from the canonical timestamp, not from the raw string.

## Q zh
「每小时最多 100 个事件。」固定小时桶 vs 滚动 60 分钟窗口 —— 它们在哪里不一致，而*按小时分段*的规则需要哪一种？

## A zh
**它们在接缝处不一致。** 固定桶（`ts // 3600`）允许 10:59 有 100 个、11:00 再有 100 个 —— 真实的一小时内有 200 个。滚动窗口保证任意 60 分钟内不超过 100 个，但需要按 key 存事件。

- 桶：每个 key O(1) 内存，重置很容易，而且当*标签*本身有意义时（「第 12 小时的交易」「2026-03-02 的日总量」）它才是正确模型。
- 滚动：精确的「最近一小时内」语义，deque 加运行和，摊销 O(1)（[[cc-toolbox-deque-window-sum]]）。
- 按钟点小时分**段**的规则（`09–11 → −1`、`12–17 → +1`、其余不变）是桶逻辑：取出小时，与每段的端点比较，并说明每一端是否闭合 —— 第 11 小时和第 12 小时属于不同段，两者都会被判分。
- 桶的 key 必须从规范化时间戳导出，而不是从原始字符串。
