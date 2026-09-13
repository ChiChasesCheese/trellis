# ps08 · Min/Max with Comparator：从"求最小值"一路走到"任意比较器求极值"，练的是"用同一个扫描骨架承接不断变宽的接口"

> [!tldr]
> - 这题考的是：同一件事（找极值）用四种越来越通用的接口表达——固定字段、参数化字段+方向、任意比较器、
>   多个并列赢家——每一步接口变宽，但扫描的骨架不变
> - 三步套路：先看清"这是一个 O(n) 线性扫描问题，不是排序问题" → Part 1 写死一个 `if val < best_val: best = val`
>   → 后面每个 Part 只是把"怎么比较"这一件事换个更通用的表达方式
> - 最值得带走的一个模式：**一次遍历里"顺手记录 best，只在严格更优时更新"，平局判定自动是"先出现的赢"**——
>   不需要额外一次遍历或者显式的 tie-break 分支

## 1. 题目在说什么（人话版）
Stripe 内部工具老要问"这堆记录里最 xxx 的是哪个"——最早的一笔纠纷、今天金额最高的交易、金额最小需要
复核精度的打款。这题练的是把这个需求从"写死一个字段"逐步通用化：先固定按金额求最小，再让调用者传
"哪个字段 + 哪个方向"，再让调用者传一个完全自定义的比较函数，最后处理"不止一个记录并列第一"的情况。

小例子（四条记录，`r2`/`r3` 金额同为 50.00）：
```
按金额求最小 → r2（并列时先出现的赢）
按 amount 然后 created_at 排序求最小 → r3（比较器能表达 r2 表达不了的复合排序）
```
四关的关系不是"越来越难的算法"，是"接口越来越通用"：Part 4 复用 Part 2 的 `(key, mode)`，Part 3 是
另一条独立的、更强的路线（比较器），互不覆盖。

## 2. 读题：把文字变成模型
- **实体**：一条记录（`id, amount, created_at, country`），一个"怎么比较"的规则——这个规则本身从
  Part 1 到 Part 3 越变越通用。
- **输入长什么样**：一行一条记录，逗号分隔，四个字段类型都不同（字符串、`Decimal`、`datetime`、字符串）
  ——这提示"记录不能是裸字符串 list，得先解析成一个带类型的小结构"。
- **输出要什么**：Part 1-3 恰好一个 id；Part 4 可能多个，按 id 字符串序。空输入永远输出 `NONE`，这是
  四个 Part 共同的边界约定。
- **状态**：不需要排序全量数据，只需要"当前见过的最优记录"这一个变量——这是本题最重要的读题结论：
  求极值是 O(n) 问题，不是 O(n log n) 问题，写出 `sorted(...)[0]` 是方法上的浪费。
- **一句话建模**：这是一个 **"比较规则的通用性逐级升级"的单趟扫描找极值问题**——`key/mode` 是比较规则
  的参数化，`comparator` 是比较规则的完全外部化，Part 4 是"收集所有并列者"而不是"选一个"。

> [!note] 为什么选这个数据结构
> 候选是"每次都 `sorted(records, key=...)`  取第一个"，或"单趟扫描维护一个 `best`"。前者简单但对
> Part 3/Part 4 的大数据量是浪费——只要极值，不需要全排序。选单趟扫描还有一个隐藏收益：`if val <
> best_val: best = val` 这一个条件，天然实现了"平局时先出现的赢"（相等时不替换），不用额外写 tie-break
> 逻辑。记录本身用 `NamedTuple` 而不是裸 list，是因为四个字段类型都不同，字段访问用 `.amount` 比
> `record[1]` 更不容易在四个 Part 之间传错下标。

## 3. 下笔顺序（面试里就按这个顺序敲）
1. **骨架先行**：`main()` 读 stdin → 按 `PART n` 分发 → 四个 `partN` 先都返回 `["NONE"]`。定义
   `Record` NamedTuple 和 `parse_records`，先跑通"解析不报错"。
2. **Part 1 最小可用**：`min_by_amount` 就是一个 `for` 循环 + 一个 `if r.amount < best.amount`。用样例
   （r2/r3 并列，r2 先出现）自测，确认"先出现的赢"不用额外代码就对了。
3. **Part 2 叠加**：把"比较哪个字段"和"往哪个方向"变成参数。写一个 `_key_extractor(key)` 返回一个
   取值函数，`extreme` 内部还是同一个扫描骨架，只是比较表达式从写死的 `r.amount` 换成
   `extract(r)`，方向从写死的 `<` 换成 `mode == "min" and val < best_val or mode == "max" and val >
   best_val`。非法 key/mode 提前 `raise ValueError`，别让它悄悄返回错误答案。
4. **Part 3 叠加**：不再要求调用者提供 `key`，直接接受一个 `comparator(a, b) -> int`。骨架不变，只是
   把 `if val < best_val` 换成 `if comparator(candidate, best) < 0`——这一步的关键是让面试官看到你
   认出"这还是同一个扫描"，只是"怎么判断更小"这件事被彻底外包给调用者了。
5. **Part 4 叠加**：不是在扫描骨架里加分支，是先复用 Part 2 的逻辑找到极值（用第一次扫描找出
   `extreme_val`），再第二次遍历收集所有 `extract(r) == extreme_val` 的记录，按 id 排序。这是"contract
   变了"（返回多个而不是一个），所以合理地是一个新函数，不是往老函数塞 `if return_all` 分支。
6. **收尾**：过一遍空输入、单条记录、负数金额、`Z` 与显式偏移量的时间戳这几个边界。

## 4. 代码怎么组织
```
Record(NamedTuple)                              # 4 个字段，类型各不相同
parse_records(lines) -> list[Record]             # 只管解析 + 时间戳归一化
_key_extractor(key) -> Callable[[Record], Any]   # Part 2/4 共用的字段取值分发
min_by_amount(records) -> id|None                # Part 1：写死字段的扫描
extreme(records, key, mode) -> id|None           # Part 2：参数化字段+方向的扫描
extreme_with(records, comparator) -> id|None     # Part 3：比较规则完全外部化的扫描
by_amount_then_created_at(a, b) -> int           # Part 3 在 main() 里用的具体比较器
extreme_all(records, key, mode) -> [id...]       # Part 4：两趟扫描，复用 Part 2 的取值分发
part1..part4(lines) -> list[str]                 # 解析控制行 + 调核心函数 + NONE 兜底
main(stdin, stdout)                              # 只做分发
```
拆分原则：**四个"求极值"函数是并列的四种接口，不是互相调用的四层封装**——`extreme_all` 复用
`_key_extractor`（取值逻辑），但不调用 `extreme`（因为它要收集所有并列者，逻辑形状不同）。这样面试官
问"这四个函数什么关系"时，你能准确说清哪些是真复用、哪些只是接口形状像。

## 5. 核心代码（骨架，≤ 40 行，带注释）
```python
# 只放主线：三种"怎么比较"的扫描 + Part 4 的两趟收集。省略解析和 ValueError 校验细节。
def min_by_amount(records):                       # Part 1：写死字段
    best = None
    for r in records:
        if best is None or r.amount < best.amount:  # 相等不替换 -> 先出现的赢，免费拿到 tie-break
            best = r
    return best.id if best else None

def extreme(records, key, mode):                  # Part 2：字段 + 方向参数化
    extract = _key_extractor(key)                  # amount/created_at/country -> 取值函数
    best, best_val = None, None
    for r in records:
        val = extract(r)
        if best is None:
            best, best_val = r, val
            continue
        if (mode == "min" and val < best_val) or (mode == "max" and val > best_val):
            best, best_val = r, val
    return best.id if best else None

def extreme_with(records, comparator):             # Part 3：比较规则完全外部化
    best = None
    for r in records:
        if best is None or comparator(r, best) < 0:  # 同一个扫描骨架，只是判断方式变了
            best = r
    return best.id if best else None

def extreme_all(records, key, mode):                # Part 4：两趟——先找极值，再收集所有并列者
    if not records:
        return []
    extract = _key_extractor(key)
    extreme_val = extract(records[0])
    for r in records[1:]:
        val = extract(r)
        if (mode == "min" and val < extreme_val) or (mode == "max" and val > extreme_val):
            extreme_val = val
    return sorted(r.id for r in records if extract(r) == extreme_val)
```

## 6. 面试里怎么说（边写边讲）
- 开始前：「我确认一下：Part 1-3 平局都是'输入序里先出现的赢'，Part 4 是唯一一个'把所有并列的都返回'
  的，这两个 tie-break 规则不一样，我按题面分别实现，不试图统一成一套。」
- 写 Part 1 时：「我只维护一个 `best`，严格更优才替换，这样平局天然选中先出现的那个，不用额外写
  tie-break 判断。」
- 写 Part 2 时：「未知的 key 或 mode 我选择直接抛 `ValueError`，而不是默默按某个默认字段比——宁可
  报错也不要悄悄给错答案。」
- 写 Part 3 时：「这里我坚持用单趟扫描而不是 `min(records, key=cmp_to_key(comparator))`——两者复杂度
  一样，但扫描把 tie-break 规则摆在一个 `if` 里，比包一层 `cmp_to_key` 更直观，如果后面要调试'为什么
  选了这条'，看这一行就够了。」然后手动过一遍 r2/r3 的例子，证明比较器选出了跟 Part 1 不一样但同样正确
  的答案。
- 写 Part 4 时：「这是唯一一个返回类型变了的 Part——不是往前三个函数塞'要不要返回全部'的开关，而是
  单独写一个函数：先扫一遍找到极值，再扫一遍收集所有等于极值的记录，按 id 排序。」
- 交付时：「如果要让 Part 4 也支持任意比较器而不只是 `(key, mode)`，我会把 `extract(r) == extreme_val`
  换成 `comparator(record, best) == 0`，函数签名变成 `extreme_all_with`，这个我先口头过一下不写代码。」

## 7. 常见跑偏（方法层面，3 条）
- **每加一个 Part 就多写一次排序**：`sorted(records, key=...)[0]` 能拿到正确答案，但既浪费（只要
  极值不需要全排序）又掩盖了"平局怎么算"这个规则——先想清楚这是扫描问题，再动笔。
- **把 Part 3 的比较器逻辑焊死在只处理 amount 上**：写 `extreme_with` 时如果内部偷偷假设"一定在比
  amount"，遇到只比较 `country` 的比较器就会出错。函数应该对比较器的具体行为一无所知，只负责调用它、
  看符号。
- **Part 4 想复用 Part 1-3 的单赢家函数，硬塞一个"是否返回全部"的布尔参数**：这会让一个函数同时有两种
  返回类型（`str | None` 和 `list[str]`），调用方和测试都变复杂。返回类型变了，就该是一个新函数，哪怕
  内部逻辑看起来相似。

## 8. 同族题 / 延伸
- q03 的用户 id 排序用的是同一条"纯字符串序，不做大小写或数字感知归一化"的规则（`"B" < "a"`，
  `"user10" < "user2"`）——Part 4 的 tie 排序直接复用这个约定，不用重新设计。
- 这题和"先固定实现、再参数化、再完全通用化"的接口设计练习是同一族——练的不是某个算法，是"看清接口
  该在哪一步从'具体字段'升级成'调用者传比较规则'"。
- 延伸思考：如果记录是流式到达而不是一次性给全，Part 1-3 的单个 `best` 可以 O(1) 增量更新；Part 4 的
  "所有并列者"在流式场景下需要额外维护一个"当前并列集合"，遇到严格更优的新记录要整体清空重开——这是
  "批处理转流式"时状态从"一个值"变成"一个集合"的典型例子。
- 练习命令：`python3 -m pytest loop/rounds/03_phone_screen/ps08_minmax_comparator`
