---
id: problems-airline-denied-boarding-rule
node: problems.booking.airline
type: qa
step: 6
tags: [grown]
---
## Q
航班管理设计里，超售导致某个舱位登机时人数超过实际座位数，`board()` 按什么规则决定拒载谁？

## A
逐舱结算，舱与舱之间不互相挤占；超出实际座位数的那部分里，先拒载“值机时没拿到座位号”的旅客，如果没拿到座位号的人数还不够，再按“值机时间越晚越先被拒”的顺序补足。被拒载的订单退回 TICKETED 状态而不是取消——票还在手上，等待客服改签，这正是超售这项政策的真实代价兑现的地方。
