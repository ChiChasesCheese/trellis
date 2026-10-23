---
id: hl-javaq-e-q21-log
node: java-questions.e-jit-gc
type: qa
step: 13
---
## Q
程序先只用 `Sq`，然后第一次出现 `Tri`，再出现 `Cir`。`-XX:+PrintCompilation` 的日志会怎样演变？如何解读 `made not entrant`？

## A
```
21  167  4  K10Jit::run (34 bytes)
61  174  3  K10Jit$Tri::area (6 bytes)
61  143 % 4  K10Jit::run @ 4 (34 bytes)  made not entrant
79  182  3  K10Jit::run (34 bytes)
114 175 % 4  K10Jit::run @ 4 (34 bytes)  made not entrant
115 189  4  K10Jit::run (34 bytes)
```
- 先有只见过 `Sq` 的 C2 版本；`Tri` 第一次被用到时，旧的投机版本被标 `made not entrant`（不再被新调用进入）。
- 随后回到 tier 3 重新 profile；`Cir` 出现再作废一次。
- 最终得到 3 种类型的 megamorphic 新 C2 版本。
- 每次出现新实现类，之前依据"只有 1 / 2 个实现"编译的方法都被作废并重编译；代价是这几十毫秒在慢路径上跑加编译开销。
