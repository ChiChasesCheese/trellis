---
id: task-schedule-interval-vs-cron
node: pipelines.task-scheduling-cron-and-dag
type: qa
source: snowflake-docs
---
## Q
任务的 `SCHEDULE` 有哪两种写法？「每周日洛杉矶时间凌晨 3:07 运行」应该用哪一种？

## A
一种是固定间隔，例如 `SCHEDULE = '10 SECONDS'` 或以分钟为单位的间隔，适合「每隔多久跑一次」；另一种是 `SCHEDULE = 'USING CRON <表达式> <时区>'`，适合基于具体时间或日期的调度。每周日凌晨 3:07 应使用 CRON 形式，例如 `USING CRON 7 3 * * SUN America/Los_Angeles`，并显式带上时区。
