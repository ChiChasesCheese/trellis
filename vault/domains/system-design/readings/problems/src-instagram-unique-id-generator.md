---
nodes: [problems.foundations.unique-id-generator]
url: https://instagram-engineering.com/sharding-ids-at-instagram-1cf5a71e5a5c
---
# Sharding & IDs at Instagram

值得读：Instagram 工程博客一手披露了他们真实使用的变体——41 位时间戳（自定义纪元
对应 2011 年 8 月 24 日）、13 位逻辑分片 ID、10 位序列号，直接用 PL/PGSQL 函数
嵌入 Postgres 的 `nextval()` 实现，让 ID 排序天然和 `created_at` 排序一致，省去
单独的时间索引。本题解把它"生成逻辑下推到数据层、不做独立服务"的思路作为嵌入式
生成的参照系，并在容量估算里独立算出了和它相同的 13 位 worker id，作为两条推理
路径互相印证的交叉验证，而不是直接照抄这个数字。

%% trellis:begin %%
## Source
[Open the original ↗](https://instagram-engineering.com/sharding-ids-at-instagram-1cf5a71e5a5c)
%% trellis:end %%
