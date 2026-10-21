# S3 · 没有报错的 bug（最难的 bug · 定位方法 · 为什么测试没抓到）

- 用于：hardest bug / on-call / how do you test / 修一类问题。

**Hook：「My hardest bug threw no error: rows that should exist were simply missing.」**

## 数字

- 约 200 个商户；成交量量级约 $10M/天（是交易额，不是费用额）
- 4 个测试漏洞原因；2 个重载 → 1 个函数
- 按"promote 后天数"分桶，每桶覆盖率都是 0%

## 60 秒

**S**
- A daily **health check I built** said some settled transactions had **no fee**.
- About **200 merchants**, on the order of **$10M a day** of volume.

**T**
- I owned the **root cause** and the **hardening**; a teammate's **stopgap** landed first.

**A**
1. I **sliced** the missing rows: all bank-account, all the new **ACH** path.
2. On **one row**, `sub_kind` was **NULL**.
3. The fee category is `'BT_' || sub_kind`, and in SQL **NULL concatenation is NULL**; nothing matched, **no fee, no error**.
4. **Walked back**: one function had **two overloads**; the final `MERGE` called the one **without a bank-account branch**.
5. Ruled out "just late" with a **control group** and **age buckets**: 0% at every age.
6. Refused to add ACH to the check's **exclusion list**: the check was right.

**R**
- Root cause in **minutes**; postmortem with **four reasons** tests missed it; **one function**, old signature dropped, new **end-to-end test**.

**L**
- An **unmappable input must fail loudly**; fix the **seam**, not the call site.

## 2 分钟（在 60 秒上加）

- **Four test gaps**: tests asserted **routing**, not the **fee**; the fixture was a **card payload**; pending rows never asserted the field; nothing spanned **promote → fee**.
- **Hardening**: one function with a **defaulted parameter**; a **versioned `DROP`** of the old signature, because deleting the source file doesn't remove the deployed object.
- **Different next time**: make the unmapped case an explicit **error** where the category is derived. 【待补：实际落地的形式】

## 追问

- **Why no exception?** SQL **NULL propagation**: `NULL || x` is NULL; the lookup found **no match**, so **no row** was produced.
- **Why are overloads dangerous?** Same **name**, different **behavior**; the call is chosen by **arguments**; the CTE and the `MERGE` picked different ones.
- **How did you rule out lag?** **Control group** with the field set had fees; **age buckets** all 0%.
- **Why not exclude ACH?** It turns a **loud** detector **silent**; the fees were really missing.
- **Why `DROP` in a migration?** Removing the file leaves the **deployed object**; the old signature stays callable.
- **Backfill?** **Fix forward**: wrong state was already consumed downstream, so you need a **correcting entry**, not a reversal. I did not backfill myself.
- **Most general test lesson?** The **fixture must look like the real population**; assert on the **output**, not only the route.
- **How would you fail loudly without killing the batch?** Record rejects to an **error log** instead of dropping them.

## 别说

- 止血 PR 是我的；"I backfilled"；零影响（那是灰度期）。
- 把 $10M 当成费用金额。

## 待补

- 【待补：从告警到根因真实用了多久；"fail loudly"最终落地的形式】
