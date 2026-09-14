---
id: cc-transfer-playbook-failure-log
node: transfer.playbook
type: qa
---
## Q
Your debrief note says "I was too slow and messed up part 4." Rewrite it into something usable, and give the format.

## A
**Record the class of failure, the minute it happened, and the counterfactual — three lines.**

- **Class**: *format* (trailing newline), *boundary* (`>` vs `>=`), *modelling* (the state could not express part 4), *performance* (a quadratic scan), *process* (started typing before reading part 5).
- **Minute**: "lost 12 minutes at minute 35 rewriting the state" is actionable; "too slow" is not.
- **Counterfactual**: the one earlier decision that would have changed it — almost always made long before the symptom appeared.

After four rounds one class has appeared twice. That repeated class is your next week of practice; everything else in the note is noise.

## Q zh
你的复盘笔记写着「我太慢了，part 4 搞砸了」。把它改写成有用的东西，并给出格式。

## A zh
**记录失败的类别、发生的分钟、以及反事实 —— 三行。**

- **类别**：*格式*（结尾换行）、*边界*（`>` 与 `>=`）、*建模*（状态表达不了 part 4）、*性能*（一次平方级扫描）、*流程*（读完 part 5 之前就开始敲）。
- **分钟**：「第 35 分钟起花了 12 分钟重写状态」是可行动的；「太慢了」不是。
- **反事实**：那个本可以改变结果的更早的决定 —— 几乎总是在症状出现之前很久做出的。

四轮之后，会有一个类别出现两次。那个重复出现的类别就是你下一周的练习内容；笔记里其余的都是噪音。
