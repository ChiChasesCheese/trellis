---
id: uth-devtools-regex-1-backtrack-automata
node: devtools.regex
type: qa
step: 1
---
## Q
**回溯引擎 vs 自动机**｜Python re · Go regexp

为什么一条正则能把 Python 的 `re` 卡死，而同样的正则在 Go 里不会？

## A
**结构。** Python、Java、PCRE 是回溯（backtracking）匹配器：沿着模式一个分支一个分支地试，失败就退回。RE2 和 Go 的 `regexp` 编译成自动机，逐字符推进状态集合，时间与输入长度成线性。

**细节。**

- Russ Cox 的经典例子：`a?` 重复 n 次再接 `a` 重复 n 次，去匹配 n 个 `a`；n = 29 时 Perl 要六十多秒，Thompson NFA 约 20 微秒
- Go 文档明确保证匹配时间与输入大小成线性
- RE2 不支持反向引用和广义断言（环视）

**为什么。** 反向引用要记住之前匹配到的内容，自动机做不到；线性时间的保证，是用放弃这些语法换来的。

**对应 LeetCode：** LC 10 正则表达式匹配 · LC 44 通配符匹配 · LC 65 有效数字
