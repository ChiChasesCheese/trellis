---
nodes: [problems.social.tinder]
url: https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-terms-query.html
---
# Elasticsearch: Terms query

值得读：Elastic 官方文档确认 `terms` 查询默认的词项数上限
`index.max_terms_count = 65,536`。本题解用这个数字和算出的重度用户 seen set 规模
（约 164,250）对比，论证"用索引侧 `must_not terms` 直接排除已划过用户"这个方案在这道
题需要覆盖的重度用户规模下不成立——这是比多数题解文章更具体的地方：多数文章只说"索引侧
过滤有上限"，很少给出这个上限具体是多少、和真实用户规模的数字关系。

%% trellis:begin %%
## Source
[Open the original ↗](https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-terms-query.html)

## Archived copy
![[src-elastic-tinder-clip]]
%% trellis:end %%
