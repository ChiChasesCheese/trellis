---
id: li-serving-batching-static-dynamic-continuous
node: serving.batching
type: qa
step: 1
---
## Q
静态批处理（static batching）、动态批处理（dynamic batching）和连续批处理（continuous batching）有什么区别？用一个时间线例子说明连续批处理为什么能大幅提高吞吐。

## A
**批处理：** 把多个请求叠在一起做一次计算。生成文字时每一步都要把模型全部参数从显存读一遍，批里的请求共享这次读取，所以批越满越划算。

- **静态批处理：** 凑满固定数量（比如 4 个）请求才开始，整批一起生成，直到**最长的那个**结束才放下一批进来。
- **动态批处理：** 不必凑满，等到"凑够数量"或"等待超过时限"任一条件满足就发车。NVIDIA Triton 推理服务器的 `dynamic_batching { max_queue_delay_microseconds: 100 }` 就是这种。适合一次前向就出结果的模型（如分类、嵌入）；对逐个生成的大模型，仍有"等最长者"的问题。
- **连续批处理（也叫迭代级调度、in-flight batching）：** 以"生成一个 token 的一步"为调度单位。每一步结束后，已完成的请求立即离开，排队的新请求立即加入。vLLM、TensorRT-LLM、SGLang 都用这种方式。

**时间线例子：** 批大小上限 4，四个请求分别要生成 10、20、50、100 个 token，队列里还有很多请求在等。
- **静态：** 这批要跑 100 步。第 10 步后请求 A 已完成，但它的位置空着，一直到第 100 步。100 步里实际产出 10 + 20 + 50 + 100 = 180 个 token，而 4 个位置 × 100 步 = 400 个位置，利用率 **45%**。新请求要等 100 步才能开始，首 token 延迟很高。
- **连续：** 第 10 步 A 离开，下一步就有新请求补进来；第 20 步 B 离开，又补一个。只要队列不空，4 个位置几乎一直满着，利用率接近 **100%**。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 182" font-family="sans-serif" font-size="11">
<text x="30" y="13" fill="currentColor">静态：等最长的跑完 100 步，利用率 45%</text>
<text x="22" y="28" text-anchor="end" fill="currentColor">A</text>
<rect x="30" y="20" width="30" height="10" stroke="currentColor" fill="currentColor" fill-opacity="0.45"/>
<rect x="60" y="20" width="270" height="10" fill="none" stroke="currentColor" stroke-dasharray="3 2"/>
<text x="22" y="42" text-anchor="end" fill="currentColor">B</text>
<rect x="30" y="34" width="60" height="10" stroke="currentColor" fill="currentColor" fill-opacity="0.45"/>
<rect x="90" y="34" width="240" height="10" fill="none" stroke="currentColor" stroke-dasharray="3 2"/>
<text x="22" y="56" text-anchor="end" fill="currentColor">C</text>
<rect x="30" y="48" width="150" height="10" stroke="currentColor" fill="currentColor" fill-opacity="0.45"/>
<rect x="180" y="48" width="150" height="10" fill="none" stroke="currentColor" stroke-dasharray="3 2"/>
<text x="22" y="70" text-anchor="end" fill="currentColor">D</text>
<rect x="30" y="62" width="300" height="10" stroke="currentColor" fill="currentColor" fill-opacity="0.45"/>
<text x="30" y="95" fill="currentColor">连续：完成就离开，新请求下一步补进来，接近 100%</text>
<text x="22" y="110" text-anchor="end" fill="currentColor">A</text>
<rect x="30" y="102" width="30" height="10" stroke="currentColor" fill="currentColor" fill-opacity="0.45"/>
<rect x="60" y="102" width="270" height="10" stroke="currentColor" fill="currentColor" fill-opacity="0.15"/>
<text x="22" y="124" text-anchor="end" fill="currentColor">B</text>
<rect x="30" y="116" width="60" height="10" stroke="currentColor" fill="currentColor" fill-opacity="0.45"/>
<rect x="90" y="116" width="240" height="10" stroke="currentColor" fill="currentColor" fill-opacity="0.15"/>
<text x="22" y="138" text-anchor="end" fill="currentColor">C</text>
<rect x="30" y="130" width="150" height="10" stroke="currentColor" fill="currentColor" fill-opacity="0.45"/>
<rect x="180" y="130" width="150" height="10" stroke="currentColor" fill="currentColor" fill-opacity="0.15"/>
<text x="22" y="152" text-anchor="end" fill="currentColor">D</text>
<rect x="30" y="144" width="300" height="10" stroke="currentColor" fill="currentColor" fill-opacity="0.45"/>
<text x="30" y="176" fill="currentColor">深色 = A–D 生成中；浅色 = 新请求；虚线框 = 空着</text>
</svg>

**连续批处理的前提：** 每个请求的 KV 缓存（保存历史 token 每层的键、值向量）必须能随时独立分配和释放，所以它和分页式缓存管理（PagedAttention，把缓存切成固定小块按需分配）是一起出现的。已发表的 vLLM 论文报告，在相同延迟下吞吐比当时的系统高 2–4 倍。
