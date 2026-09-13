---
id: dist-object-storage-transfer-cost
node: distributed.object-storage
type: qa
---
## Q
For a 40 GB object, when should a service use multipart upload and parallel range GETs, and what new failure work appears?

## A
Use multipart upload to retry independent parts and avoid restarting a huge transfer; parallel ranges can fill available bandwidth when one connection is insufficient. But concurrency raises memory, request cost, and downstream pressure. Persist upload IDs/part checksums, abort abandoned uploads, verify the final object checksum, bound parallelism, and make resume idempotent. More parts improve recovery granularity but increase coordination overhead.

## Q zh
对 40 GB object，什么时候应使用 multipart upload 和 parallel range GET？会新增哪些 failure work？

## A zh
multipart upload 可独立 retry part，避免重启整个巨大传输；当单连接无法吃满带宽时，parallel range 可提高吞吐。但 concurrency 会增加 memory、request cost 和 downstream pressure。应持久化 upload ID/part checksum、abort abandoned upload、验证最终 object checksum、限制 parallelism，并让 resume idempotent。更多 part 提高 recovery granularity，也增加 coordination overhead。
