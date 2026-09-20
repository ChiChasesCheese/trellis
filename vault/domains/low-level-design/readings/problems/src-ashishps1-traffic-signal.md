---
nodes: [problems.machines.traffic-signal]
url: https://github.com/ashishps1/awesome-low-level-design/blob/main/problems/traffic-signal.md
---
# awesome-low-level-design — Designing a Traffic Signal Control System

值得读：开源题库（GPL-3.0），六种语言各一份实现，需求清单写得全——可配置时长、平滑过渡、
紧急情况处理，适合拿来核对自己有没有漏掉面试官会追的点。它的对象是 `Signal` 枚举、`Road`、
`TrafficLight`、单例的 `TrafficController`，用观察者把灯的变化推给路。

三处值得当反面教材。第一，Python 版把 `time.sleep(green_duration / 1000)` 直接写在状态处理
函数里，再用后台线程 `while self._running` 驱动——整份设计因此无法断言任何时序，要验证
"抢占之后确实走了全红"只能靠肉眼看。第二，它的相位切换是 绿 → 黄 → 红，紧接着另一方向绿，
**没有全红清空间隔**；而那一段正是安全不变式在切换瞬间仍然成立的原因。第三，安全没有显式
判据，靠每个状态处理函数里"我记得把另一方向设成红"的人工纪律，加一个左转箭头就会漏。
本题解相应地改成：`step()` 推 tick、冲突写成图、每一 tick 末尾显式复核。
