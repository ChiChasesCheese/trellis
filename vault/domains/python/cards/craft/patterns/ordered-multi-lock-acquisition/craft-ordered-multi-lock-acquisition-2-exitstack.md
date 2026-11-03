---
id: craft-ordered-multi-lock-acquisition-2-exitstack
node: craft.patterns.ordered-multi-lock-acquisition
type: qa
step: 2
---
## Q
**固定顺序加多把锁 · 锁的数量不定时怎么写（中转行程一次订多个航班）**｜模式

一条中转行程由 N 个航班组成，每个航班实例一把锁，要么全订要么全不订，第一段订上、第二段满员会让旅客拿到一张断掉的票。N 不固定，`with a, b:` 写不出来。怎么写？

## A
**要点。** 先把要锁的对象按 key 排序，再用 `ExitStack` 逐个进入。`ExitStack` 把任意数量的上下文管理器当成一个来管理，离开 `with` 时按相反顺序释放，中途某把锁拿失败也会释放已经拿到的。持有全部锁之后，先校验再提交（见先校验后提交）。

```python
def reserve_across(legs):
    ordered = sorted(legs, key=lambda f: f.key)       # 全局固定顺序
    with ExitStack() as stack:
        for f in ordered:
            stack.enter_context(f.lock)               # 数量不定的锁，全部握住
        if any(f.free <= 0 for f in ordered):         # 校验段
            return False
        for f in ordered:                             # 提交段：全有或全无
            f.free -= 1
        return True
```

第二段已满时整体拒绝，第一段座位不变；都有座时两段同时扣减：

```
第二段已满 -> False | 第一段座位仍是 5
都有座 -> True | 座位: 4 2
```

**为什么。** 锁要同时握住：如果订完第一段就放锁，再去订第二段，中间别人可能订走最后一个座位。

**易错。** 同一个航班出现两次时，非可重入锁会自己锁死自己；订票把每个航班实例的锁定义成可重入锁（`RLock`）来容忍这种合法的极端输入。
