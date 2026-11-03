---
id: craft-saga-idempotent-compensation-2-compensate-the-failed-step
node: craft.patterns.saga-idempotent-compensation
type: qa
step: 2
---
## Q
**Saga 与幂等补偿 · 失败的那一步自己为什么也要补偿**｜模式

扣款这一步的动作是「先把钱扣走，再记账」。钱扣走后，记账那一句抛了异常。Saga 只补偿「已经成功的步骤」，扣款这一步算失败，不在其内。余额会怎样？怎么修？

## A
**要点。** 钱永远留在半路上。动作不是原子的，失败不等于「什么都没发生」。所以失败的那一步自己也要补偿，并且排在最前面。代价是补偿可能在动作根本没生效时被调用，因此补偿必须幂等，并能容忍「什么都还没发生」：以账为准，扣了多少退多少，没扣就是零，重复调用第二次也是零。

```python
def charge():
    charged["order-1"] = 30
    wallet["balance"] -= 30                  # 钱已经扣走了
    raise RuntimeError("记账失败")           # 动作的第二句抛异常

def refund():
    n = charged.pop("order-1", 0)            # 扣了才退；没扣是 0；重复调用第二次也是 0
    wallet["balance"] += n
```

余额 100，扣 30 后记账失败；只补偿已完成的步骤与失败步骤也补偿，以及再调用两次 `refund`：

```
只补偿已完成的步骤 -> 余额 70 （应为 100）
失败步骤也补偿     -> 余额 100 （应为 100）
再调用两次 refund 后余额 100
```

**为什么。** 补偿的判据是「这件事真的发生过吗」，而不是「这一步返回成功了吗」。

**易错。** 补偿里盲目 `balance += 30`：动作没生效时会凭空多出 30，重复调用会重复退款。
