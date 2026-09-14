---
id: cc-round-comm-taking-a-hint
node: round.communication
type: qa
---
## Q
Mid-implementation the interviewer asks, "what happens if the same charge is disputed twice?" You realise your code double-decrements. How do you respond?

## A
**Treat the question as a correction, not a quiz.** Say it back, name the consequence, fix it now.

> "Twice would decrement the counters twice. I'll pop the ledger entry on the first dispute, so the second finds nothing and is a no-op."

Failure modes graded harshly: defending the current code, saying "good question!" and continuing unchanged, or silently patching without acknowledging where the idea came from. Interviewers explicitly score hint-uptake; a hint absorbed in one move reads as senior. See [[cc-model-idem-second-occurrence-noop]].

## Q zh
写到一半，面试官问：「同一笔扣款被争议两次会怎样？」你意识到自己的代码会减两次。怎么回应？

## A zh
**把这个问题当成纠正，而不是考题。** 复述一遍、说出后果、当场修。

> 「两次会把计数器减两次。我在第一次争议时就把 ledger 条目弹出，这样第二次找不到记录，自然是 no-op。」

会被严厉扣分的反应：为现有代码辩护；说一句「好问题！」然后照旧；或者默默打补丁却不承认想法从哪来。面试官明确会给 hint 吸收度打分；一步就吸收的提示读起来很资深。见 [[cc-model-idem-second-occurrence-noop]]。
