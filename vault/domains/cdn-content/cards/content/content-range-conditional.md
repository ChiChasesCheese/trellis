---
id: content-range-conditional
node: content.range-compression
type: qa
---
## Q
A client resumes a download with `Range`, but the object changed since its first attempt. How does `If-Range` prevent a corrupt concatenation?

## A
The client sends `If-Range` with a strong validator. If it still matches, the server returns `206` with the requested range; if not, it ignores the range and returns the full current `200` representation. Without this check, the client could append bytes from two versions. `Content-Range` must describe the selected representation, and unsatisfiable ranges return `416`.

## Q zh
client 用 `Range` 恢复下载，但对象在首次请求后发生变化。`If-Range` 如何防止 corrupt concatenation？

## A zh
client 用 strong validator 发送 `If-Range`。若仍匹配，server 返回请求范围的 `206`；若不匹配，则忽略 range，返回完整当前 `200` representation。没有该检查，client 可能拼接两个版本的 bytes。`Content-Range` 必须描述 selected representation，不可满足的 range 返回 `416`。
