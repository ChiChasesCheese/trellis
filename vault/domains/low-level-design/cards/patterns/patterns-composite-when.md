---
id: patterns-composite-when
node: patterns.structural
type: qa
step: 2
---
## Q
什么问题形状需要 Composite？这个模式内部自带的设计张力是什么？

## A
当客户端必须用同一个接口统一处理"单个对象"和"对象的组合"时用它——问题域本身是一棵局部-整体树：文件和目录、UI 组件和容器、订单里的单品和商品包。

```python
from abc import ABC, abstractmethod

class Node(ABC):
    @abstractmethod
    def size(self) -> int: ...

class Directory(Node):
    def __init__(self, children: list[Node]) -> None:
        self.children = children

    def size(self) -> int:
        return sum(c.size() for c in self.children)
```

张力：叶子节点和容器节点共用一个接口，容器专属的方法（比如"添加子节点"）在叶子上往往没有意义，只能选择抛异常或留空实现，接口不是对每个实现都完全贴合。
