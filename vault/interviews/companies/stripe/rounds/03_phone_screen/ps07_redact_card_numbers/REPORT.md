# ps07 Redact card numbers from logs — 报告

## 概述
"在日志中打码卡号"是 interviewing.io 对一个真实 Stripe 需求的一句话表述：日志汇聚端
绝不能持久化原始 PAN。这道题本质上是 Luhn/网卡校验（q05）换了个马甲 —— 有意思的工程
点不是校验和本身，而是 (a) 在任意自由文本中找出卡号形状的片段，且不使用容易回溯灾难的
正则；(b) 以精确保留周围文本和数字自身标点的方式打码；(c) 把 Luhn+品牌校验当作过滤
假阳性的手段，而不是终点本身。四个部分从朴素的"任意数字形状的一串"启发式，逐步走到
经过校验、可流式处理的打码器 —— 这是 Stripe 电面反复重用的结构（参见 q03、q05、ps05：
朴素做法 -> 加一条规则修正一个具体的错误答案 -> 泛化 -> 扩展规模）。

## 来源与可信度
中等 —— interviewing.io 把"你会怎么在日志中打码信用卡号？"列为一道 coding 轮样题，没有
公开转录（`loop/raw/en_forums.md` 第 6.2 节，C8）；staffengprep 独立列出一道"Valid
Credit Card Number (Redaction)"题目，核心打码逻辑相同（第 3.3 节，P13）但 part 边界
约定不同（先校验后打码，而不是先打码后过滤）。本 problem.md 中除"在自由文本日志中找到
并打码卡号"之外的每一条规则都是本报告的重构 —— 见 problem.md 中的"未解决点"。

## 各部分思路
1. **裸数字串**：一次线性扫描（`_scan_candidates`）找出极大的纯数字串；长度过滤
   `[13, 19]`；对除最后 4 位外的数字打码。此时还没有品牌/Luhn 校验，所以会过度打码
   （演示样例 1c，一个 13 位的 unix-ms 时间戳）。
2. **分隔符**：同一个扫描器让候选串跨越两个数字组之间单个 `' '`/`'-'` 分隔符继续
   延伸（不能连续两个，不能出现在开头/结尾）。打码只替换数字字符，保持每个分隔符不变，
   并且统计的是*最后 4 位数字*，不是最后 4 个字符 —— 这对 AMEX 的 4-6-5 分组很重要
   （`3782-822463-10005` -> `****-******-*0005`，最后一组是 5 个字符但只保留其中最后
   4 位数字）。朴素的按空格拼接反而让过度分组变得更糟，而不是更好（一个总共 13 位数字
   的分组电话号码会被误扫进来，见演示样例 2c）—— Part 3 才是真正的修正。
3. **Luhn + 品牌过滤**：复用 q05 的 Luhn 遍历，但用了更宽的品牌表（新增 Discover 的
   `6011`/`65` 和 Mastercard 的 `2221`-`2720` 区间，二者都不在 q05 的三网卡表中），
   因为本题的任务是"捕获每一个真实 PAN 网络"，而不是"q05 已经深耕过的三个网络"。一个
   候选串当且仅当 `brand_of(digits) is not None and luhn_ok(digits)` 时才被打码 ——
   其余一切（前缀错误、长度错误、形状对但校验和错误）都原样透传，字节级不变。
4. **流式处理**：检测逻辑相同，但设计成每行单遍扫描、没有二次方级的字符串重建
   （list-append + 一次最终 `"".join"`，绝不 `str += `），也没有带嵌套量词的正则，所以
   总开销是 O(所有行长度之和)。追加 `REDACTED n`。

## 隐藏测试针对的坑点
- 打码保持格式：分隔符、标点和候选片段之外的一切原样保留；只有被打码片段内的数字字符
  发生变化
- 一旦涉及分隔符，"最后 4 位"是按*数字*计，不是按*字符*计
- 边界长度：13/19 算，12/20 不算，且长度 >19 的数字串绝不部分打码（不能把它当成"更长
  数字里的前 19 位"，整个都不动）
- 空白日志行必须原样保留为空白行，不能被丢弃 —— 这是日志文本，不是本仓库其他题目那种
  分隔记录格式
- 重复的分隔符或开头/结尾的分隔符会在该处截断链条，而不会被静默吸收进更长的候选串
- 已知的 Luhn 合法"形似卡号"绝不能在 Part 3/4 也被打码：订单/发票号、Unix-ms 时间戳
  （13 位 —— 正好碰上 PAN 的*最短*长度）、分组的国际电话号码（拼接后 13 位以上）
- q05 明确不支持的两个网络（Discover；Mastercard 的 `2221`-`2720` 区间）在这里必须被
  识别并打码 —— `2223003122003222` 在 q05 中是 `UNKNOWN_NETWORK`，但在本题中是一张
  真实、应被打码的 Mastercard 卡
- `REDACTED n` 统计的是过滤后实际被打码的片段数，不是 Part 1/2 那种原始候选串数

## 复杂度与实测开销
O(总输入长度)：每行一次遍历找片段（`_scan_candidates`），一次遍历构建打码后的输出
（`_mask_span` + list join），均以该行长度为界；没有重复扫描，循环里没有 `str +=`。
实测：10 万行日志（每 500 行混入一条真实 PAN，每 137 行混入一条形似时间戳的行，其余为
普通文本），Part 4 端到端（stdin -> stdout）远低于 2 秒，远低于 256 MB 预算 —— 见
`test_perf_100k_lines`。

## 测试清单
27 个测试 —— part1: 9 · part2: 6 · part3: 6 · part4: 6（含 4 个 io、1 个 perf）；edge 12
· fmt 1 · io 4 · perf 1。

## 涉及技能
S02 解析自由文本（非分隔记录）· S09 精确、保格式的输出 · S14 复用 Luhn 数字遍历用于新
用途 · S18 假阳性/校验纪律 · S19 增量式设计（Part 1 是 Part 2 的子集，是 Part 3/4 的
子集）· S21 标准库熟练度，不用回溯型正则

## 电面话术：边写边说什么
1. **读题时**：明确说出这不是 q05 —— q05 问"这个字符串是不是合法卡号"，本题问"这行日志
   里是否藏着一个卡号，如果有该怎么打码"。写代码前先敲定两个契约问题：打码是否保留原始
   分隔符，形似卡号但不是的东西（订单号、时间戳、电话号码）该怎么处理？这两点想错会拖累
   Part 2/3。
2. **写 Part 1 时**：先搭好"找 13-19 位数字串"的扫描器，明确说"我故意先不检查 Luhn ——
   这会导致过度打码，没关系，Part 3 会修正；把检测和校验拆开能让每一层职责单一"。主动
   暴露已知缺陷比表现得完美更加分。
3. **写 Part 2 时**：指出"最后 4 位"指的是数字，不是字符 —— 坑点是 AMEX 的 4-6-5
   分组，最后一组是 5 个字符。同时明确点出权衡："我没有要求 4-4-4-4 这种标准分组形状，
   所以会过度分组像电话号码这样的东西；Part 3 的 Luhn+品牌过滤会把范围收窄回来。"
4. **写 Part 3 时**：复用 Part 1 的 Luhn 遍历（提一句"这和卡号校验题是同一个算法，只是
   应用到了打码流水线里"），先讲"前缀 + 长度必须先匹配一个真实网络，Luhn 才会运行"——
   然后用时间戳和电话号码这两个反例现场证明。
5. **写 Part 4 时**：讲清楚复杂度选择 —— 单遍扫描配合 list-append + 一次最终 join，
   而不是逐行正则替换或字符串 `+=`，所以总开销是 O(输入长度)。如果被问到分块/流式传输
   可能把一个卡号切成两次 read()，坦承当前 API 假设行已经被重组好了，并勾勒（不必完整
   实现）一个在 `process(chunk)` 调用之间携带未解析数字后缀的有状态扫描器。
6. **收尾**：再手动过一遍演示样例（尤其是 2c/3a 这对 —— 先过度打码再修正），然后主动
   提出对一批真实日志做只读运行，对比打码前后的行长度作为上线前的健全性检查 —— 把方案
   和题面中 PCI-DSS 的动机联系起来。

## 未解决点
- interviewing.io 的来源只是一句话，没有公开 I/O 契约、part 数量或演示样例。本
  problem.md 的规则/演示样例是基于 q05 已验证的 Luhn/网络代码、本仓库反复出现的"朴素 ->
  过滤 -> 扩展"电面模板，以及真实 PCI-DSS 部分 PAN 展示惯例所做的合理重构。如果出现
  逐字转录，应据此核对 part 边界。

## 复盘（2026-09-02）
复核通过，本轮未改动 `solution.py`/`starter.py`/`starter_template.py`/`test_ps07.py`（代码已在此前
review 中定型）。
- 快速核对：problem.md 的关键 worked examples（1a/4a 单卡+多卡打码、2c 电话号码过度分组、3a 时间戳/
  电话/订单号被 Part 3 放过、3b 五个品牌样例含 Mastercard `2221-2720`/Discover 新前缀及 Luhn 失败样例）
  已用 `solution.py` 逐字重跑核对 stdin → stdout，全部与文档一致。
- 回归：`rtk proxy python3 -m pytest loop/rounds/03_phone_screen/ps07_redact_card_numbers --tb=short`
  29 passed；`IMPL=starter` 同目录 20 failed / 9 passed（starter 的桩函数默认原样透传输入而非返回空，
  故"不该被打码的行"这类用例恰好也通过，符合设计，不构成空洞测试）。
- Lint：`loop/lint.sh loop/rounds/03_phone_screen/ps07_redact_card_numbers` 直接通过，无需 `--fix`
  （black 110 列 + flake8 F 类 0）。
- `starter.py`/`starter_template.py` 内容仍完全一致，公共 API 与 `solution.py` 一致。
- 遗留：无。problem.md 的"未解决点"（interviewing.io 源为单句无逐字 transcript）已如实标注，不影响
  代码正确性。
- 文章：`loop/study/30-articles/ps07_redact_card_numbers.md`（157 行）。
复核通过，本轮未改动 `solution.py`/`starter.py`/`starter_template.py`/`test_ps07.py`（代码已在此前
review 中定型）。
- 快速核对：problem.md 的关键 worked examples（1a/4a 单卡+多卡打码、2c 电话号码过度分组、3a 时间戳/
  电话/订单号被 Part 3 放过、3b 五个品牌样例含 Mastercard `2221-2720`/Discover 新前缀及 Luhn 失败样例）
  已用 `solution.py` 逐字重跑核对 stdin → stdout，全部与文档一致。
- 回归：`rtk proxy python3 -m pytest loop/rounds/03_phone_screen/ps07_redact_card_numbers --tb=short`
  29 passed；`IMPL=starter` 同目录 20 failed / 9 passed（starter 的桩函数默认原样透传输入而非返回空，
  故"不该被打码的行"这类用例恰好也通过，符合设计，不构成空洞测试）。
- Lint：`loop/lint.sh loop/rounds/03_phone_screen/ps07_redact_card_numbers` 直接通过，无需 `--fix`
  （black 110 列 + flake8 F 类 0）。
- `starter.py`/`starter_template.py` 内容仍完全一致，公共 API 与 `solution.py` 一致。
- 遗留：无。problem.md 的 未解决点（interviewing.io 源为单句无逐字 transcript）已如实标注，不影响
  代码正确性。
- 文章：`loop/study/30-articles/ps07_redact_card_numbers.md`（157 行）。
