---
id: amz-emergency-pubsub-priority-heap-order
node: amazon.amz-emergency-pubsub
type: qa
step: 4
tags: [grown]
---
## Q
在应急发布订阅里，异步信箱用什么数据结构按严重度出队？队列里依次排着 INFO、CRITICAL、WARNING、CRITICAL、INFO 五条事件时，出队顺序是什么？

## A
用小根堆（heap），元素是 `(-severity, seq, event)`：严重度取负号，于是 CRITICAL 先出；严重度相同时比编号 `seq`，先发布的先出，保证同级 FIFO。设五条依次是 i1、c1、w1、c2、i2，出队顺序是 c1、c2、w1、i1、i2。入队出队都是 O(log n)；信箱有界，满了才对整个堆扫一遍找最该挤掉的那条。
