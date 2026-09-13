# minimako — 一个迷你的 Mako 风格模板引擎

`minimako` 是一个小型模板引擎，参照 [Mako](https://www.makotemplates.org/) 的核心
迷你语言实现：`${expr}` 插值、`% if` / `% for` 控制行，以及用于将模板拆分为多个小文件的
`<%include file="..."/>`。它是一个 bug-squash 用的 fixture ——
其结构（lexer → AST → visitor-pattern renderer，外加一个把 URI 映射到磁盘文件的
`TemplateLookup`）与真实 Mako 足够接近，使得 Mako 真实历史上的 bug 可以直接移植过来。

## 目录结构
```
src/minimako/
  lexer.py      分词器：${expr}、% if/% for/% endif/% endfor、<%include file="..."/>
  ast.py        AST 节点类型（TextNode、ExpressionNode、IfNode、ForNode、IncludeNode、
                 TemplateNode）+ 基于 token 的递归下降解析器，用于构建这些节点
  compiler.py   Compiler：通过分派 visit_<NodeType>（visitor 模式）渲染 AST
  lookup.py     TemplateLookup(directories)：官方认可的 uri -> Template 加载器
  template.py   Template(text, uri=None, lookup=None, source_dir=None)：解析+渲染；
                 同时负责解析该模板自身的 <%include> 目标
tests/
  test_minimako.py   测试套件（运行它，不要改写它 —— 见下方"如果卡住了"）
```

## 运行测试
```
python -m pytest tests -q
```
按原样运行，大多数测试会通过。有两个不会 —— 见下面的 issue。

## 问题（作为针对该仓库提交的 issue）

**Bug report 1 — `<%include>` 会导致整个渲染崩溃**

> 复现方式：
> ```python
> from minimako.lookup import TemplateLookup
> lookup = TemplateLookup(["templates/"])
> tmpl = lookup.get_template("page.html")   # page.html 中包含 <%include file="footer.html"/>
> tmpl.render()
> ```
> 期望：渲染出的页面，其中 `<%include>` 标签的位置被替换成 `footer.html` 自身渲染后的输出。
>
> 实际：
> ```
> AttributeError: Compiler has no visitor for node type 'IncludeNode' (expected a method named
> 'visit_IncludeNode')
> ```
> 其他所有标签类型（`${...}`、`% if`、`% for`）都能正常渲染。只有使用 `<%include>` 的
> 模板会崩溃，而且是 100% 必现，不是偶发的。

**Bug report 2 — `<%include>` 中精心构造的 `file="..."` 值可以读取模板目录之外的文件**

> 我们的安全审查发现，`Template.resolve_include()`（用于将 `<%include
> file="..."/>` 引用相对于包含它的模板自身目录进行解析）没有拒绝像
> `"//../../etc/something"` 这样的 `file` 值 —— 一个带有**超过一个**前导斜杠的 URI。我们在
> `TemplateLookup.get_template()`（"根据 URI 加载模板"的顶层入口，用于渲染中的第一个模板）
> 中已经有了这个检查，它会先剥离*所有*前导斜杠再与搜索目录拼接，并确认结果仍在该目录内。
> `resolve_include()` 是一条独立的代码路径 —— 它是模板解析*自身内部* `<%include>` 引用的
> 方式，相对于自身文件所在目录，而不是重新搜索每个 `TemplateLookup` 目录 —— 看起来它自己
> 长出了一套更弱、与前者不一致的归一化逻辑。
>
> 期望：`resolve_include()` 像 `TemplateLookup.get_template()` 一样拒绝（或安全地约束）
> 带有多个前导斜杠的 `file` 值。
>
> 实际：它接受了这样的值，最终可能读取到完全在模板自身源目录之外的文件。

如果你卡住了：这两个 bug 范围都很窄（一个是缺失的方法；一个是现有方法里错误的字符串操作）——
如果你的修复动了不止几行代码，或者发现自己在重写 visitor 分派机制或 URI 归一化设计，说明你
已经偏离了真正的 bug，走向了重新设计。回到失败的断言，跟着 traceback 走。
