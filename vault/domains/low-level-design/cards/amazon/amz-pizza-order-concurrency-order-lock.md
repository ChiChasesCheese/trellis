---
id: amz-pizza-order-concurrency-order-lock
node: amazon.amz-pizza-order
type: qa
step: 8
tags: [grown]
---
## Q
在披萨订单里，多个线程同时往同一张订单加披萨、同时算价，什么会出错？怎么保证？

## A
出错的是合并数量的读–改–写：两个线程都读到旧数量 1，各自写回 2，丢了一份。GIL 只保证单个字节码原子，`get` 和写回之间可以切换线程。

办法：`Order` 用一把 `Lock` 包住读–改–写，`lines` 在锁内复制成元组再返回；`PriceEngine` 只含不可变元组，`price` 是纯函数，可以共享，不用锁。

```python
def add(self, pizza, qty=1):
    with self._lock:
        self._lines[pizza] = self._lines.get(pizza, 0) + qty
```
结算时先取一次 `order.lines` 快照，之后只用快照。
