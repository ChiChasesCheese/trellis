---
id: craft-validate-then-commit-3-composite-limiter-leak
node: craft.patterns.validate-then-commit
type: qa
step: 3
---
## Q
**先校验后提交 · 组合限流里被拒的请求为什么还会吃额度**｜模式

限流器有两条规则：每用户 5 次、每 IP 5 次。实现成「依次检查规则，通过就扣一次额度」。IP 规则已经耗尽，用户连续发 5 个请求全被拒绝。此时用户自己的额度还剩多少？为什么？

## A
**要点。** 剩 0。每个请求先在用户规则上通过并扣了额度，再在 IP 规则上被拒；被拒的请求照样消耗了用户规则的额度，等 IP 规则恢复时，这个用户已经被误限流。

```python
@dataclass
class Bucket:
    name: str
    tokens: int

    def check(self, cost: int) -> bool:
        return self.tokens >= cost

    def commit(self, cost: int) -> None:
        self.tokens -= cost

def allow_naive(rules: list[Bucket], cost: int = 1) -> bool:
    for r in rules:
        if not r.check(cost):
            return False
        r.commit(cost)            # 边查边扣：前面规则的额度已经没了
    return True

def allow_two_phase(rules: list[Bucket], cost: int = 1) -> bool:
    if not all(r.check(cost) for r in rules):   # 阶段一：全部只读
        return False
    for r in rules:                              # 阶段二：全过才扣
        r.commit(cost)
    return True

for fn in (allow_naive, allow_two_phase):
    per_user, per_ip = Bucket("user", 5), Bucket("ip", 0)   # ip 规则已经耗尽
    results = [fn([per_user, per_ip]) for _ in range(5)]
    print(fn.__name__, results, "user 剩余", per_user.tokens)
```

两个版本各发 5 个请求（ip 规则额度为 0），实际输出：

```
allow_naive [False, False, False, False, False] user 剩余 0
allow_two_phase [False, False, False, False, False] user 剩余 5
```

**为什么。** 把 `check`（只读）和 `commit`（写）拆成两个方法，是为了让「是否放行」可以先对所有规则求值。组合限流器 `CompositeLimiter` 正是先 check 全部规则，全过才逐个 commit。

**易错。** 多次 `check` 与 `commit` 之间要持有各规则的锁，否则别的请求会插进来。
