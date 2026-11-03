---
id: craft-reserve-hold-confirm-with-ttl-5-scales-tcc
node: craft.patterns.reserve-hold-confirm-with-ttl
type: qa
step: 5
---
## Q
**预留—确认—过期 · 从库存预留到 TCC 分布式事务**｜架构

跨服务的订单要同时占库存服务、优惠券服务、支付服务。单进程里的 reserve / confirm / cancel 放到多个服务，需要多保证什么？

## A
**要点。** 这就是 TCC（Try-Confirm-Cancel）：Try 预留资源，所有参与方都 Try 成功就都 Confirm，否则都 Cancel。网络会重复、乱序、丢失消息，所以参与方的 Confirm / Cancel 必须幂等，还要处理两种边界：空回滚（Cancel 先于 Try 到达，要登记「已取消」）和防悬挂（之后到达的 Try 要拒绝）。

```python
def try_(self, tx, n):
    if tx in self.state:                  # 已 Cancel（空回滚）后又到的 Try：拒绝
        return False
    if self.stock < n: return False
    self.stock -= n; self.state[tx] = "TRIED"; return True

def cancel(self, tx, n):
    st = self.state.get(tx)
    if st == "TRIED":
        self.stock += n; self.state[tx] = "CANCELLED"
    elif st is None:
        self.state[tx] = "CANCELLED"      # 没见过 Try：空回滚
```

重复 Cancel、Cancel 先于 Try、重复 Confirm：

```
重复 Cancel 后库存 5 状态 CANCELLED
t2 的迟到 Try 被拒绝: True | 库存 5
重复 Confirm 后库存 3 状态 CONFIRMED
```

**尺度对照。** 内存里的 TTL 过期由惰性结清完成；多个服务里 Try 的预留也必须有 TTL 或由事务协调者定期扫描超时的事务，否则协调者宕机后各服务的预留永远不会释放。

**变化。** 单进程里确认失败是一个异常；分布式里 Confirm 失败只能重试到成功（Try 已承诺），并报警人工介入。

**信号。** 一个业务动作要占用多个独立服务里的资源，且不能用一个数据库事务包住。
