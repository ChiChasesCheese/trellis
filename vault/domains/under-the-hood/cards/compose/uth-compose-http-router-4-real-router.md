---
id: uth-compose-http-router-4-real-router
node: compose.http-router
type: qa
step: 4
---
## Q
**真实路由器多做了什么**｜httprouter v1.3.0 · Gin v1.11.0

比起上面的简化版，httprouter 和 Gin 的路由树还多做了哪些事？各为了什么？

## A
**细节。**

- 压缩：节点存一段字节前缀；注册时发现公共前缀就拆节点，例如 `/search` 与 `/support` 共用 `/s`
- 优先级：节点记着子树里的处理函数个数，孩子按它从大到小排，路由多的分支先试
- 少分配：参数只写进预先开好容量的切片；Gin 用 `sync.Pool` 复用 `Context`
- 尾斜杠：查不到时试试加上（或去掉）末尾 `/`，能命中就重定向（GET 用 301，其他方法 307）
- 并发：`addRoute` 的注释写明 not concurrency-safe，所以先注册完再开始服务

**为什么。** httprouter 规定同一层不能既有静态段又有占位符（`/user/new` 与 `/user/:user` 不论先后，第二条都会 panic），查找因此永远只有一条路。Gin 从 v1.7.0 起允许并存，代价是要记下岔路口、走不通再退回。

**坑。** 冲突在启动时 panic。占位符的名字也算冲突：`/foo/:name` 与 `/foo/:names` 不能并存。

**对应 LeetCode：** 无直接对应的题
