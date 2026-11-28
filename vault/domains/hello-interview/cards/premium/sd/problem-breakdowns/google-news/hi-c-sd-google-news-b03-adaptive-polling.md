---
id: hi-c-sd-google-news-b03-adaptive-polling
node: sd.problem-breakdowns.google-news.beyond
type: qa
step: 3
---
## Q
**新闻聚合 · 拓展：自适应轮询、条件请求与 WebSub**｜拓展 · 加分

不同出版商的发布节奏差别很大，轮询间隔怎么自动调整？有没有标准化的推送？

## A
- **自适应间隔：** 轮询发现有新文章就缩短间隔，没有就逐步拉长，限制在最小和最大之间。类似拥塞控制里的“快收慢放”：变化时快速收紧，无变化时缓慢放松。实测从 1 小时起，连续 3 次无变化，间隔变为 90、135、202 分钟；随后 3 次有新文章依次降到 101、50、25 分钟。
- **条件请求：** 带上次的 ETag 或 Last-Modified（`If-None-Match` / `If-Modified-Since`），没变就回 304，省带宽和解析；注意它不减少请求数，所以仍要靠自适应间隔和分级。
- **发布时间模式：** 很多出版商有固定的发布高峰（早间、整点），可按时段调整，高峰前后缩短间隔。
- **WebSub：** 是 W3C 推荐的开放协议（前身是 PubSubHubbub）：订阅者向出版商指定的 hub 订阅某个 feed，出版商一发布就通知 hub，hub 推送给订阅者。不需要每家出版商为我们定制 Webhook，已支持 WebSub 的出版商（部分 RSS/博客平台）可以直接推送。
- **礼貌：** 失败时指数退避；尊重 `Retry-After`；对同一域名限速。
- **模式。** 自适应采样率：用观测到的变化频率反过来决定检查频率。

```python
def next_interval(cur: float, changed: bool, lo: float = 300, hi: float = 21600) -> float:
    # 有新文章就减半，没有就乘 1.5，限制在 [5 分钟, 6 小时]
    return max(lo, cur / 2) if changed else min(hi, cur * 1.5)
```
