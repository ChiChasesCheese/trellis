# bs01 minimako（Mako 风格模板引擎）— 报告

## 概述
一个约 350 行的 Mako 风格模板引擎（`lexer.py` → `ast.py` → `compiler.py` 的
visitor-pattern renderer，外加一对用于按 URI 加载模板并解析 `<%include>` 的
`TemplateLookup`/`Template`），注入了两个相互独立、贴近真实模式的 bug：一个缺失的
visitor 方法（`visit_IncludeNode`），以及一个路径穿越 bug，源于两个本应一致却不一致的
URI 归一化函数。两者都直接对应 Stripe 自身报告的 Mako bug-squash 素材（"path
handling validation, AST node traversal edge cases"），也对应真实的历史 Mako CVE。

## 来源与置信度
"Mako 是 Stripe 报告过的 bug-squash 仓库，bug 涉及 path handling 和 AST
traversal"——置信度高：`loop/raw/en_forums.md` §4.2（"Python | **Mako**（模板引擎；'Python + Mako; no
hints'；bug 涉及 path handling validation、AST node traversal edge cases）"，来源于
programhelp VO 2025-08-07、linkjob technical 2025-12-08、staffengprep "Mako parser bug squash"）。
用作模板的具体真实 bug——置信度高：`sqlalchemy/mako` issue #434（"slash handling
issue in template URI normalization"，在 commit `e05ac61` 中修复，2026-04-14）——根本原因
与 `loop/raw/github_repos.md` §2.2 中描述的完全一致：`Template.__init__` 只剥离一个
前导斜杠，而 `TemplateLookup.get_template()` 会剥离所有斜杠，导致像
`"//../../secret.txt"` 这样的 URI 绕过目录穿越检查；修复 diff 只有 1 行。缺失
visitor 的 bug 模式（"某个 AST 节点类型缺少 visitor 函数 → 运行时报错"）在
`en_forums.md` 的 Exponent 评分笔记（第 167 行）中被直接点名，是一种已知的 Mako
bug-squash 失败模式，与"缺少目录路径检查"（本仓库的第二个 bug）并列。这个仓库具体的
模块划分（`lexer.py`/`ast.py`/`compiler.py`/`lookup.py`/`template.py` 拆成五个独立文件）
置信度为中——没有资料说明真实 Mako 的实际文件边界；本仓库的拆分是一种重构，
目的是让这两个 bug 落在能干净分离、可独立测试的文件中。

## 注入的 bug
1. **`compiler.py`：缺少 `visit_IncludeNode`。** `Compiler.visit()` 根据
   `type(node).__name__` 分派到 `visit_<Name>`；六种节点类型中有五种有对应方法，
   `IncludeNode` 没有。渲染任何包含 `<%include file="..."/>` 的模板都会抛出
   `AttributeError`，而不是内联子模板。真实模式对应：Exponent 的 Mako bug-squash
   评分笔记明确点名了这种失败模式（"某个 AST 节点类型缺少 visitor 函数 → 运行时报错"）。
2. **`template.py`：`Template.resolve_include()` 只剥离一个前导斜杠；`lookup.py`：
   `TemplateLookup.get_template()` 会剥离所有前导斜杠。** 这个不一致使得带有 2 个及以上
   前导斜杠的 `file` 值（例如 `"//" + 某个文件的绝对路径`）在经过 `resolve_include` 的
   归一化后仍保留一个斜杠，而 `os.path.join(source_dir, "/abs/path")` 会把它当作绝对路径处理——
   完全丢弃 `source_dir`，最终读取到完全在模板自身目录之外的文件。真实模式对应：
   `sqlalchemy/mako` issue #434 / commit `e05ac61`，几乎逐字一致（相同的根本原因，
   相同的修复形状：`x[1:] if x.startswith("/") else x` → `x.lstrip("/")`）。

## 调试路径（从失败断言到修复）
- 运行 `pytest tests -q`：17 个测试中有 2 个失败。
- `test_render_template_with_include_inlines_child_template` 失败，报错为
  `AttributeError: Compiler has no visitor for node type 'IncludeNode' (expected a method named
  'visit_IncludeNode')`，由 `Compiler.visit()` 抛出。从头到尾读 `compiler.py` 可以看到五个
  `visit_*` 方法（`visit_TemplateNode`、`visit_TextNode`、`visit_ExpressionNode`、`visit_IfNode`、
  `visit_ForNode`），以及本该是第六个方法的位置上有一条注释——该方法就是不存在。修复：
  添加 `visit_IncludeNode`，按 `visit_ForNode` 的形状照搬（解析某个东西、构建子
  `Compiler`、渲染、返回字符串）。
- `test_resolve_include_rejects_path_traversal_payload` 失败，报错为 `Failed: DID NOT RAISE
  <class 'LookupError'>`——该测试**直接**调用 `Template.resolve_include()`，完全绕过
  `render()`/`Compiler`，所以它的失败与 bug 1 无关（这是有意为之：它把 bug 2 单独隔离出来，
  这样只修复了 bug 1 的候选人仍会看到恰好一个剩余失败，而不是零个）。读
  `resolve_include()` 会看到 `file[1:] if file.startswith("/") else file`；
  与 `lookup.py` 中的 `uri.lstrip("/")`（被始终安全的顶层 `TemplateLookup.get_template()`
  使用）对比就能看出不一致。修复：一行代码，`file.lstrip("/")`。

## 最小修复
`solution/FIX.patch` —— 2 个文件，+8/-3 行（共 11 行改动；在 `compiler.py` 中新增一个
5 行的方法；在 `template.py` 中改动一行代码 + 更新注释）。已验证：对干净副本执行
`git apply solution/FIX.patch` → 全部 17 个测试通过。（2026-09-02 在下面的 review 移除
`src/` 中的暴露性注释后重新生成；修复本身未变。）

## 与真实库的对应关系
- Bug 1（缺失 visitor）：模式在 `en_forums.md` 的 Exponent Mako 评分笔记中被点名
  （"某个 AST 节点类型缺少 visitor 函数 → 运行时报错"）；未对应某个具体的 Mako issue
  编号（本仓库的 `Compiler`/AST-visitor 设计是一种简化——真实 Mako 会把模板编译为
  Python 源码，而不是在渲染时逐树遍历 AST）。
- Bug 2（路径穿越）：https://github.com/sqlalchemy/mako/issues/434 ，由 commit
  https://github.com/sqlalchemy/mako/commit/e05ac61989a7fb9dd7dcde6cfd72dc48328719a3 （2026-04-14）修复。
  同族的 issue #435（Windows 下的反斜杠处理，CVE-2026-44307，commit `72e10c5`）
  属于同一 bug 家族，但本仓库没有复现（这个 fixture 只涉及 POSIX 路径；单一操作系统
  的测试套件无法利用 `posixpath` 与 `os.path` 的差异）。

## 面试官评分看什么
- 候选人是否真的先运行了测试，还是直接盲目读/改代码？
- 每个失败是否从 traceback/断言出发做根因分析，而不是靠猜测和试错来改代码。
- 修复规模是否与 bug 相称（bug 1：一个新方法；bug 2：一行改动）——如果候选人最终
  动到了 tokenizer、parser 或 `TemplateLookup` 本身，说明他在找一个根本不存在的 bug。
- 是否（哪怕没被问到）注意到 bug 2 是一个*安全*问题，而不只是功能问题——能说出
  "这会导致可以读取模板目录之外的文件"比默默改字符串操作更有价值。
- 对于 bug 2：是否理解*为什么* `os.path.join(base, "/abs/path")` 会丢弃 `base`
  （Python 自身文档说明的 `os.path.join` 行为），而不只是"加了 `.lstrip` 让测试通过了"——
  这与真实 Mako CVE 的机制一致，能解释清楚的候选人才是真正理解了 bug，而不是照葫芦画瓢改 diff。

## 常见跑偏
- 重写 `Compiler.visit()` 的分派机制（例如改成一个节点类型 → handler 的 `dict`），
  而不是单纯添加缺失的方法——功能上等价，但对一个 60 分钟的回合来说是更大、更冒险的 diff，
  而且会掩盖真正的 bug 是"缺了一个方法"，而不是"分派设计有问题"这一事实。
- 用添加 `os.path.realpath` 容纳性检查（照搬 `lookup.py` 完整的安全网）来修复 bug 2，
  而不是仅仅匹配 `lookup.py` 的归一化方式（`lstrip("/")`）——这不算错，但对于失败测试
  实际要求的内容来说范围过大；`solution/NOTES.md` 直接讨论了这一点，作为"如果候选人
  提出来"时可以接受但非必需的讨论点。
- 修改 `test_minimako.py` 让两个失败消失（例如放松 `pytest.raises` 断言，或删掉
  include 渲染的测试），而不是修复 `src/minimako/`——测试就是这里的规范；改测试就
  违背了这个练习的初衷。
- 试图"修复" `TemplateLookup.get_template()`——它本来就是对的（剥离所有前导斜杠，
  有 `realpath` 容纳性检查）；bug 在 `Template.resolve_include()` 自己*独立*的
  归一化代码路径里，不在 lookup 里。

## 测试清单
17 个测试，纯 pytest（没有 `partN` 标记——bug-squash 回合是单场景的，不是多 part 的）。
按原样运行时 15 个通过、2 个失败，各自隔离出一个 bug
（`test_render_template_with_include_inlines_child_template` → bug 1；
`test_resolve_include_rejects_path_traversal_payload` → bug 2）。执行 `git apply
solution/FIX.patch` 后：17/17 通过。

## 涉及的技能
S12 树形遍历解释器 / visitor 模式 · S13 基于 token 的递归下降解析 · S18 路径穿越
校验（对齐两个归一化函数）· S20 从 traceback/失败断言做根因分析而非猜测式试错 ·
S24 真实开源 bug 模式匹配（Mako 路径处理 CVE 家族）

## 复盘（2026-09-02）

### 检查了什么
`mock.py start bs01`（把该目录除 `solution/`/`REPORT.md` 之外的内容拷贝到
`loop/work/bs01/`，运行 pytest）→ 15 通过 / 2 失败，两个失败恰好是文档中记录的两个
bug（`test_render_template_with_include_inlines_child_template`、
`test_resolve_include_rejects_path_traversal_payload`），没有意外失败。`mock.py ref bs01`
（在临时副本中应用 `solution/FIX.patch`）→ 17/17 通过。对 problem 目录执行 `git apply --check`
检查该 patch → 干净。检查了 patch 大小、`src/` 代码质量（模块边界、docstring、死代码）、
注入的 bug 是否读起来像真实 bug 而非标了 TODO、测试是否有真实意图（而非只是
`len > 0`）且不能靠改测试绕过、README 的 issue 文本是否读起来像一个真实的 GitHub issue。

### F — 已修复
**注入 bug 的位置通过注释/docstring 泄露了诊断信息，破坏了"45 分钟内定位并修复"的
练习**（review checklist："检查注入处没有留下提示性注释或命名"）：
- `src/minimako/compiler.py`：模块 docstring 说缺失 visitor 的 `AttributeError`
  "is exactly what happens today (see the `README.md` issue...)"；在注入位置正上方
  有一条注释写着 `# BUG (see README.md "面试官给的 issue"): visit_IncludeNode is missing
  entirely...`——这直接告诉候选人方法名、文件位置以及"这就是 bug"这一事实，完全不需要读 traceback。
- `src/minimako/template.py`：模块 docstring 直接说明 `resolve_include()` 的归一化
  "is not the same as `TemplateLookup`'s"——这正是 bug 2 的根本原因，在候选人查看
  这两个函数之前就被说破了。
- `src/minimako/lookup.py`：模块 docstring 自称是这对函数中"intentionally the 'correct' half of
  the pair"，并直言 `template.py` 的归一化"(buggy)"；有一条行内注释写着
  `# strips ALL leading slashes -- the correct behavior`，暗示与之相对的另一个文件的
  剥离方式是错的。
- `tests/test_minimako.py`：模块 docstring 把两个失败测试与括号内的 bug 诊断并列写出
  （`(missing visitor -> AttributeError)`、`(path-traversal bypass)`），并且两条章节注释
  直接写着 `# ---- known-broken: bug #1 (missing visitor)` /
  `# ---- known-broken: bug #2 (path traversal)`，就在两个失败测试的正上方。

修复：把这五处全部改写，只描述代码*做了什么*（准确、依然有用的 docstring/注释，
放在真实仓库里也说得通），不再提及任何 bug、不一致、"buggy"、"correct"，
也不再暗示哪个测试对应哪个 bug。候选人现在必须真的运行测试、读 traceback、
对比两个归一化函数的差异才能找到 bug 2——这才是本来想要的练习方式。
`REPORT.md`/`solution/NOTES.md`（从未被拷贝到候选人的工作目录——已通过
`mock.py` 的 `_BS_SKIP` 集合确认）仍然完整保留给面试官的诊断信息，未做改动。

F 检查表上其余各项均已满足：`starter` 等价物（bs 类没有）不适用；测试非平凡
（精确字符串/精确异常断言、`pytest.raises`、真实的临时文件 fixture，而非 `len() > 0`）；
无 flaky 测试（无线程/时间/网络依赖）；patch 一直远低于 15 行预算；lint 早已干净。

### S — 无需处理
作为一个小型库 fixture，代码本身状态已经很好：五个文件各自职责清晰
（lexer → ast/parser → compiler/visitor，外加 lookup/template），每个需要的函数都有
单行 docstring，没有死代码，没有 TODO。没有动 visitor 分派机制、URI 归一化设计，
也没有添加超出测试要求的纵深防御——README 自身的"如果卡住了"部分就明确警告过
不要这样跑偏，而且这个 fixture 本来就应该是按原样交付就 lint 干净、最小化的。

### 修复后的验证
- `solution/FIX.patch` 是基于清理后（依然有 bug）的 `src/` 文件重新生成的：创建了
  一个只包含这两个改动文件的临时 git 仓库，提交了清理后但仍有 bug 的状态，应用预期的
  修复（`visit_IncludeNode` 方法；`file.lstrip("/")`），取得 `git diff`——
  仍是同样两个文件、同样的功能性修复，新 patch 在精神上与之前完全一致（2 个文件，+8/-3，
  共 11 行改动，除上下文行中的 docstring/注释文本外，与之前没有变化）。
- 对 `git apply --check --directory=<problem dir> solution/FIX.patch` → 干净。
- 清理之后再跑 `mock.py start bs01` → 仍然是 15 通过 / 2 失败（只有目标的两个 bug）。
- `mock.py ref bs01` → 17/17 通过。
- `loop/lint.sh --fix loop/rounds/04_bug_squash/bs01_mini_template_engine` → black："8 files would
  be left unchanged"（无需重新格式化）；flake8（F 类）：0 条发现。不带 `--fix` 重新运行
  确认检查干净（exit 0）。
