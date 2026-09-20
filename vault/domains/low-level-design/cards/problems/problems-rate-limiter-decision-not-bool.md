---
id: problems-rate-limiter-decision-not-bool
node: problems.components.rate-limiter
type: qa
step: 2
tags: [grown]
---
## Q
限流器（Rate Limiter）的 `allow(key)` 该返回 `bool`、抛异常，还是别的？三种选项各付什么代价？

## A
返回一个不可变的小结果对象，并让它实现 `__bool__`：

```python
@dataclass(frozen=True, slots=True)
class Decision:
    allowed: bool
    remaining: int
    retry_after: float
    rule: str = ""

    def __bool__(self) -> bool:
        return self.allowed
```

- **裸 `bool` 的代价**：HTTP 429 要带 `Retry-After`、响应头要带 `X-RateLimit-Remaining`，而这两个数只有算法内部算得出来（令牌桶算 `(cost − 令牌数) / 速率`，滑动日志算第几条旧记录何时滑出窗口）。丢掉它们，调用方只能猜一个退避时间；更糟的是所有客户端都猜同一个数，被拒的请求在同一刻集体重试，形成惊群（thundering herd）。
- **抛异常的代价**：被限流是**正常的业务结果**，不是错误——一个健康的公开 API 每秒都在拒绝请求。把高频正常分支写成 `try/except` 既是控制流滥用，也让一次拒绝不能作为值被传递、统计和记录。异常留给配置错误（非正的 limit、非正的 cost）。

`__bool__` 是关键一笔：`if limiter.allow(key):` 照样读得通，所以从 `bool` 升级成结构化结果**不需要调用方改一行既有代码**。
