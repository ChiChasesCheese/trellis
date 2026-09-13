# ps03 · Brace Expansion：把字符串切成"段"再做笛卡尔积，练的是"一个引擎扛三关"

> [!tldr]
> - 这题考的是：像 shell 一样把 `a{b,c}d` 展开成 `abd, acd`——先能展开，再能识别坏输入原样返回，最后支持嵌套和多组
> - 三步套路：读题确认"保序、不去重" → Part 1 就把模式切成"字面段 / 分组段"然后做笛卡尔积 → Part 2/3 只在前面加一个 yes/no 的校验函数
> - 最值得带走的一个模式：**递归下降 + 段的笛卡尔积**——分组里的每个选项本身又是一个小模式，递归调用同一个 `_expand`，嵌套和多组就"免费"得到

## 1. 题目在说什么（人话版）
你在写一个文件名模板展开器。`/2022/{jan,feb,march}/report` 应该变成三个路径；`read.txt{,.bak}` 变成 `read.txt` 和
`read.txt.bak`（空 token 也是 token）。Stripe 用它来比喻 webhook 端点模板、价格 ID 模板这类"一个模板生成一批字符串"的需求。

三关：Part 1 只有一个 `{...}`，输入保证合法；Part 2 输入可能坏（括号不匹配、`{onlyone}` 只有一个选项、`{}`），
坏了就**原样返回**，不报错；Part 3 允许嵌套 `{a,{b,c}}d` 和多组 `{a,b}{1,2}`，多组之间做笛卡尔积，左边的组是外层循环。

关键约束贯穿全题：**顺序按书写顺序，重复保留**。`{z,a,z}` 就是 `z,a,z`。刷过 LC 1087 的人手会自动写 `sorted(set(...))`——这题恰恰相反。

小例子（Part 3）：
```
{a,{b,c}}d   →  ad,bd,cd          外层两个选项：字面 a、子组 {b,c}；展开后各接上 d
{a,b}{1,2}   →  a1,a2,b1,b2       左组外层、右组内层，和 bash 的 echo {a,b}{1,2} 一致
```

## 2. 读题：把文字变成模型
- **实体**：模式串、段（segment）。一个段要么是一段字面文本（只有一个选项），要么是一个分组（有若干选项）。
- **输入长什么样**：每行一个独立的模式串；`PART n` 决定语法宽严。没有别的字段。
- **输出要什么**：每行一个模式的展开结果，用 `,` 连接，按输入顺序。坏模式 = 输出它自己。
- **状态**：几乎没有跨行状态。行内只需要一个"当前括号深度"来找匹配的 `}` 和在深度 0 处切逗号。
- **一句话建模**：这是一个 **把模式切成段、对段做笛卡尔积** 的问题；嵌套只是"某个选项本身又是一个模式"，递归即可。

> [!note] 为什么选这个数据结构
> 候选方案是"找到第一个 `{`、切 prefix/suffix、对每个 token 拼接"——Part 1 五行就写完，但到 Part 3 多组和嵌套时要推倒重来。
> 改成 `list[list[str]]`（段的列表，每段是选项列表）后，"没有括号"是一个段、"一个组"是两三个段、"多组"是更多段，
> 全部走同一个 `for options in segments: results = [r + o ...]`。多花两分钟，后两关不用重写。

## 3. 下笔顺序（面试里就按这个顺序敲）
1. **骨架先行**：`main()` 读行 → `PART n` → `partN(lines)`，每个 `partN` 就是 `",".join(expand_xxx(p))`。
2. **Part 1 最小可用**：先写两个扫描小工具——`_find_matching(s, i)`（从 `{` 找到配对的 `}`，用深度计数）和
   `_split_top_commas(s)`（只在深度 0 切逗号）。然后 `_segments` 把模式切成段，`_expand` 做笛卡尔积。
   写的时候就让分组的每个选项递归调 `_expand`——Part 1 用不上，但不多花时间。用 `{z,a,z}` 和 `read.txt{,.bak}` 自测。
3. **Part 2 叠加**：写 `_is_well_formed(s)`：和 `_segments` 同样的走法，但只回答 yes/no——`}` 先于 `{` 出现 → False；
   `{` 找不到配对 → False；组内选项 < 2 → False；每个选项递归检查。Part 2 的"最多一组、不嵌套"就是再加一条 `s.count("{") <= 1`。
4. **Part 3 叠加**：去掉那条 `count("{") <= 1`，其余零改动——嵌套和多组在 Part 1 的引擎里本来就支持。
5. **收尾**：核对笛卡尔积方向（左组外层）；确认 `""` 输入返回 `[""]`；跑三关的全部样例。

## 4. 代码怎么组织
```
_find_matching(s, i) -> int            # 括号配对，找不到就 raise（引擎只吃合法输入）
_split_top_commas(s) -> list[str]      # 深度 0 切逗号
_segments(s) -> list[list[str]]        # 模式 → 段；分组段的选项 = 各选项递归 _expand 后拍平
_expand(s) -> list[str]                # 段的笛卡尔积；无括号时自然得到 [s]
_is_well_formed(s) -> bool             # 同样的走法，只回答合法与否（递归到任意深度）
_has_at_most_one_group(s) -> bool      # Part 2 的范围限制，一行
expand_braces / _safe / _nested        # 三个公共 API：（校验）+ _expand，各 3 行
part1..part3 / main                    # join + 分发
```
拆分的核心是**"能不能展开"和"怎么展开"分开**：`_expand` 假定输入合法、专心干活；`_is_well_formed` 不产生任何输出、专心判断。
两者走的是同一条扫描路径，读起来互相印证。三个公共 API 的差别只在"用不用校验、用哪个范围的校验"，面试官一眼能看出 Part 之间的递进关系。

## 5. 核心代码（骨架，≤ 40 行，带注释）
```python
# 只放主线：切段 → 笛卡尔积 → 校验。省略 _find_matching / _split_top_commas（深度计数扫描）与 main。
def _segments(s):
    segments, i, start = [], 0, 0
    while i < len(s):
        if s[i] != "{":
            i += 1
            continue
        if start < i:
            segments.append([s[start:i]])                  # 字面段：只有一个选项
        j = _find_matching(s, i)
        segments.append([out for alt in _split_top_commas(s[i + 1 : j])
                         for out in _expand(alt)])          # 分组段：每个选项递归展开后拍平，保序不去重
        i = start = j + 1
    if start < len(s):
        segments.append([s[start:]])
    return segments

def _expand(s):
    results = [""]
    for options in _segments(s):                          # 左段外层循环 —— bash 顺序
        results = [r + opt for r in results for opt in options]
    return results

def _is_well_formed(s):
    i = 0
    while i < len(s):
        if s[i] == "}":
            return False                                   # 没开就关
        if s[i] != "{":
            i += 1
            continue
        try:
            j = _find_matching(s, i)
        except ValueError:
            return False                                   # 开了没关
        alts = _split_top_commas(s[i + 1 : j])
        if len(alts) < 2 or not all(_is_well_formed(a) for a in alts):
            return False                                   # 选项不够 / 内部再坏
        i = j + 1
    return True

def expand_braces_safe(pattern):                           # Part 2 = 范围限制 + 通用校验
    return _expand(pattern) if s.count("{") <= 1 and _is_well_formed(pattern) else [pattern]

def expand_braces_nested(pattern):                         # Part 3 = 去掉范围限制
    return _expand(pattern) if _is_well_formed(pattern) else [pattern]
```

## 6. 面试里怎么说（边写边讲）
- 开始前：「我先确认一下：输出顺序按书写顺序、重复保留，不是排序去重；空 token 合法；坏输入是原样返回而不是抛异常。」
- 写 Part 1 时：「我把模式切成'段'——字面文本是只有一个选项的段，`{...}` 是多个选项的段——最后对段做笛卡尔积。
  这样'没有括号'和'有一个括号'是同一条代码路径。分组里的每个选项我递归调用展开，现在用不到，但嵌套会免费得到。」
- 写 Part 2 时：「校验和展开我分成两个函数：展开假定输入合法，校验只回答 yes/no。Part 2 的范围是'最多一组、不嵌套'，
  所以在通用校验前面加一条 `count("{") <= 1`。」
- 写 Part 3 时：「Part 3 只需要去掉那条范围限制——嵌套和多组的展开在 Part 1 的引擎里已经支持了。我用 `{a,b}{1,2}` 验证一下顺序是 `a1,a2,b1,b2`。」
- 交付时：「三关样例都过了。复杂度是输出规模线性的；校验是模式长度线性。如果再问'只数个数不列出来'，我会把笛卡尔积改成乘法。」

## 7. 常见跑偏（方法层面，3 条）
- **Part 1 写成"找第一个 `{`、切 prefix/suffix"的特化版**：快，但 Part 3 要推倒重来。看到"后面有 follow-up"就该选一个能长大的表示（段列表）。
- **把校验塞进展开函数里**：`_expand` 里到处 `if j == -1: return [pattern]`，两种职责纠缠，Part 2 和 Part 3 的"合法"定义又不同，改一处漏一处。
  校验单独一个纯函数，展开只吃合法输入。
- **凭肌肉记忆 `sorted(set(...))`**：LeetCode 1087 的契约和这题相反。开始前把"保序、不去重"复述给面试官，是最便宜的保险。

## 8. 同族题 / 延伸
- OA 侧：qA03 `lc1087_brace_expansion` 是同一引擎的"排序去重"版，顺带有 `count_expansions` / `kth_expansion` 两个追问；
  q19 `accept_language` 也是"按书写顺序展开、保序匹配"的字符串题。
- 其他轮：ps07 `redact_card_numbers` 同样是"逐字符扫描 + 状态"的解析题；ps05 `numeronym_validation` 的 Part 2/3 也是"先校验再变换"的分离结构。
- 延伸思考：把 `_expand` 的 `results = [r + opt ...]` 换成 `count *= len(options)` 就是"只数不列"；`kth` 则是按混合进制拆 k。
- 练习命令：`python3 loop/mock.py start ps03`
