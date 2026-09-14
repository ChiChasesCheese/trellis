---
id: wh-size-data-loading-files-matter
node: warehouse.sizing-t-shirt
type: qa
source: snowflake-docs
---
## Q
数据加载（COPY 导入）很慢，把仓库规格从 Medium 调到 2X-Large 一定有用吗？

## A
不一定。加载性能更多取决于要加载的文件数量和每个文件的大小，而不是仓库规格。除非要并发批量加载成百上千个文件，否则 Small、Medium、Large 通常就够了；用 X-Large、2X-Large 等更大的仓库会消耗更多 credit（信用点），却可能没有任何性能提升。
