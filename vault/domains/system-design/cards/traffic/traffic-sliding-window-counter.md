---
id: traffic-sliding-window-counter
node: traffic.rate-limiting
type: cloze
---
The sliding-window **counter** (the production approximation, e.g. Cloudflare): keep one counter for the current fixed window and one for the previous; estimated rate = {{c1::current count + previous count × the fraction of the sliding window overlapping the previous window}}. Memory is {{c2::O(1) per key — two counters}}, versus a sliding **log** storing every request timestamp; the price is assuming requests were {{c3::evenly distributed across the previous window}}, so the boundary-burst error is small and bounded.

## zh
滑动窗口**计数器**（生产近似，例如 Cloudflare）：为当前固定窗口保留一个计数器，为上一个保留一个；估计速率 = {{c1::当前计数 + 上一个计数 × 滑动窗口与上一个窗口重叠的分数}}。内存是 {{c2::O(1) 每键 — 两个计数器}}，vs 存储每个请求时间戳的滑动**日志**；价格是假设请求是 {{c3::均匀分布在上一个窗口}}，所以边界突发错误很小且有界。
