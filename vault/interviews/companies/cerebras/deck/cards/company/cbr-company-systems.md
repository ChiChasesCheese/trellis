---
id: cbr-company-systems
node: company.products
type: qa
step: 2
---
## Q
CS-3、CS-4、WSE-5、CS-5 分别是什么？各处在什么阶段？

## A
| 名称 | 是什么 | 阶段 |
|---|---|---|
| **CS-3** | 一块 WSE-3 装成的一台机器 | 2024 年发布，目前的主力 |
| **CS-4（Nexus 平台）** | 一个机柜放 3 块加强版晶圆 WSE-3T；晶圆之间用以太网上的 RDMA 直连 | 2026 Q3 开始出货；公司说速度是 CS-3 的 2 倍 |
| **WSE-5** | 下一代晶圆 | 已从工厂回来，在做系统测试 |
| **CS-5** | 基于新晶圆的系统 | 目标 2027 年夏天 |

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 82" font-family="sans-serif" font-size="11">
<text x="46" y="16" text-anchor="middle" fill="currentColor">2024</text>
<text x="128" y="16" text-anchor="middle" fill="currentColor">2026 Q3</text>
<text x="212" y="16" text-anchor="middle" fill="currentColor">现在</text>
<text x="296" y="16" text-anchor="middle" fill="currentColor">2027 夏</text>
<line x1="10" y1="30" x2="332" y2="30" stroke="currentColor"/>
<circle cx="46" cy="30" r="4" fill="currentColor"/>
<circle cx="128" cy="30" r="4" fill="currentColor"/>
<circle cx="212" cy="30" r="4" fill="none" stroke="currentColor"/>
<circle cx="296" cy="30" r="4" fill="none" stroke="currentColor"/>
<text x="46" y="52" text-anchor="middle" fill="currentColor">CS-3</text>
<text x="128" y="52" text-anchor="middle" fill="currentColor">CS-4</text>
<text x="212" y="52" text-anchor="middle" fill="currentColor">WSE-5</text>
<text x="296" y="52" text-anchor="middle" fill="currentColor">CS-5</text>
<text x="46" y="70" text-anchor="middle" fill="currentColor">发布，主力</text>
<text x="128" y="70" text-anchor="middle" fill="currentColor">开始出货</text>
<text x="212" y="70" text-anchor="middle" fill="currentColor">系统测试</text>
<text x="296" y="70" text-anchor="middle" fill="currentColor">目标</text>
</svg>
```

- **RDMA（remote direct memory access）**：一台机器直接读写另一台机器的内存，不经过对方的 CPU，延迟低。
- **对你的意义**：新硬件、新平台、新晶圆同时在推进，每一代都要把同一套推理软件验证一遍。**硬件换代 = 集成测试的工作量**。
- **训练用的另一套**（了解即可）：权重流式（weight streaming），参数放在片外的 MemoryX，按层流进晶圆；推理则是参数常驻片上。
