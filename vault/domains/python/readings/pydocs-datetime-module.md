---
nodes:
- engineering.money-time
- runtime.stdlib-map
title: datetime 模块：日期时间完整参考
corpus: python-docs
section: 54-datetime
url: https://docs.python.org/3/library/datetime.html
tags:
- canonical
---

# datetime 模块：日期时间完整参考

这是 datetime 模块的完整参考，最核心的一组概念是 aware（带时区信息）与 naive（不带时区信息）对象的区别：两者之间直接比较或相减会抛 TypeError，文档给出了判断一个对象到底是 aware 还是 naive 的标准方法（检查 tzinfo 是否为 None 以及 utcoffset() 的返回值）。文档系统介绍了 timedelta（时间差）、date、time、datetime、tzinfo、timezone 各个类型的构造和常用方法，以及 strftime()/strptime() 完整的格式码对照表。工程实践上的教训是：涉及跨时区的系统应该始终存储和传递 aware 的 UTC 时间，只在展示给用户时才转换成本地时区的 naive 表示，混用 naive 和 aware 对象是分布式系统里常见且难排查的 bug 来源。这篇参考是查具体格式码或方法签名时该回来的地方。
