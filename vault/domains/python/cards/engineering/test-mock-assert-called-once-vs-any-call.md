---
id: test-mock-assert-called-once-vs-any-call
node: engineering.testing
type: qa
source: python-docs
---
## Q
`mock.assert_called_once_with(args)` 和 `mock.assert_any_call(args)` 断言语义上有什么不同？mock 在测试中被调用了两次，第一次参数是 `(1,)`，第二次是 `(2,)`，对这两个断言分别调用 `assert_...(1)` 会发生什么？

## A
`assert_called_once_with` 要求 mock 总共只被调用过恰好一次，且那唯一一次的参数匹配；`assert_any_call` 只要求「历史上曾经有某一次调用」参数匹配，不关心调用总次数或是否是最近一次。对上面的例子，`mock.assert_called_once_with(1)` 会失败（因为总共调用了两次，不满足「恰好一次」），而 `mock.assert_any_call(1)` 会通过（因为确实有一次调用参数是 `1`）。
