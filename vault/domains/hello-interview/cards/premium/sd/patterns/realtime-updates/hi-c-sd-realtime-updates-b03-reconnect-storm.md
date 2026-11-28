---
id: hi-c-sd-realtime-updates-b03-reconnect-storm
node: sd.patterns.realtime-updates.beyond
type: qa
step: 1
---
## Q
**实时更新 · 重连风暴与退避抖动**｜拓展 · 追问

服务器发布时一万个连接同时断开，客户端该怎么重连，才不会把新服务器打垮？

## A
**模式。** 指数退避加全抖动（exponential backoff with full jitter）：等待上限随失败次数翻倍，而实际等待时间在 `[0, 上限]` 内均匀随机。

```python
import random

random.seed(7)
CAP, BASE = 60.0, 1.0


def no_jitter(attempt: int) -> float:
    return min(CAP, BASE * 2 ** attempt)                  # 所有客户端同一时刻失败 -> 同一时刻重试


def full_jitter(attempt: int) -> float:
    return random.uniform(0, min(CAP, BASE * 2 ** attempt))   # 在 [0, 上限] 内均匀随机，把重试摊开


clients = 10_000                                          # 一次发布重启，一万个连接同时断开
for name, f in (("无抖动", no_jitter), ("全抖动", full_jitter)):
    t = [f(2) for _ in range(clients)]                    # 第 3 次重试
    buckets = [0] * 4
    for x in t:
        buckets[min(int(x), 3)] += 1                      # 按秒统计到达服务器的重连数
    print(name, "每秒到达的重连数（第0..3秒）:", buckets, "峰值占比", f"{max(buckets)/clients:.0%}")
```
- **为什么需要抖动：** 只有指数退避时，所有同时断开的客户端每一轮的等待时间完全相同，整齐地一起冲回来；抖动把到达时间摊开，峰值降到几分之一（这个例子里摊到四个一秒桶里，每个约 25%）。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 170">
<g font-size="12" font-family="sans-serif" fill="currentColor">
<text x="8" y="16">无抖动：第 3 次重试全部同一时刻到达</text>
<text x="8" y="100">全抖动：四个一秒桶各约 25%</text>
<g text-anchor="middle" font-size="11">
<text x="50" y="80">第0秒</text><text x="130" y="80">第1秒</text><text x="210" y="80">第2秒</text><text x="290" y="80">第3秒</text>
<text x="290" y="36">100%</text>
<text x="50" y="164">第0秒</text><text x="130" y="164">第1秒</text><text x="210" y="164">第2秒</text><text x="290" y="164">第3秒</text>
<text x="50" y="132">25%</text><text x="130" y="132">25%</text><text x="210" y="132">25%</text><text x="290" y="132">25%</text>
</g>
</g>
<g stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))">
<rect x="260" y="40" width="60" height="26"/>
<rect x="20" y="136" width="60" height="14"/>
<rect x="100" y="136" width="60" height="14"/>
<rect x="180" y="136" width="60" height="14"/>
<rect x="260" y="136" width="60" height="14"/>
</g>
<g stroke="currentColor" stroke-width="1" fill="none">
<line x1="10" y1="66" x2="330" y2="66"/>
<line x1="10" y1="150" x2="330" y2="150"/>
</g>
</svg>

- **全抖动：** 比"在固定退避上加一点点随机"摊得更开，所以被广泛推荐。
- **配套措施：** 设上限（如 60 秒）；成功连接并稳定一段时间后才重置退避；服务端在过载时用 429 之类的响应加 `Retry-After` 提示；发布时分批排空连接。
- **连接资源：** 每条连接占一个文件描述符，单机能扛的连接数受文件描述符上限和内存限制，需要调高系统限制；L7 负载均衡到同一后端地址的连接数还受源端口数量限制（每个"源地址 + 目的地址 + 目的端口"组合约 6.5 万个）。
- **何时不用：** 只有几十个客户端的内部工具，固定短间隔重连就够。
