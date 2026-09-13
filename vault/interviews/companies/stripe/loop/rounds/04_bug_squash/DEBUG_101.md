# Python 调试从零开始 —— 为 Bug Squash 轮写的

> 假设你完全没调试过 Python：没用过 `pdb`，没设过断点，看见 traceback 只会往上翻。
> 这份文档从零讲到能进考场。**全部命令和输出都是在本仓库 `bs01` 上真跑出来的，不是编的。**

Bug Squash 这一轮，Stripe 给你一个真实开源库的 fork + 一个失败的单测，45–60 分钟里定位并修好。
Python 版的通过率被 Stripe 员工说成 **"<10%"**。挂掉的第一大原因不是不会写代码 —— 是**只会 print，不会 debugger**。

这份文档要让你从"不会"变成"够用"。够用的标准很低：**能在 30 秒内让程序停在你想看的那一行，并打印出当时的变量。** 就这一件事。

---

## 0. 先纠正一个观念

调试不是"盯着代码看，看出哪里错了"。

调试是**做实验**：你有一个关于"程序在哪一步开始偏离预期"的猜想，你让程序停在那一步，**看真实的值**，猜想被证实或推翻，然后缩小范围再来一次。

这就是为什么面试官在这一轮看的是"你会不会做实验"，而不是"你能不能一眼看出 bug"。Stripe 员工原话：

> "solving the bug isn't the primary objective"

一份被记为强表现的评语长这样（Blind）：

> "read the entry point before touching code, set a breakpoint early, formed a hypothesis, verified it, applied a targeted fix"

五个动作：**读入口 → 早下断点 → 形成假设 → 验证 → 精准修复**。这份文档教的就是中间那三个。

---

## 1. 读 traceback：只有两行是重要的

先跑失败的测试。**永远先跑，不要先读代码**——这是 leonstaff 那份 2026-08 材料里的第一条，也是"有经验的工程师不会跳过"的一步。

```bash
python3 -m pytest loop/rounds/04_bug_squash/bs01_mini_template_engine/tests --tb=short
```

真实输出（截掉中间）：

```
loop/.../tests/test_minimako.py:113: in test_render_template_with_include_inlines_child_template
    assert tmpl.render() == "Header\nFooter text\nEnd"
loop/.../src/minimako/template.py:38: in render
    return Compiler(dict(context), current_template=self).render(self.ast)
loop/.../src/minimako/compiler.py:21: in render
    return self.visit(node)
loop/.../src/minimako/compiler.py:31: in visit
    return visitor(node)
loop/.../src/minimako/compiler.py:34: in visit_TemplateNode
    return "".join(self.visit(child) for child in node.body)
loop/.../src/minimako/compiler.py:34: in <genexpr>
    return "".join(self.visit(child) for child in node.body)
loop/.../src/minimako/compiler.py:27: in visit
    raise AttributeError(
E   AttributeError: Compiler has no visitor for node type 'IncludeNode'
```

**怎么读：**

- **从下往上读。** 最后一行 `E   AttributeError: ...` 是**异常本身**，上面那一大坨是**调用栈**：最下面是最里层（异常真正发生的地方），最上面是最外层（谁最先调进来的）。
- **两行最重要**：
  1. **最后一行**（异常类型 + 消息）——它告诉你"程序不高兴的是什么"
  2. **倒数第一个属于"被测库"的帧**（这里是 `compiler.py:27`）——它告诉你"在哪里不高兴的"
- 中间那些帧大多是"路过"。`test_minimako.py:113` 那行是测试文件，也很有用：它告诉你**期望值是什么**（`"Header\nFooter text\nEnd"`）。

**一个专属于 Python 的坑**：栈里出现了 `in <genexpr>` 这么一帧。生成器表达式 `(f(x) for x in xs)` 在 Python 里**有自己独立的栈帧**，所以你会看到同一行 `compiler.py:34` 出现两次——一次是建生成器的外层，一次是生成器内部。这不是重复，别当成递归。

**另一种失败长什么样**——同一个套件里第二条红是：

```
loop/.../tests/test_minimako.py:124: in test_resolve_include_rejects_path_traversal_payload
    with pytest.raises(LookupError):
E   Failed: DID NOT RAISE LookupError
```

没有异常栈，因为**问题恰恰是"该抛的异常没抛"**。这类失败读法不同：去测试文件看那几行，搞清楚它期望什么条件下抛，然后去被测代码里找那个判断。

---

## 2. `breakpoint()` —— 你只需要记住这一个词

Python 3.7 起，在任何一行插入这一句：

```python
breakpoint()
```

程序跑到这里就停下，把控制权交给你。**不需要 import 任何东西。**（它等价于老写法 `import pdb; pdb.set_trace()`，那个你在老代码里会见到。）

停下后你看到 `(Pdb)` 提示符。这时候整个程序**冻结在那一刻**：所有变量都还活着，你可以随便查。

**不想改代码也能停**——用 pytest 的开关，程序一失败就自动停在失败点：

```bash
python3 -m pytest <测试路径> --pdb
```

这个叫 **post-mortem（事后验尸）**：不是停在崩溃前，是崩溃后现场还没拆，你进去看。**Bug Squash 里这一条最常用**，因为你还不知道该在哪里下断点，但你知道它会挂。

---

## 3. pdb 命令表（背这 12 个就够）

| 命令 | 全称 | 干什么 |
|---|---|---|
| `l` | list | 看当前停在哪，前后各几行代码 |
| `ll` | longlist | 看**整个当前函数**的源码（比 `l` 好用） |
| `p x` | print | 打印表达式 `x` 的值 |
| `pp x` | pretty print | 同上，但字典/列表会换行排版，长数据用这个 |
| `a` | args | 打印当前函数的**所有参数** |
| `n` | next | 执行下一行（**不进入**被调用的函数） |
| `s` | step | 执行下一行（**进入**被调用的函数） |
| `r` | return | 一路跑到当前函数返回 |
| `c` | continue | 继续跑，到下一个断点或结束 |
| `u` | up | 在调用栈里**往上**走一层（去调用者的那一帧） |
| `d` | down | 往下走一层 |
| `w` | where | 打印当前调用栈（跟 traceback 一样，但是活的） |
| `q` | quit | 退出 |

**`n` 和 `s` 的区别是最常问的**：停在 `result = compute(x)` 这一行时，`n` 会把 `compute()` 整个跑完停到下一行；`s` 会钻进 `compute()` 的第一行。不确定 bug 在不在 `compute` 里，就先 `n`，发现 `result` 不对再重来一次用 `s`。

**`u` / `d` 是这一轮的秘密武器**：异常在最里层抛出，但**根因常常在上面几层**（谁传了个错的参数进来）。`u` 一路往上，每层 `a` 打印参数，就能找到"值从哪一层开始就不对了"。

---

## 4. 实战：真的走一遍（bs01，两条命令找到根因）

跑：

```bash
python3 -m pytest loop/rounds/04_bug_squash/bs01_mini_template_engine/tests/test_minimako.py::test_render_template_with_include_inlines_child_template --pdb --tb=no
```

真实输出：

```
>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> entering PDB >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
>>>>>>>>>>>>>>>>>> PDB post_mortem (IO-capturing turned off) >>>>>>>>>>>>>>>>>>>
> /home/.../src/minimako/compiler.py(27)visit()
-> raise AttributeError(
(Pdb)
```

它停在 `compiler.py` 第 27 行。异常消息说"没有处理 `IncludeNode` 的 visitor"。**假设：这个 Compiler 少了一个方法。** 验证它——

```
(Pdb) p type(node).__name__
'IncludeNode'

(Pdb) p [m for m in dir(self) if m.startswith("visit_")]
['visit_ExpressionNode', 'visit_ForNode', 'visit_IfNode', 'visit_TemplateNode', 'visit_TextNode']
```

**两条命令，根因出来了**：这个类实现了 5 个 `visit_*` 方法，`visit_IncludeNode` 不在里面。`<%include>` 这个语法在 lexer 和 AST 里都存在（不然不会造出 `IncludeNode`），只是渲染器这一环漏了。

第二条命令是这一轮最值钱的一个套路：**`dir(obj)` 加一个筛选，看清这个对象到底有什么。** 记住这个写法：

```python
p [m for m in dir(self) if m.startswith("visit_")]     # 有哪些方法
p {k: v for k, v in vars(self).items()}                # 有哪些实例字段和它们的值
p type(x).__mro__                                      # 这个类继承自谁
```

顺带一个**真实的坑**（我这次演示时踩到的）：在上面那个位置敲 `u` 往上一层，会跳进 `<genexpr>` 帧，然后 `p node` 报 `NameError: name 'node' is not defined`——因为生成器表达式的帧里只有它自己的循环变量，外层的 `node` 不在这个作用域。**再 `u` 一次**才到真正的调用者。看到 `<genexpr>` 就多按一次 `u`。

---

## 5. pytest 开关（比 pdb 更早用得上）

| 开关 | 干什么 | 什么时候用 |
|---|---|---|
| `--tb=short` | 精简 traceback | 默认就用它，`long` 太吵 |
| `--tb=line` | 每个失败只打一行 | 一次挂几十个，先看全貌 |
| `--tb=no` | 不打 traceback | 只想数红绿 |
| `-x` | 第一个失败就停 | 一次挂很多、想逐个击破 |
| `--lf` | 只跑上次失败的 | **改一行跑一次，循环最快** |
| `-k "关键词"` | 只跑名字匹配的测试 | 锁定一个 part |
| `-s` | 不捕获 stdout | 你的 `print` 才会显示出来 |
| `--pdb` | 失败即进 pdb | 上一节那个 |
| `-q` / `-v` | 少说 / 多说 | — |

**本仓库注意**：`pytest.ini` 里已经带了 `-q`，命令行**别再加 `-q`**，会把汇总行吞掉。

最高频的组合是这一条，改完代码立刻验：

```bash
python3 -m pytest <目录> --lf --tb=short
```

---

## 6. print 调试的正确姿势

不是说不能 print。是**print 要用对**，而且**不能只有 print**（面试官明确记过"只用 print、不会 debugger"是挂点第一名）。

用对的姿势：

```python
import sys
print(f"{node=} {type(node).__name__=}", file=sys.stderr)
```

三个点：

1. **`file=sys.stderr`** —— 本仓库的 `CONVENTIONS.md` 要求调试输出走 stderr，因为 stdout 是要被逐字节比对的答案。真实 OA 里也一样：往 stdout 里 print 一行调试信息，你的输出就错了。
2. **`f"{x=}"`** 这个写法（Python 3.8+）会打印成 `x=3`，变量名和值一起出来，不用自己写标签。变量一多，这个省下的时间很可观。
3. print 适合**看一个循环里值怎么变**（断点在循环里要按很多次 `c`）；pdb 适合**在一个点上把周围翻个底朝天**。两者互补。

---

## 7. 缩小范围：当你完全不知道从哪下手

有时候失败测试指向的地方离根因很远。三个办法，从便宜到贵：

1. **二分注释法**：把可疑代码段一半屏蔽掉（或直接 `return` 早一点），看现象变不变。变了 → 在这一半里。
2. **对比法**：找一个**通过的**近似测试，跟失败的那个逐行对比输入差在哪。bs01 里 15 个测试通过、2 个失败——通过的那些告诉你"哪些路径是好的"，差集就是嫌疑范围。
3. **`git bisect`**（如果 repo 有历史）：`git bisect start` → `git bisect bad` → `git bisect good <某个老 commit>`，git 自动二分找出哪个 commit 引入的。真实 Bug Squash 的 fork 一般把历史 pin 住了，未必用得上，但值得知道。

---

## 8. 会咬人的 Python 机制（bug 常藏在这些地方）

这一节不讲哪道题的 bug 在哪，讲**语言本身**的坑。真实注入的 bug 十有八九落在这几类里：

| 机制 | 会出什么事 | 怎么看出来 |
|---|---|---|
| **可变默认参数** `def f(x, acc=[])` | `acc` 在**所有调用之间共享**，第二次调用带着上次的数据 | 函数第二次调用结果不对；`p acc` 看到不该有的旧值 |
| **跨调用残留状态** | 实例字段该在 `reset()`/`__init__` 清而没清 | 单跑一个测试绿、连着跑就红 |
| **闭包晚绑定** `[lambda: i for i in range(3)]` | 三个 lambda 全返回 `2`，不是 `0,1,2` | 循环里造函数/lambda 时 |
| **`is` vs `==`** | `is` 比的是"同一个对象"，`==` 比的是"值相等"。小整数和短字符串被缓存，`is` 有时"碰巧"对 | 跟 `None`/`True`/`False` 比才用 `is`，其余一律 `==` |
| **浅拷贝** `d2 = dict(d1)` | 嵌套的 list/dict 还是同一个，改 `d2` 会动到 `d1` | 改了一个对象，另一个"莫名"也变了 |
| **生成器只能迭代一次** | 第二次 `for` 拿到空 | 第一次用完好好的，第二次是空 |
| **`sorted` 的 key 写错** | 排序结果看着"差不多对"，只在 tie 时错 | 只有含相同键的用例红 |
| **整数除法 `/` vs `//`** | `/` 永远返回 float，索引会 TypeError | `TypeError: list indices must be integers` |
| **异常被吞** `except Exception: pass` | 错误消失了，结果静静地不对 | 结果不对但没有任何报错 |
| **闭区间 vs 开区间** | off-by-one，边界的那一个多算或少算 | 只有边界用例红 |

并发相关的（bs04/bs05 会用到）：

| 机制 | 会出什么事 |
|---|---|
| **GIL 不保护你** | GIL 只保证单条字节码原子，`if k not in d: d[k] = v` 是**两步**，中间可以被打断 |
| **`await` 是让出点** | 每个 `await` 处协程可能被挂起，别的协程会跑；`await` 前后共享状态可能已变 |
| **`asyncio.gather` 的顺序** | 返回值顺序 = **传入顺序**，不是完成顺序。当成完成顺序就错 |
| **`return_exceptions=True`** | 异常变成返回值里的一个对象，不再抛出——不检查的话会被当成正常结果统计 |
| **`threading.Lock` 不可重入** | 同一线程二次 acquire 直接死锁；要递归得用 `RLock` |

---

## 9. 45 分钟怎么分配 + 边调边说什么

面试官在看你的**过程**，所以过程要出声。

| 时间 | 做什么 | 说什么 |
|---|---|---|
| 0–3 min | 跑失败测试，看它到底怎么失败 | "我先跑一下测试，确认失败长什么样再读代码" |
| 3–6 min | 读 README / 目录结构，找入口 | "这个库的入口是 X，数据流大概是 A → B → C" |
| 6–12 min | 读 traceback，定位最里层属于库的那一帧 | "异常在 X，但我怀疑值在更上层就不对了，我往上翻一层看看" |
| 12–25 min | 下断点，打变量，形成并验证假设 | "**我的假设是** Y，如果成立，这里的 `node` 应该是 Z——我打印一下"（**明确说出"假设"这个词**） |
| 25–35 min | 最小修复 + 重跑 | "我只改这一处，因为根因是 Y；改大了会影响 W" |
| 35–45 min | 加一个回归测试 + 讲根因和副作用 | "我加个用例锁住这个行为；这个修复对 V 路径没有影响，因为……" |

**四类典型 bug**（leonstaff 2026-08-13，进场先按这四类猜）：逻辑错误 · off-by-one · 符号反转 · 跨调用残留状态 · 排序用错 comparator。

**一轮通常 2–3 个 bug**（2026 年三份材料一致，其中两份是搜索摘要，所以按 2–3 个准备、1 个也可能）。修完第一个要主动问"要我继续找下一个吗"。

**这一轮明确禁止用 AI 助手。**

---

## 10. 挂点（都是真实报告里的）

1. **只用 print、不会 debugger** —— 多例，第一大挂点
2. **盯着栈顶不放，或者试图读懂整个库** —— 库是大的，你只需要读数据流经过的那几个函数
3. **不读 README/文档** —— 有 Google 候选人主要因为这个挂
4. **环境（虚拟环境 / import 路径 / Python 版本）吃掉 10 分钟** —— 所以要提前拿 recruiter 发的 sample repo 跑通一次
5. **大范围重写而不是最小修复** —— 面试官要的是外科手术，不是重构

---

## 11. 进考场前的自检

- [ ] 我能在**不查文档**的情况下让程序停在任意一行（`breakpoint()`）
- [ ] 我知道 `n` 和 `s` 的区别，也知道 `u` 是干嘛的
- [ ] 我会用 `pytest --pdb` 让它失败即停
- [ ] 我会用 `dir()` / `vars()` 看清一个陌生对象有什么
- [ ] 我的 print 走 stderr，用的是 `f"{x=}"`
- [ ] 我在自己的 IDE 里跑通过一次断点（PyCharm/VS Code 的图形断点也要会，很多人现场才发现没配好）
- [ ] 我练过至少 4 次注入 bug 的计时调试，其中 1 次**不用 debugger**（逼自己练读代码）

---

## 练习顺序

```bash
python3 loop/mock.py start bs01      # 拷到 loop/work/bs01/，用你的 IDE 打开
python3 loop/mock.py test bs01       # 跑测试
python3 loop/mock.py ref bs01        # 看参考修复（打完 FIX.patch 应该全绿）
```

每道题旁边有一份 **`CODE_GUIDE.md`（中文）**，逐模块讲这份代码在干什么。
**第一遍可以读**——你现在的目标是先看懂代码。**第二遍开始别读了**，真实面试里没有这份东西。
