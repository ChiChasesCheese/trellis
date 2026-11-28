---
id: hi-c-lld-delivery-x03-rule-placement
node: lld.in-a-hurry.delivery.exam
type: qa
step: 3
---
## Q
**LLD 答题框架 · 规则放错了类的后果**｜考点 · 必会

井字棋里，把"这个格子是否被占"写在 `Game.makeMove` 里，直接读 `board.cells[r][c]`，会出什么问题？该怎么改？

## A
- **问题一：** `Game` 依赖 `Board` 的内部表示，换成稀疏结构或不同尺寸就要改 `Game`
- **问题二：** 同样的判断会在别处重复，规则散落，出错难定位
- **改法：** `Board` 提供 `can_place(r, c)`，数据规则归持有数据的类
- **`Game` 仍管什么：** 游戏是否已结束、是否轮到这个玩家，这是生命周期规则
