---
id: amz-configurable-cache-failed-write-policy-store-disagree
node: amazon.amz-configurable-cache
type: qa
step: 7
tags: [grown]
---
## Q
在可配置缓存里，文件后端写入失败（例如值是 `{1, 2}`，不能转成 JSON）时，策略和后端会怎样不一致？怎样的操作顺序能避免？

## A
反例顺序：先让策略淘汰旧 key、登记新 key，再写后端。容量 2 的文件缓存存着 a、b，`put("c", {1, 2})` 时策略已经淘汰了 b、登记了 c，后端写入才抛 `StoreError`：b 白白丢了，c 在策略里却没有数据。正确顺序：先写后端，成功后才动策略；失败时两边都停在操作之前（a、b 仍在）。淘汰时后端删旧值失败，则要把刚写入的新值撤回再抛错。
