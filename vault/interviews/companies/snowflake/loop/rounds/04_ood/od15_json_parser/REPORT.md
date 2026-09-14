# od15 JSON Parser — report

## Summary
手写 JSON 解析 + 最小化输出：Part 1 严格语法（数字/字符串转义，含刻意比 `json.loads` 更严格
的两处：拒绝孤立代理对、拒绝裸 NaN/Infinity）→ Part 2 迭代实现（显式栈，深度 10 万不递归，
reconstructed）→ Part 3 重复键策略 + 路径查询语言（reconstructed）。唯一来源是 TrueInterview
同步清单的标题级预览，语法/迭代/重复键/路径全部基于 JSON 标准（RFC 8259）与常见实践重建。

## Sources & confidence
MED：kevin-2023-code/Tech-Interview-Questions（TrueInterview 同步）第 83 题 "Implement a JSON
Parser"，LLD，日期不详，正文付费，只见"解析一个 JSON 值，输出最小化 JSON，非法输出
INVALID"这句预览摘要。

## Approach by part
1. 手写 tokenizer（`_tokenize`）在词法层面校验字符串转义（含代理对合并、拒绝孤立代理）和数字
   语法（无前导零、小数点/指数后必须有数字）；结构层面用一个基于显式栈的状态机
   （`_parse_tokens`）校验括号/逗号/冒号的位置，拒绝尾随逗号和尾随垃圾数据。内部表示是打了标
   签的元组（`('num', 原始文本)` 等），数字永远保留源文本不重新解析，避免 `1.50`→`1.5` 这类
   往返信息丢失。
2. 解析器和最小化输出器（`serialize`）都用显式栈（帧记录"当前容器还在等什么 token"/"下一个要
   emit 的子节点下标"）而不是 Python 递归，10 万层嵌套数组/对象在
   `sys.setrecursionlimit()` 调到 150 时依然能正确处理。
3. `on_duplicate_key` 用一个 `index_by_key` 字典实现"重复键替换、位置不变"（`"last"`）或"检测
   到重复即报错"（`"error"`）；`query_path` 把路径拆成 `[str | int]` 的 token 序列，沿着已解析
   的树逐层下降，类型不匹配/缺失 key/越界下标分别抛 `ValueError`/`KeyError`/`IndexError`，命
   令流层面统一折叠成 `NOTFOUND`。

## Pitfalls hidden tests target
- 数字语法边界：前导零、小数点/指数后缺数字、连续负号
- 字符串：未转义控制字符、非法转义、未闭合、孤立代理对
- 结构：尾随逗号、缺冒号/逗号、尾随垃圾数据、空/纯空白输入
- 裸 `NaN`/`Infinity`/`-Infinity`（比 `json.loads` 默认行为更严格，测试显式排除这个已知分歧
  点，不放进随机交叉验证）
- 规范转义规则：`/` 永远不转义、非 ASCII 永远不转义（等价 `ensure_ascii=False`）
- 10 万层嵌套（数组）/2 万层嵌套（对象）在低递归深度限制下不报 `RecursionError`
- 重复键两种策略、`query_path` 的三种失败模式（类型不匹配/缺失/越界）
- 200 组随机 Python 对象经 `json.dumps` 生成文本，minify 后用 `json.loads` 交叉验证值一致；
  4 种"故意破坏"变异（丢括号、加尾随逗号、丢冒号、丢首字符）逐一验证被拒绝

## Complexity & measured cost
`parse`/`serialize` 均为 O(输入长度)，迭代实现，栈深度 = 嵌套深度，不占用 Python 调用栈。
10 万层嵌套数组的往返 <0.1s；5 万元素扁平数组的端到端脚本远低于 2s 预算。

## Test inventory
36 tests — part1 18（含 1 参数化数字边界展开为多条、2 随机交叉验证）· part2 3（全部 perf）·
part3 8；edge 22 · perf 3 · io 2 · fmt 1。

## Skills exercised
S09 类设计先定契约（先讲清楚实现的是哪个规范、和 `json.loads` 的已知分歧点）· 自定义语法解析
（与 od13 trie 编码、od14 长度前缀编码同族）· 迭代实现应对深嵌套输入 · 统一的路径查询能力同时
支撑"整份文档"和"某个子路径"两种查询形状（与 od07 的双查询接口同一设计模式）。
