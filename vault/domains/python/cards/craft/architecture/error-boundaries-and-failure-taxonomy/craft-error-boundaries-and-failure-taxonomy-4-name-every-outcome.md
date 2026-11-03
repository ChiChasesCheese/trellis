---
id: craft-error-boundaries-and-failure-taxonomy-4-name-every-outcome
node: craft.architecture.error-boundaries-and-failure-taxonomy
type: qa
step: 4
---
## Q
**错误边界与失败分类 · 「没发出去」为什么每种都要有名字，而不是一个 FAILED**｜架构

通知服务发一条短信可能没发出去：用户关了这个渠道、处于静默时段、没留号码、触发限流、瞬时故障正在重试、永久失败。如果统一返回 `FAILED`，调用方（以及运维）下一步该做什么？

## A
**要点。** 失败的名字就是调用方的决策依据：要不要重试、要不要告诉用户、要不要告警。一个 `FAILED` 把这些信息压没了。通知服务的投递结果枚举（`DeliveryStatus`）里每种「没发出去」都有自己的名字，是什么就是什么，调用方用集合判断下一步，不用去猜日志。

```python
class Status(Enum):
    SENT = "sent"
    DUPLICATE = "duplicate"
    RETRY_SCHEDULED = "retry_scheduled"
    DEAD_LETTERED = "dead_lettered"
    SUPPRESSED_QUIET_HOURS = "quiet_hours"
    SUPPRESSED_NO_ADDRESS = "no_address"

# 每个名字对应一组调用方要做的决策
RETRY_LATER = {Status.RETRY_SCHEDULED, Status.SUPPRESSED_QUIET_HOURS}
ASK_USER = {Status.SUPPRESSED_NO_ADDRESS}               # 只有用户能补号码
ALERT_OPS = {Status.DEAD_LETTERED}

def next_action(s: Status) -> str:
    if s in RETRY_LATER: return "稍后重试，不打扰用户"
    if s in ASK_USER:    return "提示用户补充联系方式"
    if s in ALERT_OPS:   return "告警，人工看死信"
    return "无需处理"

for s in Status:
    print(f"{s.value:16} -> {next_action(s)}")
print("只有一个 FAILED 时，上面四种结果的决策都要从日志里猜")
```

（枚举还有 `DUPLICATE` 等成员，这里精简到五个，`for s in Status` 逐个打印。）实际输出：

```
sent             -> 无需处理
retry_scheduled  -> 稍后重试，不打扰用户
dead_lettered    -> 告警，人工看死信
quiet_hours      -> 稍后重试，不打扰用户
no_address       -> 提示用户补充联系方式
```

**为什么。** 被抑制（suppressed）不是失败：用户关了渠道是正常的业务结果，返回值就行，不是异常；调用方 bug、依赖挂了才抛。

**代价。** 状态越多，调用方要处理的分支越多；分类的标准是「调用方的下一步动作是否不同」，不同才值得一个名字，一样的就合并。
