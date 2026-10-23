---
id: hl-j13-catch-too-wide
node: java21.j13-unnamed-variables
type: qa
step: 14
---
## Q
为什么 `catch (Exception _) { }` 通常不可取，而 `catch (StackOverflowError _)` 可以接受？

## A
`catch (Exception _) { }` 把所有异常（包括 bug）吞掉，还不留痕迹，连变量名都没有，无法加日志去看它。

只对**特定的、预期的**异常用 `_`，并在注释说明为什么安全。例如测递归深度的代码里 `catch (StackOverflowError _)` 是有意吞掉的：栈溢出是预期事件，深度已记在 `probe.depth`；又如 `catch (InterruptedException _)` 表示「收到关闭信号，不需要处理」。
