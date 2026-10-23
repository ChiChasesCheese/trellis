---
id: hl-hc03-wide-accumulator
node: problems.hc03-recursive-sum
type: qa
step: 13
---
## Q
并行数组求和为什么不能每块 `addExact` 再合并？128 位累加器 `Wide(hi, lo)` 怎么解决，`plus` 怎么写？

## A
逐步 `addExact` 的结果**取决于求和顺序**：`[MAX, 1, -1]` 真实和是 `MAX`，装得下，但从左到右 `MAX + 1` 就抛；并行时块边界任意，同一份数据换个切法时而抛时而不抛（例：`MAX×2000 + MIN×2000` 每块内溢出，总和 −2000 装得下）。

**128 位累加器**不溢出，加法满足结合律，怎么切块、怎么合并都一样，最后只判一次「是否在 long 范围内」：
```java
public record Wide(long hi, long lo) {
    public Wide plus(long x) {
        long nlo = lo + x;
        long carry = Long.compareUnsigned(nlo, lo) < 0 ? 1 : 0;
        return new Wide(hi + (x >> 63) + carry, nlo);
    }
    public boolean fitsLong() { return hi == (lo >> 63); }
}
```
- `lo` 当无符号数相加，`nlo` 比 `lo` 小说明越过 2⁶⁴ 丢了进位，补到 `hi`；
- `x >> 63`：非负得 0，负得 −1，即 `x` 符号扩展到高 64 位；
- 装得下当且仅当高 64 位全等于低 64 位的符号位：`hi == (lo >> 63)`。

`sumChunk` 循环里用局部变量 `hi`、`lo`，不建 `Wide` 对象，否则 5000 万次分配压垮 GC。三种并行实现对同一输入必须与顺序 `checkedSum` 逐字相等（含 `Overflow.exact`）。C++ 可用 `__int128`，或两个 64 位拼接（`lo` 无符号回绕则给 `hi` 进位）。
