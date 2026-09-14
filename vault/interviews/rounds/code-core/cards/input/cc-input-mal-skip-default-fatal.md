---
id: cc-input-mal-skip-default-fatal
node: input.malformed
type: qa
---
## Q
For a bad field, name the three possible policies and how you choose between them.

## A
**Skip the row · substitute a default · treat it as fatal.** The statement chooses, per field, and almost always says so in a half-sentence.

- Skip: "corrupted rows are skipped and counted" — the row contributes nothing, and the count is usually part of the output.
- Default: "missing trailing columns count as empty", "an unparsable `q` counts as 1.0".
- Fatal: "a rate ≤ 0 rejects the whole input" — rare, and always explicit.

Write the chosen policy next to the check. The failure mode is mixing them: skipping a row for one bad field while silently defaulting another in the same row.

## Q zh
对一个坏字段，说出三种可能的策略，以及怎么在它们之间选择。

## A zh
**跳过整行 · 用默认值代替 · 视为致命错误。** 由题面按字段决定，而且几乎总会用半句话说出来。

- 跳过：「损坏的行被跳过并计数」—— 该行不贡献任何东西，而计数往往是输出的一部分。
- 默认：「缺失的末尾列按空处理」「无法解析的 `q` 按 1.0 计」。
- 致命：「rate ≤ 0 则整个输入被拒绝」—— 少见，而且总是明说。

把选定的策略写在检查旁边。失败模式是把它们混着用：同一行里因为某个坏字段跳过整行，却又对另一个字段悄悄取默认值。
