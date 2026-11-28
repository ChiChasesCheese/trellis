---
id: hi-c-lld-file-system-b02-py-weakref-parent
node: lld.problem-breakdowns.file-system.beyond
type: qa
step: 3
---
## Q
**内存文件系统 · Python：父指针与引用环**｜拓展 · 加分

父指向孩子、孩子指回父，形成引用环。Python 会因此泄漏内存吗？`weakref` 改变了什么？

## A
**模式。** 弱引用回指：拥有关系用强引用，反向导航用弱引用。

```python
import gc
import weakref


class Node:
    def __init__(self, strong_parent: bool) -> None:
        self.kids: list["Node"] = []
        self.parent = None
        self.strong = strong_parent

    def attach(self, kid: "Node") -> None:
        self.kids.append(kid)
        kid.parent = self if self.strong else weakref.ref(self)   # 弱引用：不增加引用计数


def alive_after_drop(strong: bool) -> bool:
    gc.disable()                      # 关掉循环垃圾回收，只看引用计数的行为
    try:
        root = Node(strong)
        root.attach(Node(strong))
        probe = weakref.ref(root)     # 观察者：不阻止对象被回收
        del root
        return probe() is not None    # 还活着？
    finally:
        gc.collect()
        gc.enable()


assert alive_after_drop(True) is True     # 环里的对象引用计数不会归零，要等垃圾回收器
assert alive_after_drop(False) is False   # 去掉环：引用计数一归零立刻释放
```
- **底层：** CPython 靠引用计数立即释放对象；环里每个对象都被别人引用，计数永远不为零，只能等循环垃圾回收器定期扫描。所以不会永久泄漏，只是释放延迟。
- **代价：** 取父节点要多一次调用（`parent()`），且父已被回收时得到 `None`；代码到处要处理这种情况。
- **何时值得：** 要立即、可预测地释放（大量节点、批量删除子树）时。
- **何时不用：** 面试规模和普通脚本里，强引用环完全可以，别增加心智负担。
