---
id: security-abuse-image-bomb
node: security-cost.abuse
type: qa
---
## Q
A compressed image is only 2 MB but expands to tens of gigapixels. Which limits must be enforced before transformation?

## A
Inspect trusted metadata with a hardened decoder and cap decoded pixels, dimensions, frame count, color/profile complexity, memory, CPU time, output bytes, and concurrent transforms. Stream and sandbox where practical, abort on deadline, and never use compressed byte size as the resource estimate. Cache only a fully validated successful output; failures must not poison the derived key.

## Q zh
一个 compressed image 只有 2 MB，但 decode 后达到数十 gigapixel。transformation 前必须强制哪些 limit？

## A zh
用 hardened decoder 检查 trusted metadata，并限制 decoded pixel、dimension、frame count、color/profile complexity、memory、CPU time、output byte 和 concurrent transform。可行时使用 stream 与 sandbox，deadline 到期就 abort，绝不能把 compressed byte size 当作 resource estimate。只缓存完整验证且成功的 output；failure 不能 poison derived key。
