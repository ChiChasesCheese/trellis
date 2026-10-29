---
id: uth-compose-interceptor-chain-5-same-skeleton
node: compose.interceptor-chain
type: qa
step: 5
---
## Q
**同一个骨架：Tomcat、Koa、Spring MVC**｜Tomcat · 11.0 / koa-compose · 4.0 / Spring MVC · 7.0

Servlet 的 FilterChain、Koa 的中间件、Spring MVC 的拦截器，也是“列表加游标”吗？各自的细节差在哪？

## A
**结构。**

| 框架 | 列表 | 游标 | 收尾怎么倒序 |
|---|---|---|---|
| Tomcat `ApplicationFilterChain` | `filters` 数组 | `pos`，取 `filters[pos++]` | 递归，调用栈展开 |
| Koa `compose` | `middleware` 数组 | `dispatch(i)` 的参数 `i` | 递归加 Promise |
| Spring MVC `HandlerExecutionChain` | `interceptorList` | `interceptorIndex` | 循环：`postHandle` 倒着走 |

**细节。**

- Tomcat：每个请求按 URL 和 Servlet 名匹配出一份过滤器列表，处理完 `release()`；过滤器不往下调 `doFilter`，Servlet 就不会执行
- Koa：闭包里的 `index` 记最大已调用的下标，`i <= index` 说明同一个 `next()` 被调了两次，直接报 `next() called multiple times`
- Spring MVC：不用递归；`preHandle` 正序，每通过一个就记下 `interceptorIndex`，`afterCompletion` 从它倒着走，只给真正进入过的拦截器收尾

**为什么。** 游标要么藏在递归的调用栈里，要么存成一个整数；存成整数，拦下之后就能按“已进入的个数”精确回退。

**坑。** 忘了调 `next`、`doFilter` 或 `proceed`，请求会悄悄停住，没有任何报错。

**对应 LeetCode：** 无直接对应的题
