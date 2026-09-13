# q38 · 功能开关（白名单 · 百分比灰度 · 属性规则 · 依赖）

> `problems/q38_feature_flags/` · 4 个 part
> **主题：规则的评估**顺序**就是这道题；以及"稳定哈希"。**

## 一句话题意

判断某个用户对某个 flag 是 `ON` 还是 `OFF`。
四层规则：kill switch / 黑白名单 → 属性规则 → 百分比灰度 → 依赖。

## 核心考点

`S02` 解析 · `S03` 建模 · `S05` 阈值 · **`S11` 确定性 / 幂等（稳定哈希分桶）** ·
`S18` 校验 · `S19` 增量

## 直觉 / Intuition

把它想成**海关安检**而不是"一堆 if"：每道关卡只回答"能不能拦下你"，
拦下就直接出结果，不拦就放你去下一关——所以顺序本身就是语义，
换个顺序就是另一道题。依赖检查放在最前面，是因为它问的是"这功能本身能不能存在"，
和"你是谁"无关，白名单再硬也换不来一个不存在的地基。
allow/deny 在中间，因为它们回答"你是谁"——一次性钦定结果，跳过后面所有"证明你符合条件"的环节。
灰度放最后，是因为它是"矮子里拔将军"：只有在没人明确说你行/不行时，才靠概率兜底。
稳定哈希桶不是为了随机好看，而是把"扔骰子"变成"查表"——同一个 `(flag, user)` 输给一个纯函数，
天然满足确定性，不用存状态，这比"随机数 + 记住结果"简单得多。

## 解题思路

**评估顺序（第一个决定性的步骤胜出）—— 这就是全题：**

```
0. 未知 flag                → OFF
1. flag 是 off（kill switch）→ OFF        （压过白名单）
2. 依赖 requires 未全部 ON   → OFF        （压过白名单）
3. 用户在 deny 里            → OFF
4. 用户在 allow 里           → ON         （跳过属性规则和灰度，但**不跳过**依赖）
5. 属性规则不满足            → OFF
6. bucket < rollout          → ON，否则 OFF
```

### 百分比灰度（Part 2）

```python
import zlib
bucket = zlib.crc32(f"{flag}:{user}".encode()) % 100
in_rollout = bucket < rollout          # rollout=100 → 全部；0 → 没有；默认 100
```

**必须用稳定哈希**（`zlib.crc32` / `hashlib`），**不能用 Python 内置的 `hash()`** ——
它对 str 每次进程启动都不同（PYTHONHASHSEED），同一个用户会在不同进程里落到不同桶。

**桶里带 flag 名**，所以不同 flag 灰度到的是不同的人（否则所有 flag 灰度同一批人）。

### 属性规则（Part 3）

`country=US|CA` 和 `plan=pro|enterprise`：**跨 key 是 AND，key 内是 OR**。
**用户缺这个属性 → 该规则不满足。**
变体 `ab=even`：id 里的数字为偶数才开 —— 当作普通规则 key。

### 依赖（Part 4）

`requires=a|b`：每个被依赖的 flag 对**同一个用户**都必须是 `ON`（**递归**，带上它自己的全部规则）。
被依赖的 flag 不存在、或存在**依赖环** → `OFF`。
依赖在 **kill switch 之后、黑白名单之前**检查 ——
**所以白名单用户也用不了前置条件不满足的功能。**

## 坑

1. **有白名单但用户不在上面 ≠ 自动 OFF**：属性规则和灰度**仍然会判**
   （`vip,carol` → ON，因为 `vip` 没有其他规则）。
2. **灰度边界**：bucket 54 在 `rollout=54` 时 OFF，在 `rollout=55` 时 ON；`rollout=0` / `100`。
3. **`off` 压过 `allow`；`deny` 压过 `allow`。**
4. 用户缺属性；key 内 OR / 跨 key AND。
5. `requires` 三级链；被依赖的 flag 不存在；**两个 flag 互相依赖的环**；
   **白名单用户但前置不满足**。
6. `CHECK` 里的未知用户；**重新声明的 flag 替换旧的配置**。

## 变体

- adonais0（2021）：限定地区的功能只对该地区用户开；A/B 功能只对 **id 为偶数**的用户开
  → 这里的 `ab=even`。
- 有的说法把**白名单当成唯一受众**（不在名单上的一律 OFF）。
  本仓库把它当成**旁路**（内测者提前看到），其他人由 kill switch / 属性 / 灰度决定。
  按"受众"读法，`vip,carol` 会是 OFF。

## Code Core 节点

**`correctness.determinism`**（稳定哈希） · **`model.state-machine`**（规则顺序） ·
`rules.thresholds` · `algorithms.graph-traversal`（依赖环） · `input.structured`

## 自测清单

- [ ] 有白名单但用户不在上面 → 仍走属性/灰度
- [ ] bucket 恰好等于 rollout / 差 1；`rollout=0` / `100`
- [ ] `off` vs `allow`；`deny` vs `allow`
- [ ] 用户缺属性；key 内 OR；跨 key AND
- [ ] `requires` 三级链 / 缺失依赖 / 两 flag 成环 / 白名单 + 前置失败
- [ ] 未知用户；重复声明的 flag
- [ ] 换一个进程重跑，同一用户的桶不变（确认没用 `hash()`）
