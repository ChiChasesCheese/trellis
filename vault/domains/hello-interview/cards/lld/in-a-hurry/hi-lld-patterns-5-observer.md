---
id: hi-lld-patterns-5-observer
node: lld.in-a-hurry.patterns
type: qa
step: 5
---
## Q
**观察者：一对多通知**｜低层设计 · 速览

设计里一个对象的变化要触发多个组件更新（股价变动后，显示和提醒都要响应）。观察者模式（Observer）怎么组织？什么措辞会提示它？

## A
**结构。** 主题（Subject）维护一个观察者列表，提供 `attach`、`detach`、`notify_observers`；每个观察者实现 `update`。主题状态改变时遍历列表逐个通知。

```python
class Stock(Subject):
    def set_price(self, price: float) -> None:
        self.price = price
        self.notify_observers()  # 通知所有人

    def notify_observers(self) -> None:
        for o in self._observers:
            o.update(self.symbol, self.price)
```

**好处。** 主题不需要知道观察者拿到信息后做什么：显示、阈值提醒，以后加日志也不用改主题。

**信号。** 需求里出现“通知”“更新多个组件”，比如下单后库存、通知、分析都要知道。这是面试里的头部模式。
