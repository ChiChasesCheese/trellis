# cd09 Bitfont Repository: Implement Decoders and Compose Them — report

## 摘要
本题是**重建题，置信度 low-medium**。唯一来源是 GitHub `divyavenn/coding_problems` 仓库里的一份
转述文件（`stripe/coding/004__20260423__bitfont_repository_implement_decoders_and_compose_them__oj_c3826719.py`），
该文件自称转录自 1point3acres 某帖，但那个 1p3a 原始 URL 在本轮和上一轮排查中都因 Cloudflare
拦截**完全无法访问核实**。`catalog/discovery/2026-09/C_batchB.md` `## C27` 对这份来源的判定是
"内容详实到面试官逐字讲稿 + 验收标准 + 参考实现的程度，风格更像二次创作而非逐字转录"。本仓库
把里面的 FRAME 格式、FLAGS 位定义、RLE/COMPACT 编码规则、三个 Part 的函数签名**原样保留**（因为
来源本身已经细到函数签名和参考实现，没有"需要仓库自己拟"的空白），只新增了 stdin/stdout 的具体
编码方式（源材料本身用 pytest 直接调函数，没有 stdin/stdout 格式）。

**关键限制**：本仓库同时还建了另外两道同名 "Bitfont" 题（`cd08`、`cd10`），三者规则互不兼容。
这**不代表本题是三者中最不可信的"陪衬"**——只代表三者证据强度不同（cd08 高、本题
low-medium、cd10 仅标题级），而"哪个是真题"这件事本身在现有证据下无法判定。

## Sources & confidence
**置信度：low-medium**。来源列表见 problem.md 底部 Sources 一节。核心风险：这份来源"过于完整"
本身就是一个可疑信号——真实候选人转述通常是碎片化的（记不全规则、记不住确切数字），而这份文件
连"面试官验收标准"("Bit-twiddling is correct -- MSB-first, big-endian length. Off-by-one on RLE
counts is the most common mistake here.")这种元评论都写得像原话，更符合"基于标题做的合理重构"
特征。

## 各 part 设计思路
1. **Part 1**（`part1`，对应源材料 "Decoder A" `decode_glyph`）：三种编码（raw/RLE/COMPACT）各自
   一个私有解码函数，`part1` 只做 flags 位判断 + 分发，不做实际解码——镜像源材料"a small dispatch
   table"的建议。
2. **Part 2**（`part2`，对应源材料 "Decoder B" `iter_frames`）：纯字节游标解析，只看 `LEN`/`FLAGS`
   头三个字节和 payload 的字节数，**完全不解释 payload 内容**——`test_zero_length_payload_frame_
   parses_without_validating_glyph` 专门验证了这一点（`LEN=0` 帧对 Part 2 来说是合法帧，即使
   `flags=0` 时 Part 1 后续会因为 payload 长度不是 8 而报错）。
3. **Part 3**（`part3`）：`[part1(payload, flags) for flags, payload in part2(data)]`，一行代码，
   不引入任何新逻辑——这正是源材料反复强调的"如果 Part 3 需要改 Part 1/2，说明边界画错了"。

## 与源材料的一处刻意偏离（已在 problem.md Clarifications 里声明）
源材料要求 `iter_frames` 是**生成器**，处理 100MB 文件时不能整体读入内存；本仓库的
`part2(data: bytes) -> list[...]` 为了配合 `CONVENTIONS.md` "纯函数返回可比较的 plain data"这条
硬性要求，退化成了"整个字节串读入内存 + 返回列表"。这是本仓库测试框架的限制，不是候选人应该
学到的最佳实践——problem.md 已经把这一点标成"仅供刷题，如果真的考到这题记得练生成器版本"。

## Pitfalls hidden tests target
- RLE 和 COMPACT 位同时置位必须报错，且要在检查完两个标志位之后**优先于**任何 payload 内容检查
  （哪怕 payload 长度也不对，报的应该还是"互斥标志"错误，不是"长度不对"——测试用 `b"\x00"*4`
  这种两种解释下都不合法的 payload 来锁定这个优先级）。
- Part 2 的 `LEN=0` 帧必须被当作合法帧解析出来，不能因为"看起来没有意义"就报错或跳过——这是
  "Part 2 不理解 payload 语义"这条设计原则最容易被破坏的地方。
- `EOFError`（流中断）和 `ValueError`（payload 内容不合法）是两种不同的异常类型，不能混用——
  Part 2 只关心字节数，Part 1 才关心 payload 内容是否合法。
- 大端序 16-bit 长度字段（`LEN_HI<<8 | LEN_LO`）、MSB-first 位提取（`(byte >> (7-col)) & 1`）、
  COMPACT 的高低半字节顺序（高 nibble 是偶数行）——任何一个方向反了都会在几乎所有测试上出错，
  但符号上"看起来能跑"（不会崩溃，只是全错），所以专门留了逐字节手算的 worked examples。

## Complexity & measured cost
`part2`：`O(len(data))`，单次线性扫描。`part1`：`O(1)`（固定 64 像素）。`part3`：
`O(帧数 * 64)` = `O(len(data))`。Perf 测试：20000 个 8 字节 raw 帧（约 220KB 原始流），
通过 `run_script` 测量，预算放宽到 5s（子进程 + 20000 帧的 stdout 拼接本身有常数开销）/
256MB，实测远低于预算。

## Test inventory
22 个测试——part1: 8（含 4 edge、1 fmt）· part2: 6（含 4 edge、1 fmt）· part3: 5（含 1 edge、
1 io、1 perf）；按 marker 汇总：edge 9 · fmt 2 · io 1 · perf 1。

## 本题覆盖的知识点
- **S02**（结构化解析）：定长头部字段 + 变长 payload 的二进制帧格式，而不是本仓库其余题目常见
  的逐行文本解析。
- **S09**（逐字节精确输出）：位网格渲染、payload 十六进制回显（大小写、补零）。
- **S18**（校验与错误路径）：raw/RLE/COMPACT 三条独立的校验路径 + 流截断的 `EOFError`。
- **S19**（Part 边界不可越界）：Part 3 被设计成不能修改 Part 1/2 就能工作，这是源材料明确的
  评分点。
- **候选新增技能，S01–S24 / A01–A16 均未覆盖**：见下方"建议新增技能 S25"。

## 建议新增技能 S25（不修改 skills_matrix.md，仅在此建议）

**建议编号**：S25
**建议名称**：二进制/位操作的帧解码（Binary frame decoding: endianness, bit/nibble extraction,
RLE run-length decode）

**这个技能具体是什么**：
1. 多字节整数字段的字节序组装——本题是 `(LEN_HI << 8) | LEN_LO` 这种显式大端序 16-bit 长度字段，
   一般形式是"从若干个 8-bit 字节按声明的字节序（大端/小端）组装出一个多字节整数"。
2. 单字节内的按位取值，且要认清"哪一端是 MSB / 哪一端是数据里定义的'第一个'元素"——本题是
   "byte 的最高位是最左边的像素"，一般形式是"给定一个整数和一个位索引约定（MSB-first 还是
   LSB-first），提取/设置某一位"。
3. 半字节（nibble）级别的同类操作——本题 COMPACT 编码把一个字节拆成高 4 位、低 4 位分别代表
   两行，一般形式是"把一个字节按更细的位组切片，每组独立解释"。
4. 变长游程编码（RLE）的解码，且要校验"总游程长度之和必须等于声明的总大小"——这是一类常见的
   无损压缩原语，出现在图像/位图/日志压缩等场景。
5. 流式/生成器式解析一个变长记录序列，每条记录先读定长头部得到长度字段，再按长度读变长
   payload，直到 EOF；边界条件是"流恰好用完 vs 流在记录中间截断"要能区分处理。

**为什么现有 S01–S24 / A01–A16 都覆盖不了**：
- 离得最近的是 **S02**（"行式解析，分隔符，类型字段"）和 **S09**（"逐字节精确输出格式"），但
  S02 描述的是**文本**按分隔符切分并转类型（CSV/管道分隔那一类），完全不涉及"按位/按字节序
  组装二进制字段"这件事；S09 描述的是"输出格式精确"，是解码完之后的格式化环节，不覆盖解码
  本身的位运算。
- A01–A16（算法/数据结构目标）里没有任何一项涉及位运算、字节序或 RLE——最接近的是压缩/编码
  概念完全没有出现在这份清单里。
- 简言之：现有清单里"结构化解析"全部隐含"文本、分隔符"这个前提，"二进制协议"是一个缺失的
  维度。

**还有哪些题可能用到这个技能**：
- 本题族的另一个变体如果真的涉及"位图字体的原始编码"（而不是本仓库 cd08 那种已经是 ASCII
  0/1 字符串的版本），大概率也需要类似的位提取。
- Stripe 真实业务里，webhook 签名校验（HMAC 摘要的字节序列比较）、幂等键/游标的 base62/base64
  编码解码、支付网络报文（如部分卡组织的 ISO 8583 风格定长/变长字段报文）都可能涉及类似的
  "字节序 + 位/半字节提取 + 变长字段"技能——如果未来在候选题源里发现这类题目，应该复用 S25
  而不是每次都临时起草一个新描述。
- 如果以后要覆盖任何"自定义二进制协议解析"类的题目（不只是 Bitfont），都应该挂到 S25 上，
  而不是继续认为 S02/S09 已经覆盖。
