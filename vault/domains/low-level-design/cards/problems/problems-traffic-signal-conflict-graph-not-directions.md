---
id: problems-traffic-signal-conflict-graph-not-directions
node: problems.machines.traffic-signal
type: qa
step: 1
tags: [grown]
---
## Q
在交通信号灯（Traffic Signal）设计里，「安全」该怎么定义才不会在加新相位时失效？

## A
不要定义成「南北绿的时候东西必须红」——那是**结论**，不是定义，而且它把判据散在每个状态处理函数里（「我记得把另一方向设成红」），加一个左转箭头就会漏掉一处。

定义成：**任意两个互相冲突的流向（movement），不能同时放行**。冲突是路口几何决定的一张图，写成数据：

```python
conflicts = [(ns, ew) for ns in (NORTH, SOUTH)
                      for ew in (EAST, WEST)]
intersection = Intersection("x", movements, conflicts)
```

这张图买到三样东西：判据只有一处，加流向不会漏；可以在**启动时**校验每个相位内部无冲突，把配置错误变成启动失败；让随机演练的性质测试成为可能——每个 tick 问一次「同时放行的流向里有没有冲突对」。
