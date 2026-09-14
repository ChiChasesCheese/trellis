---
id: result-cache-invalidation-show-query-role-match
node: cache.result-cache-invalidation
type: qa
source: snowflake-docs
---
## Q
同样是命中结果缓存所需的权限条件，为什么 `SHOW <objects>` 这类查询的复用要求比普通 SELECT 查询更严格——必须是同一个角色，而不能像 SELECT 那样只要有权限就行？

## A
SHOW 查询返回的是账户级或对象级元数据（例如某个角色能看到哪些表），这类结果本身依赖发起查询时所用角色的可见范围，不同角色即便权限有重叠，能看到的对象集合也可能不同，所以 Snowflake 要求复用 SHOW 查询缓存的角色必须与最初生成该缓存结果的角色完全一致；而普通 SELECT 查询的结果只取决于对表的访问权限是否足够，因此只要角色拥有相应权限即可复用，不要求是同一个角色。
