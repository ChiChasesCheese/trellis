---
nodes:
- engineering.testing
title: unittest.mock：模拟对象库
corpus: python-docs
section: 64-unittest-mock
url: https://docs.python.org/3/library/unittest.mock.html
tags:
- canonical
---

# unittest.mock：模拟对象库

unittest.mock 是写单元测试隔离外部依赖的标准工具，核心是 Mock/MagicMock 对象，访问任意属性或调用任意方法都不会报错，而是自动返回新的 Mock 对象，同时记录下被怎样调用过，供之后用 assert_called_with() 等断言验证。patch 系列（patch、patch.object、patch.dict）用于在测试期间临时替换掉被测代码依赖的对象，文档专门用一整节 Where to patch 讲清了一个极易踩坑的点：要 patch 的是使用该对象的模块里的引用，而不是对象原本定义的地方，patch 错位置是 mock 测试失败最常见的原因。autospec/create_autospec 能让 Mock 对象的接口签名自动匹配被替换对象的真实签名，调用时传参数错误会像真实调用一样报错，比裸 Mock() 更能捕获接口不匹配的 bug。这是把时间、I/O 等副作用替换成可控假对象、获得确定性测试的核心工具。

%% trellis:begin %%
## Source
[Open the original ↗](https://docs.python.org/3/library/unittest.mock.html)

## Archived copy
![[pydocs-unittest-mock-clip]]
%% trellis:end %%
