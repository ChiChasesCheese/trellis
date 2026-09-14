---
id: snowpipe-same-name-modified-file-skipped
node: ingestion.snowpipe-auto-ingest
type: qa
source: snowflake-docs
---
## Q
上游修正了一个已被 Snowpipe 加载过的文件，并以相同路径和文件名覆盖上传。修正后的数据会被加载吗？为什么？

## A
不会。Snowpipe 使用与每个管道关联的文件加载元数据来防止重复加载，其中记录了每个已加载文件的路径（前缀）和文件名；即使文件后来被修改（eTag 已不同），同名文件也不会再被加载。修正数据应以新文件名上传，或另行处理。
