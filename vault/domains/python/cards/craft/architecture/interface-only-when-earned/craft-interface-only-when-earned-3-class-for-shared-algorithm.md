---
id: craft-interface-only-when-earned-3-class-for-shared-algorithm
node: craft.architecture.interface-only-when-earned
type: qa
step: 3
---
## Q
**接口是挣来的 · 同样是策略，费用拆分为什么要用抽象基类**｜架构

分账系统有均分、百分比、精确金额、按份额四种拆分。停车场的分配策略写成普通函数，这里却用了抽象基类（ABC）加模板方法。差别在哪？什么信号说明「函数该升级成类」了？

## A
**要点。** 升级的信号是：（1）几种实现之间有值得共享的代码，（2）每种实现自带需要在构造时校验的数据。这里四种拆分里有三种按比例分，取整的「最大余数法」（保证各份之和恰好等于总额）只写一次，放在基类的 `_proportional`；百分比之和必须是 100，这条与具体金额无关，放在 `__post_init__` 里，构造即失败。

```python
class SplitError(Exception): ...

class Split(ABC):
    @abstractmethod
    def compute(self, amount: int, who: list[str]) -> dict[str, int]: ...

    @staticmethod
    def _proportional(amount: int, who: list[str], w: dict[str, Fraction]) -> dict[str, int]:
        """共享算法：最大余数法，保证加总恰好等于 amount。取整规则只写一次。"""
        exact = {u: Fraction(amount) * w[u] / sum(w.values()) for u in who}
        shares = {u: e.numerator // e.denominator for u, e in exact.items()}
        left = amount - sum(shares.values())
        for u in sorted(who, key=lambda u: -(exact[u] - shares[u]))[:left]:
            shares[u] += 1
        return shares

@dataclass(frozen=True)
class EqualSplit(Split):
    def compute(self, amount, who):
        return self._proportional(amount, who, {u: Fraction(1) for u in who})

@dataclass(frozen=True)
class PercentageSplit(Split):
    percentages: dict[str, int]
    def __post_init__(self) -> None:                  # 构造时就检查：与金额无关的不变量
        if sum(self.percentages.values()) != 100:
            raise SplitError("百分比之和必须是 100")
    def compute(self, amount, who):
        return self._proportional(amount, who, {u: Fraction(self.percentages[u]) for u in who})

who = ["甲", "乙", "丙"]
print(EqualSplit().compute(100, who))
print(PercentageSplit({"甲": 50, "乙": 30, "丙": 20}).compute(101, who))
try:
    PercentageSplit({"甲": 50, "乙": 30})
except SplitError as e:
    print("构造即失败:", e)
```

100 元三人均分；101 元按 50/30/20；再构造一个只有 80% 的拆分，实际输出：

```
{'甲': 34, '乙': 33, '丙': 33}
{'甲': 51, '乙': 30, '丙': 20}
构造即失败: 百分比之和必须是 100
```

**为什么。** 把算法整体替换，用函数就够；有共享代码、有自带数据时，类才是装它们的地方。精确金额拆分完全不调用共享算法，因为金额对不上是调用方输入错误，不是取整噪声。

**易错。** 不要为了「像设计模式」而用类；先问共享什么、校验什么，答不出来就用函数。
