---
id: li-compiler-runtime-device-memory-allocator
node: compiler.runtime
type: qa
step: 2
---
## Q
设备内存是怎样分配和管理的？PyTorch 的缓存分配器（caching allocator）做了什么？"明明还有空闲显存却报内存不足"是怎么回事？

## A
**为什么需要缓存分配器：** 直接向驱动申请和释放设备内存（`cudaMalloc` / `cudaFree`）很慢，而且会让 GPU 同步。推理时每一步都有大量临时张量产生和释放，不能每次都向驱动要。

**PyTorch 的 CUDA 缓存分配器：**
- 第一次需要内存时向驱动申请一大块（段，segment），之后从段里切出小块给张量用。
- 张量释放后，小块回到分配器的缓存里，不还给驱动，下次直接复用。
- 所以 `nvidia-smi` 看到的显存占用是"分配器向驱动要的总量"，通常大于实际正在使用的量。

**两个常用的观察接口：**
- `torch.cuda.memory_allocated()`：张量实际占用的字节数。
- `torch.cuda.memory_reserved()`：分配器持有的总字节数。
- `torch.cuda.memory_summary()`：详细报表，包括碎片情况。

**"有空闲却内存不足"——碎片：**
- 缓存里有很多零散的空闲小块，加起来有 10 GB，但没有一块连续的空间能放下这次需要的 2 GB 张量。
- 推理中输入长度变化频繁，各种大小的张量反复分配释放，容易产生碎片。
- 缓解：`PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True` 让段可以扩展，减少碎片；推理引擎通常在启动时一次性预分配 KV 缓存的大块内存，自己按固定大小的块管理，避免与临时张量混在一起。

**推理引擎的内存策略（以 vLLM 为例）：**
- 启动时用最大规模的假输入跑一遍，测出权重和中间结果的峰值。
- 按设定比例（`--gpu-memory-utilization`）把剩余显存一次性分配给 KV 缓存。
- 运行期间 KV 缓存的分配和释放都在这块预分配的内存里，以固定大小的块为单位，不再向驱动申请。

**测试检查：**
- **泄漏：** 长时间运行，`memory_allocated` 应在稳定范围内波动，不能单调上升。
- **峰值：** 用极端输入（最长上下文、最大批）测峰值内存，确认在启动时的估计之内。
- **快照：** `torch.cuda.memory._record_memory_history()` 加 `torch.cuda.memory._dump_snapshot("snap.pickle")` 可以记录每次分配的调用栈，用于定位泄漏来源。
