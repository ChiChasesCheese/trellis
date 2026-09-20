---
id: problems-restaurant-largest-remainder-method
node: problems.booking.restaurant
type: qa
step: 5
tags: [grown]
---
## Q
餐厅管理设计里，`split_by_share` 按份额拆账时，因为整数除法丢失的几分钱怎么分配给各个付款人，为什么不用浮点数按比例算再四舍五入？

## A
用最大余数法（largest remainder）：先算 `scaled = amount * shares[i]`，用整数除法 `scaled // total_shares` 得到每个人的基础份额，`scaled % total_shares` 作为“这个人因为取整损失了多少”的度量；再把损失得最多的人排在前面，把总金额减去所有基础份额之和剩下的那几分钱，按这个顺序逐分补给他们。全程只有整数除法和取模，不出现浮点数——这保证了同样的输入永远得到同样的输出，不会因为浮点误差在不同机器或不同次运行之间给出不一致的结果。
