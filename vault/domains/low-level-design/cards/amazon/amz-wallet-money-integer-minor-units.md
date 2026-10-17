---
id: amz-wallet-money-integer-minor-units
node: amazon.amz-wallet
type: qa
step: 2
tags: [grown]
---
## Q
在钱包设计里，金额为什么用整数最小单位（分）而不是浮点数？怎么防止币种混加？

## A
浮点无法精确表示 0.1：`0.1 + 0.2 = 0.30000000000000004`，累加后账对不平。用整数分（1.50 美元存 150），只在展示时格式化。再把金额和币种打包成不可变的 `Money`，不同币种相加直接报错，把「美元加欧元」这类错误挡在类型层。
```python
@dataclass(frozen=True)
class Money:
    minor: int
    currency: str = "USD"

    def __add__(self, other):
        if other.currency != self.currency:
            raise ValueError("currency mismatch")
        return Money(self.minor + other.minor, self.currency)
```
