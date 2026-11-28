---
id: pl-out-java-objects-equals-hashcode
node: output.java-objects
type: qa
step: 3
---
## Q
**只改 equals**｜读代码说输出

```java
class P {
    int x;
    P(int x) { this.x = x; }
    public boolean equals(Object o) { return o instanceof P p && p.x == x; }
}
public class Main { public static void main(String[] a) {
    Set<P> set = new HashSet<>(List.of(new P(1)));
    System.out.println(new P(1).equals(new P(1)));
    System.out.println(set.contains(new P(1)));
    System.out.println(new ArrayList<>(set).contains(new P(1)));
} }
```

输出什么？

## A
**输出。**
```
true
false
true
```

**为什么。**
- `P` 重写了 `equals` 却没重写 `hashCode`，两个逻辑相等的对象继承 `Object.hashCode`，哈希码按对象身份算，几乎必然不同。
- `HashSet.contains` 先用哈希码定位桶（bucket），桶不对就不会调用 `equals`，所以 false。
- `ArrayList.contains` 逐个调 `equals`，不用哈希码，所以 true：同一个对象在不同集合里结果不同。

**语言为什么这样设计。**
- `Object` 的约定：`equals` 相等的对象 `hashCode` 必须相等；哈希集合靠它把查找从 O(n) 降到平均 O(1)。语言只写了约定，编译器不检查。
- Python 做得更强：只定义 `__eq__` 的类，`__hash__` 自动变成 None，放进 set 直接 TypeError；Java 的 `record` 会成对生成 `equals` 和 `hashCode`。

**怎么写才对。**
```java
public int hashCode() { return Integer.hashCode(x); }
// 或者直接写 record P(int x) {}
```

**面试里一句话。**
If you override equals you must override hashCode, because hash collections find the bucket by hash before they call equals.
