---
id: problems-library-renewal-yields-to-the-queue
node: problems.booking.library
type: qa
step: 5
tags: [grown]
---
## Q
图书馆管理（Library Management）里，某个书目有人在排队预约，正借着它的读者申请续借。该批准吗？说出判据。

## A
**不批准。**判据：**排队是对还没拿到书的人的承诺，续借只是对已经拿到书的人的方便，后者让位。**

这是这道题里唯一一条真正的业务规则冲突，面试官最爱追，所以要主动说出来。实现上就是续借的第一道校验：

```python
if self._holds.queue_length(loan.title_id):
    raise RenewalRefusedError(...)
if loan.renewals >= policy.max_renewals:
    raise RenewalRefusedError(...)
```

另外两个值得定的细节：续借次数有上限（否则一本热门书可以被一个人永久持有）；新的到期日从**今天**起算而不是从原到期日顺延（提前续借不该白拿额外天数），实现是 `max(原到期日, now + 借期)`。

排队的人撤销预约后，续借应当立刻恢复可用——这一点值得写成一条测试。
