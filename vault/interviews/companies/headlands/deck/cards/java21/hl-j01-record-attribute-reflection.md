---
id: hl-j01-record-attribute-reflection
node: java21.j01-record
type: qa
step: 18
---
## Q
`record` 编译后的 class 文件里，哪个属性登记了组件？反射里用哪两个方法读取？

## A
class 文件多了一个 **`Record` 属性**，登记每个组件的名字和类型。

反射读取：
```java
Fill.class.isRecord();               // true
Fill.class.getRecordComponents();    // 各组件：symbol、priceTicks、qty 的名字与类型
```
例如一个四组件的 record 得到 `[String symbol, Side side, long priceTicks, long qty]`。

这也是序列化库、框架识别 record 的依据。
