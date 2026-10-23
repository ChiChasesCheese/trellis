---
id: hl-j01-canonical-ctor
node: java21.j01-record
type: qa
step: 9
---
## Q
`record` 的规范构造器（canonical constructor）是什么？不写时编译器生成什么？要在赋值前校验该怎么写显式版本？

## A
规范构造器：**参数列表与组件完全一致**的构造器。不写则编译器生成，内容就是把每个参数赋给同名字段。

显式写法（啰嗦，要自己写所有赋值）：
```java
record Order(long id, long qty) {
    Order(long id, long qty) {
        if (qty <= 0) throw new IllegalArgumentException("qty");
        this.id = id;
        this.qty = qty;
    }
}
```
更推荐用紧凑构造器，见下一张卡。
