---
id: problems-library-hold-shelf-must-expire
node: problems.booking.library
type: qa
step: 4
tags: [grown]
---
## Q
图书馆管理（Library Management）里，一位读者预约的书还回来了、给他留着，可他再也没来取。如果设计里没有「保留到期」，会发生什么？

## A
**这本副本永远停在「给他留着」的状态：馆里有书，谁也借不到。**这不是性能问题，是功能被彻底锁死——把预约做成「观察者列表」的常见写法就是这么坏掉的。

正确做法是给取书架上的每一条加一个到期时刻，并且到期就清掉：

```python
def expire(self, now: datetime) -> tuple[str, ...]:
    stale = [b for b, e in self._shelf.items() if e.expires_at <= now]
    for barcode in stale:
        del self._shelf[barcode]
    return tuple(stale)
```

还要当场回答一个策略问题：**过期之后这个人回队尾还是彻底出局？**选出局——预约是一次意愿表达，几天不来说明意愿已经不成立；自动回队尾等于让一个不来的人无限期挡在后面的人前面。要书就重新排。

把这个选择**说出来**比选哪一边更重要。

顺带把队列的**四条离队路径**数全：被排上取书架、主动取消、**通过别的副本先借到了**（漏了这条，一个人会既借着书又排着队）、保留到期。每条路径让队列变空时还要把整个键删掉，不留空 `deque`。
