---
title: Understanding overall cost¶
corpus: snowflake-docs
section: 32-cost-understanding-overall
level: 1
locator: https://docs.snowflake.com/en/user-guide/cost-understanding-overall
license: free-online
fetched: '2026-09-13'
---

# Understanding overall cost[¶](#understanding-overall-cost)

Note

This topic describes foundational costs associated with using Snowflake (compute costs, storage costs, and data transfer costs). Specific Snowflake features (for example, Snowflake Cortex and Snowpark Container Services) incur costs in unique ways, and are not discussed in this topic.

## How are costs incurred?[¶](#how-are-costs-incurred)

The total cost of using Snowflake is the aggregate of the cost of using data transfer, storage, and compute resources. Snowflake’s
innovative [cloud architecture](/user-guide/intro-key-concepts) separates the cost of accomplishing any task into one of these
usage types.

- Compute Resources
- Using compute resources within Snowflake consumes Snowflake credits. The billed cost of using compute resources is calculated by multiplying the number of consumed credits by the price of a credit. For the current price of a credit, see the [Snowflake Pricing Guide](https://www.snowflake.com/pricing/pricing-guide/) .There are three types of compute resources that consume credits within Snowflake: 
  - **Virtual Warehouse Compute** :[Virtual warehouses](/user-guide/warehouses) are user-managed compute resources that consume
credits when loading data, executing queries, and performing other DML operations. Because Snowflake utilizes per-second billing (with a
60-second minimum each time the warehouse starts), warehouses are billed only for the credits they actually consume when they are
actively working.
  - **Serverless Compute** : There are Snowflake features such as Search Optimization and Snowpipe that use Snowflake-managed compute
resources rather than virtual warehouses. To minimize cost, these serverless compute resources are automatically resized and scaled
up or down by Snowflake as required for each workload.
  - **Cloud Services Compute** : The cloud services layer of the Snowflake architecture consumes credits as it performs behind-the-scenes
tasks such as authentication, metadata management, and access control. Usage of the cloud services layer is charged only if the daily
consumption of cloud services resources exceeds 10% of the daily warehouse usage.
 For more details about compute costs, see [Understanding compute cost](/user-guide/cost-understanding-compute) .
- Storage Resources
- The monthly cost for storing data in Snowflake is based on a flat rate per terabyte (TB). For the current rate, which varies depending on your type of account (Capacity or On Demand) and region (US or EU), see the [Snowflake Pricing Guide](https://www.snowflake.com/pricing/pricing-guide/) .Storage is calculated monthly based on the average number of on-disk bytes stored each day in your Snowflake account. For more details about storage costs, see [Understanding storage cost](/user-guide/cost-understanding-data-storage) .
- Data Transfer Resources
- Snowflake does not charge data ingress fees to bring data into your account, but does charge for data egress. Snowflake charges a per-terabyte fee when you transfer data from a Snowflake account into a different region on the same cloud platform or into a completely different cloud platform. This fee for data egress depends on the region where your Snowflake account is hosted. For details, see the [Snowflake Pricing Guide](https://www.snowflake.com/pricing/pricing-guide/) .For more details about data transfer costs, see [Understanding data transfer cost](/user-guide/cost-understanding-data-transfer) .

## Total cost example[¶](#total-cost-example)

The following example provides insight into the total cost in Snowflake to load and query data.

Suppose an organization loads data constantly, 24x7. It has two different groups of users (Finance and Sales) using the database in overlapping, but different times of the day. It also runs a weekly batch report. This organization:

- Uses the Standard Edition of Snowflake.
- Stores an average of 65 TBs of compressed data (compare with 325 TB without compression).
- Loads data 24x7x365. They use a Small Standard virtual warehouse for this purpose.
- Enables seven finance users to work 5 days a week from 8am until 5pm using a Large Standard virtual warehouse.
- Enables twelve sales users in different geographies to work a total of 16 hours a day (across Europe and the Americas), 5 days a week using a Medium Standard virtual warehouse.
- Runs a complex weekly report every Friday. This report takes approximately 2 hours to run on a 2X-Large standard warehouse.

**Data Loading Requirements**

| Parameter | Customer Requirement | Configuration | Cost | 
|---|---|---|---|
| Loading Window | 24 x 7 x 365 | Small Standard Virtual Warehouse (2 credits/hr) | 1,488 credits (2 credits/hr x 24 hours per day x 31 days per month) | 

**Storage Requirements**

| Data set size (per month) | 65 TB (after compression) | 

**Compute Requirements**

| Parameter | Customer Requirement | Configuration | Cost | 
|---|---|---|---|
| Finance Users | 5 Users, 8am-5pm (9 hours) | Large Standard Virtual Warehouse (8 credits/hr) | 1,440 credits (8 credits/hr x 9 hours per day x 20 days per month) | 
| Sales Users | 12 Users, 16 hour time slot | Medium Standard Virtual Warehouse (4 credits/hr) | 1,280 (4 credits/hr x 16 hours per day x 20 days per month) | 
| Complex Query Users | 1 User, 2 hours/day | 2X Standard Virtual Warehouse (32 credits/hr) | 256 (32 credits/hr x 2 hours per day x 4 days per month) | 

**Total Cost**

| Usage Type | Monthly Cost | Total Billed Cost | 
|---|---|---|
| Compute Cost | 4,464 credits (@ $2/credit) | $8928 | 
| Storage Cost | 65 TB (@ $23/TB) | $1495 | 
|  |  | $10,423 | 

**Next Topics**
