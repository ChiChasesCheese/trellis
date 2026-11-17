---
id: lcp-feature-flag-reflection-stable-assignment
node: lcproject.lcp-feature-flag
type: qa
step: 3
tags: [作答]
---
## Q
在功能开关服务里，实验 `search_ranker` 的放量要从 20% 提到 30%，产品要求「已经看到 candidate 的用户不能被换回 baseline」。分桶哈希里为什么放 `flag_key` 和 `user_id`，却不放放量比例？比例调整时到底谁的分组会变？

## A
**桶号只由 (flag_key, user_id) 决定；比例只移动区间边界，所以只有新划进来的用户变化**

- **放 `user_id`**：同一用户每次得到同一个桶，不必存分配表，多个实例也一致
- **放 `flag_key`**：不同开关用不同的桶，否则同一批用户会在所有实验里同时被放进 candidate
- **不放比例**：比例进了哈希，每调一次比例全员重新洗牌，已入组用户会被换走
- **边界移动**：80/20 变 70/30，candidate 区间从 [8000, 10000) 扩成 [7000, 10000)，只有桶号在 [7000, 8000) 的用户从 baseline 变 candidate
- **实测 10000 个用户**：candidate 从 2006 个增加到 2999 个，原来的 2006 个全部保留，换组的 993 个正好是桶号在 [7000, 8000) 的人
- **变体顺序也是分组的一部分**：区间按 `variants` 顺序累计，把 `["baseline","candidate"]` 调成 `["candidate","baseline"]`，同样 80/20 下有 3943 个用户换组

```mermaid
flowchart TB
    A[flag_key:user_id] --> B[sha256 取模 10000]
    B --> C{桶号}
    C -->|0 到 6999| D[一直 baseline]
    C -->|7000 到 7999| E[30% 时 candidate]
    C -->|8000 到 9999| F[一直 candidate]
```

```python
def bucket(flag_key, user_id):
    raw = sha256((flag_key + ":" + user_id).encode("utf-8")).digest()
    return int.from_bytes(raw, "big") % 10000   # 不用 random，也不用 hash()

def pick(self, bucket_number):              # rollout 已按 variants 顺序排好
    upper = 0
    for variant, percent in self.rollout:
        upper += percent * 100              # 一个百分点 100 个桶
        if bucket_number < upper:           # 左闭右开
            return variant
```

<details class="pt"><summary>延伸</summary>Python 内置的 `hash("acct-1") % 10000` 每个进程的结果不同（连续两次运行得到 1938 和 8490），不能拿来分桶；想把放量调小时，被挤出区间的用户一定是区间末尾那一段，这是按序累计区间的代价。</details>

**知识点：** 策略模式与可替换算法（Strategy）、不变量与封装（Invariants）、值对象与不可变性（Value Objects）
