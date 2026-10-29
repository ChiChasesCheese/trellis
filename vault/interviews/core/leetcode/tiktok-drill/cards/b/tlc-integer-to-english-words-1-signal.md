---
id: tlc-integer-to-english-words-1-signal
node: b.integer-to-english-words
type: qa
step: 1
---
## Q
**LC 273 整数转换英文表示**｜Hard · CodeTop 国内累计 3 次 · 最近 2026-07-02（CodeTop）

把非负整数 `num` 转成英文读法，单词首字母大写、单词之间一个空格。`0 <= num <= 2^31 - 1`。例：`123` → `"One Hundred Twenty Three"`，`12345` → `"Twelve Thousand Three Hundred Forty Five"`，`1234567` → `"One Million Two Hundred Thirty Four Thousand Five Hundred Sixty Seven"`。

题面里哪些信号指向哪个模式？从暴力解怎样一步步推到最优解？

## A
**信号 → 模式。**
- 「数字转读法」→ **模拟 + 查表**：没有搜索或优化，难点是把规则分层，覆盖所有边界。
- 上界 `2^31 - 1` 约 21 亿 → 最多到 `Billion`，按三位一组切只有 4 组。
- 英语读法的结构：量级词每三位出现一次；组内 1 到 19 各有单词，20 以上是「整十 + 个位」→ 天然两层：组间按 1000 切，组内按 100、20 切。

**推导链。**
1. 朴素：逐位读十进制数字，每一位查一个单词。
2. 问题：11 到 19 不是「十位 + 个位」；量级词不是每位都有；中间的 0 不读。逐位处理要写大量特判。
3. 洞察：读法本身就是三位一组的递归结构，组内读法与量级无关。把问题拆成「1 到 999 怎么读」和「每组接什么量级词」。
4. 最优：`divmod(num, 1000)` 从低位取组，非 0 的组用 `below_thousand` 读出再接量级词，最后反转拼接；`0` 单独返回 `"Zero"`。时间 `O(log num)`。

**同模式的题**：LC 12 整数转罗马数字、LC 13 罗马数字转整数、LC 8 字符串转换整数。
