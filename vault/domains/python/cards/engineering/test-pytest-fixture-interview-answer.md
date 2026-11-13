---
id: test-pytest-fixture-interview-answer
node: engineering.testing
type: qa
---
## Q
面试里被问「你在 pytest 里怎么组织 fixture？」，怎么用 1 分钟答出层次？

## A
按下面的顺序说，每点一两句：

1. **它解决什么：** fixture 把测试的前置状态和清理从测试体里拿出来，按名字注入；`yield` 前准备、后清理，测试失败也会清理，清理顺序后进先出。
2. **作用域按成本选：** 贵的资源（被测服务进程、数据库容器、一块共享的测试硬件）用 `session` 或 `module`，便宜且会被改的状态用 `function`；再用一个函数级 fixture 把共享资源的状态重置，防止测试互相污染。
3. **放在哪里：** 全局选项和 session 资源放根 `conftest.py`，某类测试专用的放子目录的 `conftest.py`，离测试越近的同名 fixture 优先。
4. **组合与工厂：** 小 fixture 互相依赖拼起来；数量由测试决定时用工厂 fixture，统一记账、统一清理。
5. **克制 autouse：** 只给「每个测试都必须」的便宜动作用，比如固定随机种子；其余显式写进参数，读测试的人一眼能看到依赖。
6. **排查手段：** `pytest --fixtures` 看有哪些，`--setup-show` 看实际的建立和拆除顺序；并行跑（`pytest-xdist`）时记得 session fixture 是每个 worker 进程各建一次。
