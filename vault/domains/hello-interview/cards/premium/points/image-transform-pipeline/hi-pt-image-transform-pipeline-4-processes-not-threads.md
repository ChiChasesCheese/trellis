---
id: hi-pt-image-transform-pipeline-4-processes-not-threads
node: qb.lld.image-transform-pipeline.points
type: qa
step: 4
---
## Q
**图像变换流水线 · 并发为什么是进程**｜必会 · 出自：图像变换流水线 › 深入 2

对上万张图并行应用变换，纯 Python 实现该用线程池还是进程池？有什么数据支持？什么情况下线程也行？

## A
**进程池。** 像素循环是 CPU 密集的纯计算，线程要抢 GIL。一次本机实测（带 GIL 的标准 CPython，秒数随机器而变，看比例），48 张 400 x 400 的图：串行 3.33 秒，8 个线程 3.36 秒（没提速），8 个进程 0.93 秒。

**线程也行。** 像素运算在 C 里完成并释放 GIL（Pillow、numpy 大多如此）时，或用 Python 3.13 起的自由线程（free-threaded，无 GIL）构建时；读文件是 I/O 等待，线程适合做预取。

**条件。** 数据要能 pickle：冻结的数据类可以，错误转成字符串再传回。
