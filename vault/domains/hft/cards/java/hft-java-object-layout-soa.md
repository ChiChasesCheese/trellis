---
id: hft-java-object-layout-soa
node: java.object-layout
type: qa
step: 3
---
## Q
“数组的结构”（structure of arrays，SoA）相比“结构的数组”（array of structures，AoS）为什么对缓存更友好？各自适合什么场景？

## A
设有 100 万个订单，每个有价格、数量、时间等字段，现在只想求价格总和。
- **AoS**（对象数组）：每个订单 32 字节连在一起，读价格要把整条缓存行（64 字节）拉进来，却只用其中 8 字节，约 1/8 的带宽有用。
- **SoA**：把每个字段单独放一个数组，`long[] prices`、`int[] qtys`……求和只读 `prices` 这 8 MB 连续内存，每条缓存行 8 个有用值，预取也最顺。

反过来，如果每次总是同时用到同一订单的所有字段，AoS 反而更好，因为一次取一条缓存行就够了。SoA 的代价是一个订单的字段散在多个数组里，写起来麻烦。订单簿里按价格 tick 做下标的 `long[]` 就是这种思路。
