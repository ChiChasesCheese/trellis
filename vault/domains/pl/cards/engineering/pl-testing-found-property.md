---
id: pl-testing-found-property
node: engineering.testing
type: qa
step: 5
---
## Q
属性测试（property-based testing）靠什么机制工作？Rust 的 proptest 怎样找到「二分查找中点」的整数溢出？

## A
**三个部件**：
1. **生成器**（generator，也叫 strategy）：随机产生输入；
2. **属性**：对每个输入都应成立的断言，如「解码(编码(x)) 等于 x」「排序结果有序且是原数据的排列」；
3. **缩小**（shrinking）：发现失败后，框架反复把输入变简单（数变小、列表变短、字符串变短）并重跑，直到找到仍然失败的最小输入。

随机性提供覆盖面，缩小提供可读的反例。

**例**：`mid(lo, hi)` 用 `lo.wrapping_add(hi) / 2`（经典的中点溢出 bug，这里显式写出来）。性质：当 `lo <= hi` 时结果必须落在两者之间。

```rust
proptest! { #[test]
fn mid_is_between(lo in any::<i32>(), hi in any::<i32>()) {
    prop_assume!(lo <= hi);
    let m = mid(lo, hi);
    prop_assert!(lo <= m && m <= hi);
}}
```

`cargo test` 的真实输出：

```text
minimal failing input: lo = 676256113, hi = 1471227535
```

两数之和是 2147483648，刚越过 `i32` 上限而回绕成负数。人写的示例测试 `mid(2, 8) == 5` 永远发现不了。

**别的语言**：Python 有 Hypothesis，Java 有 jqwik，Go 的标准库 `testing/quick` 已冻结、功能有限，社区常用 `rapid`。

**该找什么性质**：往返（编码再解码）、幂等（做两次与做一次相同）、不变量（排序后长度不变）、与简单慢速实现对拍（用朴素算法当参照）。
