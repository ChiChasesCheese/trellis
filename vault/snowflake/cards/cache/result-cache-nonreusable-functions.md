---
id: result-cache-nonreusable-functions
node: cache.result-cache
type: qa
source: snowflake-docs
---
## Q
一条 `SELECT UUID_STRING()` 这样包含随机/不可重用函数的查询，即便反复执行、底层表数据从未改变，也无法从结果缓存中获得 100% 复用，为什么？还有哪些场景同样会阻止结果缓存被使用？

## A
像 UUID_STRING、RANDOM、RANDSTR 这类函数在每次调用时都会产生不同的返回值，如果直接返回上一次缓存的结果就会给出错误答案，所以 Snowflake 不会对这类查询启用结果复用；此外，查询中包含外部函数（external function），或者查询的是混合表（hybrid table），也同样不会走结果缓存。
