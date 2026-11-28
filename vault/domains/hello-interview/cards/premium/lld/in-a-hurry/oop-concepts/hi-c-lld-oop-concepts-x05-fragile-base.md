---
id: hi-c-lld-oop-concepts-x05-fragile-base
node: lld.in-a-hurry.oop-concepts.exam
type: qa
step: 5
---
## Q
**面向对象概念 · 预测脆弱基类的故障**｜考点 · 必会

`Base.add_all` 内部循环调用 `self.add`。子类 `Counting` 重写 `add`（计数加一），又重写 `add_all`（先加上列表长度再调用父类）。`add_all([1, 2, 3])` 后计数是多少？

## A
```python
class Base:
    def add(self, x: int) -> None: ...

    def add_all(self, xs: list[int]) -> None:
        for x in xs:
            self.add(x)           # 父类内部调用了可被重写的方法


class Counting(Base):
    def __init__(self) -> None:
        self.n = 0

    def add(self, x: int) -> None:
        self.n += 1

    def add_all(self, xs: list[int]) -> None:
        self.n += len(xs)
        super().add_all(xs)       # 父类又调用 self.add，每个元素再数一次


c = Counting()
c.add_all([1, 2, 3])
assert c.n == 6
```
- **结果：** 6 而不是 3
- **根因：** 子类依赖了父类的实现细节
- **修法：** 组合，`Counting` 持有一个 `Base` 并转发调用
