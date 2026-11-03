---
id: craft-order-side-effects-by-reversibility-4-saga-pairs
node: craft.architecture.order-side-effects-by-reversibility
type: qa
step: 4
---
## Q
**副作用按可逆性排序 · Saga 为什么要求每步成对声明动作与补偿，失败的那一步也要补偿**｜架构

下单流程跨三个参与方：库存、支付、履约，其中任何一步都可能失败。用一个大 `try/except` 在 `except` 里写回滚，随着参与方增多会出什么问题？扣款这一步自己抛异常时，要不要对它做补偿？

## A
**要点。** 补偿的对象是「已经完成了哪几步」，这件事只有执行器知道。把「做什么」和「怎么撤销」在同一个 `SagaStep` 里成对声明，顺序与补偿就只剩一处。失败的那一步本身也要补偿，而且排在最前面，因为动作不是原子的：扣款可能已经扣走了钱，却在后面记账时抛异常。代价是补偿可能在动作根本没生效时被调用，所以补偿必须幂等、能容忍「什么都没发生」。

```python
state: dict[str, bool] = {}
refunded, restocked = [], []

def ok(): pass

def do_commit():
    raise RuntimeError("预留已过期")            # 这一步自己失败：一件货都没扣
    state["committed"] = True

def undo_commit_naive():
    restocked.append("补货")                    # 盲目补货

def undo_commit():
    if state.pop("committed", None):        # 只有真的扣减过才补货
        restocked.append("补货")

def run(undo) -> None:
    restocked.clear(); state.clear()
    steps = [("预留", ok, ok), ("扣款", ok, lambda: refunded.append("退款")),
             ("扣库存", do_commit, undo)]
    done = []
    try:
        for name, act, comp in steps:
            done.append((name, comp))           # 先登记补偿：这一步自己失败时也会被调用
            act()
    except RuntimeError:
        for name, comp in reversed(done):
            comp()
    print("补货次数:", len(restocked), "退款次数:", len(refunded))
    refunded.clear()

run(undo_commit_naive)
run(undo_commit)
```

「扣库存」这一步自己抛异常（一件货都没扣），分别用盲目补货和上面的守卫补货各跑一遍，实际输出：

```
补货次数: 1 退款次数: 1
补货次数: 0 退款次数: 1
```

**为什么。** 盲目补货会凭空造出一件库存；守卫版本问「我真的扣过吗」，没扣就什么都不做。这是补偿幂等的具体含义：重复调用或在没生效时调用，结果都对。

**易错。** 补偿自己也可能失败，不能吞掉，要收进失败对象里报告出去（见错误边界）。
