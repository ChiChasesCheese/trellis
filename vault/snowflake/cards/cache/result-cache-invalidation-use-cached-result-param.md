---
id: result-cache-invalidation-use-cached-result-param
node: cache.result-cache-invalidation
type: qa
source: snowflake-docs
---
## Q
结果缓存默认是开启的，如果想在做基准测试（benchmark）时强制每次都重新计算查询、绕开结果缓存，应该怎么做？

## A
可以在账户、用户或会话级别把 `USE_CACHED_RESULT` 这个会话参数设为 `FALSE`，从而临时关闭结果复用；这样即便 SQL 文本、数据和配置都满足复用条件，Snowflake 也会强制重新执行查询，这对需要测量真实计算耗时、排除缓存干扰的基准测试很有用。
