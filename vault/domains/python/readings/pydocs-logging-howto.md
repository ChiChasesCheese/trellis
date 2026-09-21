---
nodes:
- engineering.logging-config
title: 日志 HOWTO：从基础用法到多模块配置
corpus: python-docs
section: 13-logging
url: https://docs.python.org/3/howto/logging.html
tags:
- canonical
---

# 日志 HOWTO：从基础用法到多模块配置

这是学 logging 模块该读的第一篇文档，从最简单的 logging.basicConfig() 讲到完整的日志体系：logger（发出日志）、handler（决定日志去哪，比如控制台还是文件）、formatter（决定日志长什么样）三者职责分离，可以任意组合。核心要点是日志的传播机制：logger 按名字组成树状层级（如 myapp.db 的日志会传播给 myapp），且默认会一路往上传播直到根 logger；文档明确建议，写库代码时永远不要配置根 logger 或调用 basicConfig()，配置应该完全交给使用这个库的应用来决定，否则会污染调用方的日志输出。文中还讲了日志级别的选择原则和如果没有做任何配置会发生什么（会看到一条一次性的警告并把日志丢到 stderr）。这是团队协作写库代码时最容易踩的坑之一。

%% trellis:begin %%
## Source
[Open the original ↗](https://docs.python.org/3/howto/logging.html)

## Archived copy
![[pydocs-logging-howto-clip]]
%% trellis:end %%
