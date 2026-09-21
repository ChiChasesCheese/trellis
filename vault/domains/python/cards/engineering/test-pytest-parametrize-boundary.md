---
id: test-pytest-parametrize-boundary
node: engineering.testing
type: qa
tags: [grown]
---
## Q
`@pytest.mark.parametrize` 的作用是什么？为什么它比为每个边界值单独写一个测试函数更适合覆盖边界条件？

## A
`parametrize` 用一组输入-期望输出对来驱动同一个测试函数体，pytest 会把每一组参数当成一个独立的测试用例运行、独立报告通过或失败。相比复制同一段断言逻辑给每个边界值各写一个函数，`parametrize` 把「测试逻辑」和「测试数据」分离：新增一个边界情形（比如空输入、负数、恰好等于上限）只需要在参数列表里加一行，不必重复整段测试代码，也让失败报告直接指出是哪一组具体输入触发的。
