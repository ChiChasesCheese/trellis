# 04 · Onsite · Bug Squash（45–60 min）

> 事实层在 `loop/LOOP_GUIDE.md` §4。**从零学调试在 `loop/rounds/04_bug_squash/DEBUG_101.md`**——
> 如果你没用过 pdb，先读那份，本章假设你读过了。

## 这轮到底考什么

**不是"你能不能修好"。** Stripe 员工原话：

> "solving the bug isn't the primary objective"

考的是**独立调试能力、方法论、沟通**。一份被记为强表现的评语是五个动作：

> read the entry point before touching code · set a breakpoint early · formed a hypothesis · verified it · applied a targeted fix

Python 版通过率被 Stripe 员工说成 **"<10%"**（2022）。挂掉的第一大原因不是不会写代码 —— 是**只会 print，不会 debugger**。

## 形式

真实开源库的 fork（私有 repo、版本 pin 死）+ Stripe 加的失败单测或 issue 描述。在**你自己的 IDE** 里 clone → 跑测试 → 定位 → 修。"everything else is real"。

**几个 bug：不定，1–5 个都有一手报告。别背数字，按"逐个跑、逐个修，修不完是常态"准备。**
Dublin senior 说 "4-5 unit tests failing"，Dublin new grad 说 "1/3 bugs"，India 校招报 1 个。
注意**失败的单测数不等于 bug 数**——一个 bug 能让多个测试红。

**明确禁用 AI 助手**（除 AI Programming Exercise 外的所有轮都禁），**一手证据明确到"含 IDE 自动补全"**，
不只是聊天框。用 Cursor/Windsurf 类编辑器要当场演示已关闭。

**⭐ 用不用 debugger 本身是评分项，不只是"允许"**：一手原文
"Use of an IDE is permitted and **is actually one of the evaluation parameters**"。

库按语言分流：Python `requests` / `Mako`；Java `SnakeYAML` / `Moshi` / `Jackson`；JS `Express` / `Day.js`；Ruby `Sass`。

**⭐ 这份清单的 Python 那半边有一手背书**（2025-08 Dublin senior，逐字）：

> "you're given the **entire repository of a built-in library**, for instance, for python, it could be either
> **\"requests\" or \"mako\"**. There'd be 4-5 unit tests failing and you'll be expected to run the tests one by one
> and make them pass by fixing the actual code. The challenge here is again **time** since, **if it is an unfamiliar
> library like mako, it is quite challenging to figure out what it does in the first place**."

**`bs02_mini_http_client` 就是 requests 的缩微版，`bs01_mini_template_engine` 就是 Mako 的缩微版。**
他那句"不熟的库先搞懂它在干什么最难"，正是每道题旁边那份 `CODE_GUIDE.md` 存在的理由——
**也正是为什么第二遍起不许读它**：真实面试里没有导读，"多久能读懂一个陌生库"就是这轮在考的东西。

**bug 从哪来**：问"注入的还是该库 GitHub 上真实报过的"，一手回答 "**Could be either.**"
**JS / Java 场次的库仍然零证据**（帖里问了 5 次全部转私信）——别把上面这份清单当完整清单。

## 五步硬流程（面试官在看你做没做这几步）

1. **先跑失败测试**，亲眼确认错误长什么样 —— "跳过这步直接读代码，是有经验的工程师不会犯的错"
2. **读入口点、追数据流**，再动代码
3. **把假设说出来**："我怀疑在 X，因为 Y"
4. 用**断点**验证，不要靠 print
5. 写**生产级最小修复**，不是能过测试就行的补丁 —— **并且先想清楚"这个 fix 该落在栈的哪一层"**：
   有一手挂经是面试官"told me to implement the fix in some **other function, higher up in the stack trace**
   rather than the function I was fixing"。定位到根因 ≠ 知道该改哪里。

**两条补充技巧**：

- **若 issue 里同时给了一个通过的测例和一个失败的测例，先 diff 这两个测试的输入**——
  差异处就是触发条件，比从头读库快得多。
- **卡住时不要为了"显得在推进"乱试。** 一位挂掉的候选人自述："I made poor decisions to try things that
  **I knew intuitively had little chance of being the problem, just for the sake of forward progress**."
  第 3 步"把假设说出来"正是防这个的机制：**说不出理由的方向就别动手改。**
- ⚠️ 关于第 4 步：有一条一手转述面试官说 "You can use a **debugger, print statements, or any approach you
  prefer**"。所以 print 不会当场被打断。**但"只用 print、不会 debugger"仍是被独立记录过的头号挂点**，
  而且用不用 IDE/debugger 是显式评分项——**按会用 debugger 准备，print 当补充手段。**

## 进场先按这四类猜

逻辑错误 · **off-by-one** · **符号反转** · **跨调用残留状态**（该重置没重置）· **排序里用错 comparator**

本仓库五道题覆盖了全部四类，另加两类并发：

| 题 | 两个 bug | 属于哪类 |
|---|---|---|
| bs01 minimako | 少 `visit_IncludeNode` · 路径穿越校验漏 | 分派表漏项 · 校验缺失 |
| bs02 minihttp | 测完长度没 seek 回原位 · `None` 未判空 | 资源状态没复原 · 边界未判空 |
| bs03 miniyaml | `"- "` 占两列却按一列算 · 复用 Parser 没重置 `pos` | **off-by-one** · **跨调用残留状态** |
| bs04 confmgr | check-then-act 拆成两段分别加锁 · `reload()` 没清缓存 | **竞态** · 跨调用残留状态 |
| bs05 fetchrace | `release()` 不在 `try/finally` · 异常项被计入成功 | **异常路径泄漏** · 异常被吞 |

## 一个可迁移的强信号

本仓库五道题的 bug 都做成了同一型 —— 这不是巧合，真实开源库的 bug 大多长这样：

> **docstring 把契约写对了，下面的代码违反它。**

```python
async def fetch_one(sem, url, fetcher):
    """Acquire one permit, fetch `url`, release the permit, and return a FetchResult."""
    await sem.acquire()
    result = await fetcher(url)      # 抛异常就永远不 release
    sem.release()
```

所以：**先读注释和 docstring，把它当成"应该是什么"，再看代码"实际是什么"。** 差集就是 bug。

另外两个信号：

- **单跑一个测试绿、连着跑就红** → 第一嫌疑是跨调用残留状态
- **结果不对但一个报错都没有** → 异常被吞（`except: pass` 或 `gather(return_exceptions=True)` 后没检查）

## 挂点 → 对策

| 挂点 | 对策 |
|---|---|
| 只用 print、不会 debugger | 读 `DEBUG_101.md`，练到闭眼能 `pytest --pdb` |
| 盯栈顶、想读懂整个库 | 库是大的。只读数据流经过的那几个函数 |
| 不读 README/文档 | 有 Google 候选人主要因为这个挂。**开场 30 秒读 README** |
| 环境（虚拟环境 / import / Python 版本）吃掉 10 分钟 | 提前拿 recruiter 发的 sample repo 跑通一次 |
| 大范围重写而非最小修复 | 外科手术，不是重构。改完能说清"这个修复对 V 路径没有影响，因为……" |

## 明天怎么练（具体到命令）

```bash
python3 loop/mock.py start bs01     # 拷到 loop/work/bs01/，用你的 IDE 打开
python3 loop/mock.py test bs01      # 跑测试
python3 loop/mock.py ref bs01       # 看参考修复（git apply FIX.patch 后应全绿）
```

**顺序建议**：bs01（暖身，visitor 漏项最好找）→ bs03（off-by-one + 残留状态，最典型）→ bs02（requests 形态）→ bs04 → bs05（并发最难）。

每题旁边有 **`CODE_GUIDE.md`（中文）**逐模块导读。**第一遍可以读**（你现在的目标是先看懂这类代码），**第二遍起别读了**——真实面试里没有这东西。

**练满 4 次计时，其中 1 次不用 debugger**（逼自己练读代码）。

## 并发两题特别说明

bs04 / bs05 的失败测试是**确定性**的（各连跑 20 次输出一致，满载下也一致）。这是刻意的：

> "flake 不是根因"这条规矩要成立，题本身就不能是 flaky 的。

真实面试里如果你判断某个失败是 flake，**re-run 至多一次**，第二次还失败就是真的。绝不能跳过、禁用或隔离一个测试来换绿。

## 自检清单

- [ ] 我在自己的 IDE 里设过图形断点（很多人现场才发现没配好）
- [ ] 我会 `pytest --pdb`，也会 `breakpoint()`
- [ ] 我知道 `n` / `s` / `u` 的区别
- [ ] 我会用 `dir()` / `vars()` 看清一个陌生对象
- [ ] 我的第一个动作永远是跑失败测试，不是读代码
- [ ] 我会出声说"我的假设是……"
- [ ] 修完我会主动问"要我继续找下一个吗"
- [ ] 我练过 ≥4 次计时调试，其中 1 次没用 debugger

## 对应材料

- 调试入门：`loop/rounds/04_bug_squash/DEBUG_101.md`（含在 bs01 上真跑的 pdb 实录）
- 卡片：`loop/study/20-cards/python_debug.md`（51 张）
- 题目：`loop/rounds/04_bug_squash/bs01`–`bs05`
- 真实库 issue 素材：`loop/raw/github_repos.md` §2、`catalog/discovery/2026-09/rounds_material.md` 块 1
- 事实与来源：`loop/LOOP_GUIDE.md` §4
