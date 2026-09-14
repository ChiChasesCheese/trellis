---
id: storage-online-migration-four-phase
node: storage.relational.operations
type: cloze
---
A zero-downtime **online migration** (moving live data to a new model or store while still serving traffic, Stripe-style) runs in four phases: **1)** {{c1::dual-write — every new write goes to both the old and the new store}}; **2)** {{c2::backfill — copy all pre-existing data into the new store, rate-limited and checkpointed}}; **3)** {{c3::dual-read / verify — serve from the old path but read both and compare, alerting on any mismatch}}; **4)** {{c4::cut over reads to the new store, then delete the old write path and old data}}. Each phase is observable and reversible on its own, so the migration only advances when the data is proven consistent.

## zh
一次零停机的**在线迁移（online migration）**（在持续服务流量的同时把线上数据迁到新模型或新存储，Stripe 风格）分四个阶段：**1)** {{c1::dual-write — 每个新写入同时写老存储和新存储}}；**2)** {{c2::backfill — 把所有既有数据回填到新存储，限速并带 checkpoint}}；**3)** {{c3::dual-read / verify — 仍从老路径提供服务，但两边都读并比对，发现不一致就告警}}；**4)** {{c4::把读切到新存储，然后删除老的写路径和老数据}}。每个阶段都可独立观测、独立回退，只有数据被证明一致时迁移才推进。
