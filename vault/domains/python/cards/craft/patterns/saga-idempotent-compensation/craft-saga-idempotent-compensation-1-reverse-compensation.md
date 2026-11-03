---
id: craft-saga-idempotent-compensation-1-reverse-compensation
node: craft.patterns.saga-idempotent-compensation
type: qa
step: 1
---
## Q
**Saga 与幂等补偿 · 多步操作中途失败，怎么把已做的撤销**｜写法

下单要依次占库存、扣款、创建发货单，各自是独立的步骤，没法放进一个数据库事务。发货单失败时，前两步已经生效了。用一个大 `try/except` 怎么写？为什么不够好？

## A
**要点。** Saga：每一步把「做什么」和「怎么撤销」成对声明；执行器记下哪些步骤已经完成，任何一步失败，就把已完成的步骤按相反顺序补偿（compensation）。大 `try/except` 的问题是「已经做完了哪几步」只有执行器知道；写成嵌套 `except` 时每加一个参与方就多一层，还很容易补偿一个根本没执行成功的步骤。

```python
def run(steps):
    done = []
    for step in steps:
        try:
            step.action()
        except Exception as exc:
            errors = []
            for unwind in [step, *reversed(done)]:   # 失败的那步 + 已完成的逆序
                try:
                    unwind.compensation()
                except Exception as ce:
                    errors.append((unwind.name, ce))  # 补偿失败不能掩盖原始异常
            raise SagaFailure(step.name, exc, tuple(errors)) from exc
        done.append(step)
```

占库存、扣款成功，发货单失败：

```
步骤「发货单」失败：下游失败
['做 占库存', '做 扣款', '做 发货单', '撤 发货单', '撤 扣款', '撤 占库存']
```

**为什么逆序。** 后面的步骤可能依赖前面的结果（发货单依赖已占的库存），撤销要从最近的开始，与做的顺序相反。

**代价。** 补偿不是回滚：中间状态对外可见（库存被占了又放回），所以补偿必须是语义上的撤销（退款而不是删除记录）。
