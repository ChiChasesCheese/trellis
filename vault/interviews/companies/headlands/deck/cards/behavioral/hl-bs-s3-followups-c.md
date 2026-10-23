---
id: hl-bs-s3-followups-c
node: behavioral.stories
type: qa
step: 21
---
## Q
被追问 S3：最通用的测试教训是什么？怎么做到大声失败又不让整批挂掉？
Most general test lesson? How would you fail loudly without killing the batch?

## A
- **Most general test lesson?** **fixture 必须像真实群体**；断言**输出**，不只是路径。
- **How would you fail loudly without killing the batch?** 把被拒的行记到**错误日志**，而不是丢弃——批次继续，坏数据可见。
