---
id: min60-resume-thrash
node: cost.warehouse-billing-60s-minimum
type: qa
source: snowflake-docs
---
## Q
把仓库的自动挂起（auto-suspend）设得极短，比如几秒钟，而查询每隔二三十秒来一条。为什么这反而可能更贵？

## A
每次恢复（resume）都会重新开始一个 60 秒最低计费。仓库在第一分钟内被挂起又恢复，就会被多次收取 1 分钟费用：本来连续运行 2 分钟只需 2 分钟费用，频繁挂起/恢复可能每次都付满 1 分钟。频繁冷启动还会丢掉仓库本地的磁盘缓存，使查询变慢。所以查询间隔短于约一分钟的负载，自动挂起时间应设得比查询间隔更长。
