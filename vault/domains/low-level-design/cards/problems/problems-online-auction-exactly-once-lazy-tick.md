---
id: problems-online-auction-exactly-once-lazy-tick
node: problems.marketplaces.online-auction
type: qa
step: 5
tags: [grown]
---
## Q
在线拍卖到了截止时间该怎么结束：每场拍卖一个 `sleep(delay)` 定时器、一个周期扫描线程，还是别的办法？如果进程重启、或者没有任何人访问这场拍卖，它算不算结束了？

## A
**都不是单独够用的答案。**

- 每场一个定时器：上架一百万场就是一百万个待命任务；反狙击一延时，定时器就成了错误时间的炸弹，得取消重排；进程重启，所有定时器全部丢失，状态里没有任何东西记得"这场该结束了"。
- 只用周期扫描线程：幂等、重启后自己会追上，但扫描间隔内读到的状态仍然可能是"进行中"（不够及时）。

更好的答案是**惰性推进**：任何一次读或写都先调用一个 `_tick(now)`，在锁内把状态推进到 `now` 应有的样子（该开拍就开拍、该结束就结束），扫描线程只是让通知更及时，正确性不依赖它。

```python
def _tick(self, now):
    if self._status is ACTIVE and now >= self._ends_at:
        self._status = SOLD if (self._leader and self._price >= self.reserve_price) else UNSOLD
        events.append(self._event(CLOSED, now))
```

没人访问时，诚实的答案是「什么都还没发生，但也没有任何人能观察到\`还没结束\`」——谁来看，谁就在看到之前先把它结算了，对外可见的行为等价于"到点即结束"。状态从 ACTIVE 翻出去这个动作在锁内完成、在一场拍卖的一生中最多发生一次，因而 CLOSED 事件恰好发生一次——这就是「恰好一次」的全部含义，它不依赖任何定时器活着。
