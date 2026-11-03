---
id: craft-saga-idempotent-compensation-3-compensation-errors
node: craft.patterns.saga-idempotent-compensation
type: qa
step: 3
---
## Q
**Saga 与幂等补偿 · 补偿自己失败了，不能把原始错误盖住**｜写法

扣款失败后要执行退款补偿，退款网关恰好也超时抛异常。如果补偿的异常直接冲出去，调用方看到的是什么？排查故障的人会误以为是什么问题？

## A
**要点。** 调用方只看到「退款网关超时」，真正的起因（扣款步骤失败）被盖住了，排查方向完全偏离。补偿的异常要被收集起来，随主错误一起返回（`SagaFailure.compensation_errors`），原始异常用 `raise ... from` 保留。补偿失败也不能吞掉：它意味着有一笔钱可能留在半路，要告警和人工对账。

```python
def run_masking():
    try:
        raise Original("扣款步骤失败")
    except Original:
        comp_fail()                          # 补偿抛异常，冲出去盖住原始错误

def run_collecting():
    try:
        raise Original("扣款步骤失败")
    except Original as exc:
        errors = []
        try:
            comp_fail()
        except Exception as ce:
            errors.append(ce)                # 收集，不吞
        raise SagaFailure(exc, errors) from exc
```

调用方看到的异常：

```
run_masking     调用方看到: OSError | 退款网关超时
run_collecting  调用方看到: SagaFailure | 扣款步骤失败（补偿失败 1 个）
```

**为什么。** 失败路径上的代码最不该制造新的异常：它的任务是把局面收拾干净并告诉调用方发生了什么。

**易错。** 吞掉补偿异常（`except: pass`）比盖住更糟：系统以为一切回滚成功。
