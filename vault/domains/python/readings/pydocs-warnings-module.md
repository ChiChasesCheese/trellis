---
nodes:
- engineering.robustness
title: warnings 模块：警告控制
corpus: python-docs
section: 66-warnings
url: https://docs.python.org/3/library/warnings.html
tags:
- canonical
---

# warnings 模块：警告控制

warnings 模块是做 API 迁移和废弃提示的标准工具：库作者在计划移除或改变某个接口行为之前，先用 warnings.warn(..., DeprecationWarning) 提醒调用方这个用法即将失效，给使用者留出迁移时间，而不是直接一刀切改行为搞出破坏性变更。文档讲了警告过滤器（filter）机制，同一条警告默认只在同一个位置报一次，避免刷屏，也可以用 simplefilter/filterwarnings 精细控制某类警告是忽略、报错还是每次都显示；catch_warnings() 上下文管理器可以在测试代码里临时改变过滤规则，专门用来断言这段代码确实触发了某个警告。文档还提到默认情况下 DeprecationWarning 在非主模块里是被忽略的，只有开发者主动加参数或者是在测试框架里才会显示出来，这是很多人以为警告没生效的常见原因。
