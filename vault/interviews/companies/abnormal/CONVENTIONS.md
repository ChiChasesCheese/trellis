# 练习题的形状（Abnormal kit）

Abnormal 的 AI Technical Screen 不是"写一个函数"：是**在别人写好的 Python 代码库里，用 Claude Code，把一个说不清楚的需求做成契合系统的 v1**。
所以本 kit 的主力题型是 **codebase 练习（`cbNN`）**，不是 `solution.py` 单文件题。其它题型（若后续轮次需要）沿用 `../stripe/CONVENTIONS.md`。

## 1. codebase 练习：目录

```
loop/rounds/01_ai_screen/cb01_mailguard/
  BRIEF.md          面试第 0 分钟你拿到的东西：一段话介绍这是什么系统（英文，不剧透）
  tickets/
    t1_<slug>.md    一张故意说不清楚的 ticket（英文，2–8 行，像面试官口述/Jira 原文）
  starter/          代码库本体 = 你要打开的 repo（自带 README、包、tests/、fixtures/；只依赖标准库 + pytest）
  solution/         starter + 全部 ticket 的参考实现（含新增测试），风格与 starter 一致
  acceptance/       隐藏验收：conftest.py + test_t1.py …（只走系统已有的入口，见 §3）
  interviewer.md    面试官视角：每张 ticket 的澄清问答、隐藏期望（该复用哪个抽象）、追问、按维度的打分信号（中文 + 英文原句）
  walkthrough.md    参考的 60 分钟：探索用的 Claude Code 提示词 → 第 10 分钟该说出的心智模型 → 每张 ticket 的假设/里程碑/验证/口播（中文 + 英文口播）
  REPORT.md         代码库规模（命令实测）、测试数、埋的坑清单、验收测试清单
```

每张 ticket **独立地从 starter 开始**（一次模拟 = 探索 + 一张 ticket）。`solution/` 同时实现全部 ticket，彼此不冲突。

## 2. 代码库必须像"真的别人的代码"

- 2,000–3,500 行 Python（含测试），25–45 个文件，一个顶层包；`python -m <pkg> ...` CLI 能在 `fixtures/` 上端到端跑出结果。
- 有清晰、可被复用的抽象，且**ticket 的正确做法依赖它们**：注册表 / 插件基类、settings 或按租户配置、存储层（`sqlite3` repository）、领域模型 dataclass、已有工具函数（时间窗口、邮箱/域名归一化…）、日志与指标、错误类型。
- 有真实的噪音：一段过时的 README、一个标了 deprecated 的旧模块（看起来像该改的地方但不是）、几个 TODO、一个 feature flag 机制、`CONTRIBUTING.md` 写着约定（"每个 detector 在 `tests/detectors/` 有测试"之类）。
- starter 自带测试全绿且 < 5 s；`solution/` 自带测试也全绿（含新增）。
- 英文代码、英文注释、英文文档（这是给你在面试里读的"别人的代码"）。

## 3. 验收测试（`acceptance/`）

- `conftest.py` 决定测哪份代码：环境变量 `CODEBASE=<绝对路径>`（你的练习副本）> `IMPL=starter`（`../starter`）> 默认 `../solution`；并把该包从 `sys.modules` 清掉。
- 只通过**系统原本就有的入口**测行为（pipeline 的 `process()`、CLI 输出、HTTP 路由、存储查询），只有 ticket 本身点名的新接口（命令名、端点、配置键）才可以出现在测试里——这样测试不惩罚合理的设计差异。
- marker：`core`（v1 必须过）· `stretch`（问对了澄清问题或做了第二个里程碑才会过）· `regression`（已有行为不能被破坏）。
- 验收口径（`tools/verify_suites.py`）：solution 全绿；**未改动的 starter 在 `core` 上全红**（`regression` 在 starter 上本就绿，允许）。

## 4. 练习命令（在 kit 根目录）

```
python3 loop/ai_screen.py list                       # 全部代码库与 ticket
python3 loop/ai_screen.py start cb01 t1              # 复制 starter 到 ~/abnormal-practice/cb01-t1-<时间>/，git init，打印 ticket 与 60 分钟时间表
python3 loop/ai_screen.py check cb01 t1 <练习目录>     # 跑该 ticket 的验收 + 代码库自带测试，统计你新增的测试，打印 rubric 自评表
python3 loop/ai_screen.py reveal cb01 t1             # 做完再看：interviewer.md 中该 ticket 的段落
```
