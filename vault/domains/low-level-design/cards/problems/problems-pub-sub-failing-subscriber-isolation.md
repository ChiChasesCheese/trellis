---
id: problems-pub-sub-failing-subscriber-isolation
node: problems.components.pub-sub
type: qa
step: 7
tags: [grown]
---
## Q
进程内 Pub-Sub 里，一个订阅者的处理函数抛异常。必须保证哪两件事？代码上怎么写？

## A
（1）**不影响其他订阅者**——它们各有各的位点和投递线程，本来就互不相干；（2）**不影响它自己后面的消息**——异常绝不能冒泡出投递线程，否则线程一死，这个订阅之后的消息会永远停在位点上，而且悄无声息。

订阅者抛出的异常是**数据**，不是控制流：

```python
for attempt in range(1, self._max_attempts + 1):
    try:
        self._handler(message)
        return
    except Exception as exc:
        last = exc
self._failed += 1
self._failure_policy(self, message, last)
```

重试用尽后交给失败策略——一个 `Callable[[Subscription, Message, BaseException], None]`，不为它写抽象基类：它只有一个方法、不带状态。连失败策略本身也要包在 try 里，死信投递失败同样不许炸掉投递线程。
