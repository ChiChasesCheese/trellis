---
id: hl-cache-aos-soa-def
node: foundations.cpu-cache-locality
type: qa
step: 18
---
## Q
AoS（Array of Structs）和 SoA（Struct of Arrays）是什么？用订单（`id`、`price`、`qty`、`buy`）写出两种 Java 布局。

## A
- **AoS 结构体数组**：对象数组，每个对象带所有字段，Java 默认做法。
- **SoA 数组的结构体**：每个字段一个原始类型数组，同一下标对应同一条记录。

```java
final class Order { long id; long price; int qty; boolean buy; }  // AoS

final class OrderColumns {                                         // SoA
    final long[] id;  final long[] price;
    final int[] qty;  final boolean[] buy;
    OrderColumns(int cap) {
        id = new long[cap]; price = new long[cap];
        qty = new int[cap]; buy = new boolean[cap];
    }
}
```
AoS 的 `Order[]` 存的是引用，每个订单约 40 字节且是独立对象；SoA 的 `price[]`、`qty[]` 各自连续。
