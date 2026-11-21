---
id: k8s-probes-beyond
node: p2.t02.restart-policy-probes-liveness-readiness-startup
type: qa
step: 3
tags: [拓展]
---
## Q
**Probe 的 host 字段 · 2026 实践**｜拓展 · v1.34

探针里可以写 `host:` 字段，让 kubelet 去探测 Pod IP 以外的地址。v1.34 起，这对 Pod Security 的 `restricted` 级别意味着什么？为什么？

## A
```yaml
livenessProbe:
  httpGet:
    host: 169.254.169.254    # 指向别处：restricted 级别不允许
    path: /
    port: 80
```

| | v1.34 之前 | v1.34 起 |
|---|---|---|
| `host` 字段 | 可以指向任意地址 | 要符合 `restricted`，Pod 必须不设 `host`，或者不使用这类探针 |
| 能探测什么 | 探针发起方是 kubelet，可以被指向节点的 localhost 或外部敏感主机 | `restricted` 的 Pod 只能探测自己的 Pod IP |

- **为什么：** 探针由 kubelet 发出。`host` 可以设成任意值，包括节点本机或内部敏感服务，能绕过安全控制，被滥用来攻击。
- **同样适用于：** 生命周期 handler（preStop、postStart）里的 `host` 字段。
- **怎么办：** 删掉 `host`，让 kubelet 默认探测 Pod IP。强制执行靠 Pod Security admission 或第三方策略工具。

**出处：** kubernetes.io 发布博客 v1.34「"Restricted" Pod security standard now forbids remote probes」（KEP-4940）
