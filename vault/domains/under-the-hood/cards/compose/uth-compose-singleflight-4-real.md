---
id: uth-compose-singleflight-4-real
node: compose.singleflight
type: qa
step: 4
---
## Q
**真实实现多做了什么**｜Go · golang.org/x/sync v0.24

真实的 `singleflight` 还处理了哪些情况？用它有哪些坑？

## A
**细节。**

- `fn` 出现 panic 或调用 `runtime.Goexit` 时也要善后：recover 后把 panic 记在 `call` 里，所有等待者醒来后同样 panic 或 Goexit，不会永远睡眠
- `DoChan`：返回 channel，调用方可以 `select` 加超时或取消；`Do` 一旦开始等就退不出来
- `Forget(k)`：让之后的调用不再等一个卡住的旧调用
- Go 标准库 `net` 解析域名时，同一个 `network + host` 的并发解析合并成一次（`DoChan`）。`fn` 用的是脱离取消的 ctx，免得第一个调用方取消连累别人；最后一个等待者放弃（`ForgetUnshared`）时才取消查询

**为什么。** 它只合并"同时在飞"的调用，不保存结果，所以和缓存分工：先查缓存，未命中再 `Do`。

**坑。**

- 结果是共享的：所有调用方拿到同一个对象，谁改谁影响别人。`net` 在 `shared` 为真时先复制切片再返回
- 错误也共享：先到者失败，所有等待者一起失败
- 只在单个进程里有效，多个实例各自会查一次数据库

**对应 LeetCode：** 无直接对应的题
