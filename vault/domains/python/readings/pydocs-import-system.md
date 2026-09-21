---
nodes:
- runtime.import-system
title: 导入系统（import system）完整机制
corpus: python-docs
section: 03-import
url: https://docs.python.org/3/reference/import.html
tags:
- canonical
---

# 导入系统（import system）完整机制

这是 import 语句背后发生的一切的权威说明：模块只会被真正执行一次，结果缓存在 sys.modules 里，之后的 import 只是查表；查找模块要经过 finder（决定去哪找）和 loader（决定怎么加载）两步，sys.meta_path 上的一串 finder 依次尝试；常规包靠 __init__.py，命名空间包没有这个文件也能被识别为包；相对导入（from . import x）只在包内部有效，脚本直接运行时会报错。这篇文档能解释两个常被问到的现象：为什么同一个模块在两个不同路径下 import 会被当成两个不同对象，以及循环导入到底卡在哪一步。把它当作 import 出问题时该去哪查的手册，不需要逐字记住，但要知道 finder/loader/sys.modules 这几个关键词分别对应什么阶段。
