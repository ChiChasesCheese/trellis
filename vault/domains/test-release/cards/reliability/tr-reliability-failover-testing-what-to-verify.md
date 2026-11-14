---
id: tr-reliability-failover-testing-what-to-verify
node: reliability.failover-testing
type: qa
step: 1
---
## Q
测试一个多节点服务的故障切换（failover），要验证哪些东西？要覆盖哪些故障场景？

## A
**要验证的五件事**：
- **检测时间**：从故障发生到系统发现故障，多快？
- **恢复时间（RTO，recovery time objective）**：从故障发生到服务恢复可用，是否在目标内，例如 30 秒。
- **数据丢失（RPO，recovery point objective）**：已经确认成功的写入，切换后是否还在？目标通常是 0（同步复制）或一个明确的时间窗口（异步复制）。
- **不重复、不错乱**：切换期间重试的请求有没有被执行两次（例如扣了两次款）；有没有出现两个节点同时认为自己是主节点（脑裂，split-brain）并各自接受写入。
- **进行中的请求**：故障时正在处理的请求，客户端收到明确的错误或被安全重试，而不是永远挂起或拿到不完整的结果。

前三件事在一条时间线上的位置：

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 215">
<g font-family="sans-serif" font-size="12">
<rect x="70" y="72" width="80" height="16" fill="currentColor" fill-opacity="0.15"/>
<line x1="20" y1="80" x2="325" y2="80" stroke="currentColor" stroke-width="1.5"/>
<line x1="70" y1="70" x2="70" y2="90" stroke="currentColor" stroke-width="2"/>
<line x1="150" y1="70" x2="150" y2="90" stroke="currentColor" stroke-width="2"/>
<line x1="210" y1="70" x2="210" y2="90" stroke="currentColor" stroke-width="2"/>
<line x1="290" y1="70" x2="290" y2="90" stroke="currentColor" stroke-width="2"/>
<text x="70" y="60" text-anchor="middle" fill="currentColor">最后已复制</text>
<text x="150" y="60" text-anchor="middle" fill="currentColor">故障</text>
<text x="210" y="60" text-anchor="middle" fill="currentColor">发现</text>
<text x="290" y="60" text-anchor="middle" fill="currentColor">恢复</text>
<line x1="70" y1="110" x2="150" y2="110" stroke="currentColor"/>
<line x1="70" y1="105" x2="70" y2="115" stroke="currentColor"/>
<line x1="150" y1="105" x2="150" y2="115" stroke="currentColor"/>
<text x="110.0" y="128" text-anchor="middle" fill="currentColor">RPO 可能丢的写入</text>
<line x1="150" y1="145" x2="210" y2="145" stroke="currentColor"/>
<line x1="150" y1="140" x2="150" y2="150" stroke="currentColor"/>
<line x1="210" y1="140" x2="210" y2="150" stroke="currentColor"/>
<text x="180.0" y="163" text-anchor="middle" fill="currentColor">检测时间</text>
<line x1="150" y1="185" x2="290" y2="185" stroke="currentColor"/>
<line x1="150" y1="180" x2="150" y2="190" stroke="currentColor"/>
<line x1="290" y1="180" x2="290" y2="190" stroke="currentColor"/>
<text x="220.0" y="203" text-anchor="middle" fill="currentColor">RTO 恢复时间</text>
</g>
</svg>
```

**场景矩阵**：
- **主节点崩溃**（`kill -9`）与**主节点正常停机**（滚动升级）；
- **副本崩溃**：主节点应继续服务，副本恢复后自动追上；
- **主节点卡死但未退出**（`kill -STOP`）：它可能在恢复后仍以为自己是主节点；
- **网络分区**：主节点和多数副本断开；非对称分区（A 能连 B，B 连不上 A）；
- **慢节点**：节点没死，只是很慢（注入 2 秒延迟），健康检查可能仍然通过，这类"灰色故障"（gray failure）最容易漏测；
- **连续故障**：切换刚完成，新主节点又故障；
- **全部重启**：整个集群断电后冷启动，能否恢复到一致状态。
