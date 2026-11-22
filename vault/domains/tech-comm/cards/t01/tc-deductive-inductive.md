---
id: tc-deductive-inductive
node: t01.deductive-vs-inductive-reasoning
type: qa
step: 1
tags: [原则]
---
## Q
**Deductive vs inductive reasoning · 两种推理**｜原则 · 追问

你说"我们应该换数据库，理由有三个：成本、扩展性、人手"。评审人问："这三点放在一起为什么能推出结论？" 怎么检查你的这组理由站不站得住？

## A
**原则：** 一组并列理由只能是两种推理之一，不能混用：

| | Deductive（演绎） | Inductive（归纳） |
|---|---|---|
| 形式 | 三步推理链：一个已知的事实，对它的评论，所以…… | 一组同类的事实，用同一个复数名词概括 |
| 例子 | 现有库不能水平扩展；我们明年流量翻倍；所以它撑不住 | 三个理由：成本更低、更容易扩展、更容易招人 |
| 读者负担 | 每一步都要被接受，一步不通则全链断 | 要点之间相互独立，缺了一点结论更弱但不会垮 |
| 概括写法 | 强调"所以"那一步 | 找出它们的共同点 |

**怎么做：**
1. 看每一条是不是同类（能不能用一个复数名词指代：reasons、risks、steps）。
2. 同类 → 归纳；要概括出它们**共同的特点**。
3. 不是同类，而是前后推理 → 演绎；三步要接得上。
4. Minto 提醒：演绎适合想问题，但写起来冗长；顶层陈述更适合归纳。

**常见错法：**
- **一组里一半是理由，一半是推论。**
- **用"三点"伪装推理链：** 三点之间其实有先后依赖。

<details class="pt" markdown="1"><summary>出处</summary>

Minto p. 81–96（Ch.5 Deduction and Induction: The Difference）；p. 33–40（Ch.2 The Horizontal Relationship）

</details>
