# bs01 · minimako：拿到一个陌生代码库和一个失败测试，45 分钟内定位并修复

> [!tldr]
> - 这轮考的不是"你会不会写代码"，是"你能不能在没人带你读代码的情况下，把一个陌生仓库的 bug 定位到根因"
> - 三步套路：跑测试看现象 → 读 traceback/assertion 找"数据在哪一行变错" → 假设 + 断点验证，最小改动，跑回归
> - 最值得带走的一个习惯：**永远从失败的那一行往上追，不要从代码第一行往下读**——traceback 已经把"从哪开始看"这件事替你做完了

## 1. 题目在说什么
LeetCode 刷多了会有个错觉：coding 面试就是"给你一道题，你从空白文件开始写"。Bug squash 轮完全是另一件事：
面试官给你一个几百行的陌生仓库（这题是 `minimako`，一个 Mako 风格的迷你模板引擎——`${expr}` 插值、`% if`/`% for`
控制行、`<%include file="..."/>` 拼接子模板），一份 `README.md` 里贴着"issue"，还有一个已经写好、大部分能跑通的
测试文件。你不写新功能，你的任务是：**让红的测试变绿，别把绿的测试改红**。

`README.md` 里的 issue 长这样（这题真实的两条）：

```
Bug report 1 — <%include> crashes the whole render
> Actual: AttributeError: Compiler has no visitor for node type 'IncludeNode'
> (expected a method named 'visit_IncludeNode')

Bug report 2 — a crafted file="..." value in <%include> can read files
outside the template directory
> Our security review flagged that resolve_include() does not reject a file
> value like "//../../etc/something" ...
```

这就是真实公司会给你的 bug 报告的样子：有 repro、有 expected/actual、点名了函数名，但**不会告诉你哪一行错了**。
找那一行，是你要做的事。

## 2. 读库：3 分钟摸清结构
陌生仓库不要从第一个文件读到最后一个文件——那是 45 分钟里最贵的用法。固定顺序，3 分钟内做完：

1. **README 先看"Layout"和"Running the tests"两节**，不看别的。这题的 Layout 直接告诉你：
   `lexer.py`（分词）→ `ast.py`（AST + 解析器）→ `compiler.py`（visitor 模式渲染）→ `lookup.py`/`template.py`
   （按 URI 加载模板、处理 `<%include>`）。五个文件、单向数据流，看完这几行你已经知道"渲染出错去 compiler.py，
   加载/路径出错去 lookup.py 或 template.py"。
2. **确认入口**：这题公共 API 是 `TemplateLookup(dirs).get_template(uri).render()`，或直接 `Template(text).render()`。
   不用读实现，只用记住这两个入口长什么样——待会复现 bug 就是在敲这几行。
3. **测试怎么跑**：README 写了 `python -m pytest tests -q`。跑一次，记住数字（这题：17 个测试，2 红）。

到这一步，你还没读任何一行业务逻辑，但已经知道：仓库多大、数据怎么流、从哪敲命令。这比通读代码更快建立起
"心智地图"，后面每一次读代码都是带着问题去读，而不是漫无目的地扫。

## 3. 下手顺序（面试里就按这个来）
1. **跑失败测试，只看这两个，先不读代码**：
   ```
   python -m pytest tests -q
   ```
   记下失败的测试名和数量。这题：`test_render_template_with_include_inlines_child_template` 和
   `test_resolve_include_rejects_path_traversal_payload`，17 个里 2 个红。
2. **读断言和 traceback，不是读源码**：`pytest` 默认给你完整调用栈——从测试文件的断言，一路往下到抛异常的那一行。
   这条栈本身就是一张"地图"，标好了从入口到出错点经过的每一个函数。
3. **从"数据在哪里变错"往上追**：栈的最底一帧（离异常最近的那行）几乎总是最有信息量的——那里要么是显式
   `raise`，要么是一个断言直接告诉你"期望 X，实际 Y"。从那一行开始，往上一帧一帧看：这个值是从哪个函数传进来的？
   哪一步开始它就不对了？
4. **假设，然后验证，不要连续改代码猜**：看完栈之后先在心里（或嘴上，面试官在听）说一句"我猜是 xxx"，再用
   `print`/断点确认这个猜测，而不是改一行跑一次、再改一行再跑一次。后者在面试计时器下是最亏的策略——猜错了
   你连"为什么错"都不知道，只是在瞎试。
5. **最小修复**：改动应该正好覆盖"栈顶那个断言/异常"要求的东西，不多不少。如果你发现自己在改测试没碰过的
   函数、或者删掉一整段逻辑重写，先停下来问自己："这真的是 bug 要求的范围吗？"
6. **回归测试**：改完不是只跑你修的那个测试，是整个套件重跑一遍——`% pytest tests -q`。确认失败数从 2 变 0，
   不是从 2 变成"1 个不同的失败"。

## 4. 调试工具怎么用
LeetCode 训练出来的习惯是"读代码在脑子里模拟执行"，但在一个几百行的陌生仓库里，脑内模拟很容易漏看一处赋值。
这轮真正区分候选人的，是会不会用工具把"脑内模拟"换成"实际观察"：

- **`breakpoint()`**：在你怀疑出错的那一行前面插一行 `breakpoint()`（Python 3.7+ 内置，等价于 `import pdb; pdb.set_trace()`），
  重跑那个测试，程序会停在那一行，你可以直接 `p 变量名` 看实际值，而不是靠读代码猜。
- **`pytest -x --pdb`**：`-x` 遇到第一个失败就停（省得刷一堆无关输出），`--pdb` 在失败/异常处**自动**掉进 pdb，
  不用自己加 `breakpoint()`。这是排查单个失败测试最快的组合。
- **`pytest --tb=long`**（默认就是 long；卡住看不清可以 `--tb=short` 反过来精简）：控制 traceback 详细程度，
  调用链深的时候（比如这题 `render → visit → visit_TemplateNode → visit(child) → ...`）值得看全。
- **条件断点**：`pdb` 里 `b compiler.py:32, node.__class__.__name__ == "IncludeNode"`，只在特定条件命中时停，
  比在循环里手动一步步 `n` 快得多。
- **`print` 到 stderr**：不想进 pdb 交互、只想留一条痕迹时，`print(..., file=sys.stderr)`——`pytest -q` 默认吞掉
  stdout，但 `-s` 或直接看 stderr 能看到。快、脏、够用，面试计时器下常常是最优解。

这些工具的共同点：把"我觉得这里应该是 X"变成"我看到这里确实是 Y"。工具用得好不好，本质是省下多少次"改代码再跑一遍"
的循环。

## 5. 本题两个 bug 的排查实录

**Bug 1 — `<%include>` 让整个渲染崩掉**
- 现象：`test_render_template_with_include_inlines_child_template` 报
  `AttributeError: Compiler has no visitor for node type 'IncludeNode' (expected a method named 'visit_IncludeNode')`。
- 线索：这条异常信息是 `compiler.py` 里 `visit()` 自己抛的防御性检查（不是裸的 `AttributeError`），已经把
  "缺哪个方法"直接写给你了——读 `compiler.py` 从上到下，五个 `visit_*` 方法（`TemplateNode`/`TextNode`/
  `ExpressionNode`/`IfNode`/`ForNode`），第六个 `IncludeNode` 没有对应的方法。
- 根因：`Compiler.visit()` 按 `type(node).__name__` 反射查找 `visit_<Name>`，`ast.py` 定义了六种节点类型，
  `compiler.py` 只实现了五个。
- 修复：照着 `visit_ForNode` 的形状（解出目标 → 建一个子 `Compiler` → render → 拼字符串）新增一个方法：
  ```python
  def visit_IncludeNode(self, node):
      included = self.current_template.resolve_include(node.file)
      child = Compiler(dict(self.context), current_template=included)
      return child.render(included.ast)
  ```

**Bug 2 — `resolve_include()` 能读到模板目录外的文件**
- 现象：`test_resolve_include_rejects_path_traversal_payload` 报 `Failed: DID NOT RAISE <class 'LookupError'>`——
  该拒绝的输入没被拒绝。
- 线索：这个测试**直接调用** `Template.resolve_include()`，不经过 `render()`/`Compiler`，跟 bug 1 完全独立
  （所以只修 bug 1 之后这个测试还是红，这是有意设计的）。往上看 `resolve_include()`：
  `normalized = file[1:] if file.startswith("/") else file`——只砍掉一个前导斜杠。
- 根因：`lookup.py` 里"正确"的 `TemplateLookup.get_template()` 用 `uri.lstrip("/")`（砍掉**所有**前导斜杠）；
  `resolve_include()` 是另一条独立代码路径，自己重新实现了一遍归一化，只砍了一个。喂它 `"//" + 绝对路径`，
  一个斜杠会留下来，`os.path.join(source_dir, "/abs/path")` 一看到第二个参数是绝对路径，直接把 `source_dir`
  整个丢掉——这是 Python 自己文档写明的 `os.path.join` 行为，不是什么奇技淫巧。
- 修复：一行，`normalized = file.lstrip("/")`，跟 `lookup.py` 的写法对齐。

两个 bug 合计的 diff 只有 11 行改动（新增一个 5 行方法 + 改一行字符串操作），符合"bug 范围有多大，改动就该有多大"——
如果你发现自己在改 `lexer.py`/`ast.py`/解析器，那已经找错方向了。

## 6. 面试里怎么说
- 复现完现象先说一句客观描述：「两个测试红，一个是 `AttributeError` 说缺一个 visitor 方法，一个是该抛
  `LookupError` 没抛。看起来是两个独立的问题，我先看第一个。」
- 提出假设时说出来，不要闷头改：「`Compiler.visit()` 是按类名反射找方法，我看一下 `ast.py` 里有几种节点类型，
  `compiler.py` 里有几个对应的方法——如果数量对不上，大概率就是漏了一个。」
- 修的时候讲清"为什么这样改，不是那样改"：「我照着 `visit_ForNode` 的写法加，因为它们做的事情结构一样——
  解出一个子模板/子上下文，建一个新 `Compiler`，render 完拼回字符串。这样改动量最小，也跟现有代码风格一致。」
- 主动说副作用：「第二个 bug 是路径穿越，我改成跟 `lookup.py` 一样的 `lstrip("/")`。这个函数改完之后不会再
  接受任何以 `/` 开头当"绝对路径"的输入了，如果之前有代码依赖这个行为（我看了一下没有），要一起过一遍。」
- 交付时说清验证范围：「两个红的测试现在都过了，我又跑了一遍全部 17 个确认没有新的失败。」

## 7. 常见跑偏
- **改测试让它变绿**：把 `pytest.raises(LookupError)` 删掉或把断言放宽——这题的测试就是 spec，改测试等于
  绕过题目，面试官一眼能看穿，比不修复更糟。
- **看到"设计不够优雅"就想重写模块**：比如把 `visit()` 的反射分发改成 `dict` 查表——功能等价，但对一个
  60 分钟的轮次来说是完全不成比例的改动，还会掩盖"真正的 bug 只是少了一个方法"这件事。
- **只盯着栈顶那一行，不往上追一层**：`AttributeError` 本身告诉你"缺了什么"，但不会告诉你"为什么会缺、
  该补成什么样"——这需要你往上看同级的其他方法长什么样。只读最后一行报错就动手改，容易改出一个"能过测试
  但形状不对"的实现。
- **不读 README 直接冲进代码**：README 里的 issue 已经把 repro、expected/actual 写清楚了，等于帮你省掉了
  "自己构造一个能复现问题的输入"这一步——跳过它，你会花时间重新发明它已经给你的东西。

## 8. 真实库对应 + 延伸练习
这两个 bug 不是随便编的，都对应 Mako（真实的 Python 模板引擎）历史上的真实问题：

- **Bug 2（路径穿越）** 几乎是 [`sqlalchemy/mako` issue #434](https://github.com/sqlalchemy/mako/issues/434) 的
  重现：真实 fix（commit `e05ac61`）也是把"砍一个前导斜杠"换成"砍所有前导斜杠"，一行改动。它的姊妹 issue
  #435（Windows 下反斜杠归一化不一致，CVE-2026-44307）是同一个 bug family 的另一张皮——如果你想多练一版，
  可以自己给 `resolve_include` 加一个 "拒绝 `\\` 开头" 的用例，走一遍同样的排查流程。
- **Bug 1（missing visitor）** 是 visitor-pattern 渲染器最常见的失手模式：给 AST 加了新节点类型，却忘了在
  每一个 visitor/dispatcher 里补对应分支。Exponent 的 Mako bug-squash 评分记录里，这个失败模式被直接点名为
  "missing visitor function for an AST node type → runtime error"。同样的坑在任何"反射按类型分发"的代码里
  都会出现——Django 的 template tag 注册、任何用 `getattr(self, f"handle_{kind}")` 做分发的解析器/编译器都是
  同一个模式。

**延伸练习**：`python3 loop/mock.py start bs01` 重新跑一遍；这次给自己定 20 分钟而不是 60 分钟，逼自己更快地从
"跑测试"走到"读栈"再到"改一行"——bug squash 轮真正练的就是这条路径的速度，而不是某一次具体的修复。
