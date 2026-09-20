---
nodes: [problems.social.social-network]
url: https://github.com/jkaus324/machine-coding-interview-questions/tree/main/problems/tier2-intermediate/018-twitter
---
# machine-coding-interview-questions — Simplified Twitter

值得读：这是纯粹的关注模型（没有"好友"这个概念），题面按机考的节奏分级——基础版是发帖/关注/
取关/取信息流，进阶版把信息流算法从"取出所有关注对象的帖子再整体排序"换成**按用户分流、用
最大堆做 k 路归并**，复杂度从对全部帖子排序降到 `O(结果数 × log(关注人数))`。这一步正是本题解
"信息流的候选集合怎么合并"这件事在**读扩散**路线下的标准答案；本题解选的是**写扩散**（换一种
代价：发布贵、阅读几乎免费），"关键设计决策"一节里用同一个 k 路归并的直觉去谈大V的读时合并，
方向相反、道理相通。五种语言实现，Python 版可读性最好，但两个版本都没有"好友"与"关注"分离、
也没有拉黑，属于社交图谱里更简单的一个子问题。

%% trellis:begin %%
## Source
[Open the original ↗](https://github.com/jkaus324/machine-coding-interview-questions/tree/main/problems/tier2-intermediate/018-twitter)

## Archived copy
![[src-jkaus324-social-network-clip]]
%% trellis:end %%
