---
nodes:
- engineering.serialization
title: json 模块：JSON 编解码
corpus: python-docs
section: 56-json
url: https://docs.python.org/3/library/json.html
tags:
- canonical
---

# json 模块：JSON 编解码

json 模块提供了 Python 对象和 JSON 文本之间的标准转换，dumps/loads 处理字符串，dump/load 直接处理文件对象。文档重点讲了默认能编码的类型集合（dict、list、str、数字、bool、None）之外的类型都会抛 TypeError，像 Decimal、datetime、自定义类实例这些常见的业务对象都不在默认支持范围内，需要通过自定义 JSONEncoder 子类重写 default() 方法，或者给 dumps 传 default= 回调函数来处理。反过来解码时如果要把 JSON 里的字符串还原成 datetime 或自定义对象，需要用 object_hook 回调在解析过程中拦截。文档还提到 JSON 标准本身不支持 NaN/Infinity，Python 的实现默认会输出这些非标准值，跨语言对接时需要注意关闭这个行为以避免被其他语言的解析器拒绝。

%% trellis:begin %%
## Source
[Open the original ↗](https://docs.python.org/3/library/json.html)

## Archived copy
![[pydocs-json-module-clip]]
%% trellis:end %%
