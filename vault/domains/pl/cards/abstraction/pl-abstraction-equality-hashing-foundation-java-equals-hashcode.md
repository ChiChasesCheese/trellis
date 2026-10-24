---
id: pl-abstraction-equality-hashing-foundation-java-equals-hashcode
node: abstraction.equality-hashing
type: qa
step: 2
---
## Q
Java 的 `==`、`equals` 和 `hashCode` 各自管什么？`Integer` 缓存是怎么让 `==` 时对时错的？

## A
- `==` 对基本类型比较值，对**引用**比较同一性（是不是同一个对象）。
- `equals(Object)` 比较内容，默认实现等同于 `==`，需要自己重写。
- `hashCode()` 返回哈希值，**重写 `equals` 就必须同时重写它**，保持「相等的对象哈希相同」。

忘了其一，`HashSet`/`HashMap` 就会出错。`record` 自动生成基于所有字段的 `equals` 和 `hashCode`，是推荐的做法。

装箱类型的 `==` 是同一性比较，但 `Integer` 对 −128 到 127 做了缓存，同一个值会复用同一个对象：

```java
Integer x = 127, y = 127, p = 128, q = 128;
(x == y)       // true：缓存范围内，同一个对象
(p == q)       // false：128 在缓存外，是两个对象
p.equals(q)    // true
```

结果是「小数字的 `==` 碰巧正确，大数字就错」，测试里用小数据通过，线上出现。规则很简单：比较装箱类型，一律用 `equals`（或先拆箱）。

字符串同理：字面量会被放进常量池，`"a" == "a"` 为 `true`，但 `new String("a") == "a"` 为 `false`。所以 Java 里对象的比较默认写 `equals`，把 `==` 留给基本类型和枚举。
