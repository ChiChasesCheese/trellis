---
id: k8s-networkpolicy-exam
node: p4.t04.networkpolicy
type: qa
step: 2
tags: [考点]
---
## Q
**NetworkPolicy**｜考点 · 必会

命名空间 `prod` 里先创建了「默认拒绝所有入站」的策略，然后给 `db` 加了「允许 `role=frontend` 入站 6379」的策略。判断：
1. `frontend` 连 `db:6379` 能通吗？
2. `frontend` 连 `db:5432` 呢？
3. `prod` 里另一个 `role=cron` 的 Pod 连 `db:6379` 呢？
4. 集群用的网络插件不支持 NetworkPolicy，这些策略会怎样？

## A
```yaml
# 默认拒绝：选中 prod 里所有 Pod，入站规则为空
spec:
  podSelector: {}
  policyTypes: [Ingress]
```

| # | 结果 | 原因 |
|---|---|---|
| 1 | 通 | 两条策略都选中 `db`，允许的是并集；第二条允许 frontend 的 6379 |
| 2 | 不通 | 端口不在任何允许规则里 |
| 3 | 不通 | `cron` 不在允许的来源里，默认拒绝仍对它生效 |
| 4 | 完全不生效 | 策略要靠网络插件执行，不支持就当没有，所有连接照常通过 |

- **关键：** 多条策略是**叠加（并集）**，不会因为有默认拒绝就把后面的允许覆盖掉。
- **所以 4 最危险：** 以为有保护，实际没有。上线前用一个应该被拒绝的连接实测一次。
- **别忘了出站：** 只写 `Ingress` 不限制出站；也要限制出站，要另外写 `Egress`。
- **允许 DNS：** 一旦限制出站，别忘了放行到集群 DNS 的 53 端口，否则 Service 名字解析不了。

<details class="pt" markdown="1"><summary>出处</summary>

kubernetes.io Concepts › Network Policies（isolation、additive、plugin 要求）

</details>
