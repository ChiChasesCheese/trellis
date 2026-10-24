---
id: tlc-patterns-backtracking-8-problems
node: patterns.backtracking
type: qa
step: 8
---
## Q
**回溯（Backtracking）｜本组用到回溯的题**

按变形分类，这个题组里哪些题属于回溯？

## A
**子集 / 组合**
- LC 78 子集
- LC 77 组合
- LC 39 组合总和
- LC 40 组合总和 II（排序 + 同层去重）

**排列**
- LC 46 全排列
- LC 47 全排列 II（`used` + 去重）

**约束摆放 / 网格**
- LC 51 N 皇后
- LC 79 单词搜索
- LC 212 单词搜索 II（回溯 + 字典树）

**字符串生成 / 分割**
- LC 22 括号生成
- LC 93 复原 IP 地址
- LC 301 删除无效的括号（回溯或 BFS）
- LC 140 单词拆分 II（回溯 + 记忆化）

**分配 / 装箱**
- LC 473 火柴拼正方形

提示：先写出"每一步的选择是什么、终点是什么、怎样剪枝"；再决定下一层的起点（`i` 还是 `i + 1`）、是否需要排序去重、是否能改成 DP。
