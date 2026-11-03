---
id: craft-saga-idempotent-compensation-5-scales-order-of-steps
node: craft.patterns.saga-idempotent-compensation
type: qa
step: 5
---
## Q
**Saga 与幂等补偿 · 步骤顺序怎么排才让补偿最少：从取款机到分布式 Saga**｜架构

取款机的流程有三件事：从钞箱抽出钞票（本地）、请银行扣账（远端）、出钞给客户（本地）。参考解的顺序是抽钞 → 扣账 → 出钞。为什么不是先扣账？远端的补偿怎么设计才安全？

## A
**要点。** 把便宜、可逆、本地的步骤排在前面，把昂贵、不可逆或远端的步骤往后放。先抽钞：钞箱不够时根本不碰银行；银行拒绝时本地原样放回，远端没有任何东西需要撤销。先扣账则要为本地的失败做远端冲正（reversal）。远端的冲正是银行的补偿动作，必须用同一个 ref 去重，才能幂等重试。

```python
def atm_local_first(cash, bank, amount):
    if cash < amount:
        return "钞箱不够：没碰银行"
    try:
        bank.withdraw(amount, "ref-1")
    except RuntimeError:
        return "银行拒绝：本地放回，无需冲正"
    return "成功出钞"

def reverse(self, amount, ref):
    if ref not in self.reversed_refs:       # 以 ref 去重：冲正幂等
        self.reversed_refs.add(ref)
        self.balance += amount
```

钞箱不够时两种顺序的银行调用，以及同一个 ref 冲正两次：

```
钞箱不够：没碰银行 | 银行调用 []
钞箱不够：已冲正 | 银行调用 ['withdraw', 'reverse']
同一个 ref 冲正两次，余额 1000
```

**尺度对照。** 取款机里一个 `withdraw`/`reverse` 对 → 在线购物的 Saga 执行器 → 跨微服务的 Saga（编排式由协调者调度，编舞式靠事件链）。越往外，补偿越需要：幂等键、重试直到成功、持久化「已完成哪几步」、对补偿失败的可观测与人工兜底。

**代价。** 补偿期间中间状态对外可见，不能做隔离；所以步骤要尽量让「最难撤销的」排最后。

**信号。** 一个业务动作跨多个系统且不能放进一个事务，又不能接受卡在半路。
