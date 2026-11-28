---
id: hi-sdx-delivery-dispatch-timing
node: qb.sd.nearby-restaurants-app.more
type: qa
step: 3
---
## Q
**何时派骑手：对齐出餐时间**｜补充 · 外卖平台（Uber Eats） · 加分

面试官：「派单除了决定派给谁，还有一个问题：什么时候派。骑手到店太早，在门口干等；太晚，饭菜放凉。你怎么决定派单时机？」

## A
**结论。** 派单时刻 = 预测出餐完成时刻 − 骑手到店所需时间（路程加停车），让骑手刚好在出锅时到。出餐时间按每家店的历史备餐时长预测，到店、停车、店内等待这些真实耗时，用骑手手机传感器识别的行程状态来测量。

**要点。**
- **派单公式：** 出餐预测第 18 分钟，路程 8 分钟加停车 2 分钟，就在第 8 分钟派。
- **按店预测出餐：** 每家店的备餐时长不同，随时段和订单量变化，用历史数据预测。
- **行程状态识别：** 城市里 GPS 噪声大，融合加速度计、陀螺仪和手机的活动识别，用条件随机场（CRF）把轨迹切成「到店、停车、店内等待、走回车上、送餐途中」。
- **只允许合法转移：** 序列模型规定转移顺序，例如「店内等待」只能出现在「停车」之后，抑制噪声造成的乱跳。
- **两种错误不对称：** 早到浪费运力，晚到伤害饭菜品质，提前量要按业务权重调。

**为什么。** 匹配只回答「谁去」，派单时机回答「何时出发」，两者独立。没有状态识别，就量不出「到店到取餐」的真实耗时，出餐预测也没有训练信号。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 266">
<text x="8" y="16" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">出餐预测 = 第 18 分钟；骑手路程加停车 = 10 分钟</text>
<text x="8" y="46" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">太早派：第 0 分钟</text>
<rect x="20" y="54" width="125" height="24" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="82.5" y="70" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">路程 + 停车</text>
<rect x="145" y="54" width="100" height="24" rx="6" stroke-width="1.2" stroke-dasharray="4 3" fill="none" stroke="currentColor"/>
<text x="195" y="70" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">空等 8 分钟</text>
<text x="8" y="104" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">刚好：第 8 分钟</text>
<rect x="120" y="112" width="125" height="24" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="182.5" y="128" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">路程 + 停车</text>
<text x="8" y="162" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">太晚派：第 14 分钟</text>
<rect x="195" y="170" width="125" height="24" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="257.5" y="186" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">路程 + 停车</text>
<rect x="245" y="200" width="75" height="22" rx="6" stroke-width="1.2" stroke-dasharray="4 3" fill="none" stroke="currentColor"/>
<text x="282.5" y="215" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">餐凉 6 分</text>
<line x1="245" y1="30" x2="245" y2="240" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<text x="245" y="258" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">预测出餐</text>
</svg>

**面试里这样说。** 「匹配之外我还要决定什么时候派。我按店预测出餐时间，用骑手手机的 GPS 加运动传感器通过 CRF 识别到店、停车、店内等待，量出真实的取餐耗时，再用出餐时刻减去路程和停车来定派单时刻。」

**易错。**
- **下单就派：** 饭还没做好，骑手到店空等，运力被白白占住。
- **只用 GPS 判断到店：** 商场和密集街区里 GPS 误差大，分不清是在停车还是在店里等。
