---
id: hl-javaq-e-q18-printcompilation
node: java-questions.e-jit-gc
type: qa
step: 3
---
## Q
怎么读 `-XX:+PrintCompilation` 的输出？`%` 标记和第四列数字（层级）分别表示什么？

## A
示例：
```
19  133 %     3  K10Jit::run @ 4 (34 bytes)
19  134       3  K10Jit::run (34 bytes)
20  143 %     4  K10Jit::run @ 4 (34 bytes)
21  167       4  K10Jit::run (34 bytes)
```
- `%` 表示 **OSR 编译**，`@ 4` 是循环入口的字节码位置。
- 层级列：**3** = C1 带完整 profiling，**4** = C2。
- 所以：第 1 行是 tier3 的 OSR，第 2 行是 tier3 的正常入口，第 3 行是 tier4（C2）的 OSR，第 4 行是正常入口的 C2 版本。
- 其他观察手段：`-XX:+UnlockDiagnosticVMOptions -XX:+PrintInlining`、`jcmd <pid> Compiler.codecache`、JFR 的编译事件。
