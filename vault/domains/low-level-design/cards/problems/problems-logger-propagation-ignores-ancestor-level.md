---
id: problems-logger-propagation-ignores-ancestor-level
node: problems.components.logger
type: qa
step: 5
tags: [grown]
---
## Q
日志框架里 logger 按点分名字组成树（`app.db.pool` 的父亲是 `app.db`），记录会沿祖先链向上交给沿途每个 handler。如果把父 logger `app` 的级别设成 CRITICAL，子 logger `app.db` 的一条 DEBUG 还能到达挂在 `app` 上的 handler 吗？

## A
能。级别**只在产生记录的那个 logger 上判一次**；向上传播时只看每个 handler 自己的阈值，祖先 logger 的级别根本不参与。这是 Python 标准库 `logging` 的 `callHandlers` 的真实语义，也是最多人记反的一条——凭直觉写出来的传播循环几乎总会多一句"再比一次祖先的级别"。想在中途截断传播，用的是 `propagate = False`（走到这个 logger 为止，不再往上），不是把祖先的级别调高。
