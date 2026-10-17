%% trellis:begin %%
# 机器人餐厅（Robot Restaurant）
*Amazon 专项（Amazon OOD）*

电面 OOD：点单、机器人分配、做菜与送餐状态机，机器人忙闲调度。（重建）

**Core** — part of the first pass through this subject.

**Requires:** [[domains/low-level-design/map/patterns.state|状态模式（State）]], [[domains/low-level-design/map/patterns.strategy|策略模式与可替换算法（Strategy）]]

## Readings
- [[solution-amz-robot-restaurant|设计题解：机器人餐厅（Robot Restaurant）]]
- [[src-1p3a-amz-robot-restaurant-charging|一亩三分地：Amazon Robotics 实习面经]]
- [[src-1p3a-amz-robot-restaurant|一亩三分地：Amazon SDE II 电面（先 tech 再 LP）]]
- [[src-pydocs-amz-robot-restaurant|enum — Support for enumerations（Python 标准库文档）]]

## Drills
- [[design-amz-robot-restaurant|Drill：机器人餐厅（Robot Restaurant）]]

## Cards (9)
1. [[amz-robot-restaurant-how-asked-and-three-questions]]
2. [[amz-robot-restaurant-objects-and-their-jobs]]
3. [[amz-robot-restaurant-stage1-tick-flow-in-code]]
4. [[amz-robot-restaurant-robot-state-machine-transition-table]]
5. [[amz-robot-restaurant-assignment-policy-function-vs-class]]
6. [[amz-robot-restaurant-followup-split-cook-and-delivery-robots]]
7. [[amz-robot-restaurant-edge-low-battery-no-free-charger]]
8. [[amz-robot-restaurant-concurrency-one-lock-around-queue-and-robots]]
9. [[amz-robot-restaurant-common-mistake-charger-counter-leak]]
%% trellis:end %%

## Notes
