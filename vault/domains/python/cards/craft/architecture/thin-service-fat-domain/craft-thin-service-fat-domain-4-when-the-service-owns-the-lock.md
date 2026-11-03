---
id: craft-thin-service-fat-domain-4-when-the-service-owns-the-lock
node: craft.architecture.thin-service-fat-domain
type: qa
step: 4
---
## Q
**服务层薄、领域对象厚 · 券商的下单服务为什么拿着一把大锁，它还算「薄」吗**｜架构

券商的 `Brokerage` 一把锁保护账户表、订单索引、所有订单簿，下单全程在锁里。这和订座服务「服务锁不碰库存」看上去矛盾。什么情况下，服务层持有锁是合理的？它的「薄」应该怎么衡量？

## A
**要点。** 衡量薄不薄，看规则放在哪里，而不是看谁拿着锁。下单这一个动作要同时改两个账户和一个订单簿，三者没有一个天然的拥有者，所以不变量「校验 → 预留 → 撮合 → 结算是一个原子动作」只能由门面（facade）拥有，锁因此在服务层。但规则仍在领域对象里：订单簿只管撮合，不碰钱；账户自己知道怎么预留和结算；服务只是按顺序调用它们。

```python
# 节选自 Brokerage.place_order：省略了 order_type、limit_price、now 等参数和文档字符串
def place_order(self, account_id, symbol, side, quantity, ...):
    with self._lock:
        account, book = self._account(account_id), self._book(symbol)
        order = self._build(account_id, symbol, side, quantity, ...)   # 纯校验
        self._orders[order.id] = order                                 # 被拒的单也先入表留痕
        self._reserve(account, order, book)                            # 账户冻结资金
        for resting, price, filled in book.submit(order):              # 订单簿撮合
            self._settle(order, resting, price, filled, now)           # 账户结算
        if not order.is_open:
            self._release(order)
        event = book.top_of_book(now)
    self._publish(event)                                               # 锁外通知
    return order
```

**为什么。** 把订单簿和账户各自带锁、再由服务协调，就会出现「账户锁 → 簿子锁」的嵌套和锁序问题；一个会话内部只有一个原子动作时，一把粗锁更简单。账户之间、品种之间如果要并行，再按品种或账户分片。

**易错。** 衡量标准：服务里出现业务算术（价格比较、费用公式、状态判断）就是在变胖。这里的服务只调用，没有算术，所以它仍是协调器，持有的只是原子范围。
