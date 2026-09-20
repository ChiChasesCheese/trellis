---
id: problems-parking-lot-size-as-ordinal
node: problems.machines.parking-lot
type: qa
step: 2
tags: [grown]
---
## Q
停车场设计里判断“某个车位能不能停下某辆车”，为什么用一个可比较的尺寸等级（比如 `IntEnum`：摩托车 < 小车 < 大车）比给每种车型建一个继承 `Vehicle` 的子类（`Car`、`Motorcycle`、`Truck`）更好？

## A
车位能不能装下一辆车，本质是“车位尺寸是否不小于车辆尺寸”这一个数值比较，`spot.size >= vehicle.size` 一行就够。继承树是 Java 题解里的常见写法，但如果各车型之间除了“占地大小不同”没有任何行为差异，为每种车型建一个子类只是多一层查找成本，不会带来任何多态收益；新增一种车型（比如加一档“大巴”）只需要在尺寸标尺上加一个更大的值，不需要新建类、也不用碰任何分配或计费代码。
