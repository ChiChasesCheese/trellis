---
id: tc-saying-no
node: t03.saying-no
type: qa
step: 1
tags: [原则]
---
## Q
**Saying no · 说不**｜原则 · 必会

产品经理要求你下周上线一个会改动支付流程的功能，没有回滚方案。你认为这样太危险，但你不想只是说"不行"。怎么说？

## A
**原则：** 说不要**带理由和出路**：先说你理解他要的结果，再用业务能懂的语言说风险，再给一个更窄的"可以"。

**怎么做：**
1. 先确认目标："I want this live next week too."
2. 把风险说成业务后果，而不是技术喜好："Without a rollback, a bad deploy could double-charge customers."
3. 给替代方案：缩小范围、先灰度、只读模式、手动流程，或者先把监控做好。
4. 点出谁来决定：重大风险要由有权限的人知道并拍板。
5. 若有折中，写下**到期条件**，别让临时办法变成永久。
6. 给不出替代方案时，说什么信息会改变你的看法。
7. 保持校准：只在影响面、可逆性或责任归属真的重要时反对。

**常见错法：**
- **只说"不行"：** 对方没有下一步。
- **用个人偏好当理由：** "这样太丑。"
- **什么都反对：** 信用耗光。

**改写示例：**
- Before: "We can't do that. It's too risky."
- After: "I want this live next week too. My concern is the missing rollback: a bad deploy could double-charge customers. Could we ship to 5 percent of traffic first and add the rollback in the next sprint?"

<details class="pt" markdown="1"><summary>出处</summary>

parin.work《Principal Engineer's Guide to Saying No》（parin.work/principal-engineers-guide-to-saying-no.html）

</details>
