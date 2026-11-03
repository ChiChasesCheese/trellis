---
id: craft-closure-factory-policies-1-config-once-call-pure
node: craft.idioms.closure-factory-policies
type: qa
step: 1
---
## Q
**闭包工厂做策略 · 配置只处理一次，调用只做计算**｜写法

航班退票按「离起飞还有多久」分档退款，档位由运营配置，顺序不保证。最直接的写法是一个函数 `refund(tiers, ahead, fare)`，每次调用都把 `tiers` 排序再扫描。为什么这不是好写法？闭包工厂（closure factory：外层函数收配置、返回内层函数）怎样改它？

## A
**要点。** 配置的处理（排序、校验、转换）与每次调用的计算是两件事，频率不同。工厂在外层做前者一次，内层函数只保留纯计算；调用方拿到的是一个只收业务参数的函数，不再带着配置传来传去。

```python
from datetime import timedelta

def tiered_refund(tiers):
    ordered = tuple(sorted(tiers, key=lambda t: t[0], reverse=True))  # 只排一次，且是拷贝
    def refund(ahead, fare):
        for threshold, percent in ordered:      # 从大到小，第一个命中就停
            if ahead >= threshold:
                return fare * percent // 100
        return 0
    return refund

tiers = [(timedelta(hours=24), 50), (timedelta(days=7), 100)]  # 故意乱序
refund = tiered_refund(tiers)
print(refund(timedelta(days=10), 20000))
print(refund(timedelta(days=2), 20000))
print(refund(timedelta(hours=3), 20000))
tiers.clear()                      # 调用方事后改了自己的列表
print(refund(timedelta(days=10), 20000))
```

实际输出：

```
20000
10000
0
20000
```

**为什么。** 每次调用排序是 O(n log n) 的重复劳动；更糟的是配置错误（例如档位为空）要等到第一次退票才暴露，而工厂可以在构造时就校验。`tuple(sorted(...))` 同时是防御性拷贝：最后一行说明调用方清空自己的列表也影响不到已建好的策略。

**代价。** 闭包是匿名的无状态函数。需要计数、缓存、多个方法时，就不该再靠它，改用带 `__call__` 的小类。
