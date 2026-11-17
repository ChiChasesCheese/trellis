---
nodes: [lcproject.lcp-parcel-return-policy, parsing-io.parse-errors, errors.boundary-validation, parsing-io.formats, testing.partitioning, ai.verification]
tags: [problem]
---
# Drill：退货策略引擎与严格 JSON 解析修复（Return Approval Engine）

一个退货服务每行读一个 JSON 请求，解析成字典后评估，输出一行 JSON 结果。解析器把超大数字悄悄变成 0、重复的键后一个覆盖前一个；评估器放过多余的字段，几个阈值的边界差一格，退货窗口多算了一天。规模是两个小模块加一个现成的驱动；难点是缺陷分在两层，只看最后一行输出分不清是哪一层错了。

**分关要求**（每关做完再看下一关，像真实的修复轮）
- 第 1 关（约 15 分钟）：先不改代码，把规则逐条对照现有代码写出差异清单。再修解析器的整数：形如 `-?(0|[1-9][0-9]*)`，64 位两端含，溢出是 `invalid_json` 而不是 0，超长数字也一样。每处先写一个会失败的测试。
- 第 2 关（约 15 分钟）：修重复键（按解码后的键判断）。解析器的其余部分起始代码本来就对：只认八种转义，`\u`、原始控制字符、非 ASCII 拒绝；对象之后只能是空白；数组、`null`、小数、指数、尾逗号、前导零拒绝。每一项写一个测试守住，别在改解析器时放宽。
- 第 3 关（约 15 分钟）：修评估器的三处缺陷：恰好六个字段（多余字段被放行）；金额的两个下界含（10000、50000）；窗口是 `> 30`。`True` 不是整数、六个全验完才判、拒绝顺序、被拒绝的请求也返回风险分，起始代码本来就对，留测试守住。
- 第 4 关（选做，约 15 分钟）：核对驱动（起始代码的驱动已经对，这一关是确认并补测试）：一行一结果、空行是 `invalid_json`、坏行不影响后面、`UnicodeDecodeError` 单独处理。最后写三个书面回答：语法错与策略错怎么区分、哪些测试证明溢出与完整消费、换成 JSON 库怎么保持行为。

**怎么练**：把 `vault/domains/low-level-design/problems/lcp-parcel-return-policy/starter.py` 当作要修的服务，改完后在仓库根目录运行
`IMPL=starter uv run --with pytest python -m pytest vault/domains/low-level-design/problems/lcp-parcel-return-policy -q`。

**和编程智能体一起练**：用编程智能体（Claude Code 或工作区自带的智能体）打开 `starter.py`。第一条指令给规则和一个数字例子，要求它先列出代码与规则的差异、不改代码；你核对清单后，一次只让它修一类缺陷、只给它一个失败的测试，改完立刻运行测试。整数范围是否含两端、重复键怎么算、`bool` 是否有效、拒绝规则的顺序这些决定自己留着；期望值自己独立写出，不接受"把测试改成通过"。

**评分点**
- 写得出开工前的合同：子集语法、整数规则、完整消费与重复键、校验先于决定、边界含下界、行隔离（[[lcp-parcel-return-policy-contract-rules]]）。
- 知道 `bool` 是 `int` 的子类，类型检查用 `type(x) is int`，六个字段全验完才判（[[lcp-parcel-return-policy-contract-rules]]、[[lcp-parcel-return-policy-state-and-invariant]]）。
- 说得清语法错与策略错是两层、语法先于策略、驱动只按名字捕获（[[lcp-parcel-return-policy-state-and-invariant]]）。
- 溢出拒绝而不是变成 0，超长数字先看位数，尾部内容与重复键各有测试（[[lcp-parcel-return-policy-reflection-overflow-tests]]）。
- 用标准库 JSON 加子集限制对拍，期望值独立于被测代码（[[lcp-parcel-return-policy-reflection-overflow-tests]]）。
- 能说出换成 JSON 库时哪些规则库放过、要在库外检查，并先冻结行为再并跑对拍（[[lcp-parcel-return-policy-reflection-library-swap]]）。
- 能指挥智能体：规则先行、先列差异、一次一类缺陷（[[lcp-parcel-return-policy-contract-rules]]）。

**题解**：[[solution-lcp-parcel-return-policy]]——先做，再看。

**练习记录**
- [ ] 第 1 次（日期，用时，自评）：
