---
id: auto-suspend-match-query-gaps
node: warehouse.auto-suspend-resume
type: qa
source: snowflake-docs
---
## Q
某虚拟仓库（virtual warehouse）的查询大约每 2–3 分钟来一条，管理员为了省钱把 auto-suspend（自动挂起）设成 1 分钟，同时开着 auto-resume（自动恢复）。为什么这反而可能更费钱？应该怎么设？

## A
仓库会不停地挂起又恢复，而每次恢复启动计算资源时都至少按 60 秒计费。于是每个 2–3 分钟的间隙都会付一次 60 秒最低费用，省下的空闲时间还不够抵。一般建议把 auto-suspend 设得较低（如 5 或 10 分钟以内），因为 Snowflake 按秒计费；但数值应匹配工作负载中实际的查询间隙，要比常见间隙更长，避免频繁抖动。
