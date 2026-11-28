---
id: mlp-deepdive-incident-null
node: deepdive.incidents
type: qa
step: 3
---
## Q
**NULL 传播事故的排查路径**｜项目深挖

“Walk me through the hardest production issue. How did you find it, and how did you stop it recurring?”

## A
这一题要的是方法：怎么一步步缩小范围，而不是事故本身。详细故事在“失败与压力”部分，这里讲排查路径和防再犯。

- **步骤一，按数据切片：** 缺费用的 100% 是 us_bank_account，来源类型都是 STANDARD_ACH，约 200 个商户、每天约一千万美元。
- **步骤二，到单笔：** 看单笔交易，`payment_instrument_sub_kind` 是 NULL。
- **步骤三，回溯：** 费用品类是 `'BT_' || sub_kind`，NULL 拼接仍是 NULL，匹配不到品类，所以没有异常、没有费用。沿 promote 过程往回看，CTE 用两参重载算对了，最终 `MERGE` 又用没有银行账户分支的一参重载覆盖成 NULL。
- **排除假设：** 对照组（sub_kind 有值的快速到账 ACH）费用正常；按 promote 后天数分桶覆盖率全是 0%，排除滞后。
- **防再犯：** 单一函数，用 versioned migration 删掉旧签名（删文件不会删已部署的对象），去掉动态选择；补一条覆盖 promote 到费用生成的端到端测试。

**英文答法。**
- I **scoped by data first**: 100% bank-account, standard ACH, about **two hundred merchants**, on the order of **ten million dollars a day**.
- Then one row: **sub-kind was `NULL`**, and in SQL `NULL` concatenation is `NULL`, so **no category, no fee, no error**.
- Walking back, the shared `MERGE` used the **one-argument overload with no bank-account branch**.
- I fixed the class: **one function, a versioned migration to drop the old signature**, and an **end-to-end test** from promotion to fee generation.

**追问。**
- **Your part?** I owned the RCA, the postmortem and the hardening; a teammate's stopgap landed first.
