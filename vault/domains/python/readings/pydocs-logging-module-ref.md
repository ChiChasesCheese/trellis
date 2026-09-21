---
nodes:
- engineering.logging-config
title: logging 模块：完整 API 参考
corpus: python-docs
section: 65-logging
url: https://docs.python.org/3/library/logging.html
tags:
- canonical
---

# logging 模块：完整 API 参考

这是 logging 模块的完整参考手册，配合 HOWTO 教程一起读效果更好：Logger 对象讲清了层级传播规则和 propagate 属性如何关闭向上传播；Handler 决定日志输出到哪（StreamHandler、FileHandler、RotatingFileHandler 等）；Formatter 决定输出格式；Filter 提供比日志级别更细粒度的过滤逻辑。LogRecord 属性表列出了每条日志自带的全部元数据（时间戳、模块名、行号、线程 ID 等），是自定义 Formatter 格式字符串时的查阅依据。文档强调的最佳实践是每个模块用 logging.getLogger(__name__) 获取自己的 logger，这样日志的来源天然按模块名分层，也让调用方能针对特定模块单独调整日志级别。还讲了 logging 模块本身是线程安全的，可以在多线程程序里放心使用而不用额外加锁。

%% trellis:begin %%
## Source
[Open the original ↗](https://docs.python.org/3/library/logging.html)

## Archived copy
![[pydocs-logging-module-ref-clip]]
%% trellis:end %%
