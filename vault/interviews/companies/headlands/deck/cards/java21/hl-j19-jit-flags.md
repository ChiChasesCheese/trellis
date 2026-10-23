---
id: hl-j19-jit-flags
node: java21.j19-runtime-zgc-jit
type: qa
step: 12
---
## Q
观察和控制 JIT 的常用 JVM 参数有哪些（`PrintCompilation`、`PrintInlining`、`TieredStopAtLevel`、`-Xint`、`DoEscapeAnalysis`）？

## A
```
-XX:+PrintCompilation                                  # 每个方法被编译时一行
-XX:+UnlockDiagnosticVMOptions -XX:+PrintInlining      # 内联决策（需要诊断选项）
-XX:TieredStopAtLevel=1                                # 只用 C1
-Xint                                                  # 只解释执行，关闭 JIT（调试用）
-XX:-DoEscapeAnalysis                                  # 关掉逃逸分析（做对照实验用）
```
`PrintInlining` 必须同时带 `-XX:+UnlockDiagnosticVMOptions`。
