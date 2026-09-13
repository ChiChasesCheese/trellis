# ps12 Hierarchical Task CSV — report

## Summary
一道“重放事件日志重建树 + 格式化输出”的题：输入是 CSV 事件流（`task` 根记录 / `subtask` 子记录），
按 `parent_id` 建树，再按类 Unix `tree` 命令的连接符规则（`├─`/`└─`/`│  `/三空格）逐层渲染。核心难点
不在算法而在**格式精确性**（S09）——连接符、祖先层续接符号、以及“保留输入兄弟顺序、忽略 timestamp”
这条容易被误当排序键的隐含契约。四个 part 完整复刻了候选人报告的真实拆分节奏：① 只认根记录 ② 天真地
给所有子任务同一个连接符 ③ 修正最后一个子任务的连接符 ④ 泛化到任意深度——第 ④ part 如果第 ③ part 写
成了正确的通用递归/迭代树遍历，代码完全不用改，这是本题最值得在面试里说出来的洞察。

## Sources & confidence
high。证据链：
1. PracHub `parse-and-format-arbitrarily-nested-tasks-from-csv`（id 11064）页面内嵌候选人第一人称
   原始报告（`created_at: 2026-08-25`, `interview_round: "Technical Screen"`, `is_ai_assisted: false`），
   逐字给出 4-part 拆分描述与输入样例前两行。
2. 同页面 PracHub 自动生成的结构化题面（函数签名 `format_task_csv(lines)`、连接符规则、约束、完整
   worked example）与候选人报告的逻辑完全吻合、无矛盾。
3. 本 session 于 2026-09-03 独立用 `curl` 重新抓取该页面（未使用 WebFetch，因为该站点走 Next.js
   RSC/CSR 渲染，`curl` 直接拿静态 HTML 里内嵌的 `data-seo-content="question-body"` 与
   JSON payload 即可拿到完整正文，无需登录、无 Cloudflare 挑战），核对内容与
   `catalog/discovery/2026-09/C_batchB.md` `## C12` 一节的记录逐字一致，未发现出入。

三处来源相互印证、无矛盾，故按 CONVENTIONS.md 惯例定为 **high**，不加“部分重建”警示块——但要注意：
Part 1/2/3 的 4-part 拆分节奏、以及 Part 4 的“深度任意嵌套”规则都直接来自候选人原文与结构化题面；
本 problem.md 里 Part 1/2/4 的**具体 worked example 数值**（多根、CSV 引号样例、两层嵌套样例）是本
套件在已确认规则基础上自行构造的补充用例，只有 Part 3 的样例是 PracHub 原文逐字复用。

## Approach by part
1. **Part 1**：CSV 逐行 parse（`csv.reader`），只挑 `kind == "task"` 的记录，按输入顺序输出
   `task_id + " " + name`。
2. **Part 2**：额外建一层 `children` 邻接表（只考虑根的直接子节点），每个子任务不分是否最后一个统一
   用 `"├─ "`——刻意保留候选人报告里“第③部分才修最后一个连接符”这个真实的天真实现阶段。
3. **Part 3**：换成 `_render_forest`，按“是否是父节点 children 列表里的最后一个”决定 `"├─ "` 还是
   `"└─ "`。因为 `_render_forest` 本身写的是通用递归/迭代遍历（不是“只看一层”的硬编码），Part 3 的
   测试数据虽然只有一层，但函数本身已经支持任意深度。
4. **Part 4**：直接复用 `_render_forest`，只是测试数据换成多层嵌套——验证“正确实现的 Part 3 = Part
   4”这条设计洞察。渲染器是**显式栈迭代 DFS**，不是原生递归：因为链式嵌套深度可以达到 `len(lines)`，
   原生递归会在超过 Python 默认递归限制（1000）时抛 `RecursionError`。

## Pitfalls hidden tests target
- **假排序键陷阱**：`timestamp` 字段存在但从不参与排序——测试故意让子任务的 timestamp 依次递减，
  证明实现没有偷偷按 timestamp 排序（`test_timestamps_are_not_a_sort_key`）。
- Part 2 的“统一连接符”是**故意的天真实现**，不是 bug——测试显式断言最后一个子任务在 Part 2 仍然是
  `"├─ "`，而不是提前“抢跑”到 Part 3 的正确规则。
- “最后一个孩子”同时也是“第一个孩子”时（只有一个子任务），Part 3 必须判它为 `"└─ "`（“最后”优先于
  “第一”）。
- 祖先层续接符号的传播规则容易出两种反向 bug：(a) 非最终子节点的后代应该延续 `"│  "`，不是三空格；
  (b) 某个节点自己是“最终子节点”（拿到 `"└─ "`）但它自己还有孩子时，它的孩子的祖先前缀必须是三空格，
  不是 `"│  "`——两个测试分别独立覆盖这两个方向（互为镜像，容易只测对一个方向）。
- CSV 带引号字段：字段内嵌逗号、RFC4180 转义双引号（`""` → `"`），必须走 `csv` 模块而不是手写
  `split(",")`——手写 split 在这两个用例上都会得到错误的字段切分。
- 深链递归陷阱：链式嵌套深度超过 Python 默认递归限制（1000）时，原生递归实现会崩溃；显式栈实现不会。
  同时注意：祖先前缀字符串按深度线性增长，因此“深链”场景的总输出大小是 `O(depth^2)`，量级测试因此改用
  “宽树”（一个根 + ~2×10^5 个直接子节点）而不是深链，避免 perf 用例本身耗尽内存/时间。

## Complexity & measured cost
`_parse_rows` 是 `O(n)`（`csv.reader` 逐行常数开销）；`_build_tree` 是 `O(n)`；`_render_forest` 是
`O(n)`（每个节点入栈出栈各一次，`children.get()` 均摊 O(1)），前缀字符串拼接在“宽树”场景下每行长度
为常数，总输出 `O(n)`。深链场景前缀长度线性增长，总输出退化为 `O(depth^2)`——这正是把大规模用例设计成
“宽树”而非“深链”的原因（见上）。实测：`test_perf_200k_wide_tree`（一个根 + 199,999 个直接子节点）在
预算 2s / 256MB 内完成（实测数字见本回复末尾贴出的 pytest 输出）。

## Test inventory
24 tests — part1: 7 · part2: 4 · part3: 4 · part4: 9（含 1 perf、1 io）; edge: 11 · fmt: 2 · io: 3 ·
perf: 1。（数字为 `pytest --collect-only -m <marker>` 实测计数，非估算。）

## 本题覆盖的知识点
- **S02**（带引号/转义的 CSV 逐行解析）：必须用 `csv` 模块处理 `task_name` 内嵌逗号与转义双引号，
  手写 `split(",")` 在两个 fmt 测试上都会失败。
- **S03**（父子记录建模为树/字典）：`parent_id -> children` 邻接表 + `task_id -> name` 查找表。
- **S08**（严格保留输入兄弟顺序）：`timestamp` 字段存在但绝不参与排序——本题最容易被误判为排序键
  的“假线索”，专门用递减 timestamp 的测试用例验证。
- **S09**（逐字节精确输出格式）：`├─ `/`└─ `/`│  `/三空格四种前缀在任意深度组合下必须逐字节正确，是
  本题的核心考点，专门配了两个互为镜像的祖先前缀传播测试。
- **S19**（Part1→2→3→4 递进式设计）：Part 4 与 Part 3 共用同一个渲染函数 `_render_forest`——如果
  Part 3 写成硬编码单层而不是通用遍历，到 Part 4 就必须重写；写对了则零改动，这是本题唯一真正的“设计”
  考点。

## Open points
- 未确认 PracHub 结构化题面里“parent 保证先于子记录出现”这条约束在真实 HackerRank/CoderPad 环境
  下是否真的成立（题面明说，但候选人原文没有单独确认这一点）——如果拿到更细的转录且这条不成立，
  Part 4 的实现需要改成“先收集所有边、最后统一建树”的两遍扫描，而不是假设单遍重放足够。
- Part 1/2 的具体 worked example（多根、CSV 引号样例）是本套件自行构造的补充用例，不是逐字取自候选
  人报告或 PracHub 页面——如果后续拿到更细的候选人转录（尤其是 Part 1/2 的确切测试数据），应回来核对
  是否需要调整。
