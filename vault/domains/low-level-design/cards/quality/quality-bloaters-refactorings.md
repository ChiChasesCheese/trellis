---
id: quality-bloaters-refactorings
node: quality.smells
type: qa
step: 2
---
## Q
一个方法长到要靠注释分段、一个类的字段和方法多到没人说得清它的单一职责，这类"膨胀者（bloater）"味道该怎么下刀？

## A
判断信号不是行数本身，而是"这段代码是不是在做好几件不同抽象层次的事"：如果能找到一句注释在给接下来几行"起标题"（比如 `# 校验输入`），说明那几行本该是一个独立的、以意图命名的方法。对类同理——如果一个类的字段能明显分成两组、分别被两组方法各自使用，说明这个类其实是两个类粘在一起。

```python
class OrderProcessor:
    def checkout(self, cart):
        self._validate(cart)
        total = self._price_with_discounts(cart)
        self._charge(cart.customer, total)
```
把 `checkout` 拆成一串同一抽象高度、意图明确的私有方法调用（提炼方法，extract method），是治膨胀者最基础的一步；如果拆出来的私有方法本身又需要自己的状态，通常意味着该提炼出一个新类了（提炼类，extract class）。
