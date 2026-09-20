---
id: quality-parameter-object
node: quality.refactoring
type: qa
step: 3
---
## Q
引入参数对象（parameter object）——除了缩短函数签名，还有什么设计收益能证明它不只是把参数包了个壳？

## A
```python
def book(origin: str, dest: str, depart: date, ret: date, guests: int): ...
# 变成
def book(route: Route, period: StayPeriod, guests: int): ...
```
真正的收益有两个：第一，给校验和行为一个家——`StayPeriod` 可以在自己的 `__post_init__` 里一次性强制 `depart < ret`，还能长出 `nights()` 这样的方法，这些逻辑原本会在每个调用点各自重复一遍。第二，这个对象成为一个稳定的接缝：以后加一个字段，改的是 `@dataclass` 定义本身，而不是调用链上每一处函数签名——省掉了一条潜在的霰弹式修改路径。

反模式是那种大杂烩式的 `Options`/`Context` 对象：仅仅为了让签名短一点，就把彼此无关的参数硬捆在一起，等于伪造了一个数据团，让每个调用方都平白耦合上了它根本不关心的字段。只把真正构成同一个概念的参数聚在一起，才值得升级成一个 `@dataclass`。
