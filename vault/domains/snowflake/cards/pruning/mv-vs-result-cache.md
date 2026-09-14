---
id: mv-vs-result-cache
node: pruning.materialized-views-maintenance
type: qa
source: snowflake-docs
---
## Q
物化视图（materialized view）和查询结果缓存（result cache，重跑完全相同查询时直接返回上次结果）都能复用已算好的结果。二者在灵活性、速度和基表变化后的行为上有何区别？

## A
结果缓存最快但最不灵活：只有查询文本相同、表数据未变且只用确定性函数（如不含 `CURRENT_DATE`）时才能命中，数据一变就失效。物化视图通常比结果缓存慢，但更灵活：不同查询只要能被改写到它上面就能受益；数据变化后，它对未变部分继续用已存结果，对变化部分回基表读取。此外物化视图占用存储、维护消耗信用点，结果缓存则没有这两项持续成本。
