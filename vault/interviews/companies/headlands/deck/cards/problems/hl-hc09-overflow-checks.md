---
id: hl-hc09-overflow-checks
node: problems.hc09-top-trades-by-notional
type: qa
step: 5
---
## Q
notional 的溢出怎么处理？为什么每个事件都要检查，`Trade` 的紧凑构造器为什么多乘一次？溢出边界的数是多少？

## A
`long` 范围约 ±9.2×10¹⁸。结果超出时 Java **不报错，悄悄绕回**：`Long.MAX_VALUE * 2 = -2`，天价成交排到最后——在金融系统静默给错答案比崩溃更危险。所以乘法用 `Math.multiplyExact`、累加用 `Math.addExact`，溢出抛 `ArithmeticException`（HotSpot 当内联函数，JIT 后通常是一条乘法加一次溢出检查，几乎无成本）。C++ 里有符号溢出是 UB，用 `__builtin_mul_overflow` 并抛 `std::overflow_error`；`int*int` 先溢出再转型。

**边界**：`Long.MAX_VALUE` 的平方根向下取整是 **3037000499**。`3037000499² = 9223372030926249001` 不溢出，`3037000500² = 9223372037000250000` 溢出。

**每一个事件**都经过同一个 `notionalAt(i)`：检查非空、非负，再 `multiplyExact`——包括进不了 top-k 的事件。因为「是否抛异常」不该依赖数据排列（只查进堆的，溢出事件会在快速拒绝那步被误算漏掉）。

**紧凑构造器**：
```java
public record Trade(int index, String ticker, long price, long volume) {
    public Trade {
        Objects.requireNonNull(ticker, "ticker");
        if (index < 0) throw new IllegalArgumentException(...);
        if (price < 0) throw new IllegalArgumentException(...);
        if (volume < 0) throw new IllegalArgumentException(...);
        Math.multiplyExact(price, volume);      // 丢弃结果，只为提前证明不溢出
    }
    public long notional() { return price * volume; }
}
```
「`Trade` 存在 ⇒ `notional()` 不溢出」，后面所有使用都不用再担心。

为什么不用 `double`：53 位尾数，大数丢精度，累加不满足结合律；`BigInteger` 每次运算分配对象，慢几十倍，只作检测到溢出后的慢路径。
