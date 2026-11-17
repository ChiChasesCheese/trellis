---
id: errors-taxonomy-granularity
node: errors.taxonomy
type: qa
step: 2
---
## Q
异常层次里，什么时候该新建一个子类，什么时候给现有异常加一个字段就够了？比如“帖子不存在、评论不存在、评论不属于这个帖子”。

## A
**一个子类对应调用方的一个分支，其余细节放字段**

- **判据**：有没有调用方会写不同的 `except` 来处理它。没有，就不要新类；
- **三种“找不到”都是 404**：调用方的反应相同，用一个 `NotFound` 加 `what` 字段区分，日志和测试读字段；
- **“评论属于别的帖子”也回 404**：当作找不到，不让调用方探测别处的数据（合同里写明）；
- **类太多的代价**：每个类都是公开接口，以后要维护、要写文档、不能随意改名；
- **类太少的代价**：调用方只能解析消息文本，消息一改就坏。

```python
class NotFound(Exception):
    def __init__(self, what: str, key):
        super().__init__(what, key)               # args 是构造参数
        self.what, self.key = what, key

def find_comment(threads: dict, thread_id: int, comment_id: int):
    if thread_id not in threads: raise NotFound("thread", thread_id)
    if comment_id not in threads[thread_id]: raise NotFound("comment", comment_id)
    return threads[thread_id][comment_id]

try: find_comment({1: {7: "hi"}}, 1, 9)
except NotFound as e: print(404, e.what, e.key)   # 404 comment 9
```

**知识点：**错误类型体系（Error Taxonomy）
