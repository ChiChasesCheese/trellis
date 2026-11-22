---
id: aid-defects-swallow
node: t04.ai-hallucinated-api-over-engineering
type: qa
step: 2
tags: [考点]
---
## Q
**缺陷识别 · 一段 diff**｜考点 · 必会

agent 的 diff 里有这样一段，测试全绿。你要问什么？

```python
def fetch_rate(currency):
    try:
        return client.get_rate(currency, cache=True)
    except Exception:
        return 1.0
```

## A
**三个问题：**

| 问题 | 为什么 |
|---|---|
| `get_rate` 真的有 `cache` 参数吗？ | 可能是 hallucinated API；查官方文档和装的版本 |
| `except Exception: return 1.0` 在做什么？ | 吞掉所有错误，网络失败时悄悄用汇率 1.0 算钱——**比崩溃更糟**，没人会发现 |
| 为什么测试是绿的？ | 测试没覆盖失败路径，或测试的 mock 恰好让它一直成功 |

**改法：** 只捕获具体的、预期的异常；失败时让它报错或记录并走明确的降级策略；补一个"client 抛错时应该……"的测试，**先看它红**。

**别做：** 因为"绿"就合并。

**出处：** Stack Overflow Developer Survey 2025（AI：几乎对但不对）；Claude Code docs《Best practices》（Give Claude a check to run：ask for evidence）
