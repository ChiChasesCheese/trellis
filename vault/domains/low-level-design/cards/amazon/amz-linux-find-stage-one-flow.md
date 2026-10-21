---
id: amz-linux-find-stage-one-flow
node: amazon.amz-linux-find
type: qa
step: 3
tags: [grown]
---
## Q
在 Linux find 文件搜索设计里，「找出所有大于 5MB 的 XML 文件」的最小实现怎么写？

## A
把「条件」做成对象，遍历时只问 `matches`。

```python
class Filter(ABC):
    @abstractmethod
    def matches(self, entry) -> bool: ...
    def __and__(self, other):
        return AndFilter(self, other)

class AndFilter(Filter):
    def __init__(self, left, right):
        self.left, self.right = left, right
    def matches(self, entry):
        return self.left.matches(entry) and self.right.matches(entry)

flt = Extension("xml") & Size.over("5MB")
paths = FileSearcher().paths(root, flt)
```
