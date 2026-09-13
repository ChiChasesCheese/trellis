# q38 · 功能开关（白名单 · 百分比灰度 · 属性规则 · 依赖）

> `problems/q38_feature_flags/` · 4 个 part
> **主题：规则的评估**顺序**就是这道题；以及"稳定哈希"。**

## 一句话题意

判断某个用户对某个 flag 是 `ON` 还是 `OFF`。
四层规则：kill switch / 黑白名单 → 属性规则 → 百分比灰度 → 依赖。

## 核心考点

`S02` 解析 · `S03` 建模 · `S05` 阈值 · **`S11` 确定性 / 幂等（稳定哈希分桶）** ·
`S18` 校验 · `S19` 增量

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
