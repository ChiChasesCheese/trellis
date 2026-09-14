# q42 Loose-Schema Record Aggregation — report

## Summary
一个"上游系统的记录字段随时间漂移、下游必须容忍"的解析/聚合题：每行是空格分隔的
`key=value` token 集合，字段集合逐行可能不同，未知字段要忽略而不是报错。Part 1 按
currency 求和，Part 2 泛化成"按任意一个字段分组"，Part 3 在前两者之上加一个 schema
推断块（每个见过的 key 出现在多少条记录里）。这是"webhook payload / 弱类型账本行"这类
Stripe 集成场景里最常见的一类容错解析题。

## 来源与置信度
档位 **FULL**（1p3a 转录带完整题面：输入格式、三段 PART 规则文字、Part 1/2 的输入输出
样例、以及"Interviewer notes"里对实现结构的期望），但转录文件开头自陈是
"as it would be delivered by the interviewer"——**转录者的重构，不是候选人逐字记录**。
来源：https://www.1point3acres.com/interview/problems/621a72d2-59c8-498a-b252-50be658c6aae
（镜像副本 `catalog/raw/mirror_1p3a_stripe/coding/009__20260413__parse_and_aggregate_records_with_potentially_unknown_fields__oj_621a72d2.txt`）。

**从上游原文拿到的（原样保留）：** 输入语法（`key=value` 空格分隔、字段顺序不保证、未知
key 忽略、同 key 重复取最后一次）；Part 1 的 amount/currency 校验规则（非负整数、`amount`
或 `currency` 缺失即跳过不报错）；Part 2 的"按任意 key 分组 + 缺失字段归入 `__none__`"
规则；Part 3 的"SCHEMA 块列出所有见过的 key 和计数，包括无效记录里的 key"；Part 1、Part 2
各一组完整的输入输出样例（数值原样保留，只是重新包了一层本仓库自己的 `PART n` / header
框架）；"Interviewer notes"里的实现期望（parse 产出 dict、校验是一个单独函数、聚合函数
在 Part 2/3 复用）。

**上游没给、本仓库自己补的：** Part 3 完全没有给出输入输出样例（原文只说"再加一个 SCHEMA
块"），本仓库补了一个；Part 3 的 header 到底是 `N` 还是 `N group_by_key`，原文没说清楚——
本仓库定为"跟 Part 1/2 header 形状一致，看有没有第二个 token"；一个 token 没有 `=` 号时
怎么处理，原文完全没提（只说"值不含空格"），本仓库按"Interviewer notes"里"stay loose"的
精神定为"跳过这个 token，记录其余部分照常解析"；`amount` 的精确合法字符集（本仓库定为
纯数字正则 `^[0-9]+$`，拒绝 `+5`、下划线、小数点），比原文（`amount` 是"parses as
non-negative int"，未指明是否接受 Python `int()` 那种宽松写法）更严格、更可测。

## 逐 part 思路
1. **Part 1**：`parse_record` 把一行拆成 dict（last-wins 天然由 dict 赋值顺序得到，不需要
   额外逻辑）；`extract_valid_amount_and_currency` 是唯一一个校验函数，返回
   `(amount, currency)` 或 `None`；`aggregate_totals` 按 `currency`（或 `(group, currency)`）
   求和。三个函数职责单一，Part 2/3 直接复用。
2. **Part 2**：`aggregate_totals` 多接受一个可选的 `group_by_field` 参数——传 `None` 就是
   Part 1 的行为，传字段名就变成按 `(group, currency)` 分组，`record.get(group_by_field,
   "__none__")` 一行处理"缺失字段"和"字段存在但值为空字符串"两种不同情形（后者结果是分组
   键为空字符串，前者是字面量 `"__none__"`——这两者不能混为一谈，测试专门锁死这一点）。
3. **Part 3**：复用 Part 1/2 的 `aggregate_totals` 渲染总计行，再加一个独立的
   `schema_counts`——对每条记录（不管是否通过校验）遍历它 parse 出来的 dict 的 key 集合，
   每个 key 计数 +1。因为 `parse_record` 已经把同一行内重复的 key 去重成"最后一次生效"的
   单一 dict，`schema_counts` 天然满足"一条记录里出现 3 次的 key 只算 1 次"这条规则，不需要
   额外去重逻辑——这正是上游"Interviewer notes"里说的"Part 3 是免费的，如果 Part 1 结构对
   了的话"。

## Hidden tests 会打的坑
- `amount=0` 有效（非负包含 0），`amount=-1` 无效（跳过不崩溃）——这是最容易搞错符号边界
  的地方。
- `currency=`（key 存在但值为空）按"视为缺失"处理，是无效记录，不是"currency 是空字符串
  的合法分组"。
- Part 2 里"字段缺失"（归入 `__none__`）和"字段存在但值为空字符串"（分组键就是空字符串
  `""`，一个独立于 `__none__` 的合法值）必须区分开，用 `dict.get(key, sentinel)` 而不是
  `dict.get(key) or sentinel` 才能做对（后者会把空字符串也误判成"缺失"）。
- 一行内同一个 key 出现多次，Part 3 的 SCHEMA 计数按"记录数"而不是"出现次数"——`amount=1
  amount=2 amount=3` 只让 `amount` 的计数 +1，不是 +3。
- 无效记录（缺 `amount` 或 `currency`）仍然要贡献它自己的 key 到 SCHEMA——"warts and all"，
  这是很多候选人会漏掉的一条（校验失败就直接 `continue`，忘了在那之前先给 schema 计数）。
- 一个 token 没有 `=`、或者 `=` 前面是空字符串（比如 `=badkey`），只丢弃这一个 token，
  记录里其余合法的 token 照常生效——不能因为一个坏 token 让整条记录作废。
- 排序：Part 1 按 currency 单键排序，Part 2 按 `(group, currency)` 双键排序，Part 3 的
  SCHEMA 块按 key 字母序——三处排序键不同，容易在重构时弄混。
- 大数值（`amount` 最大 `10**15`，最多 `2*10**5` 条记录）求和必须用纯 `int`，不能引入
  `float`（哪怕只是中间过程），否则会有精度丢失。

## 复杂度与实测
所有三个 part 都是 `O(n)`（`n` = 记录数），一次遍历完成解析、校验、聚合（Part 3 再加一次
schema 计数遍历，仍是 `O(n)`）。空间 `O(唯一 key 数 + 唯一分组数)`，远小于 `n`。
实测（`random.Random(0)` 生成 `2×10^5` 条记录，5 种 currency、3 种 region 之一或缺失、
字段顺序每条随机打乱、跑 Part 3 全流程含 SCHEMA）：`test_perf_2e5_records` 通过
`run_script` 子进程测量，预算 2s / 256MB，实测远低于预算（脚本本身在这个规模下运行在
亚秒级）。

## 测试清单
28 个测试——part1: 10（含 1 io）· part2: 6（含 1 io）· part3: 8（含 1 io、1 perf）·
另有 1 个跨 part 的空输入 io 测试；edge: 15 · fmt: 3 · io: 4 · perf: 1
（markers 按主 part marker 计数，edge/fmt/io/perf 可与 part marker 叠加）。

## 本题覆盖的知识点
- **S02**（行式解析）：`key=value` token 解析，显式处理"无 `=`"和"空 key"两种畸形 token，
  以及同一行内重复 key 的 last-wins 规则。
- **S03**（用 dict 建模而非自定义类）：`parse_record` 直接产出 `dict[str, str]`，这是题目
  本身的考点——弱类型记录不应该被强行套进一个固定字段的类里。
- **S04**（group-by 聚合）：Part 1 到 Part 2 是"聚合函数加一个可选分组维度"的泛化，而不是
  重写一遍聚合逻辑。
- **S05**（阈值/有效性语义）：单一校验函数 `extract_valid_amount_and_currency` 判定
  非负整数 + 非空 currency，在三个 part 里原样复用，不重复写校验逻辑。
- **S08**（确定性排序）：Part 1 单键排序、Part 2 双键排序、Part 3 的 SCHEMA 单键排序，三种
  不同的排序键在同一题里连续出现。
- **S09**（精确输出格式）：`SCHEMA` 是字面量分节符；行格式固定为空格分隔，无多余修饰。
- **S18**（校验与错误路径）：所有异常输入（缺字段、非整数、空值、畸形 token）都是"跳过"
  而不是"崩溃"，这是题目反复强调的纪律。
- **S21**（stdlib 熟练度）：`dict`/`collections.defaultdict`、`re.fullmatch`、`sorted` 的
  多键排序（元组比较）。
- **S24**（领域素养）：弱类型 webhook / 账本行 payload 在真实 Stripe 集成里极为常见，"新字段
  随时上线、旧代码不能崩"是这道题真正要考的工程直觉。

## 面试官会怎么追问
- "如果 amount 单位不统一（有的行是分，有的行是元）怎么处理？"——试探候选人是否会想到
  "这题故意没给单位转换规则，因为现实中这类信息通常在别的 metadata 字段里，不能靠猜"。
- "如果 N 和实际记录行数不一致怎么办？"——本题实现选择"以 N 为准，多退少补"（`lines[:n]`），
  可以追问这个选择的权衡（信任声明的计数 vs. 信任实际读到的行数）。
- "Part 3 的 SCHEMA 计数要不要包括从来没在任何记录里出现过、但在某种'预期字段列表'里的
  key？"——本题的答案是"不需要，SCHEMA 只描述实际输入长什么样"，可以引导候选人区分
  "observed schema" 和 "expected schema" 这两个不同概念。
