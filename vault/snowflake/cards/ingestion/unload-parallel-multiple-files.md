---
id: unload-parallel-multiple-files
node: ingestion.unload-export
type: qa
tags: [grown]
---
## Q
一次 `COPY INTO @stage/out/` 导出后，目录下出现了很多个 `data_0_0_0.csv.gz` 之类的文件，而不是一个文件。为什么？若下游只能接收单个文件怎么办？

## A
卸载默认由仓库的多个计算资源并行写出，每个线程产生自己的文件，并按 `MAX_FILE_SIZE` 限制切分文件大小，从而提高导出速度。若下游需要单个文件，可以设置 `SINGLE = TRUE`，并视需要调大 `MAX_FILE_SIZE`；代价是失去并行写出，大数据量时导出更慢，单文件大小也有上限。
