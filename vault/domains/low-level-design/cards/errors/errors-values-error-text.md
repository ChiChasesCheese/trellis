---
id: errors-values-error-text
node: errors.exceptions-vs-values
type: qa
step: 4
---
## Q
把异常转成结果里的 `error` 字符串时，用 `str(e)`、`repr(e)` 还是别的？这段文字该给谁看？

## A
**给人和日志看“类型名: 消息”，给机器和模型看固定码**

- **`str(e)` 丢掉类型名**：`str(ValueError())` 是空串，`error` 字段一片空白，查不出是什么错；
- **`repr(e)` 多出括号和引号**：`ValueError('bad')`，下游要解析或展示时很难看；
- **固定格式 `类型名: 消息`**：空消息也保留冒号，格式一致，测试可以精确断言；
- **文本可能含内部信息**：路径、SQL、密钥片段。给模型或外部调用方的结果只放固定错误码（如 `tool_error`），原文进日志；
- **要完整原因时保留异常对象**：栈和 `__cause__` 在异常上，不在字符串里。

```python
e = ValueError("bad")
print(repr(str(ValueError())))                 # ''：空消息，什么都看不出
print(str(e), "|", repr(e))                    # bad | ValueError('bad')
print(f"{type(e).__name__}: {e}")              # ValueError: bad
print(f"{type(ValueError()).__name__}: {ValueError()}")   # 末尾是冒号加空格：空消息也保留格式
```

**知识点：**异常与错误值（Exceptions vs Values）
