---
id: tc-words-acronyms-pronouns
node: t04.words-acronyms-pronoun-ambiguity
type: qa
step: 1
tags: [原则]
---
## Q
**Words, acronyms & pronoun ambiguity · 缩写与指代**｜原则 · 追问

你写："Python is interpreted, while C++ is compiled. It has a cult-like following." 读者问：It 指谁？同一份文档里你还用了 TTN，没有解释。怎么处理这类问题？

## A
**原则：** 每个代词要能**一眼找到指代的名词**；每个缩写**第一次出现就展开**；每个术语**一个名字用到底**。

**怎么做：**
1. **代词：** 先出现名词，代词紧跟其后（约五个词内）；两个名词之间夹了别的名词，就重复名词。
2. 最容易出问题的是 it、they、this、that：**this 后面加名词**，"This user ID lets users authenticate."
3. **缩写：** 第一次写全称，括号里放缩写，如 **Telekinetic Tactile Network** (**TTN**)；之后只用缩写，不要混用。
4. **只在缩写明显更短且出现很多次时才定义**；只出现两三次，每次写全称。
5. **术语：** 新术语第一次定义或给链接；一个概念全文一个名字。

**常见错法：**
- **"This" 单独做主语：** 读者不知道指前面哪一件事。
- **一会儿写全称，一会儿写缩写。**
- **缩写不展开，默认大家都懂。**

**改写示例：**
- Before: "Python is interpreted, while C++ is compiled. It has a cult-like following."
- After: "Python is interpreted, while C++ is compiled. Python has a cult-like following."
- Before: "Running the process configures permissions and generates a user ID. This lets users authenticate."
- After: "Running the process configures permissions and generates a user ID. This user ID lets users authenticate."

**出处：** Google Technical Writing One《Words》（developers.google.com/tech-writing/one/words）
