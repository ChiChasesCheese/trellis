# pc22 Document Predicate Search Engine — report

## Summary
TrueInterview 87 题清单第 26 题（2026-04）："Document Predicate Search Engine"，`INSERT_DOC`/
`CHECK_CONTAINS` 命令名与"OR over words"语义为一手预览原文。3-part：Part 1 纯 OR（一手）·
Part 2 AND/OR 优先级，显式拒绝 NOT/括号 **(reconstructed)** · Part 3 NOT + 括号 + DELETE_DOC
**(reconstructed)**，精确输出格式（`NONE`、升序空格分隔）全部为重建。

## Sources & confidence
MED（TrueInterview 聚合站预览，题面付费）；命令名与 Part 1 语义为原文；输出格式、Part 2、Part 3
为重建。

## Approach by part
1. 倒排索引 `word -> doc id 集合`，随 `INSERT_DOC` 增量维护（重复插入同一 id 先撤销旧倒排项）；
   OR 查询是把每个词的倒排集合取并集。
2. 递归下降解析器（`expr := term (OR term)*`，`term := factor (AND factor)*`）产生 AST，
   在倒排索引上用集合交/并对 AST 求值（不逐文档扫描）；解析前先检查 token 流里有没有
   `NOT`/`(`/`)`，有就直接拒绝。
3. 完整文法加上 `factor := NOT factor | '(' expr ')'`；`NOT` 求值时用"当前索引里的全部文档 id"
   做差集；`DELETE_DOC` 把该文档从倒排索引摘除（词的倒排集合为空时顺便清理掉这个词条）。

## Pitfalls hidden tests target
- 无匹配 → `NONE`（不是空行）
- 重复 `INSERT_DOC` 同一 id 必须整体替换，旧倒排项不能残留
- Part 2 遇到 `NOT`/括号显式报错，而不是默默忽略或崩溃
- Part 3 `NOT` 的全集是"当前存在的文档"，被删除的文档不会被 `NOT` 捞回来
- `DELETE_DOC` 一个不存在的 id 是 no-op；括号不匹配、悬空操作符要报错

## Complexity & measured cost
每次 `INSERT_DOC`/`DELETE_DOC` O(文档词数)；每次查询 O(命中结果规模 + 表达式长度)，不扫描全部
文档。编排者验证：150 组随机文档 + OR 查询与"直接扫描每篇文档"独立暴力实现 0 不一致；200 组
AND/OR（无 NOT/括号）查询、200 组含 NOT/括号的完整查询分别与独立的递归下降解析器 + 逐文档求值
暴力实现 0 不一致。perf：5 万篇文档 + 2000 条 OR 查询端到端 < 2 s。

## Test inventory
18 tests — part1 4 · part2 3 · part3 5 · perf 1 · io/fmt 4；edge 9 · fmt 2 · perf 1 · io 4。

## Skills exercised
S09 倒排索引与集合代数（AND=交、OR=并、NOT=全集减法）· S04 递归下降解析器与运算符优先级 ·
增量维护索引而不是每次查询重新扫描全部数据。
