---
id: pay-risk-compliance-fraud-velocity
node: risk-compliance.fraud
type: qa
step: 3
---
## Q
风控里的规则引擎（rule engine）和速度检查（velocity check）是什么？请写一个滑动窗口的速度检查并说明怎么读它的结果。

## A
**规则引擎**：一组可配置的条件，例如"收货国与卡发行国不同且金额超过 200 美元，转人工"。优点是可解释、可立刻上线、能审计；缺点是靠人维护，容易被绕过，规则多了互相冲突。

**速度检查**：统计某个实体（卡、设备、IP、账号、邮箱）在一个时间窗内的行为次数或金额，超过阈值就认为可疑。试卡、批量注册、盗刷往往在短时间内的次数异常。

```python
from collections import defaultdict, deque

hits: dict[str, deque[float]] = defaultdict(deque)

def too_fast(key: str, now: float, window: float = 60.0, limit: int = 5) -> bool:
    q = hits[key]
    while q and now - q[0] > window:
        q.popleft()
    q.append(now)
    return len(q) > limit

print([too_fast("device_9", t) for t in (0, 5, 10, 15, 20, 25, 70)])
```
实际输出：
```
[False, False, False, False, False, True, False]
```
读法：同一设备在 25 秒内做了 6 次尝试，第 6 次超过"60 秒内最多 5 次"，被标记。第 7 次发生在 70 秒，窗口移动后只剩 10、15、20、25 加上本次共 5 次，不再超限。

**工程要点**
1. 窗口计数在生产里通常放在内存数据库（如带过期的计数器），按实体键分片，每个检查要在个位数毫秒内完成。
2. 速度检查只是信号，不一定直接拒绝：命中后升级验证或提高风险分，避免误伤合法的批量购买。
3. 要同时在多个维度做：同一张卡、同一设备、同一 IP 段、同一邮箱域名，单维度容易被轮换绕过。
