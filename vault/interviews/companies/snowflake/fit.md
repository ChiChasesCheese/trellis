# fit · Why Snowflake / What do you know / Why leave（English scripts）

> 对应 Stripe 的 `stripe-fit.md`，只写 Snowflake 特有的话术。自我介绍在 `loop/rounds/00_ai_screen/playbook.md` §2。数字来自 `01-company-brief.md`（全部带来源）。

## 1. Why Snowflake?（60 s）

> Three reasons, starting with the most honest one.
>
> First, I've been one of your heaviest kinds of user for two years. Braintree's settlement and fee platform runs natively on Snowflake — Streams, Tasks, stored procedures, table functions, MERGE — and it's a financial system, so I've hit every edge: stream offsets that only advance inside a DML transaction, task DAGs that partially fail, feature flags to stop a flow, reconciling what the warehouse computed against what a partner reports. I know exactly which primitives are great and which ones I had to work around. I'd rather build and fix them than route around them.
>
> Second, the problems your backend teams work on are the ones I care about: correctness at scale, metering and billing that has to be exact, distributed coordination — I read the Execution Anchor post from May about binding each query to exactly one Global Services instance, and that's the same "exactly one writer" problem I solve with MERGE keys and handshakes, just one layer down.
>
> Third, the trajectory. Product revenue grew 37% last quarter with three quarters of acceleration, CoCo and CoWork are being adopted fast, and you're moving into OLTP with Unistore and Snowflake Postgres. A platform that's growing that fast and expanding what it does is where an early-career backend engineer learns the most.

中文注释：第二段的 Execution Anchor 是真实博客（2026-05-05），点名它 = 「我做过功课」的最强信号；第三段数字要说对：**37% / 三个季度加速 / CoCo / CoWork**。不要背更多数字。

## 2. What do you know about Snowflake?（45 s，从 backend 视角）

> At the architecture level: immutable micro-partitions in object storage, independent virtual warehouses for compute, and a stateless cloud-services layer with all metadata in FoundationDB. That separation is why clone and time travel are just metadata operations, and why multiple warehouses can read the same data without contention.
>
> At the product level, the last year has been about the agentic layer — Cortex AI, and the two agents that got renamed at Summit: CoCo for engineers and CoWork for business users — plus openness through Iceberg and Apache Polaris, and moving down into OLTP with Hybrid Tables and Snowflake Postgres.
>
> From the user side, what I actually run every day is Streams, Tasks, MERGE, and stored procedures — the primitives that Dynamic Tables now package declaratively.

## 3. Why leave PayPal?（30 s，不抱怨）

> I've owned one platform end to end for two years — designed it, ran it in production, was the on-call authority for it. The next step in depth for me is to move from consuming these data-platform primitives to building them, on a team where the platform is the product. Snowflake is the most direct version of that move.

## 4. What are you looking for in the next role?（30 s）

> Three things. A backend system where correctness matters — billing, metadata, transactions, scheduling. A team that ships and measures — I like the consumption model precisely because the product is judged on what customers actually run. And the room to grow from owning a component to owning a system.

## 5. Where do you see yourself / what team?（GenSWE 是 team matching，答开放但有偏好）

> I'm open — that's the point of the program — but my strongest pull is anything close to transactions, scheduling, or metering: the tasks and dynamic-tables side, the billing pipeline, or the FDB / Unistore side. Those are the parts I've been on the receiving end of as a user.

## 6. 一句反打（如果它问「你没有分布式系统内部经验」）

> Fair — my experience is on the application side of a distributed system, not inside its engine. What I bring is the failure modes a real financial workload exposes, and a habit of making pipelines idempotent and verifiable. The internals I'd learn fast; the instinct for where correctness breaks is already there.
