---
nodes: [problems.social.linkedin]
url: https://github.com/ashishps1/awesome-low-level-design/blob/main/problems/linkedin.md
---
# awesome-low-level-design — Designing a Professional Networking Platform like LinkedIn

值得读：开源题库（GPL-3.0），Python 实现在 `solutions/python/linkedin/`。它的
`ConnectionService.accept_request` 确实在双方各自的 `Member` 上都调用了
`add_connection`，效果上做到了互为一度人脉——这一点和本题解的方向一致：一次接受要让
两边同时看见对方。

但三处和本题解的分量不一样。第一，它完全没有实现"度数"（degrees of separation）或
"共同好友"这类查询——`Member.add_connection` 只是往一个列表里追加，没有任何一处基于
这份人脉关系做图上的搜索；本题解把有界双向 BFS 当作这道题的核心，正是因为公开题解普遍
在这里止步于"存下来"，没有再往前一步。第二，题面写了 `Skill` 类，但仓库里根本没有
`skill.py`——`Profile` 只有 `summary`、`experiences`、`educations` 三样，技能和"按技能
搜候选人"这条需求在代码里完全缺失；`SearchService.search_by_name` 是对 `members` 集合的
一次线性扫描。本题解把"按技能反查候选人"做成一张实际维护的反向索引，直接对着这个缺口写。
第三，`LinkedInService`"遵循单例模式，保证系统里只有一个实例"——这是一处教科书式的
Java 单例误用：它唯一的效果是让测试没法构造两个互不干扰的网络实例，这道题的测试恰恰
需要很多个。

%% trellis:begin %%
## Source
[Open the original ↗](https://github.com/ashishps1/awesome-low-level-design/blob/main/problems/linkedin.md)

## Archived copy
![[src-github-linkedin-clip]]
%% trellis:end %%
