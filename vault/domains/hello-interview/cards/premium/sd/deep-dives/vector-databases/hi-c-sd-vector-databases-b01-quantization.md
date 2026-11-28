---
id: hi-c-sd-vector-databases-b01-quantization
node: sd.deep-dives.vector-databases.beyond
type: qa
step: 1
---
## Q
**向量数据库 · 量化：用精度换内存**｜拓展 · 加分

向量太多放不进内存时，除了加机器还有什么办法？

## A
- **标量量化**（scalar quantization）：把每个维度从 4 字节的 float32 压成 1 字节的 int8，内存降为 1/4，召回略降。
- **乘积量化**（product quantization，PQ）：把向量切成若干段，每段用一个小码本里的编号代替，几百字节的向量可压成几十字节，与 IVF 结合（IVF-PQ）是处理超大数据集的经典组合。压缩后的距离是近似的。
- **二值量化：** 每维只保留 1 比特，内存降到 1/32，可用汉明距离快速粗筛。
- **重排（rescoring）：** 常见搭配是先用压缩向量做粗筛得到更多候选，再用原始精确向量对候选重新算距离排序，找回大部分损失的精度。原始向量可放磁盘，只有候选才读取。
- **2026 亮点：** 在 Postgres 里这套已是现成能力：pgvector 的 halfvec 折半内存，binary_quantize 加汉明距离粗筛，再用原始向量重排；嵌入模型支持降维（Matryoshka 式截断）时，先降维再量化，截断后要重新归一化，并用自己的数据测 recall@k。
- **磁盘索引：** 一些方案把图索引放在 SSD 上，内存里只放压缩向量，换取更低成本和稍高延迟（如 DiskANN）。
- **取舍：** 内存、召回、延迟三者之间的又一组旋钮。
