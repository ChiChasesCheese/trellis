---
id: nr-amz-g3-followups
node: amazon.g3
type: qa
step: 2
---
## Q
【什么时候 GenAI 不必要，或者更慢】面试官会追问什么？每个怎么答？

## A
- **Give me a case where the AI was just wrong for the job.**
    - 计数 / 覆盖率：确定性问题，模型给出「看起来合理的数」；脚本就是 oracle。
- **Did that ever cost you?**
    - 有：手工计数错进了正文两次；读者拿到错的 cut line。
    - 说「手数 / 凭记忆数的计数错过两次」，不要说成「agent 数错了」。
    - 【待补：具体是哪两次？没有记忆就别展开】
- **How do you decide to delegate vs do it?**
    - 答案是确定性的吗？是 → 脚本。
    - 改动多大？一行 → 就地改；实质 → 回到同一个 agent（它还有上下文）。
    - 有可执行的验收吗？没有 → 先写 gate 再委派。
- **What about at work?**
    - 【待补：PayPal 里一个「脚本 / SQL 比 agent 好」的真实例子；没有就说上面这个】
- **Isn't that anti-AI?**
    - 不是：把 AI 放在优势区，开放式、可验证；成本 / 延迟取舍见 [[primer]]。
