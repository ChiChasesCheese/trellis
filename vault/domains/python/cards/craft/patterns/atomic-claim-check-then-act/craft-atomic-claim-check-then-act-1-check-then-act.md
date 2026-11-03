---
id: craft-atomic-claim-check-then-act-1-check-then-act
node: craft.patterns.atomic-claim-check-then-act
type: qa
step: 1
---
## Q
**原子占位 · 为什么「先查再占」在多线程下会出两个赢家**｜写法

两个用户同时抢座位 A1。代码写成 `if seat not in taken: taken[seat] = user`。每一行单独看都没错，Python 还有 GIL（全局解释器锁），为什么两个人还是都抢到了？怎么改？

## A
**要点。** 把「检查可用」和「写入占用」合成一个不可分割的步骤（原子操作）。GIL 只保证单条字节码不被撕开，不保证两行代码之间不被切换；`in` 与 `[]=` 是两条语句，中间随时可能换线程。

```python
def claim_check_then_act(seat, user):
    if seat not in taken:            # 检查
        time.sleep(0.01)             # 线程在此被切走
        taken[seat] = user           # 行动
        return True
    return False

def claim_atomic(seat, user, lock=threading.Lock()):
    with lock:                       # 检查与占用合成一步
        if seat in taken:
            return False
        taken[seat] = user
        return True
```

两个线程（ann、bob）同时抢 A1，实际输出：

```
claim_check_then_act [True, True] 座位归属 bob
claim_atomic [True, False] 座位归属 ann
```

**易错。** 第一个版本里两个人都收到 `True`，ann 的占位被 bob 悄悄覆盖，没有任何报错。`sleep` 只是把窗口放大到必现，没有它竞态也在，只是概率低。

**为什么。** 占位函数要返回「我赢了吗」，调用方才能知道自己是不是唯一拥有者。
