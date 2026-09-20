---
id: oop-composition-vs-aggregation
node: oop.relationships
type: qa
step: 4
---
## Q
`ParkingLot`–`Floor` 与 `Course`–`Student`：哪个是 composition，哪个是 aggregation——靠哪一个问题就能判定？

## A
那个问题是：**部件的生命周期是否随整体结束，并且被独占拥有？**

- `Floor` 只存在于唯一一个停车场里，并随它消亡 → **composition**（实心菱形）。
- `Student` 比课程活得久，而且同时属于多门课 → **aggregation**（空心菱形）。

两者都是 has-a；判别式是所有权 + 生命周期，而 composition 正是你的析构/级联删除逻辑必须尊重的那一种。
