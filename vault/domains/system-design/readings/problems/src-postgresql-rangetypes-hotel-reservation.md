---
nodes: [problems.commerce.hotel-reservation]
url: https://www.postgresql.org/docs/current/rangetypes.html
---
# Range Types

值得读：官方文档给出了排他约束（exclusion constraint）在一张 `reservation` 表上的标准例
子——`EXCLUDE USING GIST (during WITH &&)`，直接对应本题"区间行"数据模型方案；比大多数题
解文章更精确的地方是它明确了排他约束保证的是"同一把键（这里默认只有一列）上不出现两个重叠
区间"，本题据此论证了这个模型天然适合单一物理单元，而不是天然适合"一个房型下 N 个可互换单
元"的池化库存——这一区分是很多简化题解略过的地方。

%% trellis:begin %%
## Source
[Open the original ↗](https://www.postgresql.org/docs/current/rangetypes.html)

## Archived copy
![[src-postgresql-rangetypes-hotel-reservation-clip]]
%% trellis:end %%
