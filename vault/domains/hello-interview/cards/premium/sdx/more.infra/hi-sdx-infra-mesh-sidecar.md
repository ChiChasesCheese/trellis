---
id: hi-sdx-infra-mesh-sidecar
node: more.infra
type: qa
step: 8
---
## Q
**服务网格的 sidecar 做了什么**｜补充 · 平台基础设施：容器、服务网格、发布 · 追问

面试官：「服务网格的 sidecar 具体对 Pod 的流量做了什么？为什么在这个位置拦截，就能实现所有网格功能？」

## A
**结论。** Pod 启动时安装 iptables 规则，把进出的 TCP 流量透明地重定向到同一 Pod 里的七层代理（Istio 用 Envoy）。应用不用改，也毫无感知。每个调用的两端都经过代理，网格就能做 mTLS、解析 HTTP 或 gRPC 得到逐请求的指标和链路、执行重试超时和授权策略、按请求头或比例路由，全部由控制面当配置推下去。

**要点。**
- **透明拦截：** 靠 iptables 重定向，而不是应用主动调用库。
- **mTLS：** 代理两端终止和发起加密，证书由控制面签发和轮换。
- **可观测性：** 代理能看懂 HTTP 或 gRPC，直接产出每个请求的延迟、状态码和链路。
- **策略与路由：** 重试、超时、熔断、按比例分流，都是改配置，不改应用。
- **2026 亮点：** 代理和业务容器的启动顺序，K8s 1.33 起有原生 sidecar（restartPolicy: Always 的 init 容器）：保证代理先就绪、业务容器退出后才停代理，支持探针，Job 里的 sidecar 也不会再让 Pod 一直无法结束。代价是每个 Pod 仍多一份资源，想彻底省开销要看 ambient 这类无 sidecar 方案。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 276">
<rect x="8" y="10" width="150" height="150" rx="8" stroke-width="1" stroke-dasharray="4 3" fill="none" stroke="currentColor" opacity="0.5"/>
<text x="16" y="28" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">Pod A</text>
<rect x="182" y="10" width="150" height="150" rx="8" stroke-width="1" stroke-dasharray="4 3" fill="none" stroke="currentColor" opacity="0.5"/>
<text x="190" y="28" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">Pod B</text>
<rect x="22" y="40" width="122" height="34" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="83.0" y="61.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">应用（不改代码）</text>
<rect x="22" y="106" width="122" height="34" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="83.0" y="127.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">Envoy 代理</text>
<polyline points="83,74 83.0,97.0" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="83,104 79.8,97.0 86.2,97.0" style="fill:var(--accent,#3b6fd4)"/>
<rect x="196" y="106" width="122" height="34" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="257.0" y="127.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">Envoy 代理</text>
<rect x="196" y="40" width="122" height="34" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="257.0" y="61.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">应用</text>
<polyline points="257,104 257.0,83.0" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="257,76 260.2,83.0 253.8,83.0" style="fill:var(--accent,#3b6fd4)"/>
<polyline points="144,123 187.0,123.0" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="194,123 187.0,126.2 187.0,119.8" style="fill:var(--accent,#3b6fd4)"/>
<line x1="8" y1="178" x2="332" y2="178" stroke-width="1" stroke="currentColor" opacity="0.4" stroke-dasharray="3 3"/>
<text x="8" y="200" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">启动时 iptables 规则把进出的 TCP 流量</text>
<text x="8" y="220" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">透明地转给同 Pod 里的代理；应用毫无感知</text>
<text x="8" y="246" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">两端代理之间自动 mTLS；路由、策略、证书由</text>
<text x="8" y="262" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">控制面当配置推给代理</text>
</svg>

**面试里这样说。** 「网格把所有服务间的流量都过一层代理，所以 mTLS、重试、指标、流量切分都能统一在这一层做，应用代码不用动。」

**易错。**
- **以为网格会替应用处理业务语义：** 它只处理传输层面的事，业务相关的降级和幂等仍在代码里。
- **忘了代理自己也要运维：** 每个 Pod 多一个代理，升级和故障排查都多一层。
