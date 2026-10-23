---
id: hl-bs-r1-numbers
node: behavioral.stories
type: qa
step: 2
---
## Q
个人研究平台 R1（Quant-Stroller）有哪些要记的数字和技术栈事实？

## A
- **Python**，**66K+ 行**，**470+ 个测试文件**；覆盖美股、加密、A 股、外汇。
- **340+ 次实验**记入只增不改的账本（append-only ledger）。
- 一个 **A 股小盘月度策略**过了两道门：扣除 **10 bps** 成本后超额 Sharpe **1.39**，上了 paper trading。
- **点时数据平面**（DuckDB / Parquet）；**5,500 只**A 股面板；**8-GPU 服务器** PyTorch + 自托管 CI。
