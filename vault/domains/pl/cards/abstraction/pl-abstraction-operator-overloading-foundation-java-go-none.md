---
id: pl-abstraction-operator-overloading-foundation-java-go-none
node: abstraction.operator-overloading
type: qa
step: 4
---
## Q
Java 和 Go 不支持运算符重载，用大数运算时代码长什么样？为什么这是有意的设计？

## A
Java 的 `BigDecimal` 做 `(0.1 + 0.2) * 3` 只能这样写：

```java
BigDecimal x = new BigDecimal("0.1"), y = new BigDecimal("0.2");
x.add(y).multiply(new BigDecimal("3"));      // 0.9
```

表达式一长，嵌套的方法调用就读不出运算优先级。Go 的 `math/big` 也同样，而且还要显式指定接收结果的变量（`z.Add(x, y)`）。

这是**有意的**。Java 的设计者认为运算符重载在 C++ 里被滥用，让代码难读（`<<` 既是移位又是输出，`+` 可以做任何事），所以只保留一个例外：**字符串的 `+` 由编译器内置**。它的规则也有坑：

```java
"a" + 1 + 2 + 'c'    // "a12c"：从左到右，一旦有字符串就全是拼接
```

Go 官方 FAQ 的说法是：不需要做类型匹配，分派就保持简单；运算符重载更像是便利而不是必需，去掉它语言也更简单。结果是 Go 里的 `+` 永远是整数、浮点或字符串拼接，读者无需查定义就知道代价。

取舍很清楚：Java 和 Go 牺牲了数学、图形、金融等领域的代码的简洁性，换来「看到 `+` 就知道它很便宜」的可预测性。这对做业务系统的团队是好交易，对做数值计算的团队就不是，这也是 Python 和 Rust 在科学计算里占优的原因之一。
