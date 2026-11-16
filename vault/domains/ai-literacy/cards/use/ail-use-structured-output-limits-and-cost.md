---
id: ail-use-structured-output-limits-and-cost
node: use.structured-output
type: qa
step: 2
---
## Q
结构化输出有什么限制和代价？哪些 schema 特性不能用，为什么第一次请求更慢？

## A
**约束解码保证"形状"合法，不保证"内容"正确；schema 要先编译成语法，所以首次请求更慢，且只支持 schema 的一个子集。**

| 方面 | 事实 |
|---|---|
| 保证 | 合法 JSON、字段齐全、类型和枚举正确 |
| 不保证 | 内容对不对：年龄填 -5、类别选错，格式仍然合法 |
| 不支持（Claude） | 递归 schema、外部引用、数值范围（minimum、maximum）、字符串长度限制；additionalProperties 只能是 false |
| 首次延迟 | 第一次用某个 schema，要编译语法；编译结果缓存 24 小时，改了结构就要重编 |
| 缓存影响 | 修改输出格式设置，会让该会话的提示缓存失效 |
| 被截断 | max_tokens 太小，JSON 写到一半被切断，就不再合法 |

- **解码代价：** 每生成一个 token 都要算一次"合法 token 集合"；若这一步和模型的 GPU 计算串行，就拖慢每个 token，所以推理引擎会预先编译语法并让两件事并行。
- **字段顺序有讲究：** 模型是顺序生成的，要先写 reasoning 字段，再写答案字段，让答案建立在推理之上；反过来写，推理只是事后辩解。
- **范围校验自己做：** 因为不支持数值范围，"折扣在 0 到 1 之间"要在程序里再检查一遍。

**新进展（2025 年 1 月）。** vLLM 把 XGrammar 集成进来以后，受约束解码在高负载下每输出 token 的时间最多改善 5 倍：XGrammar 的做法是把语法预先编译好，运行时快速查出每步的合法 token，使"保证格式"不再明显拖慢吞吐。

<details class="pt"><summary>想一想：为什么把 reasoning 字段放在 answer 字段后面，答案质量会变差？</summary>模型按顺序逐 token 生成，answer 先写出来时还没有推理草稿可依赖，后面的 reasoning 只是在给已定的答案找理由。</details>
