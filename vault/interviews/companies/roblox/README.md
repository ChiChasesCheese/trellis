# Roblox

Roblox 的在线测评是游戏化的：给你一张地图或一条产线，限时在游戏里摆出得分最高的方案。`games/` 里是两个游戏各自的练习工具：
先把游戏规则写成模拟器，再用模拟器搜出方案，最后回游戏里核对分数。

| 目录 | 内容 | 先读 |
|---|---|---|
| `games/kaiju_cats/` | Kaiju Cats（官方练习游戏）：15 回合、三只猫、$200 经费，在楼层上挂指令来得分。地图转录、规则模拟器、搜索脚本、两张地图的最好方案 | `games/kaiju_cats/README.md` |
| `games/factory/` | 工厂游戏：24 小时产线冲分，考试只有 25 分钟。规则模拟器、60 秒内收敛的搜索、教学关对账脚本 | `games/factory/README.md` |

两个目录的做法一样：转录题面，核对模拟分数等于游戏分数，再搜索。每个目录的测试在目录里直接跑：

```bash
cd games/kaiju_cats && python3 -m unittest test_sim -v
cd games/factory && python3 -m unittest test_factory -v
```
