---
id: structure-api-rich-return-contract
node: structure.api
type: qa
---
## Q
停车场轮次: 你可以签 `park(Vehicle)` 作为返回 `boolean` 或返回一个 `Ticket`。面试官会在 20 分钟内添加"在出口计算费用"。哪个合约存活，为什么?

## A
`Ticket park(Vehicle)` 存活。**丰富的返回对象**携带进入时间、位置和车辆 — `unpark(Ticket)` 能计算费用、找到位置、验证，全部不改变任何签名。`boolean` 版本为每一个新需求强制打破改变并给调用者没有什么返回。

通用规则: 返回一个**命名交互的域对象**（Ticket、Booking、Receipt），不是一个赤裸的成功标志。新需求然后着陆作为新**字段**，不是新**签名**。
