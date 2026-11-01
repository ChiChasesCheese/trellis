---
id: hi-pt-figma-draw-api-2-frame-coalesce
node: qb.lld.figma-draw-api.points
type: qa
step: 2
---
## Q
**矢量图形编辑器绘图 API · 按帧合并事件**｜出自：矢量图形编辑器绘图 API › 深入 1

矢量编辑器的指针事件可达每秒 120 到 240 次，而渲染预算是 60 帧每秒、单帧约 16 毫秒。拖动时事件怎么处理？

## A
**要点。** 工具的 on_pointer_move 只记录最新位置，浏览器每帧回调（requestAnimationFrame）调用一次 on_frame，把一帧内的多个事件合并成一次预览更新。
**为什么正确。** 位移按相对起点的绝对值计算（起点位置 + 当前指针 − 按下指针），卡顿时丢掉中间事件也不会漂移。
**反面。** 逐事件改模型、重绘、发网络，CPU 和带宽都爆。
