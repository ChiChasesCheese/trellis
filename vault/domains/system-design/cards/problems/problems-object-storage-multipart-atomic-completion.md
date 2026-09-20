---
id: problems-object-storage-multipart-atomic-completion
node: problems.foundations.object-storage
type: qa
step: 5
tags: [grown]
---
## Q
In multipart object upload, a client uploads 5,120 parts of a 500GB object in parallel over several minutes, and part 3,000 fails and is retried twice before succeeding. Why does none of this partial progress ever become visible to a concurrent GET on that key, even though most parts have already landed on the server?

## A
Uploaded parts are staged but not registered as the object - the object identified by that key does not exist (or, if overwriting, the old version is still what GET returns) until the client makes a single CompleteMultipartUpload call listing all part numbers and their checksums, which the server processes as one atomic operation that assembles the parts and flips the key to point at the new, complete object. Individual part failures and retries only affect that one part's staging area and are invisible outside the upload session; there is no intermediate state where a reader could see an object that is half-old, half-new bytes.

## Q zh
在 multipart 对象上传中，客户端在几分钟内并行上传一个 500GB 对象的 5,120 个分片，第 3,000 个分片失败并重试了两次才成功。即使大多数分片已经到达服务器，为什么这些部分进度从不会对并发的 GET 请求可见？

## A zh
已上传的分片只是暂存，并未注册为该对象——这个 key 对应的对象不存在（或者如果是覆盖，GET 返回的仍然是旧版本），直到客户端发起一次 CompleteMultipartUpload 调用、列出所有分片号和校验值，服务器将其作为一个原子操作处理：拼装分片并把 key 指向新的、完整的对象。单个分片的失败和重试只影响该分片自己的暂存区，对上传会话以外不可见；不存在一种读者能看到「一半旧字节、一半新字节」的中间状态。
