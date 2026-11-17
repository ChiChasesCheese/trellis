"""图片变换流水线（PixelFlow）的参考解。

设计五句话：
1. 单图路径 `_run_one` 是纯函数：按顺序套用变换，`Exception` 变成带类型名的错误文本，`BaseException` 一律不碰。
2. 准入判断放进一个不带线程的类 `AdmissionWindow`：同时在途的任务数不超过 `max_workers`，在途原图字节不超过预算，
   但在途为空时队头一张超大的图仍然可以进（只有它自己在途）。
3. 协调线程（调用 `run` 的线程）独占全部状态：从迭代器一次拉一个队头，窗口放行就提交，不放行就等一个任务完成，
   队头不放行时后面的任务不会被拉取，所以准入严格先进先出。
4. 线程池只用来执行 `_run_one`；任务数从不超过 `max_workers`，所以池自己的队列永远是空的，内存也不会多出一份。
5. 结果按输入下标放进字典，最后按下标取出，输出顺序与完成顺序无关；任何路径退出都等运行中的任务结束。
"""

from __future__ import annotations

from concurrent.futures import FIRST_COMPLETED, Future, ThreadPoolExecutor, wait
from dataclasses import dataclass
from typing import Callable, Iterable, Sequence

Transform = Callable[[bytes], bytes]


@dataclass(frozen=True)
class ImageJob:
    image_id: str
    data: bytes


@dataclass(frozen=True)
class TransformResult:
    index: int
    image_id: str
    data: bytes | None
    error: str | None


def describe(exc: Exception) -> str:
    """错误文本固定为 `类型名: 消息`；空消息和多行消息原样保留。"""
    return f"{type(exc).__name__}: {exc}"


class AdmissionWindow:
    """准入窗口：回答"这张图现在能不能提交"，自己不碰线程，所以可以直接单元测试。

    不变量：在途任务数不超过 `max_jobs`；在途字节不超过 `byte_limit`，唯一的例外是窗口里只有这一张
    超大的图（它独自在途，才有进展）。所有方法只由协调线程调用，因此没有锁。
    """

    def __init__(self, max_jobs: int, byte_limit: int) -> None:
        if max_jobs < 1 or byte_limit < 1:
            raise ValueError("max_jobs and byte_limit must be positive")
        self._max_jobs = max_jobs
        self._byte_limit = byte_limit
        self._jobs = 0
        self._bytes = 0

    @property
    def jobs_in_flight(self) -> int:
        return self._jobs

    @property
    def bytes_in_flight(self) -> int:
        return self._bytes

    @property
    def has_slot(self) -> bool:
        return self._jobs < self._max_jobs

    def __repr__(self) -> str:
        return f"AdmissionWindow(jobs={self._jobs}/{self._max_jobs}, bytes={self._bytes}/{self._byte_limit})"

    def can_admit(self, size: int) -> bool:
        """只判断，不记账：名额满了不行；窗口非空且加上这张会超预算不行；窗口为空时一律可以。"""
        if size < 0:
            raise ValueError("size must not be negative")
        if not self.has_slot:
            return False
        if self._jobs and self._bytes + size > self._byte_limit:
            return False
        return True

    def try_admit(self, size: int) -> bool:
        """放行就记账并返回 True；不放行什么都不改。"""
        if not self.can_admit(size):
            return False
        self._jobs += 1
        self._bytes += size
        return True

    def release(self, size: int) -> None:
        """一张图的整条链结束（成功或失败）后归还它的名额和字节。"""
        if self._jobs == 0 or size > self._bytes:
            raise RuntimeError("released more than was admitted")
        self._jobs -= 1
        self._bytes -= size


class ImagePipeline:
    def __init__(self, max_workers: int = 4, memory_limit_bytes: int = 16_000_000):
        """两个上限都必须是正数，否则 ValueError。"""
        for name, value in (("max_workers", max_workers), ("memory_limit_bytes", memory_limit_bytes)):
            if value < 1:
                raise ValueError(f"{name} 必须大于 0，收到 {value}")
        self.max_workers = max_workers  # 同时在跑的图片链上限
        self.memory_limit_bytes = memory_limit_bytes  # 同时在途的原图字节预算

    @staticmethod
    def _run_one(
        index: int,
        job: ImageJob,
        transforms: Sequence[Transform],
    ) -> TransformResult:
        """对一张图按顺序套用全部变换，返回它的结果；Exception 变成错误文本，别的异常不碰。"""
        data = job.data
        try:
            for transform in transforms:
                data = transform(data)
        except Exception as exc:  # 只吞 Exception：KeyboardInterrupt 之类要原样冒出去
            return TransformResult(index, job.image_id, None, describe(exc))
        return TransformResult(index, job.image_id, data, None)

    def run(
        self,
        jobs: Iterable[ImageJob],
        transforms: Sequence[Transform],
    ) -> list[TransformResult]:
        """按顺序、并发和内存合同处理全部任务；结果按输入顺序排列。"""
        chain = tuple(transforms)  # 只读一次，之后所有任务共用同一份
        source = enumerate(jobs)  # 惰性：每次 next 才从调用方的迭代器取一个
        window = AdmissionWindow(self.max_workers, self.memory_limit_bytes)
        in_flight: dict[Future[TransformResult], int] = {}  # 任务 -> 它占用的原图字节
        results: dict[int, TransformResult] = {}
        head: tuple[int, ImageJob] | None = None  # 已取出、还没放行的队头
        exhausted = False
        pool = ThreadPoolExecutor(max_workers=self.max_workers)
        try:
            while True:
                while not exhausted and window.has_slot:
                    if head is None:
                        head = next(source, None)
                        if head is None:
                            exhausted = True
                            break
                    index, job = head
                    size = len(job.data)
                    if not window.try_admit(size):
                        break  # 队头放不进去：后面的一律不取，先进先出
                    in_flight[pool.submit(self._run_one, index, job, chain)] = size
                    head = None
                if not in_flight:
                    break
                done, _ = wait(in_flight, return_when=FIRST_COMPLETED)
                for future in done:
                    window.release(in_flight.pop(future))
                    result = future.result()  # 只有 BaseException 会从这里原样抛出
                    results[result.index] = result
        finally:
            pool.shutdown(wait=True, cancel_futures=True)
        return [results[i] for i in range(len(results))]


if __name__ == "__main__":
    demo_jobs = [ImageJob("a", b"x"), ImageJob("b", b"y"), ImageJob("a", b"z")]

    def upper_unless_y(data: bytes) -> bytes:
        if data == b"y!":
            raise ValueError("invalid image")
        return data.upper()

    for item in ImagePipeline(2, 100).run(demo_jobs, [lambda d: d + b"!", upper_unless_y]):
        print(item)

    demo_window = AdmissionWindow(3, 10)  # 演示准入：4 + 4 放得下，再来 4 超预算，再来 2 恰好用满
    print([demo_window.try_admit(size) for size in (4, 4, 4, 2, 25)], demo_window)
