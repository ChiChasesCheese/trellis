---
id: uth-devtools-build-deps-2-pip
node: devtools.build-deps
type: qa
step: 2
---
## Q
**pip 的版本解析为什么要回溯**｜pip · resolvelib

两个包对同一个依赖要求不同的版本范围，pip 怎么找到一组都满足的版本？

## A
**结构。** 约束满足问题（本质是 SAT，NP 完全）：为每个包选一个版本，遇到冲突就回溯（backtracking）换一个。

**细节。**

- pip 的求解器来自 resolvelib，是抽象的回溯算法；pip 只提供候选版本与依赖的 provider
- 依赖要下载 wheel 或构建源码包才知道，不可能先拿到完整依赖树
- 所以只能边选边查：对每个候选“按需”取依赖，冲突了再回退

**为什么。** 元数据昂贵，先建全图再求解不现实；回溯式求解只付出实际走到的候选的代价。

**对应 LeetCode：** LC 46 全排列 · LC 39 组合总和
