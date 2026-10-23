---
id: hl-oa01-overflow-addexact
node: problems.oa01-job-chain
type: qa
step: 8
---
## Q
累加 job 时长为什么要用 `long` 加 `Math.addExact`，而不是 `int` 直接相加？

## A
`int` 最大 2,147,483,647（约 21 亿），超过会**悄悄绕回负数**，不报错：

```java
int a = 2_000_000_000;
int b = a + a;            // -294967296
long c = (long) a + a;    // 4000000000
Math.addExact(a, a);      // 抛 ArithmeticException
```

两个各 20 亿秒的 job 用 `int` 累加就会变负数，是隐藏用例常考的边界。所以时长字段用 `long`（最大约 9.2 × 10^18），累加用 `Math.addExact`：万一 `long` 也溢出，至少抛异常，而不是静默给出错答案。

同理 record 里 `id` 用 `int`（题面是正整数，还要做 map 键），时长必须 `long`，因为它要被累加。
