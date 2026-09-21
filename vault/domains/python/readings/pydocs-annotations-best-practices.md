---
nodes:
- types.basics
title: 注解（Annotations）最佳实践
corpus: python-docs
section: 12-annotations
url: https://docs.python.org/3/howto/annotations.html
tags:
- canonical
---

# 注解（Annotations）最佳实践

这篇文档讲的是一个常被忽略的事实：函数和变量的类型注解在运行时只是存在 __annotations__ 字典里的普通数据，解释器不会因为参数类型不对就拒绝调用，类型检查完全是外部工具（mypy 等）在做的事。文档给出了 3.10 及以后版本获取注解字典的推荐方式（inspect.get_annotations()），以及旧版本的兼容写法，并讨论了字符串化注解（annotations 以字符串形式延迟求值）带来的坑：直接读 __annotations__ 可能拿到字符串而不是真实类型对象，需要手动反字符串化。读完能准确回答给函数加了类型注解、传错类型的参数会怎样，答案是完全不会报错，这正是面试里经常用来考察对类型系统本质理解程度的问题。
