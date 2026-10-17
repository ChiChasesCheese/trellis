# Task: amazon.amz-robot-restaurant

- **Leaf id**: `amazon.amz-robot-restaurant`   **slug**: `amz-robot-restaurant`   **kind**: problem
- **题目**: 机器人餐厅（Robot Restaurant）
- Instructions: `proposals/lld/PROBLEM_AGENT.md` + `proposals/lld/AMAZON_AGENT.md` (the latter wins).

## What Amazon candidates reported (2026-09-16..10-16 unless noted) — quote at most one sentence per source

- 1p3a 1189999 (2026-09-18, Amazon SDE II phone interview; same candidate as 1193105, whose OP says 「9 月 18 日 phone interview, 面筋在这儿」): visible 「这个面试是先tech, 再LP。tech 问了三个问题，第一题就是 要死刘」; a reader's reply lists the rest: 「…剩下20分钟你完成了设计机器人餐厅以及追问以及设计file watcher system？」 https://www.1point3acres.com/bbs/thread-1189999-1-1.html [medium for the problem name; body hidden]
- 1p3a 1191952 (2026-10-04, Amazon Robotics intern, interviewed 2026-03): a reader asks 「第一轮机器人充电那题，是怎么维护 robot / charging station 状态的？低于 50% 但没空 charger 怎么处理？」 https://www.1point3acres.com/bbs/thread-1191952-1-1.html [medium; a robot-state problem from another team — use as the battery/charging follow-up, labelled 推断]

## (reconstructed) — not in any visible report

- almost everything except the name: orders, robots (cook / serve), robot states, assignment policy, battery & charging follow-up. Say so plainly in 题目与澄清

## Reuse / link (our own repo first)

- bank [[solution-restaurant]] (tables/orders/kitchen — link)
- concept leaves patterns.state, patterns.strategy

## Card ladder notes

- ladder; step 4 = robot state machine (IDLE → COOKING/DELIVERING → CHARGING) with a transition table; step 7 = battery below threshold and no free charger
