---
id: method-final-twenty-minutes
node: method.delivery
type: qa
---
## Q
20 minutes left. Two features are half-written and nothing has been run end-to-end yet. What is the order of operations?

## A
1. **Freeze scope immediately** — no new feature enters the file after this point.
2. **Delete or stub the half-written branches.** Code that doesn't compile costs more than a missing feature; a one-line `throw new UnsupportedOperationException("out of scope")` reads as a decision.
3. **Get it running** (~8 min): compile, wire dependencies by hand in `main`, fix crashes.
4. **Demo driver** (~7 min): happy path + one edge case, printed output.
5. **Narrate** (~5 min): what's in, what's stubbed, where each stub plugs in.

Half-finished code scores as broken code; a stub scores as scoping.


## Q zh
20 分钟剩下。两个特性半写入，还没有什么端到端运行过。操作顺序是什么?

## A zh
1. **立即冻结范围** — 这个点之后没有新特性进入文件。
2. **删除或存根半写入的分支。** 不编译的代码花费比缺失特性更多；一行 `throw new UnsupportedOperationException("out of scope")` 读作一个决定。
3. **让它运行**(~8 分钟): 编译、在 `main` 中手工连接依赖、修复崩溃。
4. **演示驱动**(~7 分钟): 快乐路径 + 一个边界情况，打印的输出。
5. **讲述**(~5 分钟): 什么在里面，什么存根了，每个存根插入的地方。

半完成的代码作为破碎代码得分；存根作为范围得分。
