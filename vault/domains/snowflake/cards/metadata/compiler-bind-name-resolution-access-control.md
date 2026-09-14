---
id: compiler-bind-name-resolution-access-control
node: metadata.query-compiler-pipeline
type: qa
tags: [grown]
---
## Q
在 Snowflake 中执行一条引用了不存在的表或无权访问的表的查询，报错发生在哪个编译阶段？会消耗虚拟仓库（virtual warehouse）的 credit 吗？

## A
发生在绑定（bind）阶段，也叫对象解析：云服务（Cloud Services）层依据元数据把 SQL 中的名称解析为具体的数据库对象，并检查当前角色是否拥有相应权限；对象不存在和无权访问通常都报同一类“不存在或未授权”错误。由于这一步在分配任何计算资源之前完成，查询在此失败不会让仓库执行任何工作，也就不会消耗仓库 credit。
