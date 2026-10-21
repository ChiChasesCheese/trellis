---
id: amz-configurable-cache-bridge-vs-subclass-explosion
node: amazon.amz-configurable-cache
type: qa
step: 5
tags: [grown]
---
## Q
在可配置缓存里，淘汰策略和存储后端两条轴怎么组合？为什么不写成 `LruMemoryCache`、`LfuFileCache` 这样的子类？

## A
两种做法：(1) 子类组合：2 种策略 x 2 种后端要写 4 个类，每多一种后端再多 2 个，策略的 bug 要在每个组合里各修一遍；(2) 组合（桥接 Bridge）：`Cache` 持有一个策略和一个后端，只写 2+2 个小类，新增后端只加 1 个类。选 (2)：两个维度互相独立变化，就该用持有关系而不是继承。策略只有一个方法族、不带状态时才能写成函数；LRU/LFU 带状态，所以写成类。
