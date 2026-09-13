# ps05 · Numeronym validation：把"一条格式规则"长成三段递进的字符串题

> [!tldr]
> - 这题考的是：读懂一条格式规则并守住它（前导零、大小写、digit ≥ 1），然后在后两个 part 里**复用**这条规则而不是重写
> - 三步套路：把 numeronym 抽象成 `(首字母, 省略数, 尾字母)` → 先用一个正则把 Part 1 跑通 → Part 2 用它做过滤、Part 3 用它做分组
> - 最值得带走的一个模式：**"生成会撞车"的题 = 先按"会撞的 key"分组，再只在组内消歧**

## 1. 题目在说什么（人话版）
numeronym 就是程序员常用的缩写法：`internationalization` 太长，保留首尾字母，中间 18 个字母用数字代替，
写成 `i18n`；`kubernetes` → `k8s`。题目分三层：

1. 给你一串字符串，判断每个是不是"长得像 numeronym"（`i18n` 是，`i018n`、`I18n`、`i0n` 不是）；
2. 给一个 numeronym 和一本词典，找出词典里所有它可能代表的词；
3. 反过来，给一本词典，为每个词生成 numeronym——麻烦在于 `cart`/`cost`/`cyst` 都会变成 `c2t`，
   撞车了怎么办？题目规定：多保留几个字母前缀，直到区分开（`ca1t`/`co1t`/`cy1t`）。

小例子：
```
PART 3                      cart -> ca1t
cart / cost / few     →     cost -> co1t
                            few  -> f1w
```

## 2. 读题：把文字变成模型
- **实体**：numeronym（一个字符串，但本质是三元组 `(first, omitted_count, last)`）；dictionary word（`[a-z]+`）。
- **输入长什么样**：第一行 `PART n`；之后每行一个字符串。Part 2 的第一行是 numeronym，其余是词典。
  真正用到的字段只有：首字母、尾字母、长度/省略数。
- **输出要什么**：Part 1 按输入顺序一行一个 `VALID/INVALID`；Part 2 匹配词按字典序，没有就 `NONE`；
  Part 3 `word -> numeronym` 按 word 排序。三个 part 的输出都是"一行一个字符串"，所以 `partN` 统一返回 `list[str]`。
- **状态**：Part 1/2 无状态（逐行判断）；Part 3 需要一个 `dict[base_form, list[word]]` 把会撞车的词攒在一起。
- **一句话建模**：这是一个"**按 (首字母, 尾字母, 长度) 分组**，组内**逐步加长前缀直到互不相同**"的分组消歧问题；Part 1/2 只是这个三元组的验证和反查。

> [!note] 为什么选这个数据结构
> Part 3 的朴素做法是"每个词独立算 numeronym"，一算完才发现重复，再回头修——修谁、修到多长，都说不清。
> 反过来想：两个词的 numeronym 相同 ⇔ 首尾字母和长度都相同 ⇔ base 形式相同。所以直接用 base 形式当
> key 做 `dict` 分组，单元素组直接输出，多元素组才进入消歧循环。撞车判断从"事后比较"变成了"分组时就知道"。

## 3. 下笔顺序（面试里就按这个顺序敲）
1. **骨架先行**：`main()` 读 stdin → 取头行 → 查表分发到 `part1/2/3` → `"\n".join` 打印。三个 part 先返回 `[]`，跑通空输入。
2. **Part 1 最小可用**：一个正则 `^[a-z][1-9][0-9]*[a-z]$` 包成 `is_valid()`；`part1` 就是一行推导式。
   写完立刻把题面那 10 个样例喂进去——**前导零和 `i0n` 这两个坑就是靠 `[1-9]` 这一个字符防住的，边写边说出来**。
3. **Part 2 叠加**：先 `is_valid` 挡掉坏 numeronym（直接 `NONE`），再写一个谓词 `_expands_to(numeronym, word)`：
   长度 = 数字 + 2，首尾相同。过滤 + `sorted` 就完了。词典解析（strip、跳坏行、去重）抽成 `_parse_dictionary`，因为 Part 3 也要用。
4. **Part 3 叠加**：先写 `numeronym_for(word, prefix_len)`——它把"base 形式"和"加长前缀的形式"统一成一个公式
   （prefix_len=1 就是 base）。然后：解析 → 短词直接映射自己 → 其余按 base 分组 → 单元素组直接给 base，多元素组交给 `_resolve_group`。
5. **收尾**：`_resolve_group` 里前缀上限写成 `len - 2` 并注释"再长 digit 就是 0，违反 Part 1"；到上限还撞车就整组退回原词。跑全部样例。

## 4. 代码怎么组织
```
NUMERONYM_RE / WORD_RE / MIN_WORD_LEN       # 规则常量，集中在文件顶部
_clean_lines(lines) -> list[str]            # strip + 去空行（所有 part 共用）
_parse_dictionary(lines) -> list[str]       # 过滤坏行 + 去重（Part 2/3 共用）
is_valid(s) -> bool                         # Part 1 核心，Part 2 直接调用
part1(lines) -> list[str]
_expands_to(numeronym, word) -> bool        # Part 2 的匹配谓词
part2(lines) -> list[str]
numeronym_for(word, prefix_len=1) -> str    # Part 3 唯一的"公式"
_resolve_group(group) -> dict[str, str]     # 组内消歧
part3(lines) -> list[str]
PARTS = {...}; main(stdin, stdout)          # 只做 I/O 与分发
```
拆分的原则：**规则放常量、解析放 helper、每个 part 的"核心谓词/公式"单独成函数**。这样面试官读 `part2` 时
看到的是"过滤 + 排序"，读 `part3` 时看到的是"分组 + 消歧"，不用在一堆 `len(w) - 2` 里找逻辑。后 part 只
新增函数、不改前 part，这就是面试官想看的"增量设计"。

## 5. 核心代码（骨架，≤ 40 行，带注释）
```python
NUMERONYM_RE = re.compile(r"^[a-z][1-9][0-9]*[a-z]$")   # [1-9] 同时挡住前导零和 digit=0
WORD_RE = re.compile(r"^[a-z]+$")

def is_valid(numeronym: str) -> bool:
    return bool(NUMERONYM_RE.fullmatch(numeronym))

def part1(lines):
    return ["VALID" if is_valid(ln) else "INVALID" for ln in _clean_lines(lines)]

def _expands_to(numeronym, word):            # 同首尾、长度 = 省略数 + 2
    omitted = int(numeronym[1:-1])
    return len(word) == omitted + 2 and word[0] == numeronym[0] and word[-1] == numeronym[-1]

def part2(lines):
    cleaned = _clean_lines(lines)
    if not cleaned or not is_valid(cleaned[0]):       # 复用 Part 1
        return ["NONE"]
    words = _parse_dictionary(cleaned[1:])
    return sorted(w for w in words if _expands_to(cleaned[0], w)) or ["NONE"]

def numeronym_for(word, prefix_len=1):       # prefix_len=1 就是 base 形式
    return f"{word[:prefix_len]}{len(word) - prefix_len - 1}{word[-1]}"

def _resolve_group(group):                   # 整组一起加长前缀，直到互不相同
    max_prefix = len(group[0]) - 2           # 再长 digit 就是 0，Part 1 不允许
    for prefix_len in range(2, max_prefix + 1):
        forms = [numeronym_for(w, prefix_len) for w in group]
        if len(set(forms)) == len(group):
            return dict(zip(group, forms))
    return {w: w for w in group}             # 不可消歧：整组退回原词

def part3(lines):
    result, groups = {}, {}
    for word in _parse_dictionary(lines):
        if len(word) < 3:
            result[word] = word              # 没有可省略的字母
        else:
            groups.setdefault(numeronym_for(word), []).append(word)
    for base, group in groups.items():
        result.update({group[0]: base} if len(group) == 1 else _resolve_group(group))
    return [f"{w} -> {result[w]}" for w in sorted(result)]
```

## 6. 面试里怎么说（边写边讲）
- 开始前：「我先确认一下：数字段不允许前导零、必须 ≥ 1，大小写敏感；Part 2 是长度精确相等而不是至少；Part 3 撞车时你希望我报错、去重，还是加长前缀消歧？」
- 写 Part 1 时：「我用一个正则，`[1-9][0-9]*` 而不是 `\d+`，这一个字符同时挡住 `i018n` 和 `i0n`。」
- 写 Part 2 时：「先用 Part 1 的 `is_valid` 挡掉坏输入，匹配条件就是三元组相等——所以我把它写成一个谓词函数。」
- 写 Part 3 时：「两个词撞车当且仅当首尾字母和长度都一样，所以我直接按 base 形式分组，只在组内消歧。前缀上限是 `len - 2`，超过它 digit 就变 0；到上限还撞车，比如 `flap/flip`，我让整组退回原词。」
- 交付时：「样例过了；如果时间允许，我会补一个 property-based test 验证正则和手写扫描等价，以及把大小写不敏感做成一个 `.lower()` 开关。」

## 7. 常见跑偏（方法层面，3 条）
- **Part 3 从"逐词生成"起步**：先算完所有 numeronym 再找重复，会陷入"修哪一个、修到多长"的泥潭。先问"什么条件下会撞"，答案就是分组 key。
- **三个 part 各写一遍解析**：Part 2 写一次 strip/过滤，Part 3 再写一次，然后两处规则不一致（一处去重一处不去重）。解析 helper 第一次就抽出来。
- **公式散落**：`w[0] + str(len(w)-2) + w[-1]` 在 base、消歧、单元素组三处各写一遍——一个 `numeronym_for(word, prefix_len)` 统一，改起来才不漏。

## 8. 同族题 / 延伸
- ps03 Brace expansion：同样是"字符串规则 → 生成"，区别是它靠递归展开，这题靠分组消歧。
- OA 里的"短链接 / slug 生成"类题：本质相同——生成有冲突就退化到更长的形式。
- 练习命令：`python3 loop/mock.py start ps05`
