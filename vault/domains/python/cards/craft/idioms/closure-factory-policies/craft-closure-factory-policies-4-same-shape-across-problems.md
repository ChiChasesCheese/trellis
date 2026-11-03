---
id: craft-closure-factory-policies-4-same-shape-across-problems
node: craft.idioms.closure-factory-policies
type: qa
step: 4
---
## Q
**闭包工厂做策略 · 超售、退票、涨价三个策略长得一样**｜写法

航班超售、退票、打车涨价，三个不同领域的规则，代码里都是「工厂 + 内层函数」。它们的结构有什么共同点？策略签名里为什么要把完整上下文都传进去，哪怕这次用不上？

## A
**要点。** 共同点是三步：外层接配置并做一次性处理，内层接运行时的完整上下文，返回值是业务答案。内层签名统一是「该决策可能用到的全部上下文」，这样以后加一个用到新字段的策略，不用改调用方，也不用改已有策略。

```python
# airline：超售额度，外层只捕获 by_cabin，内层按舱位取百分比
def percent_overbooking(by_cabin):
    def extra(cabin, instance):
        return instance.capacity(cabin) * by_cabin.get(cabin, 0) // 100
    return extra

# airline：退票，外层排序一次，内层扫描
def tiered_refund(tiers):
    ordered = tuple(sorted(tiers, key=lambda tier: tier[0], reverse=True))
    def refund(booking, now): ...

# ride-sharing：涨价，外层排序，内层用 Fraction 比较
def demand_surge(steps):
    ordered = tuple(sorted(steps, key=lambda s: s[0], reverse=True))
    def surge(request, waiting, available):
        ratio = Fraction(waiting, max(1, available))
        return next((m for t, m in ordered if ratio >= t), Fraction(1))
```

以上各题的代码是节选：省略了类型标注、文档字符串和 `...` 处的细节，个别行为讲解而合并成一行，不是逐字摘抄。

不变的是：配置在外层固化，内层只依赖闭包变量和调用参数，没有可变状态。变的是外层做什么：超售只存字典，退票和涨价要排序。`surge` 接收 `request`，虽然当前实现没用它，是为了以后写「按地区涨价」的策略时，不用改调用点。

**见于。** airline（超售、退票）、ride-sharing（涨价、司机打分 weighted_score，三个权重固化在闭包里）、vending-machine（找零算法 `ChangeMaker` 是纯函数，构造时注入）。

**信号。** 一个类里有一个会变化的规则（价格、退款、匹配、找零），测试想换不同版本，而规则本身没有状态。
