---
nodes: [problems.social.reddit]
url: https://github.com/reddit-archive/reddit/blob/master/r2/r2/lib/db/_sorts.pyx
---
# reddit-archive/reddit — `_sorts.pyx`

值得读：Reddit 2008 年开源的原始代码库里，`hot`、`_confidence`（Wilson 置信区间下界）、
`controversy` 三个排序函数的精确实现，带着本题解直接引用的常数（45000 秒时间衰减除数、
80% 置信度的 `z` 值）。比任何转述文章都权威，因为它就是被跑在生产环境里的那份代码本身；
本题解在此基础上补充了"分数是创建时刻的纯函数、不需要后台定时重算"这层架构含义的论证。

%% trellis:begin %%
## Source
[Open the original ↗](https://github.com/reddit-archive/reddit/blob/master/r2/r2/lib/db/_sorts.pyx)

## Archived copy
![[src-reddit-archive-reddit-clip]]
%% trellis:end %%
