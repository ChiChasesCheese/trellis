---
nodes:
- classes.dataclasses
title: PEP 557：数据类（Data Classes）
corpus: peps
section: 12-pep-0557
url: https://peps.python.org/pep-0557/
tags:
- canonical
---

# PEP 557：数据类（Data Classes）

把 dataclass 定位讲得很清楚：不是 namedtuple 的替代品，而是“带默认值的可变 namedtuple”，靠类装饰器扫描 PEP 526 风格的类型注解字段，自动生成 __init__、__repr__ 和比较方法，但不改变类本身——不用元类、不用基类，用户仍可自由继承。Rationale 部分列出了在它之前解决同一问题的方案谱系（namedtuple、typing.NamedTuple、attrs、各种手写 recipe），说明标准库版本的定位是覆盖“简单场景”，复杂校验和第三方生态仍然并存而非被取代。同时明确划出不适用边界：需要和 tuple/dict 做 API 兼容、或需要超出 PEP 484/526 的类型校验和值转换时不该用 dataclass。这段边界判断是面试里“什么时候该用 dataclass、什么时候该用 attrs 或手写类”的直接依据。

%% trellis:begin %%
## Source
[Open the original ↗](https://peps.python.org/pep-0557/)

## Archived copy
![[peps-pep557-dataclasses-clip]]
%% trellis:end %%
