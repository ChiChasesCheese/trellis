---
id: amz-linux-find-follow-up-new-condition
node: amazon.amz-linux-find
type: qa
step: 6
tags: [grown]
---
## Q
在 Linux find 文件搜索设计里，面试官要求新增「空目录」和「修改时间」两种条件，需要改哪里、哪里不动？

## A
各新增一个 `Filter` 子类，别处不动。

```python
class EmptyDir(Filter):
    def matches(self, entry):
        return entry.node.kind is Kind.DIR and not entry.node.children

flt = EmptyDir() | Extension("gz")
```

`FileSearcher`、`AndFilter`、`Extension` 一行不改，这就是开闭原则的证据。要「查询语言」（`ext=py and size>1k`）：写一个解析器把字符串变成 `Filter` 树，树本身就是语法树。
