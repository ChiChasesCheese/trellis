---
nodes:
- runtime.adaptive-jit
title: PEP 744：JIT 编译器现状说明
corpus: peps
section: 05-pep-0744
url: https://peps.python.org/pep-0744/
tags:
- canonical
---

# PEP 744：JIT 编译器现状说明

讲清楚 3.13 起合入的实验性 JIT 为什么选择 copy-and-patch 而不是 LLVM 这类成熟框架：后者会引入沉重的运行时依赖和更高的编译开销，而 copy-and-patch 直接从生成解释器用的同一份字节码 DSL 生成 JIT 模板，核心开发者只需编辑指令定义就能让所有平台的 JIT 后端“免费”同步更新。文档还交代了技术脉络——3.11 的特化自适应解释器（PEP 659）产生了丰富的运行时画像信息，3.13 起始终存在但默认关闭的微操作（micro-op）追踪与优化管线，因为解释微操作本身开销太大而收益有限，才促使把优化后的追踪静态编译成机器码。面试要点：JIT 何时会“转正”有三条明确门槛（至少一个平台 5% 提速、可低成本构建分发、指导委员会评估价值），当前仍应视为实验特性，不能用于生产。

%% trellis:begin %%
## Source
[Open the original ↗](https://peps.python.org/pep-0744/)

## Archived copy
![[peps-pep744-jit-compilation-clip]]
%% trellis:end %%
