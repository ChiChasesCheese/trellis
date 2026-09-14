---
id: variant-object-is-map-not-oop
node: semistructured.variant-type-storage
type: qa
source: snowflake-docs
---
## Q
Snowflake 的 OBJECT 类型与面向对象编程里的「对象」是一回事吗？要存「灾害类型 → 发生日期列表」这种数据，内部的类型结构长什么样？

## A
不是。Snowflake 的 OBJECT 相当于字典（dictionary）或映射（map），就是一组键值对，没有方法或类。存「灾害类型 → 日期列表」时，外层是 OBJECT，键为 `Hurricane`、`Flood` 等；因为 OBJECT 中的值必须是 VARIANT，每个日期数组实际是「包在 VARIANT 里的 ARRAY」，再作为对应键的值放进 OBJECT。
