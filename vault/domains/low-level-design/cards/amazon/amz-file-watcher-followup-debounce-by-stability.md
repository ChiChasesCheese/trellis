---
id: amz-file-watcher-followup-debounce-by-stability
node: amazon.amz-file-watcher
type: qa
step: 6
tags: [grown]
---
## Q
在 Amazon 文件监听器设计里，编辑器保存大文件会连续写多次，怎样不用时钟去抖（debounce）？

## A
一个路径的新状态必须在连续两次轮询里相同才被采纳，否则沿用订阅者已知的旧状态，再正常比对。时间线：文件出现（大小 10）无事件；变成 500 无事件；仍是 500，发出一个 CREATED。连写 6 次只得到最后一个 MODIFIED；出现又消失的文件没有事件。轮询间隔本身就是安静窗口，不需要时钟。代价：事件晚一个间隔，持续被写的日志永远没有事件。
