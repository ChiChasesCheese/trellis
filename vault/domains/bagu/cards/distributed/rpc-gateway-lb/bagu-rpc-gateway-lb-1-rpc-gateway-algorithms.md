---
id: bagu-rpc-gateway-lb-1-rpc-gateway-algorithms
node: b.distributed.rpc-gateway-lb
type: qa
step: 1
---
## Q
**RPC、网关与负载均衡 · 内部为什么用 RPC、网关管什么、算法怎么选**｜追问

面试官：「已经有 HTTP 了，内部服务为什么还用 RPC？API 网关承担哪些职责，单点和性能怎么办？负载均衡有哪些算法？」

## A
**基本回答。** HTTP 把交互建模成访问资源，RPC 建模成调用方法。内部服务多用 RPC：二进制序列化（如 Protobuf）比 JSON 小而快，长连接加连接池，框架自带服务发现（注册中心如 Consul、etcd、Nacos 保存服务名到地址列表，调用方按名查地址）、负载均衡、超时重试。对外开放的接口仍用 HTTP，通用好调试。网关是统一入口，管路由转发、鉴权、限流、熔断、灰度、日志监控。
**2026 亮点。** 网关落在 K8s 上，入口层用 Gateway API 而不是 Ingress：GatewayClass、Gateway、HTTPRoute/GRPCRoute 分别由平台方、集群运维、业务团队各管一层，权重字段直接做灰度分流；Ingress NGINX 已于 2026 年 3 月退役，不再有安全补丁。各实现对扩展特性支持不一，迁移要逐项核对。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 274">
<rect x="120" y="6" width="100" height="24" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="170.0" y="22.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">客户端</text>
<line x1="170" y1="30" x2="170" y2="48" stroke-width="1.2" stroke="currentColor"/>
<polygon points="170.0,48.0 166.8,41.0 173.2,41.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="30" y="50" width="280" height="44" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="170.0" y="69.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">API 网关（无状态，多实例）</text>
<text x="170.0" y="84.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">鉴权 · 限流 · 路由 · 灰度 · 日志</text>
<rect x="10" y="130" width="96" height="40" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="58.0" y="147.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">订单服务</text>
<text x="58.0" y="162.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">多个实例</text>
<line x1="58" y1="94" x2="58" y2="128" stroke-width="1.2" stroke="currentColor"/>
<polygon points="58.0,128.0 54.8,121.0 61.2,121.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="122" y="130" width="96" height="40" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="170.0" y="147.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">账户服务</text>
<text x="170.0" y="162.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">多个实例</text>
<line x1="170" y1="94" x2="170" y2="128" stroke-width="1.2" stroke="currentColor"/>
<polygon points="170.0,128.0 166.8,121.0 173.2,121.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="234" y="130" width="96" height="40" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="282.0" y="147.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">渠道服务</text>
<text x="282.0" y="162.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">多个实例</text>
<line x1="282" y1="94" x2="282" y2="128" stroke-width="1.2" stroke="currentColor"/>
<polygon points="282.0,128.0 278.8,121.0 285.2,121.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="8" y="118" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">RPC</text>
<rect x="45" y="198" width="250" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2" stroke-dasharray="4 3"/>
<text x="170.0" y="215.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">注册中心：服务名 → 地址列表</text>
<line x1="58" y1="170" x2="58" y2="198" stroke-width="1.2" stroke="currentColor" stroke-dasharray="4 3"/>
<line x1="170" y1="170" x2="170" y2="198" stroke-width="1.2" stroke="currentColor" stroke-dasharray="4 3"/>
<line x1="282" y1="170" x2="282" y2="198" stroke-width="1.2" stroke="currentColor" stroke-dasharray="4 3"/>
<text x="8" y="248" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">算法：随机 · 轮询 · 两次随机 · 哈希</text>
<text x="8" y="266" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">最小连接 · 最少活跃（Dubbo，按在途请求）</text>
</svg>
客户端先到网关，网关做鉴权、限流、路由、灰度；网关和各服务之间用 RPC 调用，服务实例的地址从注册中心拿；最下面是常见的负载均衡算法。
**容易错。**
- **以为 RPC 和 HTTP 底层不同：** 两者都是 TCP 长连接，gRPC 跑在 HTTP/2 上，差别在序列化和治理能力。
- **以为内部也该全用 HTTP，或对外也该全用 RPC：** 对外要通用好调试，内部要效率和治理。
- **把业务逻辑塞进网关：** 网关会变成巨石，长事务、复杂聚合放回业务服务或 BFF。
- **以为最小连接等于最闲：** 连接数不等于真实负载，最少活跃（Dubbo 用）按在途请求数选更准；其他算法有随机、轮询、两次随机（抽两台取较闲的）、一致性哈希（相同 key 落同一台，适合缓存亲和）。
- **网关只有一个实例：** 单点，要多实例加负载均衡。
**举个例子。** 权重 a=5、b=1、c=1，Nginx 平滑加权轮询连续 7 个请求落在 a、a、b、a、c、a、a，a 占 5/7 但不连发。最少活跃：在途数 a=5、b=1、c=3 选 b；b 变慢在途数涨到 6，新请求自动绕开；最小连接数的盲点是空闲长连接也占连接数。接口变慢先分层：网关到服务慢，还是服务到某个下游慢。
