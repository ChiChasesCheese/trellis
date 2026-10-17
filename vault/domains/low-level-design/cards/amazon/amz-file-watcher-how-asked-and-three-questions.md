---
id: amz-file-watcher-how-asked-and-three-questions
node: amazon.amz-file-watcher
type: qa
step: 1
tags: [grown]
---
## Q
Amazon 面试里「文件监听器（File Watcher）」是怎么问的？开场先问哪三个澄清问题？

## A
报告里只有题名：2026-09 一亩三分地的 SDE II 电面，三道题之一是「设计 file watcher system」，题面细节不可见，其余都是重建。三问：(1) 靠系统通知还是定期轮询——决定依赖与延迟，答案是轮询并把读文件系统藏在接口后；(2) 递归与否、是否过滤文件——两个参数；(3) 改名与写到一半的文件怎么报——轮询里改名是删除加新建，半截文件要去抖。
