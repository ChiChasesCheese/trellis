---
nodes: [problems.marketplaces.food-delivery]
url: https://github.com/ashishps1/awesome-low-level-design/blob/main/problems/food-delivery-service.md
---
# awesome-low-level-design — Designing an Online Food Delivery Service Like Swiggy

值得读：这是这道题最流行的免费题面，八条需求（浏览餐厅与菜单、餐厅自管菜单与可售状态、
骑手接单履约、订单跟踪、支付、并发一致性、实时通知）写得全，拿来核对自己的分关有没有漏项
很好用；六种语言（含 Python）并排给出同一份实体切法 `Customer` / `Restaurant` / `MenuItem` /
`Order` / `OrderItem` / `OrderStatus` / `DeliveryAgent` / `FoodDeliveryService`。三处根本分歧：
它的服务类用单例；它的 `OrderStatus` 只是订单上的一个枚举字段、`updateOrderStatus` 谁都能调，
**完全没有"哪一方有权做这次转移"的概念**——而三方系统的全部难点正在这里；它的
`assignDeliveryAgent` 在下单后立刻指派，既没有"等餐厅接单"这道闸，也没有出餐时间估计，
于是"什么时候派骑手"这个真正的取舍题在它那里根本不存在。它的菜单可售状态是 `MenuItem` 上的
一个布尔字段，本题解把它移到餐厅上，并要求校验与抄价在餐厅的锁里一次完成。
