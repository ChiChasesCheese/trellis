---
id: craft-protocol-callable-abc-1-callable-for-one-behavior
node: craft.idioms.protocol-callable-abc
type: qa
step: 1
---
## Q
**策略接口 · 只有一个行为时为什么不写 ABC**｜写法

机票系统要让超售、票价、退款规则可替换。第一反应是写一个 `RefundPolicy(ABC)`，再为每种规则写一个子类。实际只写了一行 `RefundPolicy = Callable[[...], int]` 加几个普通函数。多出来的那一层类到底买到了什么？什么时候才值得升级成类？

## A
**要点。** 策略（strategy）的本质是「把一段可替换的行为交给调用方」。行为只有一个入口、没有状态、实现之间没有共同代码时，函数就是最小的接口：签名即契约，类型别名只是给它起名字。ABC 版多出一个基类、一个子类、一次实例化，却没有增加任何约束。需要参数就用闭包返回函数。

```python
# 仪式版：只有一个行为，却要一个基类、一个子类、一个实例
class RefundPolicyBase(ABC):
    @abstractmethod
    def refund(self, paid: int, now: datetime) -> int: ...

class FullBeforeNoon(RefundPolicyBase):
    def refund(self, paid: int, now: datetime) -> int:
        return paid if now.hour < 12 else paid // 2

# 函数版：签名本身就是接口，名字起别名即可
RefundPolicy = Callable[[int, datetime], int]

def full_before_noon(paid: int, now: datetime) -> int:
    return paid if now.hour < 12 else paid // 2

def percent(p: int) -> RefundPolicy:            # 要参数？闭包返回函数
    return lambda paid, now: paid * p // 100

t = datetime(2026, 1, 1, 15)
print("ABC  :", FullBeforeNoon().refund(100, t))
print("函数 :", full_before_noon(100, t), "| 带参数:", percent(30)(100, t))
# 测试里直接传 lambda，不用先写一个子类
print("测试 :", (lambda paid, now: 0)(100, t))
```

实际输出：

```
ABC  : 50
函数 : 50 | 带参数: 30
测试 : 0
```

**为什么。** 测试也更省：传一个 `lambda` 就是一个替身，不用先写子类。

**升级的信号。** （1）策略要带可变状态，或者要有多个相关方法（`check` + `commit`）；（2）几种实现有真正想共享的算法骨架；（3）需要在策略对象上放额外行为（比如组合运算符）。出现其中之一再升级，不要预先写。

**代价。** 函数没有名字之外的结构：想在日志里打印「当前是哪种策略」需要自己给函数起好名字或包一层。
