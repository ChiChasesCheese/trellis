---
id: bagu-schema-money-backup-1-money-time-backup
node: b.mysql.schema-money-backup
type: qa
step: 1
---
## Q
**表设计规范 · 金额、时间、外键与备份**｜追问

面试官：「金额怎么存才不丢精度，DECIMAL 和 BIGINT 怎么选？DATETIME 和 TIMESTAMP 怎么选？为什么很多公司不用外键？备份怎么做，RTO 和 RPO 是什么？」

## A
**基本回答。** 金额用 `DECIMAL` 或以「分」为单位的 `BIGINT`，不用 `FLOAT`、`DOUBLE`。`DATETIME` 范围到 9999 年、不随时区变；`TIMESTAMP` 存 UTC 秒数，只到 2038-01-19 03:14:07，读写按会话时区转换。外键多数公司不用。备份看 RTO（多久恢复）和 RPO（最多丢多少数据）。
浮点不准：0.1 在二进制里无限循环，实测 0.1 乘 3，`FLOAT` 得 0.30000000447034836，`DOUBLE` 得 0.30000000000000004，`DECIMAL` 得 0.3。备份：`mysqldump --single-transaction` 是逻辑备份，xtrabackup 是物理备份，恢复快得多。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 262">
<text x="10" y="14" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">存金额：0.1 乘 3 的结果</text>
<rect x="10" y="22" width="104" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="62" y="39" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">FLOAT</text>
<rect x="114" y="22" width="216" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="222" y="39" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">0.30000000447034836</text>
<rect x="10" y="48" width="104" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="62" y="65" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">DOUBLE</text>
<rect x="114" y="48" width="216" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="222" y="65" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">0.30000000000000004</text>
<rect x="10" y="74" width="104" height="26" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="62" y="91" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">DECIMAL</text>
<rect x="114" y="74" width="216" height="26" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="222" y="91" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">0.30</text>
<rect x="10" y="100" width="104" height="26" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="62" y="117" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">BIGINT（分）</text>
<rect x="114" y="100" width="216" height="26" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="222" y="117" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">30</text>
<text x="10" y="148" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">备份时间线：RPO 管丢多少，RTO 管停多久</text>
<line x1="10" y1="190" x2="330" y2="190" stroke="currentColor" stroke-width="1.2"/>
<line x1="40" y1="184" x2="40" y2="196" stroke="currentColor" stroke-width="1.2"/>
<text x="40" y="178" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">全量备份</text>
<line x1="150" y1="184" x2="150" y2="196" stroke="currentColor" stroke-width="1.2"/>
<text x="150" y="178" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">最后备份点</text>
<line x1="222" y1="184" x2="222" y2="196" stroke="currentColor" stroke-width="1.2"/>
<text x="222" y="178" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">故障</text>
<line x1="298" y1="184" x2="298" y2="196" stroke="currentColor" stroke-width="1.2"/>
<text x="298" y="178" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">恢复</text>
<line x1="150" y1="204" x2="222" y2="204" stroke="currentColor" stroke-width="1.2"/>
<line x1="222" y1="204" x2="298" y2="204" stroke="currentColor" stroke-width="1.2"/>
<text x="186" y="222" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">RPO 丢的数据</text>
<text x="260" y="240" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">RTO 停的时间</text>
</svg>
上半是同一个计算 0.1 × 3 在四种类型里的结果，高亮的两种是金额该用的；下半是备份时间线，RPO 是故障前最后一次备份之后丢的那一段，RTO 是故障到服务恢复的那一段。
**举个例子。** 账户余额 19.90 元：
1. **用 FLOAT：** 余额存成 FLOAT，是二进制近似值，反复加减之后就可能和账面对不上。
2. **用 BIGINT 存分：** 存 1990，所有加减都是整数运算，不会有误差；展示时除以 100。
3. **换币种：** 日元没有小数位，1990 就是 1990 日元，所以表里要有币种和精度字段，不能一律除以 100。
4. **时间字段：** 订单的 `expire_at` 用 `TIMESTAMP` 存 2038 年之后的到期日会报错，改用 `DATETIME` 并统一存 UTC。
5. **备份：** 每天凌晨一次 xtrabackup 全量加 binlog 持续备份。周三 10:00 误删表：恢复全量后重放 binlog 到 09:59，丢失的数据只有那一分钟。
**容易错。**
- **以为 DOUBLE 比 FLOAT 够用：** 精度更高但依然是二进制浮点数，0.1 乘 3 仍是 0.30000000000000004。
- **以为 BIGINT 存分就万事大吉：** 币种小数位不同，没有记录币种与精度，换币种就错。
- **把 TIMESTAMP 当长期时间：** 2038 年之后会溢出，读写还随会话时区变。
- **把 RPO 和 RTO 混为一谈：** RPO 管丢多少数据，RTO 管停多久，两者决定的备份策略不同。
