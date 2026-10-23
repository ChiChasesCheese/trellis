---
id: hft-java-object-layout-pointer-chase
node: java.object-layout
type: qa
step: 5
---
## Q
订单簿用 `TreeMap<Long, List<Order>>` 实现，为什么在热路径上会有看不见的延迟代价？

## A
从价格查到一个订单，要依次经过：`TreeMap` 的节点对象、`Long` 键对象、`List` 对象、它内部的数组、最后才是 `Order` 对象，每一步都是一次指针跳转，每一跳都可能 cache miss。一次主存访问约 100 ns，跳 5 次就是约 500 ns，还没算任何业务逻辑，而整笔订单的延迟预算可能只有几微秒。同时每次插入还会创建节点和装箱的 `Long`，产生垃圾。

对比：价格在有界范围内时，把价格按 tick 换算成 `long[]` 的下标，一次内存访问就能到价位，布局连续、不产生垃圾。这是“机械同理心”（mechanical sympathy，按硬件的工作方式写代码）的典型例子。
