---
id: problems-rate-limiter-composite-two-phase
node: problems.components.rate-limiter
type: qa
step: 8
tags: [grown]
---
## Q
限流器（Rate Limiter）要同时按用户和按接口限流、任一条拒绝即整体拒绝。逐条调用 `allow` 会出什么错？正确做法带来的死锁风险又怎么处理？

## A
逐条 `allow` 的错在于**扣早了**：用户规则先通过并已经扣掉一份额度，接口规则随后拒绝——这次请求根本没被服务，却吃掉了用户的配额，用户会发现自己被限流得莫名其妙地快。

正确做法是**两阶段判定**：先把所有涉及的状态锁住并各自 `check`（纯查询、绝不写状态），全过了才逐个 `commit`。这也正是要把算法的 `check` 和 `commit` 拆开、把「持锁取状态」公开成上下文管理器的原因：

```python
with ExitStack() as stack:
    for rule in self._rules:
        state = stack.enter_context(
            rule.limiter.reserve(rule.key_of(subject), now))
        decision = state.check(now, cost)
        if not decision.allowed:
            return replace(decision, rule=rule.name)
        reserved.append(state)
    for state in reserved:
        state.commit(now, cost)
```

同时持有多把锁就有死锁风险，这里靠**固定的加锁顺序**规避：规则元组顺序不变，所有线程按同一顺序拿锁。这个前提有个漏洞——两条规则若共用同一个限流器实例，加锁顺序就取决于 key 落在哪个分片，不再固定；所以构造函数直接拒绝这种配置，把一条只存在于脑子里的约束变成一次会抛异常的检查。

另外：组合判定必须让所有规则读到**同一个 `now`**，否则判定基准不一致——这是时钟必须注入、而算法绝不自己读时钟的另一个理由。
