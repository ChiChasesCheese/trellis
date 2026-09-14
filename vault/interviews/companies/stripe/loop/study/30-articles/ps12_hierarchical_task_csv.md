# ps12 · Hierarchical Task CSV：事件日志重建任务树，练的是"把 Part 3 写成通用递归，Part 4 就白给"

> [!tldr]
> - 这题考的是：重放一份"任务/子任务创建事件"的 CSV 日志，重建出任务森林，再按 Unix `tree` 命令的连接符规则打印出来
> - 三步套路：用 `csv` 模块（不要手写 `split(",")`）解析成邻接表 → 先写"最后一个孩子用不同连接符"这条规则的**通用**树遍历 → Part 4 的任意深度直接白嫖，因为规则从没变过
> - 最值得带走的一个模式：**如果 Part 3 只覆盖一层就特判"是不是最后一个"，Part 4 就要推倒重写；如果 Part 3 一开始就写成"连接符 + 继承给子孙的前缀"这个通用递归，Part 4 是零代码改动**

## 1. 题目在说什么（人话版）
Stripe 内部的任务系统把"创建任务"和"创建子任务"都记成一行 CSV（时间戳只是格式的一部分，**从来不是排序依据**——它甚至可以乱序出现）。子任务可以任意深度嵌套，但日志保证父记录一定先于子记录出现，所以可以一遍扫描重建树。四个 Part 依次是：只有根任务 → 加上直接子任务（但连接符全用 `├─`，包括最后一个，这是故意留的 bug）→ 修正最后一个子任务用 `└─` → 任意深度嵌套（连接符规则和 Part 3 完全一样，只是深度不再限制在一层）。

```
T1 cook dinner              # 根
├─ T2 buy groceries         # 非最后一个孩子
│  └─ T4 buy milk           # T2 的孩子，因为 T2 自己不是最后一个，前缀继承 "│  "
└─ T3 prepare meal          # T1 的最后一个孩子
```

## 2. 读题：把文字变成模型
- **实体**：任务/子任务，本质是一棵（森林）树，节点是 `task_id`，边是 `parent_id -> task_id`。
- **输入长什么样**：每行是合法 CSV（`csv` 模块解析，`task_name` 可能带引号转义的逗号和双引号）；4 字段是根，5 字段是子任务；`timestamp` 读了就扔，**绝不能拿来排序**。
- **输出要什么**：按输入顺序（不是按 `task_id` 或时间戳）的树形文本行，非根行是 `<继承前缀><连接符><task_id> <task_name>`。
- **状态**：一张邻接表 `children[parent_id] -> [child_id, ...]`（保留输入序）和一个 `name` 查找表，仅此而已——不需要额外的排序结构。
- **一句话建模**：这是一个 **按输入顺序重建森林 + 通用树渲染** 的问题，`timestamp` 是题面故意放的"假排序键"陷阱。

> [!note] 为什么用显式栈而不是递归
> 候选是"每个节点递归渲染自己的子树"，代码更短更直觉，但题面明确给了"深度可达 10 万层的单链子任务"这个 perf 用例——Python 默认递归深度限制是 1000，递归实现会直接 `RecursionError`。换成显式栈的迭代 DFS，深度不再受调用栈限制，且和递归版本产出完全相同的顺序（栈里按"逆序压入"保证弹出时是输入序）。

## 3. 下笔顺序（面试里就按这个顺序敲）
1. **骨架先行**：`main()` 读 `PART n` + 剩余行，分发到 `part1..part4`。先写 `_parse_rows`：用 `csv.reader([raw])` 解析单行（不要手写 split），4 字段是根、5 字段是子任务。
2. **Part 1 最小可用**：过滤出根记录，`f"{task_id} {name}"` 按输入序输出，立刻用样例自测（包括带引号逗号的那条）。
3. **Part 2 叠加**：写 `_build_tree`（`roots` 列表 + `children` 邻接表 + `name` 表），Part 2 遍历 `children.get(root, [])` 时先统一用 `"├─ "`——先让"能跑"的版本过，故意留着最后一个连接符的 bug。
4. **Part 3 叠加，直接写成通用递归/栈**：不要写"只处理一层、单独判断最后一个下标"这种局部逻辑，直接写 `_render_forest`：显式栈存 `(task_id, ancestor_prefix, is_last)`，`is_last` 决定这一行的连接符和传给子孙的继续前缀（`"│  "` 或三个空格）。
5. **Part 4**：如果 Part 3 写对了，`part4` 函数体和 `part3` 完全一样，直接复用 `_render_forest`——这一步是全题的"分水岭"，面试官很爱看你有没有提前把 Part 3 写成通用版本。
6. **收尾**：确认没有任何地方按 `timestamp` 排序；深度测试用一条几千层的单链跑一遍，确认不报 `RecursionError`。

## 4. 代码怎么组织
```
_parse_rows(lines) -> list[Row]                    # csv 模块解析，区分根/子任务
_build_tree(rows) -> (roots, children, name)       # 邻接表，输入序
_render_forest(roots, children, name) -> list[str] # 通用树渲染：显式栈，连接符 + 继承前缀
part1(lines)                                        # 只看 roots
part2(lines)                                        # 一层，连接符全 "├─ "（故意的 bug）
part3(lines) / part4(lines)                         # 都直接调 _render_forest，函数体相同
main(stdin, stdout)
```
拆分原则：**解析、建树、渲染三层分离**，渲染层从写下第一行代码起就按"任意深度"设计，不针对"只有一层"做特殊优化——这样 Part 2 到 Part 3 到 Part 4 的代码增量是递减的（Part 2 引入邻接表，Part 3 引入通用渲染，Part 4 引入 0 行新代码），这条曲线本身就是这题想考的"预判后面会怎么扩展"的能力。

## 5. 核心代码（骨架，≤ 40 行，带注释）
```python
# 只放主线：解析 -> 建树 -> 通用渲染。省略 CSV 引号细节与 5 字段/4 字段的具体拆解。
def _build_tree(rows):
    roots = [r.task_id for r in rows if r.kind == "task"]
    name = {r.task_id: r.name for r in rows}
    children = defaultdict(list)
    for r in rows:
        if r.kind == "subtask":
            children[r.parent_id].append(r.task_id)     # 保留输入序，不排序
    return roots, children, name

NON_FINAL, FINAL = "├─ ", "└─ "
NON_FINAL_ANCESTOR, FINAL_ANCESTOR = "│  ", "   "

def _render_forest(roots, children, name):
    out = []
    for root in roots:
        out.append(f"{root} {name[root]}")
        stack = []                                        # (task_id, ancestor_prefix, is_last)
        kids = children.get(root, [])
        for i in range(len(kids) - 1, -1, -1):             # 逆序压栈 -> 弹出时是输入序
            stack.append((kids[i], "", i == len(kids) - 1))
        while stack:
            task_id, prefix, is_last = stack.pop()
            connector = FINAL if is_last else NON_FINAL
            out.append(f"{prefix}{connector}{task_id} {name[task_id]}")
            next_prefix = prefix + (FINAL_ANCESTOR if is_last else NON_FINAL_ANCESTOR)
            grand = children.get(task_id, [])
            for i in range(len(grand) - 1, -1, -1):
                stack.append((grand[i], next_prefix, i == len(grand) - 1))
    return out

def part4(lines):                                          # Part3 和 Part4 完全一样
    roots, children, name = _build_tree(_parse_rows(lines))
    return _render_forest(roots, children, name)
```

## 6. 面试里怎么说（边写边讲）
- 开始前：「我确认一下——`timestamp` 只是日志格式的一部分，输出顺序看的是输入行序，不是按时间排序，对吧？」
- 写解析时：「`task_name` 可能带引号转义的逗号，我用 `csv` 模块而不是手写 `split(",")`，否则遇到 `"say ""hi"" now"` 这种字段会直接拆错。」
- 写 Part 3 时：「我不打算只处理一层再特判最后一个，我直接写一个支持任意深度的通用渲染——这样 Part 4 基本不用改代码，也顺便避开了后面深度很大时的递归栈溢出，我用显式栈实现。」
- 交付时：「四个 Part 都过了；我特意用一条几千层的单链子任务测了一下渲染函数，确认没有 `RecursionError`。」

## 7. 常见跑偏（方法层面，3 条）
- **把 Part 3 写成"只处理一层，判断 `i == len(list)-1`"的局部逻辑**：能过 Part 3 但 Part 4 一来就要整个重写，因为"继承前缀"这个概念在只有一层时根本不需要存在。看到"最后一个连接符不同"这种规则时，先想"这条规则会不会在更深的层级也成立"，成立就直接写通用版本。
- **拿 `timestamp` 当排序键**：小样例里输入顺序和时间戳顺序恰好一致，看起来"排序一下也没错"，直到 hidden test 故意把 `timestamp` 打乱才暴露——读题看到"这个字段存在但规则里从没提它要排序"就要留个心眼，不要凭直觉加 `sorted`。
- **解析和渲染没分层，导致 CSV 转义细节散落在渲染函数里**：`_render_forest` 只应该知道"谁是谁的孩子、名字是什么"，完全不该知道 CSV 引号规则；反过来 `_parse_rows` 也不该关心连接符——混在一起会导致改一处引发另一处的连锁调试。

## 8. 同族题 / 延伸
- 同族模式：任何"S09 字节级/格式级精确输出"题（连接符、缩进、固定宽度对齐）都要求"格式规则集中在一个渲染函数里"，不要让格式判断散落到解析或建树逻辑中——这题的 `_render_forest` 就是这条纪律的示范。
- 延伸思考：如果要支持"展开/折叠某个节点"（前端常见需求），只需要在 `_render_forest` 加一个"跳过其子树"的判断，不影响解析层；如果要支持"倒着渲染"（子节点在前），要改的是 `_build_tree` 的邻接方向，不动渲染逻辑。
- 练习命令：`python3 loop/mock.py start ps12 -m 45`
