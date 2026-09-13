# Recruiter 轮 —— 自评表

> 依据：`loop/LOOP_GUIDE.md` §2、`catalog/raw/bq_hm_recruiter.md` §1。这一轮没有打分表，但 recruiter 决定：① 送不送电面 ② 送去哪个 org ③ 在 team matching 时怎么介绍你。AI 轮（Chakra）按 transcript 打分，见 `../../../../../core/playbooks/ai-voice-screen.md` §1。

## 用法

`python3 loop/mock.py bq recruiter -n 5 -m 2`，每题 2 分钟内讲完；讲完按下面 4 项打分，任一项 ≤ 2 分重讲。

## 评分维度

### 1. 具体性（Specific）
| 分数 | 长什么样 |
|---|---|
| 1 | "我对数据平台很感兴趣" |
| 2 | 提到了 Snowflake 的产品名，但和自己无关 |
| 3 | 说出自己用过的原语（Streams/Tasks/MERGE）和踩过的坑 |
| 4 | 3 + 指向一个具体团队方向 + 一个近期事实（Execution Anchor 博客 / Summit 改名 / Postgres GA） |

### 2. 时长控制
| 分数 | 长什么样 |
|---|---|
| 1 | 自我介绍 > 2 min |
| 2 | 90 s 但没有落点 |
| 3 | 60 s，三件事 + 数字 |
| 4 | 3 + 结尾把主动权交回（hook） |

### 3. 边界问题（薪资 / level / 他家进度 / 签证）
| 分数 | 长什么样 |
|---|---|
| 1 | 报了数字或他家公司名 |
| 2 | 回避得生硬 |
| 3 | 标准句式，不失礼 |
| 4 | 3 + 顺势问对方 level 结构与 team matching 机制 |

### 4. 反问质量
| 分数 | 长什么样 |
|---|---|
| 1 | 没有问题 |
| 2 | 问了官网能查到的 |
| 3 | 问流程矛盾（Chakra vs Intake、OA 有无） |
| 4 | 3 + 问 org/headcount，为 team matching 埋线 |
