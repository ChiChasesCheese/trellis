---
id: problems-traffic-signal-movement-go-clear-stop
node: problems.machines.traffic-signal
type: qa
step: 6
tags: [grown]
---
## Q
交通信号灯（Traffic Signal）要加行人相位（走 / 闪烁禁止通行 / 禁止通行）或保护左转箭头，怎么加才能不动相位引擎？

## A
关键是让引擎只问流向三个问题，而不是直接操作颜色：

```python
@property
def go(self) -> Aspect:
    return Aspect.WALK if self.kind is PEDESTRIAN else Aspect.GREEN

@property
def clear(self) -> Aspect:
    return (Aspect.FLASHING_DONT_WALK
            if self.kind is PEDESTRIAN else Aspect.YELLOW)
```

引擎在「亮绿」「进入清空」「全红」三处分别问 `go` / `clear` / `stop`，从不关心这个流向是车还是人。于是行人的三段显示和机动车的绿黄红走的是同一段代码。

加行人相位 = 造一个 `Movement("ped-ns", PEDESTRIAN)`、在冲突表里写明它横穿哪条车道、把它放进某个相位。加保护左转 = 造一个流向、写明它和对向直行冲突、加一个相位到环里。两者都是**只改数据**，控制器一个字不动——这就是「可扩展」该有的证据形态。
