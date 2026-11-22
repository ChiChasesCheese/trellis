---
id: k8s-resources-exam
node: p2.t04.resource-requests-limits-qos-classes
type: qa
step: 2
tags: [考点]
---
## Q
**Requests、limits 与 QoS**｜考点 · 必会

一个 Pod 里只有一个容器：`requests: {cpu: 500m, memory: 256Mi}`，`limits: {cpu: 500m, memory: 512Mi}`。它是哪个 QoS class？如果想让它成为 Guaranteed，怎么改？容器内存涨到 600Mi 会怎样？CPU 要用 800m 呢？

## A
**QoS：** Burstable。CPU 的 request 等于 limit，但内存 256Mi ≠ 512Mi，不满足 Guaranteed 的条件。

**改成 Guaranteed：** 内存 request 和 limit 设成一样，如都是 `512Mi`（CPU 已相等）。

| 情况 | 结果 |
|---|---|
| 内存涨到 600Mi（超过 limit 512Mi） | 内核 **OOM kill** 杀掉容器，kubelet 重启它，`describe` 看到 `OOMKilled` |
| CPU 想用 800m（limit 是 500m） | **被限速**（throttle），变慢但不会被杀 |
| 所有 node 的剩余内存都不到 256Mi | 调度失败，Pod 停在 Pending |

- **规律：** CPU 是「可压缩」资源，超了只会慢；内存是「不可压缩」的，超了就得杀。
- **想要最不容易被驱逐：** 用 Guaranteed。
- **常见坑：** 不设 requests，调度器认为这个 Pod 不占资源，node 被塞满；不设 limit，一个 Pod 可以吃光整个 node 的内存。

<details class="pt" markdown="1"><summary>出处</summary>

kubernetes.io Concepts › Resource Management for Pods and Containers、Pod Quality of Service Classes；KIA2 §2.3.2（cgroup 限制 CPU 与内存）

</details>
