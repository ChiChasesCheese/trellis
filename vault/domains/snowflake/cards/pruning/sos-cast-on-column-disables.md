---
id: sos-cast-on-column-disables
node: pruning.search-optimization-service
type: qa
source: snowflake-docs
---
## Q
同样是隐式类型转换（implicit cast），一条谓词里转换加在常量上、和转换加在表的列本身上，对能否使用搜索优化服务有什么不同影响？

## A
如果隐式类型转换发生在常量一侧（比如把比较用的字面量转换成列的类型），谓词仍然可以使用搜索优化服务加速；但如果转换发生在表的列本身上（先对列做类型转换，再和常量比较），就无法使用搜索优化服务了，因为搜索访问路径记录的是列原始值的分布，一旦列被转换成了别的表达式，访问路径里的信息就不再直接适用。
