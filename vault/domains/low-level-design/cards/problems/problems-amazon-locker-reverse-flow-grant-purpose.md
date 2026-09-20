---
id: problems-amazon-locker-reverse-flow-grant-purpose
node: problems.machines.amazon-locker
type: qa
step: 8
tags: [grown]
---
## Q
快递柜（Amazon Locker）要加「退货投柜」（顾客投件、快递员来收）这条反向流程，怎么加才算证明了设计可扩展？

## A
不新开一套服务，而是承认：正反两个方向唯一的差别是**这个码允许做什么**。加一个两成员的枚举即可：

```python
class GrantPurpose(Enum):
    COLLECT = "collect"     # 开门，把东西拿走
    DROP_OFF = "drop_off"   # 开门，把东西放进去
```

反向流程于是是：`reserve_return` 分配柜格并置为 `RESERVED`（离开可用池但里面是空的），签发 `DROP_OFF` 码给顾客；顾客 `drop_off` 用掉它把退货放进去，系统随即签发 `COLLECT` 码给快递员。

证据形态是能指着 diff 说哪几块没动：分配、码表、限流、过期扫描全部复用，一行没改。过期扫描甚至不需要知道两种流程的区别——释放柜格时拿到 `None` 就说明这是一个没人来投的预留，没有包裹要标记退回。新增的只有一个枚举成员、一个柜格状态成员和两个方法。
