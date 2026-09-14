---
id: s18-validation-error-paths
node: stripe.parsing-validation
type: qa
---

## Q
为什么评分表里明确写着 "dictionary key presence / number validity checks"？错误处理该集中写还是散落在各处 try/except 里？三类错误该怎么区分处理？

## A
**为什么考**：phone screen 的评分表里明确写着 "dictionary key presence / number validity checks"。

**做法**：错误策略在一个函数里集中决定，而不是散落的 `try`：

```python
def parse_row(fields):
    """返回 (record, None) 或 (None, reason)。调用方决定跳过还是报错。"""
    if len(fields) != 5:            return None, "wrong arity"
    if not fields[2].isdigit():     return None, "bad amount"
    ...
```

**三类错误，行为不同**：
1. **格式坏**（字段数不对、数字解析失败）→ 通常"跳过这一行"。
2. **引用坏**（引用了不存在的 id）→ 通常"忽略这条事件"。
3. **业务坏**（余额不足、状态不允许）→ 通常"输出一行拒绝信息"。

题面的 "Edge cases" 一节会说明是哪一类。**不要用 `try/except` 兜底所有情况** ——
你会把真 bug 也吞掉，然后在隐藏测试里静默地输出错误答案。
