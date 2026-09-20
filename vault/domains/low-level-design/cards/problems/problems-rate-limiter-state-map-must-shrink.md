---
id: problems-rate-limiter-state-map-must-shrink
node: problems.components.rate-limiter
type: qa
step: 5
tags: [grown]
---
## Q
限流器（Rate Limiter）按 key 懒创建状态，一百万个 IP 各来过一次会怎样？可是回收又不能太早——太早会出什么事？判据该怎么定？

## A
不回收就是内存泄漏，而内存有界恰恰是限流器存在的意义之一。

回收太早的后果更隐蔽：**删掉一个 key 的状态等于把它的配额清零**，客户端只要停一下就能给自己解封。

判据不该是「多久没用过」（那要靠调用方传对一个阈值，把正确性寄托在参数上），而该是**状态与新建状态等价**：

```python
def is_idle(self, now: float) -> bool:
    return self._used(now) <= 0.0
```

占用为 0 的状态，留着和删掉对后续任何一次判定都给出相同答案，所以「删早了」根本不可能发生。具体到各算法：固定窗口是格号已翻篇，令牌桶是令牌补满，滑动日志是条目全部滑出窗口。

扫描时机用摊还：每个分片累计的操作数超过门槛就扫一遍自己，一次 O(条目数)，摊到那么多次操作上是 O(1)。
