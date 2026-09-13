---
id: leetcode-q-basic-calculator-ii-pattern
node: stack-queue-monotonic.stack
type: qa
anki: 1787102261931
tags: [lc::227, leetcode, pattern, recall]
---
## Q
如何在一次遍历中计算含 +、-、*、/ 的表达式（无括号）？

## A
维护 num（当前数字）、ops（上一个运算符，初始为 '+'）、prev（待处理的最近一项）、res（已确定不会被 * / 影响的累加和）。遍历每个字符：数字则累加 num；遇到运算符（或到达字符串末尾）时，根据 ops 处理 prev：'+' → res+=prev, prev=num；'-' → res+=prev, prev=-num；'*' → prev*=num；'/' → prev=int(prev/num)（向零截断需用 int(prev/num) 而非 //，因为负数时 // 是向下取整）。然后更新 ops=当前字符，num=0。最终返回 res+prev。也可用等价的栈写法：'+' push num，'-' push -num，'*'/'/' 与栈顶做运算后替换栈顶，最后 sum(stack)。

**Evidence**

calculate 方法用 prev/ops/num/res 变量实现；calculate0 方法用栈实现，两者等价，除法均用 int(prev/num) 保证向零截断。

[原文 ↗](obsidian://open?vault=lc&file=questions%2F227%20-%20Basic%20Calculator%20II)
