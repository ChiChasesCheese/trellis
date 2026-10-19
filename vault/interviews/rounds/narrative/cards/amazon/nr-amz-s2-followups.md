---
id: nr-amz-s2-followups
node: amazon.followups
type: qa
step: 6
---
## Q
<p class="title">Quality-check 框架<span class="meta">03 追问</span></p>

面试官会追问什么？每个怎么答？

## A
- **Why dynamic SQL, isn't that risky?**
    - 这是 config-driven 的代价；配置经 **migration** 控制，不是用户输入
    - 真风险是失去**静态检查**；缓解：**exception handler** + 结果表**健康检查**
- **Why a status table, not task dependencies?**
    - 下游在**不同库/账号**；`AFTER` 依赖不跨账号；**复制的状态行**是最低公约数
- **What is the correctness argument for merchant-level?**
    - **Strictest wins**：先判 `NOT EXISTS(表级失败)`，再判 `NOT EXISTS(商户级失败)`
    - 未改造的 procedure 退化成表级阻塞 = 今天的行为
- **Why not VARIANT?**
    - secure view 上逐行 UDF / VARIANT 解析**关闭谓词下推**
    - VARIANT **16 MB/cell** 上限（~98K 商户）；扁平行 + 等值 JOIN 保留剪枝
- **What's the actual status?**
    - 框架 + 8 次铺开在生产；商户级 proven in one area（TRANSFERS，16 个月）；全框架铺开排在 net settlement 之后
- **What did you learn?**
    - 粒度要随规模重审；修自己的缺陷走更正式的流程；先问爆炸半径

<div class="sources"><b>表达 · business English</b><br>• <b><i>strictest wins</i></b> — 取最严格的结果<br>&nbsp;&nbsp;&nbsp;<span style="opacity:.85">“Strictest wins means a table-level failure always blocks, so mixed deployments stay safe.”</span><br>• <b><i>predicate pushdown</i></b> — 谓词下推<br>&nbsp;&nbsp;&nbsp;<span style="opacity:.85">“A per-row UDF over a secure view turns off predicate pushdown, which is why I rejected the VARIANT option.”</span><br>• <b><i>degrade gracefully</i></b> — 平滑降级<br>&nbsp;&nbsp;&nbsp;<span style="opacity:.85">“An unconverted procedure degrades gracefully to today&#x27;s table-level blocking.”</span></div>
