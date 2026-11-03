---
id: craft-closure-factory-policies-5-scales-config-push
node: craft.idioms.closure-factory-policies
type: qa
step: 5
---
## Q
**闭包工厂做策略 · 从一个函数到配置中心下发规则**｜写法

打车涨价规则原来写死在代码里，现在运营想不发版就改档位，配置中心会推送新参数。同样的闭包工厂在一个进程里怎么支持热更新？放到多台机器时又要多考虑什么？

## A
**要点。** 把「配置」和「执行」分开，是闭包工厂的核心；热更新只是把「调用工厂」换成「收到新配置时再调用一次工厂，替换引用」。一个进程里替换引用就是一次赋值；多台机器要面对「各实例什么时候看到新配置」，需要版本号和一致性约定。

```python
from fractions import Fraction

def demand_surge(steps):
    ordered = tuple(sorted(steps, key=lambda s: s[0], reverse=True))
    def surge(waiting, available):
        ratio = Fraction(waiting, max(1, available))
        return next((m for t, m in ordered if ratio >= t), Fraction(1))
    return surge

class Dispatcher:
    def __init__(self, policy) -> None:
        self._policy = policy
    def reload(self, policy) -> None:
        self._policy = policy              # 一次赋值，不会读到一半的配置
    def price(self, base, waiting, available):
        policy = self._policy              # 每次请求只读一次，同一单前后一致
        return int(base * policy(waiting, available))

d = Dispatcher(demand_surge([(Fraction(2), Fraction(3, 2)), (Fraction(1), Fraction(6, 5))]))
print(d.price(1000, 10, 4))     # 比值 2.5
print(d.price(1000, 5, 4))      # 比值 1.25
d.reload(demand_surge([(Fraction(1), Fraction(2))]))
print(d.price(1000, 5, 4))
```

实际输出：

```
1500
1200
2000
```

**为什么。** 新策略完整建好之后才换引用，旧策略在途的调用仍用旧的那一份，没有「一半旧一半新」。这和不可变快照发布同理：策略是只读的，换的只是指针。

**多机。** 每个实例各自收到推送，时刻不同，同一用户短时间内可能先后看到两套价格。要么接受最终一致，并把「策略版本」写进订单；要么价格由单一服务算出再返回。配置在构造时校验，错误的配置被拒绝，就不会替换掉正在用的好策略。
