---
id: pl-binding-evaluation-order-foundation-java
node: binding.evaluation-order
type: qa
step: 2
---
## Q
Java 语言规范对求值顺序做了哪些保证？`i = i++ + i++` 和 `x += (x = 1)` 的结果能不能推演出来？

## A
Java 的规则很严：

1. **操作数从左到右**求值，而且**先于运算本身**。
2. 方法调用的实参从左到右。
3. 复合赋值 `x += e`：先把左边 `x` 的**当前值保存下来**，再算右边 `e`，最后相加。
4. 数组元素赋值 `a[i] = e`：先算数组引用和下标，再算右边。

所以结果可以逐步推演，在任何 JVM 上都一样：

```java
static int t(String s, int v) { System.out.print(s + " "); return v; }
int r = t("a", 1) + t("b", 2) * t("c", 3);   // prints: a b c   r = 7
```

输出 `a b c`：操作数按书写顺序求值，虽然 `*` 的优先级更高，但优先级只决定「怎样结合」，不决定「谁先算」。

```java
int i = 1;
i = i++ + i++;        // 1 + 2 = 3, then the assignment overwrites i
int x = 10;
x += (x = 1);         // saved left x = 10, plus 1 = 11
```

`i = i++ + i++`：第一个 `i++` 取值 1 并把 `i` 变成 2，第二个取值 2 并把 `i` 变成 3，和为 3，最后赋值把 `i` 设为 3，输出 `3`。`x += (x = 1)` 的结果是 `11`，因为保存下来的是旧值 10。

这种可推演性是 Java「一次编写，到处运行」的组成部分：如果顺序因 JVM 实现而异，同一个 `.class` 文件在不同平台的行为就不同。代价是编译器和 JIT 在存在副作用时不能随意重排，但 JIT 可以在能证明无依赖时照样重排，因为可观察的行为不变。

注意：能推演不代表该这样写。`i = i++ + i++` 是面试题，不是工程写法。
