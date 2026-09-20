---
id: problems-online-judge-plagiarism-review-not-autoban
node: problems.realtime.online-judge
type: qa
step: 8
tags: [grown]
---
## Q
In an online judge design, why should code-plagiarism detection route flagged submission pairs to human review instead of automatically banning accounts?

## A
Structural similarity checks (comparing submissions to the same problem within a time window, typically at an abstract-syntax-tree level to resist superficial changes like renaming variables) will inevitably produce false positives — two contestants can independently converge on the same standard, idiomatic solution to a problem. The cost of wrongly banning a legitimate contestant for a coincidental match is much higher than the cost of a missed detection, so the detector's output should be treated as a ranked queue for human review rather than an automated verdict.

## Q zh
在一个在线判题系统设计中，为什么代码抄袭检测应该把标记出的可疑提交对交给人工复核，而不是自动封号？

## A zh
结构相似度检测（在一个时间窗口内比较同一题目的提交，通常在抽象语法树层面做比较以抵抗改变量名之类的表面改动）必然会产生假阳性——两名选手完全可能各自独立地写出同一种标准、惯用的解法。错误封禁一个恰好写法相似的正当选手，代价远高于漏掉一次真正的抄袭，因此检测系统的输出应该当作一份排好序的人工复核队列，而不是自动判决。
