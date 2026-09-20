---
id: quality-replace-conditional-polymorphism
node: quality.refactoring
type: qa
step: 4
---
## Q
```python
def pay(emp):
    if isinstance(emp, Engineer):
        return emp.base * 1.1
    elif isinstance(emp, Manager):
        return emp.base + emp.bonus
```
这条 `isinstance` 阶梯不止在 `pay()` 里出现，`in_report()`、`annual_review()` 里也各有一份几乎一样的分支。该怎么重构，什么时候反而不该这样做？

## A
触发条件是**同一组类型分支**重复出现在多个地方——每加一种员工类型，就要在所有这些地方各加一个分支，是一条霰弹式修改的路径。修法是把每个分支的逻辑搬进各自子类的同名方法里，用多态分派取代类型判断：

```python
class Engineer(Employee):
    def pay(self) -> float:
        return self.base * 1.1
class Manager(Employee):
    def pay(self) -> float:
        return self.base + self.bonus
```
如果不想引入类层次，`functools.singledispatch` 能达到类似效果，把分支拆成按类型注册的独立函数。该保留 `isinstance`/`match` 分支的情况：这组判断只出现**一次**（多态是拿"一处可读的代码"换"散落在多个文件里的类"，划不来）；或者新增的是**操作**而不是**类型**——多态为"加类型不改分支"优化，集中式的条件判断为"加操作不改每个类型"优化，这就是 expression problem，要选那个真正在变的轴。
