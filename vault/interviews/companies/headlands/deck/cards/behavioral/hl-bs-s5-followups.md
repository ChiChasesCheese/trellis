---
id: hl-bs-s5-followups
node: behavioral.stories
type: qa
step: 27
---
## Q
被追问 S5：为什么不双写？结算视图也晚了怎么办？还有什么会出问题？
Why not dual-write? Settlement view late too? What can still go wrong?

## A
- **Why not dual-write?** 一个开关把两个任务**往相反方向门控**，这就是互斥；没有它，双写会**重复收费**。
- **Settlement view late too?** 质量状态的 join 返回**空**；手续费**等待**，不会读到半成品。
- **What can still go wrong?** 在**窗口之外**重新处理；单侧当日记录必须稍后到达；开关提供**快速关闭**。
