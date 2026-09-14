---
id: cc-round-debug-failing-test-id
node: round.debugging
type: qa
---
## Q
All you get back is "test 12 failed" — no input, no expected output, no diff. What can you actually infer, and what do you do?

## A
**Infer the part, then run the standard edge catalogue against it.** Graders group tests by part, so test 12 of 20 with five parts is Part 3; the visible samples are usually the first tests in each group, so a failure late in a group is an *edge* test, not the happy path.

Then, in order: empty input, single record, duplicate id, out-of-order events, zero and negative values, exactly-at-threshold, and the largest input. One of them reproduces it far more often than staring at the code does.

## Q zh
你唯一拿到的反馈是「test 12 失败」—— 没有输入、没有期望输出、没有 diff。你实际能推断什么，然后做什么？

## A zh
**先推断是哪一部分，再对它跑一遍标准边界清单。** 评测机按部分分组，所以五部分共 20 个测试里的第 12 个是 Part 3；可见样例通常是每组的头几个测试，因此组内靠后的失败是**边界**测试，而不是 happy path。

然后按顺序：空输入、单条记录、重复 id、乱序事件、零和负值、恰好等于阈值、最大规模输入。它们中的某一个复现问题的概率，远高于盯着代码看。
