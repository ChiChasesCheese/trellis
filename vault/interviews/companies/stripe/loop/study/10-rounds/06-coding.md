# 06 · Onsite · Programming Exercise（45–60 min）

> 事实层在 `loop/LOOP_GUIDE.md` §6。本章讲练法。

## 这轮和电面的真正区别

同类题，但更长、part 更多，而且 —— **这一条最重要** ——

> **VO coding 期望你做类设计，电面不用。**

一份 2026 年面经把这个差别写得极清楚：候选人在 VO 挂了，原因是

> "一开始没注意 input 要写 class，导致没写到第三 part"

而同一个人在电面只写完 2/3 part、第三个口头说思路，**当天就过了**。

所以：电面像脚本题（函数 + dict 够用）；**VO coding 是小型 LLD**。你按电面的写法糊一堆 dict + 函数，加到 part 2 改需求时就会被自己的数据结构卡死。

其余差别：更常"从 JSON/测试数据出发按逐步加码的需求实现"，有时先 clone repo；平台 CoderPad / 本地 IDE / HackerRank 都有；"Stripe usually wants two parts"（L2 说法）。

## 怎么下笔

**先写接口签名，再填实现。** 本仓库 cd 系列的 `starter_template.py` 就是按这个形状给的。

```python
class SubscriptionStore:
    def add(self, sub: Subscription) -> None: ...
    def change_plan(self, sub_id: str, new_plan: str, at: date) -> None: ...
    def emails_between(self, start: date, end: date) -> list[str]: ...
```

写完签名先跑一遍空实现，让整条链路通了再填。**面试官看到接口就知道你想清楚了**，这本身就在得分。

判断标准：**如果一个实体要在多个 part 之间携带状态、或者要挂方法，就建类**；纯查表用 dict。

## 追问方向是固定的

做完主体，面试官会从这几个方向追：

**部分退款 · 去重 / 幂等 · 时间范围查询 · 持久化 · 并发 · 海量数据**

每道题的 `REPORT.md` 里有「面试官会怎么追问」一节，**做完题一定要读那一节并口头答一遍**。这轮的追问权重很高，答不上等于没做完。

## AI Programming Exercise（2026 新增）

HackerRank 内嵌 AI，**30 分钟**，题为 transactions + rules（关键词 → AND/OR）。评的是：

> 能否指挥 / 验证 / 调试 AI 输出，而不关掉脑子。

打法：让 AI 读 README 出计划、生成代码，**自己写测试**，主动抓它的过度工程和漏边界。
练习题是 `cd07_transactions_rules_ai`。

**注意：除这一轮外，其余所有轮次严禁 AI。**

## 真实拒因（一手）

- 两个 part 都完成，但**第二个 part 有 bug 没修** → 拒因之一
- "output has some extra commas" → 格式
- 面试官要求改变量名可读性 → 命名

三条都不是"不会做"，都是**收尾质量**。留足最后 5 分钟。

## 明天怎么练（具体到命令）

```bash
python3 loop/mock.py start cd01 -m 60
```

顺序建议：

| 题 | 练什么 |
|---|---|
| `cd01` 订阅邮件调度 | **类设计**的入门；和 OA 的 q07 同题材但规则集不同，**别混着背** |
| `cd02` 支付账本 | 账本建模 + 追问（部分退款/去重） |
| `cd03` 账户调度 LRU | 数据结构组合 |
| `cd04` 限流 4-part | part 4 有线程安全测试 |
| `cd05` 企业账户核验 | 多层校验规则 |
| `cd06` 滑窗可疑用户 | 窗口 + 分组 |
| `cd07` transactions + rules | **AI 轮专用** |
| `cd08`–`cd10` Bitfont 三版本 | **S09 字节级输出** + `cd09` 的 S25 二进制帧解码 |

OA 库里也有 VO 常考的：`q07 q13 q32 q23`。

**Bitfont 三题特别说明**：同一个题名下三个互不兼容的版本，本仓库各建一道。`cd08` 是真实复原，`cd09`/`cd10` 是重建题（题面有警示块）。练的是**渲染类题目的字节级格式控制**——多一个空格、行尾多一个字符就挂。

## 自检清单

- [ ] 我拿到题会**先写类和接口签名**，而不是直接写逻辑
- [ ] 我能说清"这个实体为什么建类，那个为什么用 dict"
- [ ] 我的输出格式集中在一个 `_format()` 函数里
- [ ] 我留了最后 5 分钟做收尾（命名、格式、跑全部样例）
- [ ] 我读过每道题 REPORT 的「面试官会怎么追问」并口头答过
- [ ] 我知道部分退款 / 幂等 / 并发 / 海量 这四个方向该怎么答
- [ ] AI 轮：我练过"让 AI 写、我写测试"这个分工

## 对应材料

- 题目：`loop/rounds/06_coding_onsite/cd01`–`cd10`；OA 的 `q07 q13 q32 q23`
- 卡片：`loop/study/20-cards/patterns.md`
- **模板**：`loop/study/00-prereq/templates/skeleton.py`——VO coding 尤其要先写接口签名，骨架就是签名
- 文章：`loop/study/30-articles/cd*.md`
- 事实与来源：`loop/LOOP_GUIDE.md` §6
