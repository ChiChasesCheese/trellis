---
nodes: [problems.machines.amazon-locker, structure.storage]
tags: [problem]
---
# Drill：快递柜（Amazon Locker）

一个写字楼大堂里的快递柜网点：几十个大小不一的柜格，快递员投件、顾客凭一次性取件码来取。
这道题的分不在顺路径，而在两处：分配规则写成什么样才经得起第 4 关加一种新尺寸；以及那个
取件码到底是什么东西——它不是密码，这句话会一路决定错误尝试怎么计数、日志里能不能出现它。
时间一律从注入的时钟进来，代码里不许出现 `time.time()`、`sleep` 或后台定时器。

**分关要求**（每关做完再看下一关，像真实的机器编码轮）
- 第 1 关（约 20 分钟）：一个网点，若干不同尺寸的柜格。投件时把包裹放进**装得下它的最小
  空柜**并签发一个一次性取件码；凭码取件时交还包裹并释放柜格。没有合适的空柜要明确拒绝，
  而且拒绝之后柜位一个都不能少。先想清楚尺寸用什么表达——这个决定在第 4 关会被兑现。
- 第 2 关（约 15 分钟）：取件的失败路径。码不存在、码过期、码用错了门，必须是三件不同的
  事，而且**只有一种算可疑**；想清楚"连续输错就锁定"锁的到底是什么（提示：一个错误的码不
  属于任何人）。再加过期回收：注入时钟走过期限之后，一次显式扫描让码作废、柜格回池、包裹
  标成退回寄件人。顺手回答：如果扫描还没跑，顾客拿着过期的码来按键盘，会发生什么？
- 第 3 关（约 15 分钟）：多个网点，找到"装得下且还有空位"的最近网点。地理部分请刻意做成
  朴素的距离排序，并说得出为什么——真正的邻近搜索是另一道题。然后是并发：同一网点上多个
  快递员同时投件，不能有两个包裹拿到同一个柜格，也不能签出重复的码。说清楚临界区覆盖哪
  几步、GIL 在这里帮不上什么忙。
- 第 4 关（选做）：退货投柜的反向流程（顾客投件、快递员来收），以及一种系统此前没见过的
  尺寸。判分点只有一个：这两件事都**不许动分配逻辑和码表**。如果你发现自己在复制一份分配
  代码，回头看"码允许做什么"能不能变成一个字段。

**怎么练**：把 `vault/domains/low-level-design/problems/amazon-locker/starter.py` 的方法体补全，
然后在仓库根目录运行
`IMPL=starter uv run --with pytest python -m pytest vault/domains/low-level-design/problems/amazon-locker -q`。

**评分点**
- 尺寸不做成封死的枚举档位，而是带三维的值对象，分配逻辑里不出现任何一个具体尺寸名（[[problems-amazon-locker-size-value-object-not-enum]]）。
- 分配是"最小可容纳优先"而不是精确匹配，并说得出它的贪心代价；三维下用 `(体积, 名字)` 把偏序补成全序（[[problems-amazon-locker-smallest-fitting-allocation]]）。
- 说得出取件码是持有即凭证而不是密码，因此限流只能按终端、不能按包裹或账号；码用 `secrets` 生成（[[problems-amazon-locker-code-is-not-a-password]]）。
- 三种失败区别对待：只有"码不存在"累计失败；过期不计失败但要就地回收；用错门的码必须活下来（[[problems-amazon-locker-three-failures-differ]]）。
- 过期用注入时钟 + 显式扫描 + 到期堆，而不是定时器或后台 `sleep` 线程；惰性删除的陈旧条目在弹出时真的被丢掉（[[problems-amazon-locker-expiry-heap-lazy-deletion]]）。
- 码表、可用索引、到期堆三个容器都会缩，并且用只读计数属性暴露出来供测试断言，而不是让测试去读私有字段（[[problems-amazon-locker-every-container-shrinks]]、[[structure-api-leaking-internals]]）。
- 一把粗锁覆盖"挑柜 + 占柜 + 发码"整段，说得清 GIL 为什么不够；多网点路由不先查后投（[[problems-amazon-locker-lock-covers-allocate-and-issue]]、[[structure-storage-chm-compound-ops]]）。
- 反向投件靠给授权加一个"用途"字段实现，分配、码表、过期扫描一行不改（[[problems-amazon-locker-reverse-flow-grant-purpose]]）。
- 事件只描述发生了什么，**不带取件码**——事件会流进日志和监控（[[structure-storage-secondary-index]]）。

**题解**：[[solution-amazon-locker]]——先做，再看。

**练习记录**
- [ ] 第 1 次（日期，用时，自评）：
