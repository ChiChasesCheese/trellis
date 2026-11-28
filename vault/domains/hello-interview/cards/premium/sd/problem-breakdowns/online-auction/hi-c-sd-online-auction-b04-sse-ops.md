---
id: hi-c-sd-online-auction-b04-sse-ops
node: sd.problem-breakdowns.online-auction.beyond
type: qa
step: 4
---
## Q
**在线拍卖 · 拓展：SSE 的运维细节与慢客户端**｜拓展 · 加分

SSE 上生产会遇到哪些具体问题？服务端如何避免慢客户端拖垮广播？

## A
- **协议能力：** 浏览器 `EventSource` 自带断线重连，并在重连时带上 `Last-Event-ID`，服务端可据此补发；事件带 `id:` 字段（用出价序号）就能做到这一点。
- **连接数限制：** HTTP/1.1 下浏览器对同一域名的并发连接有限（通常 6 个），多个标签页各开一条 SSE 会占满；用 HTTP/2 多路复用解决。
- **代理与负载均衡：** 中间层可能缓冲响应，使事件延迟到来，要关闭缓冲（如 Nginx 的 `X-Accel-Buffering: no`）；空闲连接会被超时断开，定期发注释行心跳（`: ping`）保持连接。
- **慢客户端：** 如果给每个连接都排队缓存所有事件，一个慢客户端会让内存无限增长。因为只关心最新最高价，所以每个连接的队列容量设为 1，满了就丢旧值换新值（合并）。
- **优雅下线：** 服务器要发布时，通知客户端重连到别的机器，并让它带着 `Last-Event-ID` 来，避免重启造成惊群。
- **模式。** 最新值覆盖：对"状态"类事件只保留最新，不保留历史，背压（backpressure）自然消失。

```python
class Hub:
    def __init__(self): self.subs: dict[str, set[asyncio.Queue]] = {}
    def subscribe(self, auction: str) -> asyncio.Queue:
        q = asyncio.Queue(maxsize=1)            # 只留最新一条
        self.subs.setdefault(auction, set()).add(q)
        return q
    def publish(self, auction: str, max_bid: int) -> None:
        for q in self.subs.get(auction, ()):
            if q.full(): q.get_nowait()         # 客户端没来得及取：覆盖旧值
            q.put_nowait(max_bid)
```
