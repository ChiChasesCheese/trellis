---
id: pl-sig-gotchas-intro-java
node: signatures.gotchas
type: qa
step: 3
---
## Q
Java 最值得认识的经典陷阱有哪些：`Integer` 缓存与 `==`、字符串比较、`remove` 重载、整数溢出？每个的真实输出和根源是什么？

## A
**1. `Integer` 的 `==`**。基本类型 `int` 与装箱类型 `Integer` 并存。`Integer` 的 `==` 比较的是**引用**，而 JVM 缓存了 -128 到 127 的 `Integer` 对象：

```java
Integer x = 127, y = 127, p = 128, q = 128;
(x == y) + " " + (p == q) + " " + p.equals(q)     // true false true
```

真实输出 `true false true`：127 相等，128 不相等。根源：装箱对象是引用类型。修法：对象比较用 `equals`，数值计算用 `int`。

**2. 字符串的 `==`**。`new String("hi") == "hi"` 为 `false`，`equals` 为 `true`，`intern()` 后又为 `true`（真实输出 `false true true`）。字面量在常量池里共享，`new` 创建新对象。修法：永远用 `equals`。

**3. `List.remove` 的重载**。`remove(int index)` 与 `remove(Object o)` 两个重载，对 `List<Integer>`：

```java
l.remove(Integer.valueOf(1));   // removes the value 1
l.remove(1);                    // removes the element at index 1
```

从 `[1,2,3]` 依次执行，结果是 `[2]`。传 `int` 时选 `remove(int)`，容易误删。

**4. 整数溢出静默回绕**。`Integer.MAX_VALUE + 1` 得到 `-2147483648`；`Math.abs(Integer.MIN_VALUE)` 仍是负数；`long big = Integer.MAX_VALUE + 1` 先在 `int` 里溢出再提升（真实输出 `-2147483648`）。修法：`Math.addExact` 等会抛异常的方法，或先转 `long`。

**5. 字符串拼接与加法**：`1 + 2 + "x" + 1 + 2` 得到 `3x12`（真实输出），按从左到右求值。

**6. `Arrays.asList(int[])`**：传基本类型数组得到只含一个元素的 `List<int[]>`，`size()` 为 1。

**7. `map.get(1L)` 取不到键 `1`**：`Long` 与 `Integer` 的 `equals` 不相等，返回 `null`。

**共同点**：都能编译、静默出错。根源是 Java 保留的历史设计：基本类型与对象并存、重载解析、隐式的数值提升。防线是 Error Prone、SpotBugs、IDE 检查和代码评审。
