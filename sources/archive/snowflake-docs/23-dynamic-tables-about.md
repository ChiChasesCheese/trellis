---
title: Dynamic tables¶
corpus: snowflake-docs
section: 23-dynamic-tables-about
level: 1
locator: https://docs.snowflake.com/en/user-guide/dynamic-tables-about
license: free-online
fetched: '2026-09-13'
---

# Dynamic tables[¶](#dynamic-tables)

A dynamic table materializes the results of a SELECT query and keeps them up to date. You specify a SELECT query and a target lag, and Snowflake tracks dependencies and refreshes the data on schedule. For a detailed comparison with materialized views, streams and tasks, and dbt, see [Decision guide for dynamic tables](/user-guide/dynamic-tables/decision-guide).

This statement defines what the table contains (the SELECT query), how fresh the data must be (`TARGET_LAG`), and how Snowflake refreshes the data (`REFRESH_MODE`). Once created, Snowflake monitors the base table (`raw_orders` in this example) and refreshes the dynamic table automatically. For a full tutorial, see [Create a dynamic table](/user-guide/dynamic-tables/create).

## How Snowflake keeps dynamic tables up to date[¶](#how-snowflake-keeps-dynamic-tables-up-to-date)

When you create a dynamic table, Snowflake parses your query, identifies the base tables it reads from, and registers the dynamic table for refresh. From that point on, Snowflake monitors the base tables for changes and refreshes the dynamic table to stay within the target lag you set.

Each refresh follows these steps:

1. Snowflake detects that the base tables have changed.
2. If the dynamic table uses an incremental refresh, only the rows that changed are computed. If it uses a full refresh, the entire result set is refreshed.
3. The new results are applied to the dynamic table atomically, so readers never see a partial refresh.

When you have multiple dynamic tables that depend on each other, Snowflake treats them as a pipeline. It infers the dependency graph from the queries and picks a consistent snapshot timestamp. Snowflake refreshes tables in dependency order so that downstream tables always see a consistent view of their upstream inputs.

### Build a pipeline of dynamic tables[¶](#build-a-pipeline-of-dynamic-tables)

A single dynamic table cleans or transforms one data source. To build a full pipeline, create additional dynamic tables that read from each other. For example, `dt_orders_daily` aggregates daily revenue on top of `dt_orders`, while also joining to `dim_customers`. For the full definitions, see [Create a dynamic table](/user-guide/dynamic-tables/create).

Snowflake manages these dynamic tables as a pipeline: `dt_orders` -> `dt_orders_daily`. Snowflake also tracks `dim_customers` as a dependency of `dt_orders_daily`. Each dynamic table has its own target lag, and refreshes are coordinated so that `dt_orders_daily` always reflects a consistent snapshot of its inputs.

## Key concepts[¶](#key-concepts)

**Target lag.** Target lag tells Snowflake how fresh the data must be. A target lag of 10 minutes means Snowflake tries to keep the data no more than 10 minutes behind the base tables, but actual lag can exceed the target when refreshes take longer than expected. You can also set `TARGET_LAG = DOWNSTREAM` on intermediate tables so they refresh only when their downstream dependents need fresh data. For details, see [Set the target lag for a dynamic table](/user-guide/dynamic-tables/target-lag).

**Refresh modes.** Dynamic tables support several refresh modes. `INCREMENTAL` processes only the rows that changed since the last refresh. `FULL` refreshes the entire result set. `AUTO` lets Snowflake choose at creation time based on whether the definition supports incremental refresh.

`ADAPTIVE` uses incremental refresh by default but automatically reinitializes when large upstream changes are detected. For advanced use cases, `CUSTOM_INCREMENTAL` lets you define your own refresh logic using DML statements. For details, see [Dynamic table refresh modes](/user-guide/dynamic-tables/refresh-modes).

**Automated scheduling.** Snowflake monitors your dynamic tables, detects upstream changes, and dispatches refreshes automatically in dependency-graph order. You can set `SCHEDULER = DISABLE` to manage refreshes manually or through an external tool such as dbt or Airflow. For details, see [Manage dynamic tables](/user-guide/dynamic-tables/manage).

**Pipelines.** When dynamic tables read from each other, they form a pipeline. Snowflake infers the dependency graph automatically from the queries you write. You don’t need to declare dependencies or script the execution order.

## Cost summary[¶](#cost-summary)

Dynamic tables incur three categories of cost:

| Cost category | What it covers | Key factors | 
|---|---|---|
| Warehouse compute | The virtual warehouse runs each refresh query. | Warehouse size, how often refreshes run, query complexity, data volume. | 
| Cloud Services | Snowflake compiles the refresh query, tracks dependencies, monitors changes, and coordinates refreshes. | Query complexity, number of dynamic tables, pipeline depth, target lag (shorter lag means more scheduling work). | 
| Storage | Refreshes add, replace, or remove micro-partitions in the table. | Dynamic table size, number of refreshes, Time Travel retention. | 

For a detailed breakdown, see [Understanding costs for dynamic tables](/user-guide/dynamic-tables/cost).

## When to use dynamic tables[¶](#when-to-use-dynamic-tables)

As a general rule, if your logic is expressible as a SQL SELECT statement, it is a candidate for a dynamic table.

Dynamic tables are well-suited for workloads where you:

- Want to materialize query results that stay up to date without writing custom orchestration code.
- Need to build multi-step pipelines with joins, aggregations, or window functions.
- Prefer a declarative approach where you define the desired result and let Snowflake handle scheduling.
- Want to transition from batch processing to near-real-time freshness by adjusting a single parameter (target lag).

Dynamic tables do not support workloads that:

- Require data fresher than 60 seconds (the minimum target lag) or strictly guaranteed refresh timing.
- Need stored procedures or external functions in the definition.
- Use UDTFs outside of lateral joins. See [Supported queries for dynamic tables](/user-guide/dynamic-tables/supported-queries) for details.

For a side-by-side comparison with streams and tasks, materialized views, and other approaches, see [Decision guide for dynamic tables](/user-guide/dynamic-tables/decision-guide).

## What’s next[¶](#whats-next)

- To create your first dynamic table, see [Create a dynamic table](/user-guide/dynamic-tables/create) .
- To understand refresh modes, see [Dynamic table refresh modes](/user-guide/dynamic-tables/refresh-modes) .
- To learn how target lag controls data freshness, see [Set the target lag for a dynamic table](/user-guide/dynamic-tables/target-lag) .
- To compare dynamic tables with other features, see [Decision guide for dynamic tables](/user-guide/dynamic-tables/decision-guide) .
- To monitor refresh health and set up alerts, see [Monitor dynamic tables](/user-guide/dynamic-tables/monitoring) .
- To delete or archive expired rows asynchronously and reduce storage, see [Use storage lifecycle policies with dynamic tables](/user-guide/dynamic-tables/storage-lifecycle-policies) .
