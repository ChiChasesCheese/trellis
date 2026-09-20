---
id: problems-traffic-signal-property-test-and-assert
node: problems.machines.traffic-signal
type: qa
step: 8
tags: [grown]
---
## Q
怎么给交通信号灯（Traffic Signal）设计拿出最强的「它永远不会饿死」的证据？安全不变式该写成 `assert` 吗？

## A
最强的证据是**性质测试**（property test）：在**多个固定种子**上各跑几百个 tick，每个流向每格以一定概率到达车辆，并有随机的紧急抢占与释放；每一 tick 断言两件事——

1. **安全**：同时放行的流向里没有冲突对。
2. **公平**：每个流向距上一次放行的间隔不超过一个上界，即没有流向被饿死。

**那个上界必须是推导出来的，不是跑出来的。** 写一个自己观察到的数字，换个种子就会翻车，而且它回答不了面试官真正在问的那句话：你凭什么说它永远不会饿死？从控制器参数算：

```python
intergreen   = clearance_ticks + all_red_ticks
normal_slot  = max_green + intergreen
preempt_slot = max_green + max_preempt_ticks + intergreen
bound = (intergreen
         + (len(phases) - 1) * normal_slot
         + preempt_slot + 1)
```

其余每个相位最多各插进来一次（切相位只沿环向前走），再单独留一个相位区间给抢占——它会改写下一个相位的选择，可能跳过几个相位，也可能把当前相位再点一次。前提是一个等待窗口里最多一次抢占，靠请求之间的冷却期保证。

**不要用裸 `assert` 写安全不变式**：`python -O` 会把 `assert` 语句整条删掉，而这是一条会撞死人的不变式，恰恰不能在优化模式下消失。写成显式检查加一个自定义异常。「把不变式写成断言」这句话描述的是精神（每一步都复核），不是那个关键字。
