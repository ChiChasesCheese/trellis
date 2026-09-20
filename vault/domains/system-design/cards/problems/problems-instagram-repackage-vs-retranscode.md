---
id: problems-instagram-repackage-vs-retranscode
node: problems.social.instagram
type: qa
step: 3
tags: [grown]
---
## Q
In a video processing pipeline that must generate multiple adaptive-bitrate (ABR) renditions of an uploaded clip, why is re-transcoding each rendition from scratch far more expensive than repackaging already-encoded frame data into an ABR container, and roughly how much of a difference does this make?

## A
Independently transcoding each ABR rendition re-runs the full video encoding process (motion estimation, quantization, entropy coding) once per rendition, which is CPU-intensive work repeated redundantly. Repackaging reuses frame data that has already been encoded once (e.g. as a progressive file) and just restructures it into an ABR-compatible container without re-encoding. Meta's engineering team reported that transcoding a 23-second video to a 720p ABR rendition from scratch took about 86.17 seconds of CPU time, while repackaging the same content into ABR format took about 0.36 seconds — roughly a 239x difference.

## Q zh
在一个需要为上传视频生成多档自适应码率（ABR）版本的视频处理管道中，为什么从头独立转码每一档码率，比复用已经编码好的帧数据、重新打包成 ABR 容器格式要昂贵得多？大致差多少？

## A zh
独立转码每一档 ABR 版本要为每一档都重新跑一遍完整的视频编码过程（运动估计、量化、熵编码），是重复消耗的 CPU 密集型工作。重新打包则复用已经编码过一次的帧数据（例如渐进式编码文件），只是把它重新组织成 ABR 兼容的容器格式，不需要重新编码。Meta 工程团队披露的真实数字：把一段 23 秒的视频从头转码到 720p ABR 版本约需 86.17 秒 CPU 时间，而把同样内容重新打包成 ABR 格式只需约 0.36 秒——约 239 倍的差距。
