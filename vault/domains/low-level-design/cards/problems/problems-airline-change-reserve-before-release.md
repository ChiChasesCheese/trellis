---
id: problems-airline-change-reserve-before-release
node: problems.booking.airline
type: qa
step: 7
tags: [grown]
---
## Q
航班管理设计里，改签（`change`）为什么不写成字面意义上的“先取消旧行程、再订新行程”两步？

## A
字面上的“先取消再重订”会让旅客在两步之间有一瞬间没有任何有效订单，而且如果重订失败，旅客连老票都没了；更微妙的是，新旧行程共用的那一段（比如中转第一段没变）会被无意义地放掉又重新抢占，已经选好的座位号白白丢失。正确的做法是先占新行程的全部航段——`reserve_across` 发现某段已经属于同一个订单会直接跳过、不动座位——再释放旧行程里不再需要的那部分，全程旅客手里始终有一张有效的票。
