---
id: hl-j13-pattern-variable
node: java21.j13-unnamed-variables
type: qa
step: 6
---
## Q
什么是未命名模式变量（unnamed pattern variable）？在 `switch` 和 `instanceof` 里怎么写？

## A
类型模式里不绑定变量：

```java
case Fill _ -> "FILL";            // 等价于 case Fill f -> ...，但不引入变量 f
if (o instanceof Fill _) { ... }  // 只判断类型
```
适用于「只需要知道是什么类型，不需要用这个对象」的场景。`sealed` 穷尽性照常检查。
