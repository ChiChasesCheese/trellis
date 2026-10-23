---
id: hl-bq-q16-ship-fast
node: behavioral.question-bank
type: qa
step: 33
---
## Q
你怎么既发布得快、又知道它是安全的？（45 秒）
How do you ship fast and still know it's safe?

## A
故事：S5。

- **Deploy ≠ release**：合并时开关（toggle）**关着**，先在 **pre-prod** 打开，再上生产。
- **Reversible**：开关是**快速关闭**的手段；两条路径靠**按来源过滤**互斥，所以不会重复计算。
- **Compare first**：先影子对比，在完整一天上跑 **count**，再切换。
