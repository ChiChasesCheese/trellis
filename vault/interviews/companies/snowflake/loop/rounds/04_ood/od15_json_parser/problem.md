# od15 · JSON Parser — 手写 JSON 语法 + 迭代深度 + 路径查询

> TrueInterview 同步清单第 83 题 "Implement a JSON Parser"（LLD，日期不详）。题面付费，确认的
> 骨架只有："解析一个 JSON 值，输出最小化 JSON，非法输出 `INVALID`"。具体语法边界（数字/字符
> 串转义规则）、迭代深度要求、重复键策略、路径查询语言全部 **(reconstructed)**。`json`
> （标准库）只允许出现在测试文件里做交叉验证，`solution.py` 里完全手写。

## 背景

手写一个 JSON 解析器 + 极简化输出器，是"自定义序列化格式"这条技能线（与 od13 的 trie 编码、
od14 的长度前缀编码同族）里最贴近真实语法的一道——JSON 的语法本身有大量容易被面试候选人忽视
的边界（数字不能有前导零、字符串控制字符必须转义、尾随逗号非法），逼你把"语法"这件事讲清楚而
不是含糊地调用 `json.loads` 蒙混过去。

## API 契约（英文签名）

```python
def parse(text: str, on_duplicate_key: str = "last") -> tuple: ...   # internal tagged-tuple tree
def serialize(value: tuple) -> str: ...                               # minified JSON text
def minify(text: str) -> str: ...            # parse(text) 再 serialize；非法输入抛 ValueError
def query_path(value: tuple, path: str) -> str: ...   # Part 3，如 "a.b[2].c"
```

## 规则

### Part 1 — 语法、转义、最小化输出

- 支持 object、array、string、number、`true`/`false`/`null`；值外围允许空白（空格/制表符/换
  行/回车），值之后如果还有非空白字符（哪怕是另一个合法的 JSON 值）→ `INVALID`（trailing
  garbage）。
- **字符串转义**：`\"` `\\` `\/` `\b` `\f` `\n` `\r` `\t` `\uXXXX`；未转义的控制字符
  （码点 < `0x20`）出现在字符串里 → `INVALID`；`\uXXXX` 的高位代理（`0xD800`–`0xDBFF`）必须紧
  跟一个低位代理（`0xDC00`–`0xDFFF`）组成一个完整的增补平面字符，否则 → `INVALID`
  （**(reconstructed)** 的严格化选择：Python 标准库 `json.loads` 对孤立代理是宽容的，本题选择
  更严格，因为孤立代理无法被编码成合法 UTF-8，写到 stdout 会直接崩溃——这条与 `json.loads` 的
  行为差异在 `test_od15.py` 的交叉验证里被显式排除，不作为随机模糊测试的一部分）。
- **数字语法**（比大多数候选人以为的更严格）：`-`? (`0` | `[1-9][0-9]*`) (`.` `[0-9]+`)?
  (`[eE]` `[+-]?` `[0-9]+`)?——**不允许前导零**（`01` 非法，`0.5` 合法）、小数点后必须至少一位
  数字（`1.` 非法）、指数部分至少一位数字（`1e` 非法）；裸的 `NaN`/`Infinity`/`-Infinity` 不是
  合法 JSON 数字 → `INVALID`（**(reconstructed)** 的严格化选择：Python 的 `json.loads` 默认把
  这三个当作非标准扩展接受，本题遵循 RFC 8259 严格拒绝，同样在交叉验证里显式排除）。
- **输出**：最小化（去掉所有值之间的空白），数字原样保留源文本（不重新解析成
  `int`/`float`——`1.50` 不会被"优化"成 `1.5`，`1E+10` 不会被改写成 `1e10`），字符串按下面的
  **规范转义规则**重新输出：

  > **规范转义规则**：只转义 `"`、`\`、五个短转义（`\b \f \n \r \t`）对应的控制字符，以及其它
  > 任何码点 `< 0x20` 的控制字符（转义成小写 `\u00xx`）；**`/` 永远不转义**（源文本里的 `\/`
  > 解码后原样输出 `/`）；**非 ASCII 字符永远不转义**（保留原始 UTF-8 文本，等价于
  > `json.dumps(..., ensure_ascii=False)` 的行为，而不是把每个非 ASCII 字符都编码成 `\uXXXX`）。

### Part 2 — 迭代实现（深度 10 万不递归）**(reconstructed)**

- `parse`/`serialize` 都必须用**显式栈**处理嵌套容器（object/array），不能写
  `def parse_value(): ... parse_value()` 这种 Python 递归——`[[[...]]]` 嵌套 10 万层会在默认
  递归深度上限下直接 `RecursionError`。参考实现的解析器是一个显式栈上的状态机（每个栈帧记录
  "当前容器还在等什么token"），最小化输出器同样是显式栈上的先序遍历（与 od13 的迭代序列化同
  一手法）。

### Part 3 — 重复键策略 + 路径查询 **(reconstructed)**

- `parse(text, on_duplicate_key="last")`（默认）：同一个 object 里出现重复 key，**后出现的值
  覆盖前面的**，但**位置**保持第一次出现时的位置（就像反复对同一个 Python `dict` 赋值）；
  `on_duplicate_key="error"`：只要同一个 object 里出现重复 key 就整体 `ValueError`。
- `query_path(value, path)`：一个小型路径语言，`.` 表示"进入 object 的某个 key"，
  `[N]` 表示"进入 array 的第 N 个元素（0-based）"，两者可以组合，如 `"a.b[2].c"`；路径不存在
  （key 缺失、下标越界、类型不匹配——比如对一个字符串用 `[2]`）在命令流层面统一表现为
  `NOTFOUND`；路径语法本身写错（比如 `"a..b"`、`"a[x]"`）也算 `NOTFOUND`。

### 命令流

```
PARSE <json>                        Part 1/2：输出最小化 JSON，非法 → INVALID
PARSE_DUP <last|error> <json>       Part 3：按策略解析，重复键在 error 策略下 → DUPLICATE，
                                     其它非法 → INVALID
PATH <path> <json>                  Part 3：json 本身非法 → INVALID；路径解析不到 → NOTFOUND；
                                     否则输出该路径处子树的最小化 JSON
```
（`PATH` 把 `path` 放在 `json` 前面，是因为 `path` 语法本身不含空格，而 `json` 可能含空格，这
样才能用简单的 `split(" ", 2)` 无歧义地切开一行命令。）

## Worked examples（全部由 `solution.py` 实际运行得出）

```
PART 1
PARSE {"a": 1, "b": [1,2,3]}    → {"a":1,"b":[1,2,3]}
PARSE {"a":1,}                  → INVALID          (尾随逗号)
```

```
数字原样保留 + 规范转义：
minify('{"num":1.50e+2,"nested":{"x":null,"y":true}}')
  → {"num":1.50e+2,"nested":{"x":null,"y":true}}     (1.50e+2 没有被重新格式化)
minify('"line1\\nline2\\ttab"') → "line1\nline2\ttab"
```

```
PART 2（10 万层嵌套数组，临时调低 sys.setrecursionlimit()）：
text = "["*100000 + "1" + "]"*100000
minify(text) == text     成立，且不抛 RecursionError
```

```
PART 3
PARSE_DUP last {"a":1,"a":2}     → {"a":2}          (后者覆盖，位置不变)
PARSE_DUP error {"a":1,"a":2}    → DUPLICATE
PATH a.b[2].c {"a":{"b":[1,2,{"c":3}]}}   → 3
PATH a.z {"a":1}                 → NOTFOUND         (a 是数字，不是 object，无法再往下 .z)
PATH a bad json                  → INVALID          ("bad json" 本身不是合法 JSON)
```

## 边界清单

- 数字：前导零（`01`）、小数点后无数字（`1.`）、指数无数字（`1e`）、连续负号（`--1`）全部
  `INVALID`；`0`、`0.5`、`-0`、`1e10`、`1E+10`、`-1.5e-10` 全部合法且原样保留源文本
- 字符串：未转义的控制字符、未闭合的字符串、非法转义字符（如 `\x`）、孤立的 UTF-16 代理对
  全部 `INVALID`；合法的高低代理对组合成一个增补平面字符（如 `😀`）正确往返
- 结构：空 object `{}`、空 array `[]`、尾随逗号（object 和 array 都要覆盖）、缺冒号
  （`{"a" 1}`）、缺逗号（`[1 2]`）、value 之后的多余数据（哪怕是另一个合法 JSON 值）全部
  `INVALID`
- 空输入 / 纯空白输入：`INVALID`
- 值外围空白全部被忽略；字符串内部的空白（含字面 tab/换行的转义形式）保留
- 裸 `NaN`/`Infinity`/`-Infinity`：`INVALID`（与 `json.loads` 默认行为不同，见 Part1 规则一节
  的说明，交叉验证测试显式排除这个已知分歧点）
- Part 2：嵌套深度 10 万的数组和对象（`sys.setrecursionlimit()` 调低后）解析 + 最小化输出都不
  抛 `RecursionError`，且在 3 秒预算内完成
- Part 3：重复键在 `"last"` 策略下位置不变、值取最后一次；`"error"` 策略下任何重复键都拒绝；
  `query_path` 对缺失 key、越界下标、类型不匹配（对非 object 用 `.key`、对非 array 用
  `[N]`）、路径语法本身错误统一表现为 `NOTFOUND`（命令流层面），Python API 层面区分抛
  `KeyError`/`IndexError`/`ValueError`

## 追问

1. **为什么数字要原样保留源文本，而不是解析成 `float` 再格式化输出？** 因为 JSON 数字的文本
   表示不是唯一的（`1.50` 和 `1.5` 数值相等但文本不同），如果解析时就转换成 Python 的
   `int`/`float`，往返之后会丢失原始格式（`1.50e+2` 变成 `150.0`），这对"最小化输出"这个目标
   是不必要的信息损耗——本题的"最小化"只针对**空白**，不针对数字的十进制表示，这是候选人容易
   想当然做错的一点。
2. **为什么孤立代理对和裸 `NaN`/`Infinity` 要比 Python 的 `json.loads` 更严格？** 因为
   `json.loads` 的宽容行为（默认接受 `NaN`/`Infinity`，默认允许孤立代理进入 Python 字符串）都
   是 CPython 实现的历史包袱，不是 JSON 标准（RFC 8259）本身要求的；一个"手写、面向规范"的
   JSON 解析器应该讲清楚"我实现的是哪个规范"，并且能解释为什么某些看似合理的输入（孤立代理写
   到 UTF-8 会直接编码失败）必须被拒绝而不是静默接受后在下游炸掉。
3. **`on_duplicate_key="last"` 为什么要保持第一次出现的位置，而不是把重复的 key 挪到最后一次
   出现的位置？** 这模拟的是大多数语言里"字典/映射"数据结构的行为（Python `dict`、Java
   `LinkedHashMap` 的默认语义都是"key 的位置由首次插入决定，值由最后一次赋值决定"）——如果面
   试官追问"这和 JS 的 `JSON.parse` 后面塞进 `Object` 的行为一致吗"，可以顺着讲到"大多数运行
   时环境对象的键序都遵循首次插入序"这条更广泛的语言实现共识。
4. **如果要支持流式解析（不把整个 JSON 读进内存再处理，而是边读边处理超大文档）呢？** 需要把
   现在"先 tokenize 出完整 token 列表、再喂给状态机"的两阶段设计合并成一个真正的增量状态
   机——tokenizer 本身也要能在任意字节边界处"挂起"（比如一个字符串跨越了两次网络包）等待更多
   输入，这是 SAX 风格 JSON 解析器（相对于本题这种 DOM 风格，一次性建出完整树）的核心差异，也
   是这题一个合理但工作量显著更大的延伸方向。

## 来源与置信度

- **MED**：kevin-2023-code/Tech-Interview-Questions（TrueInterview 同步清单）第 83 题
  "Implement a JSON Parser"，LLD，日期不详；正文付费，只见标题、格式标签与"解析一个 JSON 值，
  输出最小化 JSON，非法输出 INVALID"这句预览摘要。见 `../../../catalog/raw/github_repos.md`
  §2 第 83 行、§3 "od15" 一条。
- 具体语法边界（数字/字符串的详细语法）、迭代深度要求、重复键策略、路径查询语言全部
  **(reconstructed)**；数字/字符串语法本身来自 JSON 标准 RFC 8259，不是面试题面本身提供的。

## 考什么

S09 类设计先定契约（先讲清楚"实现的是哪个规范、和 `json.loads` 的已知分歧点在哪"，而不是含糊
地说"标准 JSON"）· 自定义语法解析（与 od13 trie 编码、od14 长度前缀编码同族，但语法本身更复
杂，需要真正的 tokenizer + 结构化状态机）· 迭代实现应对深链/深嵌套输入 · 用统一的路径查询能力
支撑"给我完整文档"和"给我某个子路径"两种查询形状（与 od07 的
`get_inheritance_order`/`succession_after` 同一设计模式）。
