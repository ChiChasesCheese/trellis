---
id: reliability-gray-failure
node: reliability.availability
type: qa
---
## Q
A node passes every health check but serves 100x slower due to a dying disk. What is this failure class, why is it worse than a crash, and what detects it?

## A
**Gray (partial) failure** — the component is degraded, not dead, and the health checker's view differs from the clients' view (*differential observability*).

Worse than crash-stop because nothing evicts the node: it keeps receiving traffic, drags down tail latency, and slow responses tie up caller threads (a slow dependency is more dangerous than a down one).

Detection: health checks that exercise **real work paths** (not just "port open"), and **outlier ejection** — compare each instance's error/latency stats against its peers and evict the relative outlier.

## Q zh
一个节点通过每个健康检查但由于垂死磁盘服务 100 倍慢。这个故障类是什么，为什么比崩溃更差，什么检测它？

## A zh
**Gray（partial）failure** ——组件降级，不是死，健康检查器的视图不同于客户端的视图（*差分可观测性*）。

比 crash-stop 更差因为没有任何东西驱逐节点：它继续接收流量，拖累尾延迟，慢响应绑定调用者线程（慢依赖比倒下更危险）。

检测：执行**真实工作路径**的健康检查（不只是"端口开放"），和**离群值驱逐** ——比较每个实例的错误/延迟统计与其对等，驱逐相对离群值。
