---
id: principles-unwinding-wrong-abstraction
node: principles.simplicity
type: qa
---
## Q
A shared helper now takes `(input, boolean isLegacy, Mode mode)` and branches on them; the fourth caller needs a fifth flag. What's the prescribed fix, and why isn't it "add the flag"?

## A
The flags are the abstraction telling you the callers don't actually share behavior. Adding another compounds it — every caller pays for paths it never takes, and every change risks all four.

Prescription (Sandi Metz's "unwinding"):
1. **Re-inline** the helper back into each caller, flags resolved to constants.
2. Delete the branches each caller can't reach — now you can see what is genuinely common.
3. Re-extract only that, along the real seam, if anything is left.

Rule to state: **a boolean parameter that selects behavior is a merged-too-early signal**, and sunk cost in the existing helper is not a reason to keep it.

## Q zh
当你意识到一个抽象是错误的，为什么解开它而不是改进它？

## A zh
当一个抽象错误时，尝试改进它通常会导致更多的复杂性。更好的方法：

1. 复制代码回到每个调用者（是的，重新引入重复）
2. 现在在隔离的上下文中优化每个版本
3. 一旦它们稳定并且真正的模式出现，提取正确的抽象

这违反了 DRY，但：
- 一个坏的抽象比重复更糟
- 重复暴露了真正的差异
- 改进一个坏的抽象很难；更好地开始就是正确的

这来自 Sandi Metz 的 "All the Little Things" 演讲。
