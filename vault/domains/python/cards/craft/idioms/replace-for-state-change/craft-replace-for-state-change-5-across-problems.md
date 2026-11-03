---
id: craft-replace-for-state-change-5-across-problems
node: craft.idioms.replace-for-state-change
type: qa
step: 5
---
## Q
**用 replace 表达状态变化 · 司机、额度包、聊天消息、重试信封里的同一次替换**｜写法

司机抢占、额度包作废、聊天消息编辑、通知重试，都用了 `replace`。它们替换的东西和目的各是什么，什么保持不变？

## A
**要点。** 不变的是形状：持有一条冻结的记录，改一两个字段，造出新记录，再换进它所在的容器（字典、堆、列表）；旧记录不动。变的是**换进哪里、为了什么**：为了让比较并交换没有缝隙，为了让重放自然生效，为了保留历史，为了不改动正在处理的那一份。

```python
# ride-sharing：锁内校验 + 整条替换 = 比较并交换
self._drivers[driver_id] = replace(driver, status=DriverStatus.OFFERED, held_by=offer_id)

# credit-token-balance：作废额度包 = 把到期时间提前，重放时自然生效
self._commit(grants={**self._grants, grant_id: replace(grant, expires_at=at)})

# chat-room：编辑产生新版本，旧版本不被改写
edited = replace(message, text=new_text, edited_at=self._clock())
self._messages[message_id] = edited

# notification-service：重试是一个新信封，正在投递的那封不动
nxt = replace(envelope, attempt=envelope.attempt + 1)
heapq.heappush(self._delayed, (due, next(self._tick), nxt))
```

以上各题的代码是节选：省略了类型标注、文档字符串和 `...` 处的细节，个别行为讲解而合并成一行，不是逐字摘抄。

额度包的例子最特别：作废没有删除任何东西，只是把到期时间改小，扣费是按事件顺序重放算出来的，历史自然就对了。通知的例子说明为什么要新信封：旧信封可能还在另一个线程里被读取。

**见于。** inventory-management、ride-sharing、credit-token-balance、chat-room、notification-service。airline 的 `Booking` 是反例（见上一张卡）。

**信号。** 一个对象被存进容器后，别处还持有它的引用；或者「状态改了，之前拿到的结果也变了」的 bug。
