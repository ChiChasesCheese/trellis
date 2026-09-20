---
id: quality-exception-design
node: quality.errors
type: qa
step: 1
---
## Q
设计一套自定义异常层次结构，一个"好"的领域异常长什么样？

## A
```python
class BookingError(Exception):
    """所有预订相关异常的基类，调用方按需要的粒度捕获"""

class SeatAlreadyLockedError(BookingError):
    def __init__(self, seat_id: str):
        super().__init__(f"seat {seat_id} already locked")
        self.seat_id = seat_id
```
一个好的领域异常是具体且带语义的：类名本身就点名了被违反的业务规则,而不是笼统地抛一个 `Exception("error")`；它还携带调用方做出反应所需要的数据（这里是 `seat_id`，用来决定重试还是换一个座位）。这些异常继承自一个共同的小型基类（`BookingError`），让调用方能按自己关心的粒度去捕获——只想处理座位冲突就捕 `SeatAlreadyLockedError`，想统一兜底就捕 `BookingError`。

层次不宜过深：两三层通常够用，每一层都要对应一种"调用方真的会区别对待"的分类，为了显得"设计完整"而堆出用不上的中间层，只是又造了一种过度设计的可有可无者。
