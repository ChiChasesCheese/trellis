---
id: hi-sdx-anycast-geodns
node: sd.core-concepts.networking-essentials.more
type: qa
step: 1
---
## Q
**Anycast 与 GeoDNS 选哪个**｜补充 · 网络基础 · 追问

用户遍布全球，要把他们引到最近的站点。Anycast 和 GeoDNS 各怎么做？各有什么缺陷？

## A
**结论。** Anycast 靠网络路由选最近的站点，故障切换快，但你控制不了映射；GeoDNS 靠 DNS 应答选站点，控制精细，但看不到真实用户的位置，还受 TTL 限制。大厂常两个一起用。

**要点。**
- **Anycast：** 同一个 IP 从多个站点用 BGP 宣告，网络把客户端路由到拓扑上最近的站点。站点故障就撤回路由，不用等客户端的 DNS 缓存过期。
- **Anycast 的缺陷：** 映射由 BGP 决定，你不能精确指定。路由变化会把一条进行中的 TCP 连接送到另一个站点而中断，所以适合短连接和 UDP（DNS 根、CDN 边缘）。
- **GeoDNS：** 权威 DNS 按发起查询的位置返回不同的 IP，能做权重分流、容量调度、故障摘除。
- **GeoDNS 的缺陷：** 它看到的是递归解析器的位置，不是用户的位置；用户用远处的公共 DNS 就会被引错（EDNS Client Subnet 只能部分解决）。每次改动还受 TTL 限制。
- **组合：** GeoDNS 先选大区，区内再用 Anycast 或负载均衡器。

**面试里这样说。** 「全球接入我用 GeoDNS 选区域，区内用 Anycast IP 加负载均衡。要知道 GeoDNS 看的是解析器位置、切换受 TTL 限制；Anycast 切换快，但长连接可能被路由变化打断。」

**易错。**
- **以为 Anycast 能精确控制流量比例：** 比例由 BGP 路径决定；要精确配比，用 GeoDNS 或上层调度。
- **在 Anycast 上放长时间的有状态连接：** 路由抖动会让连接断开，需要客户端重连或会话可迁移。
