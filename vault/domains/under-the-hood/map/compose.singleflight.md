%% trellis:begin %%
# singleflight：合并同时到来的重复请求
*数据结构组合：开源框架里的类设计*

缓存失效的一瞬间成百上千个请求同时去查数据库：用一张“正在进行的调用”表，同一个 key 只真正执行一次，其他请求等这次的结果；缓存击穿的标准解法。

**Core** — part of the first pass through this subject.

## Cards (5)
1. [[uth-compose-singleflight-1-need]]
2. [[uth-compose-singleflight-2-parts]]
3. [[uth-compose-singleflight-3-code]]
4. [[uth-compose-singleflight-4-real]]
5. [[uth-compose-singleflight-5-interview]]
%% trellis:end %%

## Notes
