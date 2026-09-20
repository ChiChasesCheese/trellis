---
nodes: [problems.commerce.flash-sale]
url: https://redis.io/docs/latest/develop/programmability/eval-intro/
---
# Scripting with Lua

值得读：官方文档明确写出 Redis 对 Lua 脚本的原子执行保证——"脚本执行期间，服务器所有其
他活动都被阻塞，脚本产生的效果要么全部尚未发生，要么已经全部发生"。本题据此论证"读取剩余
库存、判断、扣减"这三步包进一条 `EVAL` 就足以防止并发超卖，而不是笼统地说"Redis 很快所以
安全"；比大多数题解文章更精确的地方是明确了这个保证的代价——脚本执行期间会阻塞其他所有命
令，长脚本会拖慢整个实例。
