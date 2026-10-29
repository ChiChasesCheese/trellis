---
id: uth-devtools-build-deps-1-topo
node: devtools.build-deps
type: qa
step: 1
---
## Q
**构建系统怎么决定先编译谁**｜Ninja · 1.13

你改了一个 `.h`，Ninja 怎么知道哪些文件要重编，还不会陷入死循环？

## A
**结构。** 构建图是 DAG：节点是文件，边是构建命令。`RecomputeNodeDirty` 从目标出发做 DFS，沿途用一个栈检测环。

**细节。**

- 后序遍历（先处理输入）就是拓扑序；输出缺失，或最新的输入比输出新（比较 mtime），就标记为脏
- 递归时遇到栈里已有的边，报错 `dependency cycle: a -> b -> a`
- 互不依赖的任务并行执行，默认并行度是核数 + 2（核数大于 2 时）
- GNU make 遇到环只警告：`Circular x <- y dependency dropped`

**为什么。** 只靠修改时间和图遍历，不需要比较文件内容，增量构建就是一次图的遍历。

**对应 LeetCode：** LC 207 课程表 · LC 210 课程表 II
