---
id: problems-logger-effective-level-and-notset
node: problems.components.logger
type: qa
step: 4
tags: [grown]
---
## Q
日志框架里绝大多数 logger 都不该单独配置级别，而是"听祖先的"。这条"有效级别（effective level）"规则具体怎么算？用 `None` 表示继承，和标准库 `logging` 用 `NOTSET = 0` 表示继承，哪个更好？

## A
算法是沿 `parent` 一路向上，返回遇到的第一个显式设过的级别；根 logger 必须有一个具体级别（标准库默认 `WARNING`，这正是"我的 `info()` 为什么什么都没打印"的答案），递归才有底。

```python
node = self
while node is not None:
    if node.level is not None:
        return node.level
    node = node.parent
return LogLevel.WARNING
```

用 `None` 更好：`NOTSET = 0` 让同一个值同时表示"一个级别"和"我没设过"，于是 `setLevel(0)` 到底是"打开全部日志"还是"继承父亲"要查文档；`None` 把"没有值"和"值是 0"分得干干净净。
