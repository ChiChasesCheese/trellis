---
id: hl-hc07-codec-pack
node: problems.hc07-ticker-hash-map
type: qa
step: 9
---
## Q
股票代码怎么打包进一个 `long`？5 比特编码规则、`"AAPL"` 的值、为什么合法 key 恒 > 0，好处是什么？

## A
`'A'..'Z'` → `1..26`，每个字符 **5 比特**（2⁵=32 ≥ 27，0 留给「没有字符」）；第 i 个字符（i 从 0 起）放在比特 `[35−5i, 39−5i]`；不足 8 个字符尾部补 0。结果总是 `> 0` 且 `< 2⁴⁰`。

`"AAPL"`：A=1、A=1、P=16、L=12，值 `(1<<35) | (1<<30) | (16<<25) | (12<<20)` = 35,982,934,016 = `0x860C00000`。`"AB"` = `(1<<35) | (2<<30)` = `0x880000000`。

```java
key |= (long) (c - 'A' + 1) << (5 * (7 - i));    // 必须先转 long
```
**坑**：`(c - 'A' + 1) << 35` 不转 `long` 时 `int` 移位量取模 32，`<< 35` 实际是 `<< 3`（`ABCDEFGH` 会暴露）。C++ 里把 `int` 左移 ≥ 32 位是 UB，先转 `uint64_t`。

好处：不同代码得不同 long（单射）；合法代码 > 0，所以 **0 可当「空格」、−1 当墓碑**，无需状态数组；比较两个代码 = 比较两个 long，不用 `equals`、不分配。取字段：`(x >>> 20) & 0x1F`。

`parse(CharSequence)` 返回 sealed `Parsed permits Ticker(long key), Invalid(String reason)`；null / 空 / 超过 8 个 / 含非 A–Z → `Invalid`。`pack` 非法时抛 `IllegalArgumentException`：
```java
return switch (parse(s)) {
    case Ticker(var key) -> key;
    case Invalid(var reason) -> throw new IllegalArgumentException(reason);
};
```
为什么用值而不是异常：行情流里非法输入是常态，值不需抓栈，调用者被迫处理两种情况；失败罕见时异常更简洁。`unpack` 对非法 key（≤ 0、≥ 2⁴⁰、字段 > 26、第一个 0 字段之后又有字符）抛 `IllegalArgumentException`。
