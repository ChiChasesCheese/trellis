# loop/ — Stripe 面试 Loop 演练套件

OA 之后全部轮次（recruiter → HM → 电面 → onsite：bug squash / integration / coding / system
design → behavioral）的离线 mock 面试环境。技术轮沿用根目录 OA 套件的约定（见
`../CONVENTIONS.md`：`partN()` + `main()`、pytest markers、根 `../conftest.py` 的 `impl` /
`run_script` fixture）；`loop/mock.py` 是入口，用法对齐根目录的 `../drill.py`。

## 目录一览

```
loop/rounds/01_recruiter/  02_hm/  08_behavioral/   非编码轮：bank.json 题库 + 准备材料
loop/rounds/03_phone_screen/psNN_slug/               与 problems/qNN 同结构（problem.md 等）
loop/rounds/06_coding_onsite/cdNN_slug/              同上
loop/rounds/05_integration/intNN_slug/               同上 + data/，测试自起 mockserver
loop/rounds/04_bug_squash/bsNN_slug/                 src/<pkg>/ tests/ README.md solution/FIX.patch
loop/rounds/07_system_design/sdNN_slug/              prompt.md rubric.md model_answer.md followups.md
loop/mockserver/                                     stdlib http.server：maps / payments
loop/work/<id>/                                      bug squash 工作区（已 gitignore，会被清空重建）
loop/study/                                          前置课 + 每轮准备材料 + 速记卡片
loop/CATALOG.md · loop/tree/                         题库总表、知识树（校验脚本）
```

## `mock.py` 用法速查

```bash
python3 loop/mock.py list                    # 按轮次列出 id + 题名 + 时长；非编码轮列题库题数
python3 loop/mock.py show <id>                # 打印题面（sd 打印 prompt.md；bs 打印 README.md）
python3 loop/mock.py start <id> [-m MIN]      # 打印题面 + 复位/拷贝工作区 + 开始计时
python3 loop/mock.py test <id> [-k EXPR]      # 跑你的 starter（或 bs 的 loop/work/<id>）
python3 loop/mock.py ref <id> [-k EXPR]       # 跑参考解（bs 会先 git apply solution/FIX.patch）
python3 loop/mock.py time <id>                # 查看剩余时间
python3 loop/mock.py serve <id> [--port N]    # int 题：启动题面声明的 mockserver（Ctrl-C 停止）
python3 loop/mock.py bq [round] [-n N] [--seed S]   # 从 recruiter/hm/behavioral 题库随机抽题计时
python3 loop/mock.py status [--all] [--all-kinds]   # 进度板：哪些题绿了、最好用时、最近 10 次趋势
```

`id` 用短前缀即可（`ps01`/`cd03`/`int01`/`bs02`/`sd01`），只要能在
`loop/rounds/*/<id>_*` 下唯一匹配。默认时长：ps 45 · cd 60 · int 60 · bs 60 · sd 45 分钟；
`bq` 每题默认提示 3 分钟。

## 演练协议

1. **读题 5 分钟**：`start <id>`，先把 problem.md / prompt.md / README.md 完整看一遍，圈出
   worked example 和边界条件，再动手写。
2. **编码**：ps/cd/int 题编辑 `starter.py`，随时 `test <id> [-k partN]` 跑局部测试；bs 题在
   `loop/work/<id>/` 里改（IDE 直接打开这个目录），`test <id>` 重跑同一份拷贝。
3. **最后 5 分钟自测**：`test <id>` 全量跑一遍，看 `time <id>` 是否超时；卡住了用
   `ref <id>` 对照参考解定位差异，别在最后一刻死磕。
4. **bug squash 特例**：`start bsNN` 会先把 `src/`+`tests/` 拷到工作区并跑一次 pytest 显示
   失败用例——**先看失败测试再读 README**，这才是真实排查顺序；改完 `test bsNN` 重跑确认
   全绿，`ref bsNN` 可看参考修复（`git apply` 后跑测试）。
5. **integration 特例**：编码前先另开一个终端 `serve intNN` 把本地 mockserver 跑起来，
   题目里的 HTTP 客户端代码打到 `localhost`；`test intNN` 会自己起临时 mockserver，不依赖
   `serve` 常驻。
6. **非编码轮**：`bq [recruiter|hm|behavioral] -n 3` 抽题、计时口述；`show`/`list`
   之外没有自动测试，对照 `rounds/<round>/rubric.md`（若存在）自评。

## 测试

`loop/tests/test_mock.py` 用 `tmp_path` 造假的 `rounds/`/`work/` 目录树（monkeypatch
`mock.ROUNDS`/`mock.WORK`/`mock.MOCKSERVER`），不碰真实 `loop/` 内容。运行：

```bash
rtk proxy python3 -m pytest loop/tests -q
```
