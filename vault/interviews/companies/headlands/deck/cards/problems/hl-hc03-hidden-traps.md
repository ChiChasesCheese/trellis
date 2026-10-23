---
id: hl-hc03-hidden-traps
node: problems.hc03-recursive-sum
type: qa
step: 18
---
## Q
递归求和题的常见误区和隐藏测试会打的坑有哪些？

## A
1. `catch (StackOverflowError e) { return 0; }`：把「栈不够」伪装成合法答案；
2. `n*(n+1)/2` 当成正确的 O(1) 解：n 到 40 亿量级静默出负数；
3. 中间量溢出就报 `Overflow`：`MIN..MAX` 的和是 `Long.MIN_VALUE`，装得下；要 BigInteger 复核；
4. 区间 `a > b` 返回 0 还是抛异常：约定要明确（这里抛 `IllegalArgumentException`），面试先问清楚；`a == b`；`a` 为负数时套用 `n*(n+1)/2`；
5. 并行每块各自 `addExact` 再合并；`threshold` 写 0 造成无限递归；块数 > 元素数时 `from > to`；
6. 「虚拟线程是更快的线程，到处用」；虚拟线程版里吞掉 `InterruptedException`；
7. 「trampoline 能让程序变快」：不能，每步多一次堆分配；
8. 只在小 n 上测，从没碰过 `StackOverflowError`；
9. 浮点：`double` 加法不满足结合律，`(a+b)+c ≠ a+(b+c)`，并行结果与切块有关；Kahan / 成对求和降低误差但不消除顺序依赖。求平方和 `n(n+1)(2n+1)/6` 需要先除 2 再除 3，数值顺序同样重要。
10. 把 `StackOverflowError` 当可恢复的业务错误。
