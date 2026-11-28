---
id: hi-pt-spreadsheet-engine-3-cycle-detect
node: qb.lld.spreadsheet-engine.points
type: qa
step: 3
---
## Q
**电子表格引擎 · 环检测**｜必会 · 出自：电子表格引擎 › 深入 2

怎么判断一次 `set` 会让公式成环？菱形引用（`D1` 同时读 `B1` 和 `C1`，二者都读 `A1`）算环吗？

## A
**做法。** 从新公式的直接依赖出发，沿"我读了谁"（`_deps`）做 DFS，能走回被写的格子就是环，抛 `CycleError`，而且检测在改任何状态之前。

**菱形不是环。** 只问能不能走回自己；`seen` 集合避免同一个格子被重复展开。

**易错。** 自己引用自己（`A1` 的公式含 `A1`）也要拦住；改线后旧依赖没摘掉，会造成误判。
