---
id: review-ai-needless-abstraction
node: review.ai-code
type: qa
step: 3
---
## Q
你要求“按会员等级打折”，AI 返回了抽象基类、三个策略类和一个工厂，共 40 行，需求只有两个等级。评审时该怎么处理？

## A
**AI 倾向于写“看起来专业”的结构：问一句“现在谁需要这层抽象”**

- **没有第二个使用者的接口、工厂、配置**：删掉，用最直接的函数；
- **多出来的代码也是要维护的**：每个类都要测试、要读、要在改规则时同步；
- **评审用的问题**：这层抽象解决的是现在的哪个问题？删掉它，代码会不会更难懂？
- **例外**：需求里明确写了会增加更多种类、需要运行时配置，那时抽象才有顾客；
- **别批量接受**：“生成的代码能跑”不等于“这个代码库想要这样的代码”；改小再合并。

```python
from abc import ABC, abstractmethod
class DiscountStrategy(ABC):                         # AI 版本：抽象 + 两个类 + 工厂
    @abstractmethod
    def apply(self, amount): ...
class Gold(DiscountStrategy):
    def apply(self, amount): return amount * 0.9
class Basic(DiscountStrategy):
    def apply(self, amount): return amount
def make(tier): return {"gold": Gold, "basic": Basic}[tier]()
RATES = {"gold": 0.9, "basic": 1.0}                  # 直接的版本
def discount(amount, tier): return amount * RATES[tier]
assert make("gold").apply(100) == discount(100, "gold") == 90.0
```

**知识点：**评审 AI 生成的代码（Reviewing AI Code）
