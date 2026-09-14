---
id: auto-suspend-60s-restart-billing
node: warehouse.auto-suspend-resume
type: cloze
source: snowflake-docs
---
虚拟仓库（virtual warehouse）每次启动计算资源最少计费 {{c1::60 秒}}，之后按秒计费。运行 30–60 秒计 {{c2::60}} 秒；运行 61 秒计 61 秒；运行 61 秒后关闭、再启动并运行不到 60 秒，共计 {{c3::121}} 秒（60 + 1 + 60）。因此在前 60 秒内提前挂起 {{c4::没有任何节省}}。
