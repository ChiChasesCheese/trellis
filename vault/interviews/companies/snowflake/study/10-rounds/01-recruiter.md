# 01 · Recruiter / HR call（15–30 min）

> 事实层在 `../../loop/LOOP_GUIDE.md` §2；题库 `../../loop/rounds/01_recruiter/`（18 题含 Chakra 6 题）。

## 这轮到底考什么（一句话）

**你适不适合送去电面，以及送去哪个 org。** 不考技术，但方向偏好会决定你后面匹配到谁。

## 必备的四段话

| 段 | 长度 | 在哪 |
|---|---|---|
| 自我介绍 | 45 s / 60 s | `../../../03-chakra-playbook.md` §2（60 s 版，删掉 intern 句即 45 s） |
| Why Snowflake | 60 s | `../../../fit.md` §1 |
| 方向偏好 × 3 | 各一句 | `../../../fit.md` §5；`../10-rounds/08-team-matching.md` |
| Level / comp / 签证 | 各一句 | 见下 |

**边界问题标准句：**
- Comp："I'm focused on fit and level right now; I'd expect a competitive package for the scope, and I'm happy to discuss once we know the team."
- Level："I'd like leveling to reflect the end-to-end ownership I've had; I trust the loop to calibrate."
- 他家进度："I'm in a few processes and my timeline is roughly X weeks."（不报公司名）
- 签证："H-1B effective October 2026; I'll need a transfer, no lottery."

## 必问 recruiter 的三件事

1. Chakra 筛选和 Ashby 的 "Talent Intake" 是不是同一环节？
2. 这个 track 电面前有没有 OA？
3. team matching 在 onsite 前还是后？现在在匹配哪些 org、headcount 是否已批？

## 练法

```bash
python3 loop/mock.py bq recruiter -n 5 -m 2
```
对 `../../loop/rounds/01_recruiter/rubric.md` 四维打分。
