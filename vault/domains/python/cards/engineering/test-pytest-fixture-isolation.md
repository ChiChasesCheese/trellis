---
id: test-pytest-fixture-isolation
node: engineering.testing
type: qa
tags: [grown]
---
## Q
pytest 里的 fixture（夹具）解决了什么问题？为什么比在每个测试函数开头手写「创建资源 → 测试 → 清理资源」的样板代码更好？

## A
fixture 把「测试需要的前置状态」（如数据库连接、临时目录、构造好的对象）单独定义成一个函数，用 `@pytest.fixture` 声明，测试函数把它的名字作为参数声明依赖即可自动注入；fixture 内部用 `yield` 分隔「准备」和「清理」两部分，pytest 保证测试结束（包括测试失败）后一定执行清理。这样多个测试可以复用同一份初始化逻辑而不必复制粘贴，也不会因为某个测试忘记清理而污染后续测试的状态。
