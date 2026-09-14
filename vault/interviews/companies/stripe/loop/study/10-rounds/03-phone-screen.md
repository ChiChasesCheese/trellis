# 03 · Technical Phone Screen（60 min = 45 编码 + 15 Q&A）

> 事实层（形式 / 通过线 / 挂点）在 `loop/LOOP_GUIDE.md` §3，本章不重复。
> 本章回答的是：**明天坐下来练这一轮，具体做什么。**

## 这轮到底考什么（一句话）

**把一段啰嗦的业务描述，快速翻成好代码。** 不是算法题。

Stripe 员工的原话是 "Read in this JSON, transform it / do something interesting with it"。
难点有两个，都不在算法上：

1. **阅读理解** —— 题面故意写得长，规则藏在句子里
2. **为 part N+1 设计** —— 做完一个 part 才给下一个，而下一个会动你的数据结构

## 通过线：没有硬线

三条一手证据互不相容：

| 说法 | 来源 |
|---|---|
| recruiter **面试前明说** "you need to solve **4/4 parts** to proceed forward" | 2026-06 一手 |
| 另一位的 recruiter 说 "**it doesn't depend on how many parts you solve**"，本人 **2/3 过了** | 2026-06 一手 |
| Python ≈ 3/4 part、Java/C++ ≈ 2/4 part | 本仓库原记录（Blind） |

而且 **part 总数本身就不固定**——有 3-part 的电面，也有 2-part 的。

**实用读法：把 part 数当努力方向，不当及格线。真正在被打分的是代码质量和出声沟通。**

面试官不完全按 rubric 判。四个真正打动人的点：**High code quality · Fast completion · Simple clear thought process · Humble attitude**。

注意"Fast completion"排第二 —— 但 prep 材料又说 "quality over speed"，**有候选人因为打磨太久而挂**。
这个矛盾的解法是：**Part 1 快，Part 3 慢**。前面的 part 都是后面的地基，越快锁死越好。

## 45 分钟怎么走

| 时间 | 做什么 | 出声说什么 |
|---|---|---|
| 0–5 | **读完 intro + 全部 part 再动手** | "我先把 intro 和三个 part 都读一遍，避免第一版结构撑不住后面" |
| 5–8 | 复述 + 确认假设 | "我理解是……；有两个地方想确认：空输入返回什么？相同分数怎么排序？" |
| 8–10 | 骨架先行 | `main()` 读入 → `parse()` → `part1()` 空实现 → 打印。**先让整条链路跑通** |
| 10–20 | Part 1 + 自测 | 写完立刻用题面样例验，再补 2–3 个自己的 `assert` |
| 20–33 | Part 2 | 复用 part 1 的 helper；改不动就说明分层错了 |
| 33–42 | Part 3 | 时间不够就**口头说思路**——这能过 |
| 42–45 | 收尾 | 排序 key 补全、格式集中到一个函数、跑一遍全部样例 |

**没有自动测例。** 你自己造输入、自己验证。这是最多人栽的地方（有人一直等系统给反馈，等到时间结束）。

## ⚠️ 约束会藏在 intro 里（一条代价 12 个月 cooldown 的挂经）

> "the **sliding window constraints where nowhere mentioned in the actual task (part 1)** but rather was
> **buried in the intro** which i skimmed cause i knew i was gonna be tight on time. This led me to make wrong
> assumptions and i wasted so much time. Now I'm blocked for 12 months"

**intro/背景段不是废话，是约束的藏身处。** 前 5 分钟连 intro 一起读，
**把 intro 里每个数字 / 时间窗 / 阈值抄进代码注释再动手。**

有意思的是这条建议在 2017 年就有人说过（"just make sure to **read the problem statement carefully**"）——
**九年没变的建议，通常意味着九年没变的挂法。**

## ⚠️ 两条平台/工具的现实（都有实拒案例）

1. **"可以用自己 IDE + 任意库"是书面条款，现场可能被推翻。** 2025-10 一位 Backend 候选人按 prep guide
   准备了 Java + Lombok + Jackson，面试官当场要求改用 HackerRank 并禁用 Lombok，**两次争论各 2–3 分钟，
   两天后被拒**。同帖两条独立回复："don't use your own IDE because they aren't prepared for it
   **even though they say so**"、"expect to code in the **whiteboard kind of a scenario**"。
   **面试官要求换什么就换什么，一句 "sure, happy to" 结束，不要引 prep guide 反驳。**
2. **HackerRank 很可能只给标准库。** 那位面试官的理由就是 "it will not [work] on hackerrank"；
   2024 另有两条同向说法（Gson 在 HackerRank IDE 里不工作 / "Hackerrank has always dictated how API calls
   should be done per language. Usually it is using the **standard library**"）。这两条不是一手，
   但**对 Python 的含义是明确的：练 `urllib.request`，别练 `requests`。**

## 挂点 → 对策

| 挂点 | 对策 |
|---|---|
| 追求最优复杂度，不先写能跑的 | 先写 O(n²) 能跑的版本，说一句"先跑通，需要的话我再优化"。复杂度"carry little weight" |
| 期待自动测例 | 开场就说"我会自己写几个 assert 来验" |
| 求助 ≥3 次 | 卡住先自己出声推演 30 秒再问；问的时候问**决策**（"这里我倾向 A，因为 X，你觉得呢"）不是问答案 |
| 只做到第一个 follow-up | Part 1 提速。你在 part 1 省的每一分钟都是 part 3 的 |
| 有剩余时间却没推进 | **做完一个 part 立刻主动要下一个**："this part works, here are my asserts — can we move on?" 一位候选人剩 15 min 才开口，面试官直接转 Q&A 了；另一位剩 10+ min "没得到机会"尝试 |
| 把 part 1 的 bug 带进 part 2 | 每个 part 写完立刻 2–3 个 assert。有一手挂经就是回头查 part 1 的 bug，连锁吃掉后面全部 part |
| 花太多时间打磨 | 变量名一次到位，别回头改；格式化集中一处，别散在各处 |

## 明天怎么练（具体到命令）

**热身梯度**（前两天，别一上来啃硬的）：

```bash
python3 loop/mock.py start ps08 -m 45   # Min/Max comparator，最轻
python3 loop/mock.py start ps05 -m 45   # Numeronym，规则干净
python3 loop/mock.py start ps07 -m 45   # 卡号脱敏，纯字符串
```

**主力**（refs 最高的电面题，撞题率也集中在这段）：

```bash
python3 drill.py start q19    # Accept-Language，4 part，2021→2026 常青
python3 drill.py start q21    # 汇率换算，图 + BFS
python3 drill.py start q22    # 运费，25 refs，全库最高
python3 drill.py start q25    # 发票对账
python3 drill.py start q20    # 手续费 + 对账，4 part
```

**loop 里的电面题**：

```bash
python3 loop/mock.py start ps01 -m 45   # 滑窗 + TopK
python3 loop/mock.py start ps06 -m 45   # 巴西应收款分组
python3 loop/mock.py start ps09 -m 45   # 记录关联（真实复原）
python3 loop/mock.py start ps12 -m 45   # CSV 建树 + 文件树输出（真实复原）
```

**冷启动专练**（每周 2 次，这是唯一能治"撞不上就写不出来"的训练）：
挑一道**没看过的**，45 分钟计时，全程 think loud（真的出声）。

每次跑完 `python3 drill.py status` 看趋势 —— **首个 part 通过的用时在不在下降**，那是手感恢复的客观证据。

## 复盘怎么写

做完一题，读 `loop/study/30-articles/<id>_*.md` 对照。重点不是看答案，是看**第 2 节「读题：把文字变成模型」**——
比较它的"一句话建模"和你当时脑子里的那句差在哪。差在哪，下次就赢在哪。

## 自检清单（进考场前）

- [ ] 我能在 3 分钟内把一段业务描述复述成"这是一个按 X 分组的 Y 问题"
- [ ] 我的解析永远是独立函数，不和业务逻辑揉在一起
- [ ] 我每个 `sorted` 都能说出完整的 tie-break key
- [ ] 我写完每个 part 都会立刻写 2–3 个 assert
- [ ] 我知道金额要用整数分，不用 float
- [ ] 我能一边写一边说，而不是沉默五分钟
- [ ] 我练过至少 5 次 45 分钟计时的冷启动

## 对应材料

- 题目：`loop/rounds/03_phone_screen/ps01`–`ps13`；OA 库里的电面高频 `q19 q21 q22 q25 q20 q08 q18`
- 卡片：`loop/study/20-cards/patterns.md`（跨题模式）
- 前置：`loop/study/00-prereq/04-字符串与解析`、`05-csv与json`
- **模板**：`loop/study/00-prereq/07-模板-常用模式.md` + `templates/`——多 part 骨架和九个高频模式，做题前先把骨架敲熟
- 事实与来源：`loop/LOOP_GUIDE.md` §3
