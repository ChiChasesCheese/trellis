---
id: stream-stale-after-calculation
node: pipelines.stream-staleness-and-retention-extension
type: cloze
source: snowflake-docs
---
流的 `STALE_AFTER` 时间戳 = {{c1::流最近一次被消费的时间}} + MAX({{c2::`DATA_RETENTION_TIME_IN_DAYS`}}, {{c3::`MAX_DATA_EXTENSION_TIME_IN_DAYS`}})。例如保留期 1 天、最大延长 14 天时，应在 {{c4::14}} 天内消费流；保留期 0、最大延长 90 天时，应在 {{c5::90}} 天内消费。
