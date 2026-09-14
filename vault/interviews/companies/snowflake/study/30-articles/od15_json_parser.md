# od15 · JSON Parser：手写语法 + 迭代深度 + 数字原样保留

> [!tldr]
> - 这题考的是：手写一个 JSON tokenizer + 结构化解析器 + 最小化输出器，逼你把"语法"讲清楚而不
>   是含糊调用 `json.loads`——外加迭代深度、重复键策略、路径查询三层追问
> - 三步套路：先写严格语法的 tokenizer（数字不能有前导零、字符串控制字符必须转义）→ 解析器和
>   最小化输出器都用显式栈而不是 Python 递归 → 加重复键策略和 `a.b[2].c` 式路径查询
> - 最值得带走的一个模式：**"最小化输出"只针对空白，不针对数据本身的文本表示——数字必须原样
>   保留源文本（`1.50` 不能被"优化"成 `1.5`），因为同一个数值可以有多种合法的文本表示，解析时
>   过早转换成 `float` 会造成不可逆的信息丢失**

## 1. 题目在说什么（人话版）

解析一段 JSON 文本成内部表示，再输出去掉全部空白的最小化 JSON；输入不合法就报告 `INVALID`。
听起来像调用一次 `json.loads`/`json.dumps` 就完事，但面试要求手写，逼你把 JSON 语法里那些容
易被忽视的边界讲清楚：数字不能有前导零、字符串里的控制字符必须转义、尾随逗号非法。

三行小例子：
```
minify('{"a": 1, "b": [1,2,3]}')  -> '{"a":1,"b":[1,2,3]}'
minify('{"a":1,}')                 -> 抛 ValueError（尾随逗号，命令流层面输出 INVALID）
minify('"line1\\nline2"')          -> '"line1\nline2"'
```

## 2. 读题：把文字变成模型

- **实体**：JSON 值（object/array/string/number/bool/null）、token 流、嵌套容器的"打开中"帧。
- **输入长什么样**：`text: str`；Part 3 额外有 `on_duplicate_key` 策略、路径字符串
  `"a.b[2].c"`。
- **输出要什么**：最小化 JSON 文本，或 `INVALID`；Part 3 的路径查询返回子树的最小化 JSON 或
  `NOTFOUND`。
- **状态**：内部表示是打了标签的元组（`('num', 原始文本)`、`('obj', [(key,value),...])` 等），
  数字永远保留源文本不重新解析；解析/序列化都用显式栈管理"当前容器还在等什么"。
- **一句话建模**：这是一道**自定义语法解析**题——tokenizer 负责词法层面的转义/数字校验，栈式
  状态机负责结构层面的括号/逗号/冒号校验。

> [!note] 为什么要比 `json.loads` 更严格
> Python 标准库 `json.loads` 默认宽容地接受孤立 UTF-16 代理和裸 `NaN`/`Infinity`，这些都是
> CPython 的历史包袱，不是 RFC 8259 标准本身要求的。孤立代理无法被编码成合法 UTF-8，写到
> stdout 会直接崩溃；一个"手写、面向规范"的解析器应该讲清楚自己实现的是哪个规范，并主动拒绝
> 这些看似合理、实则会在下游炸掉的输入。

## 3. 下笔顺序（面试里就按这个顺序敲）

1. **骨架先行**：写 `_tokenize(s)`，在词法层面校验字符串转义（`\"` `\\` `\/` 五个短转义
   `\uXXXX`）和数字语法（无前导零、小数点/指数后必须有数字）。
2. **Part 1 最小可用**：写一个基于显式栈的结构化解析器，校验括号/逗号/冒号位置，拒绝尾随逗号
   和尾随垃圾数据；配一个同样迭代的 `serialize`，字符串按规范转义规则重新输出（`/` 永远不转
   义、非 ASCII 永远不转义）。
3. **Part 2 叠加**：确认解析器和序列化器都没有用 Python 递归——10 万层嵌套数组的输入必须能扛
   住 `sys.setrecursionlimit()` 调低后的限制。
4. **Part 3 叠加**：`parse(text, on_duplicate_key="last"|"error")` 用一个 `index_by_key` 字典
   实现"重复键替换、位置不变"或"检测到即报错"；`query_path` 把路径拆成 `[str|int]` token 序列
   沿树下降。
5. **收尾**：跑一遍数字/字符串语法的边界清单，用 `json.dumps` 生成的随机文本做交叉验证（显式
   排除孤立代理和裸 `NaN`/`Infinity` 这两个已知分歧点）。

## 4. 代码怎么组织

```
_tokenize(s) -> list[token]                   # 词法：字符串转义、数字语法在这一层校验
_parse_tokens(tokens, on_duplicate_key)        # 结构：显式栈状态机，校验括号/逗号/冒号
parse(text, on_duplicate_key="last") -> tuple  # tokenize + parse_tokens + 检查尾随数据
_escape_string(s) -> str                       # 规范转义规则集中一处
serialize(value) -> str                        # 显式栈迭代先序遍历，minify 输出
query_path(value, path) -> str                 # Part3：路径 token 化 + 沿树下降
```

## 5. 核心代码（骨架，≤ 40 行，带注释）

```python
def _scan_number(s, i):
    # 不允许前导零；小数点/指数后必须至少一位数字——比大多数人以为的更严格。
    start = i
    if s[i] == "-":
        i += 1
    if s[i] == "0":
        i += 1                          # 前导零只允许单独一个 '0'，不能是 "01"
    else:
        while i < len(s) and s[i].isdigit():
            i += 1
    if i < len(s) and s[i] == ".":
        i += 1
        if not (i < len(s) and s[i].isdigit()):
            raise ValueError("expected digit after '.'")
        while i < len(s) and s[i].isdigit():
            i += 1
    if i < len(s) and s[i] in "eE":
        i += 1
        if i < len(s) and s[i] in "+-":
            i += 1
        if not (i < len(s) and s[i].isdigit()):
            raise ValueError("expected digit in exponent")
        while i < len(s) and s[i].isdigit():
            i += 1
    return s[start:i], i                # 原样保留源文本，从不重新解析成 float

def query_path(value, path):
    # '.' 进入 object 的某个 key，'[N]' 进入 array 的第 N 个元素，两者可组合。
    node = value
    for token in _parse_path(path):
        if isinstance(token, str):
            if node[0] != "obj":
                raise ValueError("not an object")
            node = dict(node[1])[token]      # 缺失 key -> KeyError，命令流折叠成 NOTFOUND
        else:
            if node[0] != "arr":
                raise ValueError("not an array")
            node = node[1][token]            # 越界 -> IndexError，命令流折叠成 NOTFOUND
    return serialize(node)
```

## 6. 面试里怎么说（边写边讲）

- 开始前：「我讲清楚实现的是哪个规范——RFC 8259，比 `json.loads` 更严格：拒绝孤立 UTF-16 代
  理、拒绝裸 `NaN`/`Infinity`，这两点我会在交叉验证测试里显式排除。」
- 写数字解析时：「数字要原样保留源文本，不重新解析成 `float` 再格式化——`1.50` 和 `1.5` 数值
  相等但文本不同，过早转换会丢失原始格式，这和'最小化'的目标（只去空白）是两回事。」
- 写解析器/序列化器时：「都用显式栈而不是 Python 递归，因为深度可以到 10 万层，递归会直接撞
  上默认递归深度限制。」
- **如果被追问并发**：「`parse`/`serialize`/`query_path` 都是对不可变输入的纯函数，没有共享
  可变状态，多线程并发调用天然安全。如果要加一层'解析结果缓存'（比如按文本内容缓存已解析的
  树），那层缓存的读写才需要加锁，解析逻辑本身不用改。」

## 7. 常见跑偏（方法层面，含并发一条）

- 图省事直接调用标准库 `json.loads`/`json.dumps`，而不是真正手写 tokenizer + 结构化解析
  器——面试要考的正是"能不能把语法讲清楚"，不是"能不能拼出正确结果"。
- 用 Python 递归实现 `parse_value`/`serialize`，在 10 万层嵌套的输入上撞上递归深度限制。
- **并发相关**：给纯函数式的 `parse`/`serialize` 加不必要的锁，或者反过来，给"解析结果缓存"
  这类真正有共享可变状态的部分漏加锁——分不清"这段代码本身要不要保护"和"这段代码操作的状态要
  不要保护"是两个不同的问题。

## 8. 同族题 / 延伸

- 与 `od13_dictionary_trie_codec` 的 trie 编码、`od14_durable_kv_serialization` 的长度前缀编
  码同族，都是"自定义序列化格式设计"，但本题语法本身更复杂，需要真正的 tokenizer。
- `query_path` 同时支撑"给我完整文档"和"给我某个子路径"两种查询形状，这个设计模式与
  `od07_throne_inheritance` 的 `get_inheritance_order`/`succession_after` 双查询接口思路一
  致：用同一套内部表示服务不同粒度的查询。
- 练习命令：`python3 loop/mock.py start od15`
