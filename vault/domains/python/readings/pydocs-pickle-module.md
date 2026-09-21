---
nodes:
- engineering.serialization
- runtime.stdlib-map
title: pickle 模块：Python 对象序列化
corpus: python-docs
section: 55-pickle
url: https://docs.python.org/3/library/pickle.html
tags:
- canonical
---

# pickle 模块：Python 对象序列化

pickle 能把几乎任意 Python 对象（包括自定义类实例、函数引用）序列化成字节流再还原，但文档用醒目的警告强调了一个安全事实：反序列化不可信来源的 pickle 数据等同于执行任意代码，因为 pickle 的还原过程可以调用任意可导入的函数，绝不能用来解析来自网络请求或用户上传的数据。文档还讲了一个容易被忽视的运维坑：pickle 数据里记录的是类的模块路径和类名，如果之后重命名了类或者搬动了模块，旧的 pickle 文件会加载失败，需要用 copyreg 注册兼容的加载逻辑或者提供模块级别的别名来兼容旧数据。文档还对比了 pickle 和 json：前者是 Python 专属、支持任意对象但不安全不跨语言，后者跨语言、安全但只能表示有限的数据类型。

%% trellis:begin %%
## Source
[Open the original ↗](https://docs.python.org/3/library/pickle.html)

## Archived copy
![[pydocs-pickle-module-clip]]
%% trellis:end %%
