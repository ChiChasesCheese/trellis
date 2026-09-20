---
nodes: [problems.foundations.unique-id-generator]
url: https://blog.x.com/engineering/en_us/a/2010/announcing-snowflake
---
# Announcing Snowflake

值得读：Twitter（现 X）工程博客一手公布了 Snowflake 最初的位布局——1 位符号位、
41 位毫秒级时间戳（自定义纪元对应 2010 年 11 月 4 日）、10 位机器标识（5 位数据
中心 + 5 位机器）、12 位序列号，目标是在不需要任何跨节点协调的前提下生成大致
按时间有序的 64 位 ID。本题解把这套具体数字当成"专用发号机群"这一种部署形态下的
合理选择，并通过和 Instagram 不同的位分配对比，得出"位预算该由需要多少独立生成
身份决定，而不是照抄某个知名系统的数字"这条更一般的结论。

%% trellis:begin %%
## Source
[Open the original ↗](https://blog.x.com/engineering/en_us/a/2010/announcing-snowflake)
%% trellis:end %%
