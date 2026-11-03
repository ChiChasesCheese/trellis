---
id: craft-transition-table-state-machine-5-scales-optimistic-cas
node: craft.patterns.transition-table-state-machine
type: qa
step: 5
---
## Q
**转移表状态机 · 并发请求下怎样防止非法转移**｜模式

订单在数据库里。请求 A 要把 PAID 订单发货，请求 B 要把同一个订单取消，两个请求都读到了 PAID，且都通过了内存里的转移表检查。怎么保证只有一个成功？

## A
**要点。** 表只能挡「流程上不合法」，挡不住并发读到同一旧状态。做法是让写入带上旧状态：`UPDATE ... SET status=新 WHERE id=? AND status=旧`，影响行数为 0 说明状态已经被别人改了。这是比较并交换（CAS），也叫乐观锁。

```python
db = sqlite3.connect(":memory:")
db.execute("CREATE TABLE orders (id INTEGER PRIMARY KEY, status TEXT)")
db.execute("INSERT INTO orders VALUES (1, 'PAID')")

ALLOWED = {("PAID", "SHIPPED"), ("PAID", "CANCELLED")}

def move(order_id: int, frm: str, to: str) -> bool:
    assert (frm, to) in ALLOWED                   # 转移表
    cur = db.execute("UPDATE orders SET status=? WHERE id=? AND status=?", (to, order_id, frm))
    return cur.rowcount == 1                      # 状态仍是 frm 才有人赢

# 两个并发请求都读到 PAID：一个要发货，一个要取消
print("发货:", move(1, "PAID", "SHIPPED"))
print("取消:", move(1, "PAID", "CANCELLED"))
print("最终状态:", db.execute("SELECT status FROM orders").fetchone()[0])
```

两个请求顺序提交，实际输出：

```
发货: True
取消: False
最终状态: SHIPPED
```

**尺度对照。** 一个对象：方法里查表、改状态，必要时加锁；一个服务：转移表在代码里，数据库的条件更新守住并发；跨服务的工作流：每次转移写一条事件（事件溯源），状态由事件重放得到，重复投递靠事件 ID 去重。

**代价。** 赢不了的请求要有处理：重读状态、重试，或返回「状态已变」。不能当成成功。

**信号。** 订单、支付、工单这类有生命周期的实体，且会有多个来源（用户、定时任务、回调）同时改它。
