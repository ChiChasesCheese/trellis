# bs01 minimako — 解决方案笔记（不展示给候选人；在 `ref` 之后阅读）

## Bug 1 — 缺失 `visit_IncludeNode`
`compiler.py` 的 `Compiler.visit()` 根据 `type(node).__name__` 分派到某个
`visit_<Name>` 方法。`ast.py` 中的每种节点类型（`TemplateNode`、`TextNode`、
`ExpressionNode`、`IfNode`、`ForNode`、`IncludeNode`）都需要一个对应方法。六种中有五种
已实现；`visit_IncludeNode` 缺失，所以 `getattr(self, "visit_IncludeNode", None)`
返回 `None`，`visit()` 因自身的防御性检查而抛出 `AttributeError`（而不是
`getattr(self, name)` 不带默认值时会抛出的、更令人困惑的裸 `AttributeError: 'Compiler'
object has no attribute ...`——根本原因相同，只是报错信息稍好一些）。

修复方式是添加缺失的方法，形状照搬 `visit_ForNode`（解析某个东西、构建一个
限定在该解析结果范围内的子 `Compiler`、渲染、返回字符串）：
```python
def visit_IncludeNode(self, node: astmod.IncludeNode) -> str:
    included = self.current_template.resolve_include(node.file)
    child = Compiler(dict(self.context), current_template=included)
    return child.render(included.ast)
```
`current_template` 之所以要一路穿过 `Compiler.__init__` 传下去，就是为了让这个方法
有东西可以调用 `resolve_include`——除此之外没有其他任何 visitor 用到它，如果候选人问
"为什么 Compiler 要带着一个模板引用"，这一点值得指出。

## Bug 2 — 通过 `Template.resolve_include` 的路径穿越
`lookup.py` 的 `TemplateLookup.get_template()` 做法是对的：`uri.lstrip("/")` 剥离
所有前导斜杠，所以 `"//../../etc/passwd"` 会被归一化为 `"../../etc/passwd"`——
没有留下前导斜杠让 `os.path.join` 当作绝对路径处理，随后 `os.path.realpath(...).startswith
(real_dir + os.sep)` 的容纳性检查还会在此基础上再拦截 `..` 穿越，作为纵深防御。

`template.py` 的 `Template.resolve_include()`——这条*独立*的代码路径用于解析
`<%include>` 引用，相对于包含它的模板自身目录，而不是重新搜索每个
`TemplateLookup` 目录——有它自己单独写的归一化逻辑：
`file[1:] if file.startswith("/") else file`。这只剥离**恰好一个**前导斜杠。
给它一个带有两个或更多前导斜杠的 `file` 值（例如 `"//" + 某个秘密文件的绝对路径`），
就会有一个斜杠残留下来。`os.path.join(source_dir, "/abs/path")` 随后会完全丢弃
`source_dir`，这是 Python 自身文档记载的 `os.path.join` 行为（"如果某个组件是
绝对路径，之前的所有组件都会被丢弃"）——拼接结果就是攻击者提供的绝对路径本身，
与 `source_dir` 无关。随后的 `os.path.isfile(path)` 检查会愉快地确认它存在
（它确实是个真实文件，只是不在沙箱之内），于是这个文件被读取并作为"模板"返回。

这正是真实 bug 的形状：`mako/lookup.py` 的 `TemplateLookup.get_template()` 被
修复为剥离所有前导斜杠；而代码库中另一处独立维护的归一化逻辑（`mako/template.py`）
保留了旧的单斜杠剥离行为，两者逐渐脱节。见 `sqlalchemy/mako` issue #434
（在 commit `e05ac61` 中修复）——真实的修复同样是从"剥离单个字符"改为
"剥离所有前导斜杠"的一行改动。

修复：
```python
normalized = file.lstrip("/")   # was: file[1:] if file.startswith("/") else file
```
这让 `resolve_include` 的归一化与 `TemplateLookup.get_template` 完全一致。注意，
这里**没有**添加 `lookup.py` 那样额外的 `os.path.realpath(...)` 容纳性检查——
对 `resolve_include` 而言，单靠 `lstrip("/")` 就已足够，因为归一化后的字符串
不可能再是绝对路径（Python 的 `os.path.join` 只有在第二个参数看起来是绝对路径时
才会逃出 `source_dir`），所以对于本 fixture 的测试覆盖范围来说，没有什么是普通
`os.path.isfile` 检查本身还漏不掉、需要靠单纯相对路径的 `..` 向上穿越才能触及的。
生产环境的加固版本仍然应该加上容纳性检查以做纵深防御（解析到 `source_dir` 父目录树中
某个符号链接或其他可达路径的 `../` 片段是一个相关但不同的问题）——如果候选人主动
提出来值得一提，但通过这里的测试并不需要。

## 一次评分良好的运行应该是什么样
- 候选人从 `visit()` 复现出 `AttributeError`，读 traceback，找到现有的五个
  `visit_*` 方法，注意到第六个缺失，照搬 `visit_ForNode` 的形状（解析 → 子
  Compiler → 渲染 → 返回字符串）把它加上。
- 候选人重新运行测试；`test_render_template_with_include_inlines_child_template`
  现在通过了，`test_resolve_include_rejects_path_traversal_payload` 仍然失败。
- 候选人读这个测试，注意到它直接调用 `Template.resolve_include`（而不是通过
  `render()`），把 `resolve_include` 的归一化与 `TemplateLookup.get_template` 的
  归一化做对比，发现 `file[1:]` 与 `.lstrip("/")` 的不一致。
- 总 diff：一个新方法（约 4 行）+ 一行改动。如果候选人重写了 tokenizer、parser 或
  `TemplateLookup` 本身，说明他在找一个根本不存在的 bug。
