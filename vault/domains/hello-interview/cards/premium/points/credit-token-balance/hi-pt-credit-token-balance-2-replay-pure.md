---
id: hi-pt-credit-token-balance-2-replay-pure
node: qb.lld.credit-token-balance.points
type: qa
step: 2
---
## Q
**额度账本 · 纯函数重放与试跑提交**｜必会 · 出自：额度账本 › 深入 1

写操作（`grant`、`charge`）怎么保证"所有已接受的扣费仍能全额扣下"，失败时账本原封不动？

## A
**做法。** `_replay` 是不碰 `self` 的纯函数；`_commit` 先对副本试跑，抛 `InsufficientCreditsError` 就中止，通过才替换真实的事件表。

```python
def _commit(self, grants, charges):
    _replay(grants, charges)           # 对新的事件副本试跑：额度不够会在这里抛异常，真实账本还没动
    self._grants, self._charges = grants, charges   # 试跑通过才整体替换
```
**为什么。** 写在方法里就没法对副本试跑，失败时要手工回滚（事件溯源加试运行提交）。
