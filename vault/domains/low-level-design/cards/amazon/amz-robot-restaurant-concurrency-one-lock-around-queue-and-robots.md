---
id: amz-robot-restaurant-concurrency-one-lock-around-queue-and-robots
node: amazon.amz-robot-restaurant
type: qa
step: 8
tags: [grown]
---
## Q
在 Amazon 机器人餐厅设计里，多个线程同时下单、另一个线程推进时间，什么会出错？怎么防？

## A
「看队首订单 → 选机器人 → 改机器人状态与队列」是多步操作，CPython 的 GIL 只保证单条字节码原子，不保证这一整体：两个线程可能把同一张单派给两台机器人。用一把 `threading.Lock` 罩住全部可变状态（队列、机器人、事件日志、订单号计数），对外只给快照（`RobotView` 元组、事件元组）。测试用 `Barrier` 让线程同时下单，断言每张单恰好送达一次。
