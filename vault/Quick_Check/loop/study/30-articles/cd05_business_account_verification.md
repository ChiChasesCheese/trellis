# cd05 · Business Account Data Verification：规则引擎 = 数据（一份规则表）+ 解释器（一个求值函数）

> [!tldr]
> - 这题考的是：校验一个企业账户的资料是否齐全，但校验规则不是写死在代码里的 if，而是一份 JSON 规则列表（`when`/`requires`/`one_of`），程序要做的是"解释"这份规则，不是"实现"它
> - 三步套路：先把 `when`/`requires`/`one_of` 当成三种"指令"抽出来 → Part 1 只实现 `requires` 这一种指令的解释器 → Part 2 加 `when` 这个"执行前守卫"和 `one_of`/通配这两种新指令，解释器骨架不用重写
> - 最值得带走的一个模式：**规则表是数据，求值是一个函数**——业务方（合规团队）改规则不需要改代码、不需要重新部署，这正是 Stripe 真实 onboarding 系统的做法

## 1. 题目在说什么（人话版）
Stripe 放行一个企业账户之前，要检查资料是否齐全：公司名、经营类型、受益所有人列表、联系方式……
但这些"要求什么字段"的规则经常变——合规团队可能今天要求填 EIN，明天对某类账户改成要 SSN 后四位。
如果这些规则被写成一堆 `if account.business_type == "company": ...`，每次改规则都要改代码、跑测试、
发版。这题让你把规则做成**数据**：一份 JSON 列表，每条说"在什么条件下（`when`），哪些字段必须非空
（`requires`），或者哪一组字段至少要有一个非空（`one_of`）"。程序只写一次，之后改规则只改数据。

小例子：
```
account: {"business_name": "Acme"}
rules:   [{"requires": ["business_name", "ein"]}]
→ 输出:   ein          （business_name 有值，ein 缺失，只报缺的）
```

## 2. 读题：把文字变成模型
- **实体**：`account`（任意深度嵌套的 JSON 对象，只读，不需要修改）；`rule`（一个小 dict，最多带
  三个 key：`when`/`requires`/`one_of`）。没有第三种实体——不用建"用户"或"会话"之类的额外概念。
- **输入长什么样**：第一行 `PART n`，剩下整个是一个 JSON 文档 `{"account": ..., "rules": [...]}`。
  两个 Part 共用一份输入格式，区别只在规则允许出现哪些 key、路径是否允许 `owners[]` 通配。
- **输出要什么**：全部满足 → 单行 `VERIFIED`；否则把所有缺失项按 Python 默认字符串序排序、去重后
  逐行打印。`one_of` 失败时输出的是整段 `one_of(a|b|c)` 字符串，也参与同一次排序——不是"先排普通
  路径再排 one_of"两组拼接。
- **状态**：不需要跨规则的可变状态，只要一个正在累积的"缺失 token 集合"（`set`，天然去重）。每条
  规则、每个路径的判断都是独立的纯函数调用，互不影响。
- **一句话建模**：这是一个 **规则引擎** 问题——规则表是数据，`requires`/`one_of` 是解释器要执行的
  两种"检查指令"，`when` 是执行指令之前的一道守卫（gate），路径里的 `.`/`[]` 是这门迷你 DSL 的
  语法。

> [!note] 为什么选这个数据结构
> 候选方案是"给 `requires` 和通配路径各写一套遍历逻辑"，或者"把路径展开做成一个统一的递归函数，
> 每一段可能返回一个值也可能返回多个（通配时）"。选后者，因为 `owners[].first_name` 和
> `business_name` 本质上是同一件事——"解析路径的下一段，可能落到一个值，也可能落到一组值"——
> 用一个递归函数 `_expand` 统一处理，Part 1 到 Part 2 从"零通配"到"最多一段通配"只是这个函数
> 输入的路径字符串变了，函数本身不用改。缺失 token 用 `set` 收集是因为题面明确要求"去重"，用
> `list` 还得手写去重逻辑，纯粹多余。

## 3. 下笔顺序（面试里就按这个顺序敲）
1. **骨架先行**：`main()` 读第一行拿到 `part`，剩余文本 `json.loads` 成 `doc`，按 `part` 调
   `part1`/`part2`，`"\n".join` 打印。两个 `partN` 先都 `return []`，跑一下确认能读懂输入。
2. **Part 1 最小可用**：写一个单值路径解析 `_resolve_one(node, path)`（按 `.` 一段段走 dict），
   再写"非空"判断 `_is_nonempty`（只有 `null`/`""`/`[]` 算空）。`part1` = 遍历所有规则的所有
   `requires` 路径 → 判断非空 → 缺失的丢进 `set` → 排序输出或 `VERIFIED`。用题面样例自测。
3. **Part 2 叠加**：
   - 先加 `when` 守卫：`_when_matches` 对条件列表做 AND，一条不满足整条规则跳过（连
     `requires`/`one_of` 都不检查）。这是纯新增函数，`part1` 完全不用碰。
   - 把 `_resolve_one` 升级成 `_expand`：能处理路径里最多一段 `owners[]` 通配，返回
     `(展开后的路径, 值)` 的列表而不是单个值。**这一步不是重写，是把"单值返回"改成"列表返回"**，
     `requires` 判断逻辑（判断非空、收集缺失）不用动，只是现在可能一次拿到多个 pair。
   - 加 `one_of`：复用 `_resolve_one`（`one_of` 不支持通配，用单值版就够），任意一个非空就满足，
     否则拼出 `one_of(a|b|c)` 整段字符串加入缺失集合。
4. **收尾**：确认排序是对整个 `set` 一次 `sorted()`，不是分组排序再拼接；确认通配数组为空列表时
   "无元素可查 = 视为满足"，数组整体缺失时"回退输出未展开的字面路径"；跑一遍所有样例。

## 4. 代码怎么组织
```
_split(path) -> list[str]                       # "." 切段
_is_nonempty(value) -> bool                      # 非空定义，两个 Part 共用
_expand(node, segments, prefix) -> [(path,val)]  # 核心：递归路径展开，含 "[]" 通配
_resolve_one(node, path) -> (exists, value)      # when / one_of 用的单值版（无通配）
_when_matches(account, conditions) -> bool       # when 守卫：AND 语义
_missing_for_requires(account, path) -> [str]    # 调 _expand，挑出非空判断失败的
_missing_for_one_of(account, paths) -> str|None  # 调 _resolve_one，拼 one_of(...) token
part1(doc) -> [str]                              # 只用 requires 这一种指令
part2(doc) -> [str]                              # when 守卫 + requires + one_of
main(stdin, stdout)                              # 只做分发
```
拆分原则：**路径展开（怎么从 account 里取到值）和规则语义（requires/one_of/when 分别怎么用这个值）
分成两层**。`_expand`/`_resolve_one` 完全不知道"规则"这个概念，只管路径解析；`part1`/`part2` 完全
不管路径怎么解析，只管拿到值之后怎么判断。好处是面试官问"如果加一种新指令 `forbids`（要求某字段
必须为空）"时，你能明确指出只需要在 `part2` 里加一段调用 `_expand` 的代码，路径解析层一行不改。

## 5. 核心代码（骨架，≤ 40 行，带注释）
```python
# 只放主线：路径展开 → 规则语义 → 输出。省略 _split/_resolve_one/_when_matches 的实现细节。
def _expand(node, segments, prefix):
    """递归解析一条 "." 路径；遇到 "owners[]" 这种通配段就对数组每个元素分别递归。"""
    seg, rest = segments[0], segments[1:]
    if seg.endswith("[]"):
        arr = node.get(seg[:-2]) if isinstance(node, dict) else None
        if not isinstance(arr, list):
            return [(prefix + ".".join([seg, *rest]), MISSING)]      # 数组整体缺失 -> 回退字面路径
        return [
            pair
            for i, elem in enumerate(arr)
            for pair in (
                _expand(elem, rest, f"{prefix}{seg[:-2]}[{i}].")
                if rest
                else [(f"{prefix}{seg[:-2]}[{i}]", elem)]
            )
        ]
    if not isinstance(node, dict) or seg not in node:
        return [(prefix + ".".join([seg, *rest]) if rest else prefix + seg, MISSING)]
    return _expand(node[seg], rest, prefix + seg + ".") if rest else [(prefix + seg, node[seg])]

def part1(doc):                                   # 只有 requires 这一种指令
    account, missing = doc.get("account", {}), set()
    for rule in doc.get("rules", []):
        for path in rule.get("requires", []):
            missing.update(p for p, v in _expand(account, _split(path), "") if not _is_nonempty(v))
    return sorted(missing) if missing else ["VERIFIED"]

def part2(doc):                                   # when 守卫 + requires + one_of
    account, missing = doc.get("account", {}), set()
    for rule in doc.get("rules", []):
        if not _when_matches(account, rule.get("when", [])):
            continue                              # 整条规则跳过，requires/one_of 都不检查
        for path in rule.get("requires", []):
            missing.update(p for p, v in _expand(account, _split(path), "") if not _is_nonempty(v))
        if rule.get("one_of") and (token := _missing_for_one_of(account, rule["one_of"])):
            missing.add(token)
    return sorted(missing) if missing else ["VERIFIED"]
```

## 6. 面试里怎么说（边写边讲）
- 开始前：「我先确认一下：'非空' 只排除 `null`/空字符串/空列表，数字 0 和布尔 false 都算非空；
  `owners[]` 这种通配路径最多允许一段，不会嵌套两层。如果理解错了请打断我。」
- 写 Part 1 时：「我先写一个按 `.` 走 dict 的路径解析，配合一个统一的'非空'判断函数，这两个后面
  Part 2 都要复用，所以我先把接口定清楚。」
- 写 Part 2 时：「`when` 是一个执行前的守卫，不满足直接 `continue`，这样 `requires`/`one_of` 的
  代码完全不用管'规则是否生效'这件事，职责分开。通配路径我把单值解析升级成列表解析，Part 1 的调用
  方代码基本不用改，只是现在拿到的是一组结果。」
- 交付时：「样例都过了。缺失项我用 `set` 收集再统一 `sorted()`，保证 `one_of(...)` 和普通路径混排
  时顺序也是确定的。」
- 被追问"规则集有环/死规则怎么发现"时：「运行时不好查，但可以在规则加载阶段做静态检查——对每个
  `when` 里引用的路径，看它相对 account 的 schema 是否可达，这是一次性的、部署前的检查，不影响
  运行时性能。」

## 7. 常见跑偏（方法层面，3 条）
- **一上来把 `requires`/`when`/`one_of` 用嵌套 if-else 写死在一个大函数里**：Part 1 能跑，但
  Part 2 加 `when` 守卫和通配时，发现"非空判断"和"规则是不是生效"两件事绞在一起，改一处漏一处。
  先把"这是规则引擎"这个判断做出来，把路径解析和规则语义拆成两层，后面加指令才是纯增量。
- **通配和普通路径各写一套遍历**：`requires: ["business_name"]` 一套逻辑，`requires:
  ["owners[].first_name"]` 又临时加个 for 循环——两套逻辑意味着两处都要处理"路径解析不到"的
  情况，容易一个处理了回退语义，另一个漏了。用同一个"可能返回多个 (path, value)"的函数统一处理，
  普通路径只是"返回恰好一个"的特例。
- **排序时把 `one_of(...)` 和普通路径分两组各自排序再拼接**：这题的示例专门构造成
  `one_of(representative.email|representative.phone)` 要排在 `owners[1].first_name` 前面
  （因为 `'n' < 'w'`），如果先输出普通路径组再输出 `one_of` 组，顺序就反了。收集到同一个容器里，
  最后统一排序一次，不要分组处理"最后一步"。

## 8. 同族题 / 延伸
- 同一轮：`cd07 transactions_rules_ai` 是另一版规则引擎——`ALLOW|BLOCK if <condition>`，从关键字
  匹配到 `AND`/`OR`/`NOT` 布尔组合，练的是"规则从平铺到带优先级/短路求值"这条延伸线；OA 侧
  `q12_platform_balance_radar_rules` 是这套模式的生产级语法版本（`:field:` 标记、余额账本）。
  三题共享"规则是数据、解释器是一个函数"这一个核心思路，只是 DSL 复杂度不同。
- 延伸思考：如果要支持 `not`（取反一个 `when` 条件）和嵌套的 `any`/`all` 组合子，当前"扁平字典
  + 特殊 key"的规则表示就不够用了，需要画一棵小型表达式树（`AllOf`/`AnyOf`/`Not`/`Present`/
  `Equals` 节点），`_when_matches` 从"遍历一个 list"变成"递归求值一棵树"，但"规则是数据、有一个
  统一求值入口"这个骨架不变。
- 练习命令：`python3 loop/mock.py start cd05`
