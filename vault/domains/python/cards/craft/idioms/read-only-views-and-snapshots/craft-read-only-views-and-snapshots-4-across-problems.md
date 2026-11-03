---
id: craft-read-only-views-and-snapshots-4-across-problems
node: craft.idioms.read-only-views-and-snapshots
type: qa
step: 4
---
## Q
**只读视图与快照 · 币箱、拼车、日志器里「不交出可变容器」的三种做法**｜写法

自动售货机的币箱、拼车行程、日志器都不把内部容器交给调用方。它们各自用了什么手段，选择的依据是什么？

## A
**要点。** 同一个原则：内部容器只在拥有者手里。三种手段的区别在于**谁付拷贝的代价**：读的时候拷贝（读少写多），写的时候整体替换（读多写少），或者构造时拷贝一次（之后不再变）。

```python
# vending-machine.CoinBank.counts：读时拷贝，再包成只读视图
def counts(self) -> Mapping[Coin, int]:
    return MappingProxyType(dict(self._counts))

# ride-sharing.Trip.legs：读时拷贝成 tuple，内部用 list 追加
@property
def legs(self) -> tuple[RideLeg, ...]:
    return tuple(self._legs)

# logger.Logger：构造时拷贝上下文；handlers 是 tuple，写时整体替换，读路径无锁
self._context = MappingProxyType(dict(context or {}))
self._handlers: tuple[Handler, ...] = ()
```

以上各题的代码是节选：省略了类型标注、文档字符串和 `...` 处的细节，个别行为讲解而合并成一行，不是逐字摘抄。

选择依据：币箱和行程每次状态变化频繁、被读的次数少，读时拷贝最简单；日志器每次打日志都要遍历 handlers，注册却很少，所以让写者付代价（造新 tuple、换引用），读者零拷贝零锁。熔断器的 `Metrics` 则直接是一个冻结对象：每次取指标得到的就是那一刻的整张快照，不会读到半截更新。

**见于。** vending-machine、dasher-payout、api-circuit-breaker、logger、ride-sharing。

**信号。** 类里有 `self._xxx: list/dict/set`，且有公开的 getter 或 `@property` 把它返回出去；或者一个读路径很热、写路径很冷的集合。
