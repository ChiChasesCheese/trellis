---
id: packaging-lockfile-reproducibility
node: engineering.packaging-env
type: qa
tags: [grown]
---
## Q
`pyproject.toml` 里声明的依赖通常是带版本范围的（如 `requests>=2,<3`），为什么还需要额外的锁文件（lock file，如 `uv.lock`）来保证「可复现」（reproducible）？

## A
版本范围只约束了「安装时允许选哪些版本」，不同时间、不同机器上解析同一份范围可能因为依赖方发布了新版本而选出不同的具体版本号，造成「在我机器上能跑」的不一致。锁文件把一次解析结果——每个直接依赖和间接依赖精确的版本号（以及通常还有哈希值用于校验）——完整记录下来，之后任何人在任何时间用锁文件安装，都会得到完全相同的一组包版本，从而保证环境可复现。
