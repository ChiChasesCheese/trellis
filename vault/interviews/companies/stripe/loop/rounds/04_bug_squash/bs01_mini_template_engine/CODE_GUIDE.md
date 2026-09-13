# minimako 代码导读

面向"没读过模板引擎源码"的人。目的是让你看懂这份代码在干什么、模块之间怎么调，
**不是**帮你定位这道题的 bug——找 bug 的过程本身就是这轮练习的价值所在，所以下文不会提这份代码哪里有问题。

全部源码只有 **313 行**，分 5 个模块。读完这份导读大概 10 分钟。

## 数据流

```
模板文本  "Header\n<%include file="footer.html"/>\n% if x:\n${x}\n% endif"
  │
  ▼
lexer.tokenize()
  │  逐行扫描，把文本切成 token 流。三类东西被识别出来：
  │    ${expr}                → 表达式
  │    % if / % for / % end…  → 控制行（整行以 % 开头）
  │    <%include file="..."/> → 包含指令
  │  其余原样变成文本 token
  ▼
一串 token
  │
  ▼
ast.parse()
  │  递归下降：把线性的 token 流变成一棵树。
  │  控制结构（if / for）会把它们之间的 token 收成子节点，形成嵌套
  ▼
TemplateNode（树根）
  │    body = [TextNode, ExpressionNode, IfNode(body=[…]), IncludeNode, …]
  │
  ▼
compiler.Compiler.render()
  │  访问者模式（visitor）遍历这棵树，每种节点类型交给对应的方法处理，
  │  各自返回一段字符串，最后拼起来
  ▼
渲染结果字符串
```

`lookup.py` 和 `template.py` 是**外围**：负责"从磁盘上把模板文件找出来变成 Template 对象"，
以及"一个模板要包含另一个模板时，去哪儿找那个文件"。

## 逐模块

### `lexer.py`（60 行）— 切词

按行处理。判断顺序很重要：先看整行是不是控制行（`% if` 之类），
再在普通行里找 `${...}` 和 `<%include .../>`。

产出的 token 是简单的元组/小对象，**不带任何嵌套结构**——嵌套是下一步的事。

### `ast.py`（102 行）— 建树

两部分：**节点类型定义** + **解析器**。

节点类型：`TextNode`（纯文本）· `ExpressionNode`（`${}`）· `IfNode` · `ForNode` ·
`IncludeNode` · `TemplateNode`（树根）。

解析器是**递归下降**：遇到 `% if` 就开一个新的 `IfNode`，把后面的 token 递归收进它的 `body`，
直到撞见 `% endif` 才收尾返回。`% for` 同理。这就是嵌套是怎么产生的。

### `compiler.py`（56 行）— 渲染

**访问者模式**。核心是这个分派：

```python
visitor = getattr(self, f"visit_{type(node).__name__}", None)
```

节点类型叫 `TextNode`，就去找自己身上叫 `visit_TextNode` 的方法。找不到就抛 `AttributeError`。

**这是这份代码里最需要理解的一个机制**：分派靠的是**字符串拼出来的方法名**，
不是继承、不是注册表。所以"这个 Compiler 支持哪些节点类型"这件事，
在代码里没有任何一处显式列出来——它隐含在"有哪些 `visit_*` 方法"里。

调试时对应的动作是：
```
(Pdb) p [m for m in dir(self) if m.startswith("visit_")]
```

### `lookup.py`（34 行）— 从磁盘找模板

`TemplateLookup(directories)` 拿到一组搜索目录，`get_template(uri)` 按顺序在每个目录里找。

它做了**目录逃逸检查**：把候选路径 `realpath` 之后，确认它还在搜索目录里面，
否则跳过。这是防 `../../etc/passwd` 这类路径穿越的。

### `template.py`（52 行）— 一个模板对象

`Template(text, uri, lookup, source_dir)`：构造时就把文本 lex + parse 成 AST，
`render(**context)` 时交给 Compiler。

它**自己也有一份 include 路径解析逻辑**（`resolve_include()`），
用于处理"这个模板里的 `<%include>` 该去哪儿找文件"——注意它和 `lookup.py` 的
`get_template()` 是**两处独立实现的路径处理**，各自服务不同场景。

## 读这份代码时容易误解的地方

讲的是**语言机制**，不是这道题的 bug。

| 机制 | 容易怎么误解 |
|---|---|
| `getattr(self, f"visit_{...}")` | 以为分派是靠继承或某个显式的表。**不是**，是运行时用字符串拼方法名。所以"支持哪些类型"要靠 `dir()` 去看 |
| `type(node).__name__` | 返回的是**类名字符串**（`"IfNode"`），不是类对象。写 `type(node) == "IfNode"` 永远是 False |
| 递归下降解析 | 解析器是**共享一个游标**在往前走的。多个函数互相调用时改的是同一个位置，不是各自独立的 |
| 生成器表达式的栈帧 | `"".join(f(c) for c in body)` 在 traceback 里会多出一帧 `<genexpr>`。在 pdb 里往上翻时要多按一次 `u` |
| `os.path.realpath` vs `abspath` | `realpath` 会解析符号链接，`abspath` 不会。做安全检查时这个区别是实质性的 |
| `str.lstrip("/")` | 它剥掉的是**开头所有**的 `/`，不是一个。`"//a".lstrip("/")` → `"a"` |
| `os.path.join(a, b)` | 如果 `b` 是绝对路径（以 `/` 开头），结果直接**变成 b**，前面的 `a` 被丢弃 |

## 怎么开始

```bash
python3 loop/mock.py start bs01     # 拷到 loop/work/bs01/，用你的 IDE 打开
python3 loop/mock.py test bs01      # 先跑，看它怎么失败
```

**先跑测试，再读代码。** 调试从零开始的话，先读 `loop/rounds/04_bug_squash/DEBUG_101.md`——
那份文档里的 pdb 实录就是在这道题上真跑出来的。

---

**真实面试里没有这份导读。** 第一遍可以读（你现在的目标是先看懂这类代码），
**第二遍开始别读了**——那时候你要练的正是"没人给你导读时，多久能读懂一个陌生库"。
