---
id: hi-pt-image-transform-pipeline-7-idempotent-key
node: qb.lld.image-transform-pipeline.points
type: qa
step: 7
---
## Q
**图像变换流水线 · 幂等的输出位置**｜必会 · 出自：图像变换流水线 › 深入 3

队列至少一次投递，同一个任务可能被执行两次。输出怎么写才安全？

## A
**做法。** 输出位置由 `(图, 变换内容)` 决定：对变换内容做规范化 JSON（键排序）再哈希，作为路径的一部分。重复执行就是覆盖同一个文件。

```python
canonical = json.dumps(spec, sort_keys=True, separators=(",", ":"))
return f"{image_id}/{hashlib.sha256(canonical.encode()).hexdigest()[:16]}.png"
```
**细节。** 键顺序不同的两份相同变换得到同一个路径。某张图总是失败，重试几次后进死信队列，不阻塞整批。
