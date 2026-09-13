# ps07 · Redact Card Numbers from Logs：在自由文本里"找到形似卡号的片段再决定要不要打码"，练的是"探测"和"验证"分两层写

> [!tldr]
> - 这题考的是：从日志这种自由文本里揪出"长得像卡号"的数字片段并打码——先写一个宽松的探测器（找出所有
>   候选），再叠一层验证器（Luhn + 品牌前缀过滤假阳性），两层职责不能揉在一起
> - 三步套路：先认清这是"自由文本扫描"不是"分隔记录解析" → 写一个单趟、只前进不回溯的候选片段扫描器
>   → 后面每个 Part 只是给扫描器加能力（吸收分隔符）或给候选加过滤（Luhn+品牌），扫描器本身不重写
> - 最值得带走的一个模式：**探测（这段文字长得像卡号）和验证（这确实是卡号）是两个独立的函数**——
>   探测器越宽松越好写，假阳性完全交给验证层收窄，不要试图让探测器一步到位就精确

## 1. 题目在说什么（人话版）
Stripe 的日志管道不能把原始卡号落盘，这是 PCI-DSS 硬性要求。题目要求写一个日志脱敏器：扫一行日志文本，
找出里面形似卡号的数字片段，把除了最后 4 位之外的数字换成 `*`，其余文字原样保留。天真版本（"看到 13-19
位连续数字就打码"）会误伤订单号、时间戳；题目让你一步步加过滤条件把它变成真正能上生产的脱敏器。

小例子：
```
user 4242424242424242 charged $10   →   user ************4242 charged $10
{"ts":1735689600000,...}            →   不变（13 位时间戳，Part 3 起不再误伤）
```
四关：Part 1 找纯数字串打码（会误伤）；Part 2 让候选可以带空格/`-`分组（误伤更严重）；Part 3 加
Luhn+品牌过滤修正误伤；Part 4 要求单趟线性扫描撑住 10 万行规模，并追加统计行。

## 2. 读题：把文字变成模型
- **实体**：一行日志文本（不是分隔字段，是任意自由文本），文本里零个或多个"候选片段"（一段数字，或
  数字+分隔符的链），每个候选片段要么是真卡号要么不是。
- **输入长什么样**：整行原样读入，**空行是日志内容要保留，不能当成分隔符跳过**——这句话在题面里很容易
  漏读，一旦漏读会导致输出行数和输入不一致。
- **输出要什么**：行数和输入一一对应，每行内该打码的片段打码、其余字节不变。Part 4 末尾多一行统计。
- **状态**：不需要跨行状态——每行独立处理；但每行内部需要"当前扫到哪、当前候选片段从哪开始"这类局部
  游标状态，这决定了要写一个手工的单趟扫描器，而不是用一次正则整体匹配再后处理。
- **一句话建模**：这是一个 **"先探测候选（宽松），再验证候选（严格），两层职责分离"的自由文本脱敏
  问题**——探测负责"形状像不像"，验证负责"是不是真的"，打码只是把验证通过的候选片段重写。

> [!note] 为什么选这个数据结构
> 候选是"一个大正则一次性匹配再判断"，或"手写一个字符级单趟扫描器"。选手写扫描器的原因有两个：一是
> 正则在允许分隔符、要求不能连续两个分隔符这类规则下容易写出灾难性回溯的模式；二是打码需要精确知道
> "这个候选片段里第几个字符是第几个数字"（最后 4 位数字，不是最后 4 个字符），手写扫描器天然拿到这个
> 位置信息，正则事后还要再扫一遍字符串去定位。扫描器返回 `Span(start, end, digit_count)`，探测和验证
> 之间只传这一个轻量元组，两层完全解耦。

## 3. 下笔顺序（面试里就按这个顺序敲）
1. **骨架先行**：`main()` 读 stdin → 按 `PART n` 分发 → 四个 `partN` 先原样透传（`return list(lines)`），
   确认行数不变、空行不丢。
2. **Part 1 最小可用**：写 `_scan_candidates`（找纯数字最大连续段），过滤长度在 `[13,19]`，写
   `_mask_span`（除最后 4 位数字外全换 `*`）。用样例 `4242424242424242 → ************4242` 自测，
   顺手测一下 12 位/20 位不该被打码。
3. **Part 2 叠加**：给 `_scan_candidates` 加一个开关 `allow_separators`——扫到数字后如果下一个字符是
   单个空格或 `-` 且再下一个字符还是数字，就把分隔符也吸收进候选，继续扫描；连续两个分隔符或候选收尾
   在分隔符上都要停止。**打码时数满 4 位是数数字，不是数字符**——AMEX 的 `4-6-5` 分组最后一组是 5 个
   字符但只有 4 个数字要保留，这是这题最容易漏的格式化细节。
4. **Part 3 叠加**：复用 Part 2 的扫描器（`allow_separators=True`），新增一层过滤：把候选片段里的
   纯数字提出来，跑 Luhn 校验 + 查品牌前缀表，两者都过才真正打码，否则原样保留。这一步不改扫描逻辑，
   只改"要不要打码"这一个判断。
5. **Part 4 叠加**：检测逻辑和 Part 3 完全一样（已经是单趟），只是要确认整体是 `O(总输入长度)`——
   用 list 收集片段最后一次 `join`，不要在循环里 `str +=`；额外统计打码次数，末尾加一行 `REDACTED n`。
6. **收尾**：过一遍时间戳、电话号码这类"形似卡号但不是"的样例，确认 Part 3/4 真的放过了它们。

## 4. 代码怎么组织
```
NETWORK_RULES                                    # (品牌, 长度, 前缀位数, 前缀下限, 前缀上限) 常量表
luhn_ok(digits) -> bool                          # 复用 q05 的 Luhn 逐位校验
brand_of(digits) -> str | None                   # 查表：长度 + 前缀匹配哪个品牌
is_card_number(digits) -> bool                   # brand_of 命中 且 Luhn 通过
_scan_candidates(line, allow_separators) -> [Span]   # 唯一的扫描器，Part 1-4 共用
_mask_span(text, digit_count) -> str             # 唯一的打码函数，按数字计数保留最后 4 位
_qualifies(line, span, check_luhn_brand) -> bool # 长度窗口 + 可选的 Luhn/品牌过滤
_redact_line(line, allow_separators, check_luhn_brand) -> (new_line, count)  # 扫描+过滤+打码串起来
part1..part4(lines) -> list[str]                 # 只传两个策略开关给 _redact_line，不含扫描/打码逻辑
main(stdin, stdout)                              # 只做分发
```
拆分原则：**四个 Part 的区别只是传给 `_redact_line` 的两个布尔开关**（`allow_separators`、
`check_luhn_brand`），扫描、打码、校验这三段核心逻辑一次写好，四个 Part 零重复代码。这样面试官问
"如果要加 Part 5：只脱敏 VISA"，你能准确指出只需要在 `_qualifies` 加一个品牌白名单参数，别的都不动。

## 5. 核心代码（骨架，≤ 40 行，带注释）
```python
# 只放主线：扫描候选 → 过滤 → 打码。省略 Luhn 校验和品牌表细节（详见 q05）。
def _scan_candidates(line, allow_separators):        # 单趟：i 只前进，不回溯
    spans, n, i = [], len(line), 0
    while i < n:
        if not line[i].isdigit():
            i += 1
            continue
        start, count = i, 0
        while i < n:
            if line[i].isdigit():
                i, count = i + 1, count + 1
            elif allow_separators and line[i] in " -" and i + 1 < n and line[i + 1].isdigit():
                i += 1                                # 吸收一个分隔符，前提是它后面紧跟数字
            else:
                break
        spans.append(Span(start, i, count))
    return spans

def _mask_span(text, count):                          # 只数数字，分隔符原样透传
    mask_upto, out, seen = count - KEEP_LAST, [], 0
    for ch in text:
        if ch.isdigit():
            out.append("*" if seen < mask_upto else ch)
            seen += 1
        else:
            out.append(ch)
    return "".join(out)

def _qualifies(line, span, check_luhn_brand):          # 长度窗口永远查；Luhn+品牌按需查
    if not (13 <= span.digit_count <= 19):
        return False
    if not check_luhn_brand:
        return True
    digits = "".join(ch for ch in line[span.start:span.end] if ch.isdigit())
    return is_card_number(digits)

def _redact_line(line, allow_separators, check_luhn_brand):
    pieces, cursor, redacted = [], 0, 0                # list + 一次 join，避免 O(n^2) 拼接
    for span in _scan_candidates(line, allow_separators):
        if not _qualifies(line, span, check_luhn_brand):
            continue
        pieces.append(line[cursor:span.start])
        pieces.append(_mask_span(line[span.start:span.end], span.digit_count))
        cursor, redacted = span.end, redacted + 1
    pieces.append(line[cursor:])
    return "".join(pieces), redacted
```

## 6. 面试里怎么说（边写边讲）
- 开始前：「我确认两点：打码要保留原始的空格/`-`分组，不是换成统一的 `••••` 展示；空行是日志内容，
  要在输出里原样保留，不能被当成分隔符跳过。」
- 写 Part 1 时：「我先只做形状探测，不查 Luhn——这会误伤时间戳之类的东西，我知道，这是故意的，Part 3
  会用校验层修正，先把探测和验证拆成两个职责。」
- 写 Part 2 时：「'保留最后 4 位'我数的是数字个数不是字符个数，AMEX 是 4-6-5 分组，最后一组 5 个字符
  但只留 4 个数字——这是最容易漏的格式化细节，我先确认题面口径。」
- 写 Part 3 时：「过滤逻辑复用了 Luhn 校验，这跟卡号校验题是同一个算法，只是这里是拿它当'排除假阳性'
  的工具，不是终点。」然后用时间戳和电话号码的例子过一遍，证明确实被放过了。
- 写 Part 4 时：「扫描本来就是单趟，我这里额外注意的是不要用字符串 `+=` 拼接结果，改成 list 收集最后
  一次 `join`，避免整体退化成 O(n²)。」
- 交付时：「如果日志是分块流式到达、卡号可能被切断在两次 `read()` 之间，现在的 API 假设行已经拼好了；
  真要支持这个，需要一个有状态的扫描器在 chunk 之间带一个'未完成的数字后缀'，我可以口头画一下接口
  但不现场全写。」

## 7. 常见跑偏（方法层面，3 条）
- **一上来就想用一个大正则把探测和验证都塞进去**：`\d[\d -]{11,23}\d` 这类模式在带分隔符规则下容易写出
  灾难性回溯，而且拿不到"第几个字符对应第几个数字"这种打码需要的位置信息。手写扫描器一次搞定两者。
- **探测器想一步到位就精确，混入 Luhn/品牌判断**：这会让 Part 1 的"故意过度打码"这个教学点消失——
  题目的重点恰恰是"先宽松探测、再严格验证"这个分层，硬要一步到位反而丢了这道题真正在考的东西。
- **打码时数"保留的字符数"而不是"保留的数字数"**：遇到带分组分隔符的号码（尤其 AMEX 的 4-6-5）会
  算错保留几位。写 `_mask_span` 前先把"最后 4 位"在题面里确认清楚是指数字还是字符。

## 8. 同族题 / 延伸
- q05 `card_validation_luhn` 是这题的"下游依赖"：Luhn 算法和品牌前缀表在这里被直接复用，但 q05 问的是
  "这个字符串是不是合法卡号"，这题问的是"这行文本里有没有藏一个"——不要把两题的 Part 进度搞混，这题
  不重新做 q05 的通配符补全/损坏字符枚举那部分。
- ps05 `numeronym_validation` 同样是"先写一个宽松规则，再叠加过滤条件收紧"的方法论，只是应用在不同
  的字符串规则上。
- 延伸思考：把品牌表从 4 行扩展到支持 JCB/银联，只需要在 `NETWORK_RULES` 加行，扫描器和 Luhn 校验完全
  不用动——这正是"探测"和"验证"分层带来的收益：新增一个验证规则不影响探测逻辑。
- 练习命令：`python3 -m pytest loop/rounds/03_phone_screen/ps07_redact_card_numbers`
