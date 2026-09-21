---
id: string-interning-purpose
node: memory.interning-immortal
type: qa
source: cpython-internals
---
## Q
字符串驻留（string interning）保证了什么性质？这个性质能被用来优化什么？

## A
被驻留（interned）的字符串在整个解释器里是「概念上的一个全局集合」：集合内不会有两份内容相同的字符串，因此两个驻留字符串可以直接用指针相等（Python 里的 `is`）来判断内容是否相等，而不用逐字符比较。这个性质被用来加速 dict 查找和属性（attribute）查找：字典查 key、对象查属性名时，先比较是不是同一个驻留对象，往往比逐字符比较字符串内容更快。
