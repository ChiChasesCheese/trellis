---
title: Introduction to tasks¶
corpus: snowflake-docs
section: 22-tasks-intro
level: 1
locator: https://docs.snowflake.com/en/user-guide/tasks-intro
license: free-online
fetched: '2026-09-13'
---

# Introduction to tasks[¶](#introduction-to-tasks)

Tasks are a powerful way to automate data processing and to optimize business procedures on your data pipeline.

Tasks can run at scheduled times or can be triggered by events, such as when new data arrives in a [stream](/user-guide/streams-intro).

Tasks can run SQL commands and stored procedures that use [supported languages and tools](/developer-guide/stored-procedure/stored-procedures-overview#label-stored-procedures-handler-languages),
including JavaScript, Python, Java, Scala, and [Snowflake scripting](/developer-guide/snowflake-scripting/index).

For complex workflows, you can create sequences of tasks called [task graphs](/user-guide/tasks-graphs).
Task graphs can use logic to perform dynamic behavior, running tasks in parallel or in series.

## Task creation workflow overview[¶](#task-creation-workflow-overview)

1. 
Create a [task administrator role](#label-task-admin-role) that can run the commands in the following steps.
2. 
Define a new task using [CREATE TASK](/sql-reference/sql/create-task) .
3. 
Manually test tasks using [EXECUTE TASK](#label-tasks-executing) .
4. 
Allow the task to run continuously using [ALTER TASK … RESUME](/sql-reference/sql/alter-task) .
5. 
[Monitor task costs](#label-task-monitoring-cost)
6. 
Refine the task as needed using [ALTER TASK](/sql-reference/sql/alter-task) .

For information about running tasks, see:

## Define compute resources[¶](#define-compute-resources)

Tasks require compute resources to run statements and procedures. You can choose between the following two models:

- [Serverless tasks](#label-tasks-compute-resources-serverless) : Snowflake predicts resources that are needed and assigns them automatically.
- [User-managed virtual warehouse model](#label-tasks-compute-resources-warehouse) : You manage the compute resources using a virtual warehouse.

### Serverless tasks[¶](#serverless-tasks)

With this model, you set when you want the task to run, and Snowflake predicts and assigns compute resources needed to complete the task in that time. The prediction is based on a dynamic analysis of the most recent runs of the same task.

#### Limitations[¶](#limitations)

- The maximum compute size for a serverless task is equivalent to an XXLARGE [virtual warehouse](/user-guide/warehouses) .

#### Create a task using the serverless compute model[¶](#create-a-task-using-the-serverless-compute-model)

Use [CREATE TASK](/sql-reference/sql/create-task) to define the task. Don’t include the WAREHOUSE parameter.

The role that runs the task must have the global EXECUTE MANAGED TASK privilege. For more information, see [Task security](#label-task-security-reqs).

The following example creates a task that runs every hour.

#### Cost and performance: Warehouse sizes[¶](#cost-and-performance-warehouse-sizes)

To make sure serverless tasks run efficiently, you can set the minimum and maximum [warehouse sizes](/user-guide/warehouses-overview#label-warehouse-size) by setting the following parameters:

- SERVERLESS_TASK_MIN_STATEMENT_SIZE: the minimum warehouse size for predictable performance (default: XSMALL).
- SERVERLESS_TASK_MAX_STATEMENT_SIZE: the maximum warehouse size to prevent unexpected costs (default: XXLARGE).

After a task completes, Snowflake reviews the performance and adjusts compute resources for future runs within these limits.

The following example shows a task that runs every 30 seconds, with a minimum warehouse size of SMALL and a maximum warehouse size of LARGE.

#### Target completion interval[¶](#target-completion-interval)

You can set an earlier target for a serverless task to complete.
A target completion interval is required for [serverless triggered tasks](/user-guide/tasks-triggered#label-tasks-triggered-migrate-serverless).

When set, Snowflake estimates and scales resources to complete within the target completion interval. When a task is already at its maximum warehouse size and is running too long, the target completion interval is ignored.

In the following example, a task runs every hour at the 24th minute, with a target of completing within 120 minutes.
The start time and time zone are defined by [USING CRON](/sql-reference/sql/create-task#label-create-task-schedule).
If the task gets to the largest warehouse size, it may run as long as three hours before finally triggering a timeout.

### User-managed virtual warehouse model[¶](#user-managed-virtual-warehouse-model)

With this model, you have full control of the compute resources used for each workload.

#### Choose a warehouse[¶](#choose-a-warehouse)

When choosing a warehouse, consider the following:

- Review the best practices in [Warehouse considerations](/user-guide/warehouses-considerations) .
- Analyze average task run times using different warehouses based on warehouse size and clustering.
For more information, see [Task duration](#label-task-duration) .
- If the warehouse is shared by multiple processes, consider the impact of the task on other workloads.

#### Create a task using the user-managed compute model[¶](#create-a-task-using-the-user-managed-compute-model)

Use [CREATE TASK](/sql-reference/sql/create-task), and include the WAREHOUSE parameter.

The role that runs the task must have the global EXECUTE MANAGED TASK privilege.
For more information, see [Task security](#label-task-security-reqs).

The following example creates a task that runs every hour.

### Recommendations for choosing a compute model[¶](#recommendations-for-choosing-a-compute-model)

The following table describes various factors that can help you decide when to use serverless tasks versus user-managed tasks:

| Category | Serverless tasks | User-managed tasks | Notes | 
|---|---|---|---|
| Number, duration, and predictability of concurrent task workloads | Recommended for under-utilized warehouses with too few tasks running concurrently, or completing quickly. Tasks with relatively stable runs are good candidates for serverless tasks. | Recommended for fully utilized warehouses with multiple concurrent tasks. Also recommended for unpredictable loads on compute resources. [Multi-cluster warehouses](/user-guide/warehouses-multicluster) with[auto-suspend and auto-resume](/user-guide/warehouses-overview#label-auto-suspension-and-auto-resumption) enabled could help moderate your credit consumption. | For serverless tasks, Snowflake bills your account based on the actual compute resource usage. For user-managed tasks, billing for warehouses is based on warehouse size, with a 60-second minimum each time the warehouse is resumed. | 
| Schedule interval | Recommended when adherence to the schedule interval is highly important. If a run of a standalone task or scheduled task graph exceeds the interval, Snowflake increases the size of the compute resources. | Recommended when adherence to the schedule interval is less important. | *Schedule interval* refers to the interval of time between scheduled runs of a standalone task or the root task in a task graph. Increasing the compute resources can reduce the runtime of some, but not all, SQL code. It doesn’t ensure a task run is completed within the batch window. | 

The maximum size for a serverless task run is equivalent to an XXLARGE warehouse. If a task workload requires a larger warehouse, create a user-managed task with a warehouse of the required size.

## Define schedules or triggers[¶](#define-schedules-or-triggers)

A task can be set to run on a fixed schedule, or it can be triggered by an event, for example, when a stream has new data.

When a task is created, it starts as suspended.
To allow a task to follow a schedule or detect events continuously, use [ALTER TASK … RESUME](/sql-reference/sql/alter-task).
To run the task one time, use [EXECUTE TASK](/sql-reference/sql/execute-task).

### Run a task on a fixed schedule[¶](#run-a-task-on-a-fixed-schedule)

To run tasks on a fixed schedule, define the schedule when creating or altering task using [CREATE TASK](/sql-reference/sql/create-task) or [ALTER TASK](/sql-reference/sql/alter-task),
or by editing the task in Snowsight, using the SCHEDULE parameter.

Snowflake ensures only one instance of a task with a schedule is run at a time. If a task is still running when the next scheduled run time occurs, then that scheduled time is skipped.

The following example creates a task that runs every 10 seconds:

To define a schedule based on a specific time or day, use the SCHEDULE =’USING CRON…’ parameter.

The following example creates a task that runs every Sunday at 3:07 a.m., using the Americas/Los_Angeles time zone:

For more information, see [CREATE TASK … SCHEDULE](/sql-reference/sql/create-task#label-create-task-schedule).

### Run a task whenever a stream has new data[¶](#run-a-task-whenever-a-stream-has-new-data)

To run tasks whenever a defined [stream](/user-guide/streams-intro) has new data, use [Triggered tasks](/user-guide/tasks-triggered).
This approach is useful for Extract, Load, Transform (ELT) workflows, because it eliminates frequent polling of the source when new data arrival is unpredictable.
It also reduces latency by processing data immediately. For example:

For more information, see [Triggered tasks](/user-guide/tasks-triggered).

### Run on a schedule, but only if a stream has new data[¶](#run-on-a-schedule-but-only-if-a-stream-has-new-data)

You can combine a scheduled task with a triggered task. For example, the following code creates a task that checks a stream for new data every hour:

## Define what happens when a task fails[¶](#define-what-happens-when-a-task-fails)

### Automatically suspend tasks after failed runs[¶](#automatically-suspend-tasks-after-failed-runs)

Optionally suspend tasks automatically after a specified number of consecutive runs that either fail or time out. This feature can reduce costs by suspending tasks that consume Snowflake credits but fail to run to completion.

Set the `SUSPEND_TASK_AFTER_NUM_FAILURES =`  parameter on a task. When the parameter
is set to a value greater than *num*`0`, tasks are automatically suspended after the specified number of consecutive task runs either fail or time out.

The parameter can be set when creating a task using [CREATE TASK](/sql-reference/sql/create-task) or later using
[ALTER TASK](/sql-reference/sql/alter-task). You can also change this value in Snowsight.

The [SUSPEND_TASK_AFTER_NUM_FAILURES](/sql-reference/parameters#label-suspend-task-after-num-failures) parameter can also be set at the account, database, or schema level.
The setting applies to all tasks contained in the modified object.
Note that explicitly setting the parameter at a lower level overrides the parameter value set at a higher level.

### Automatically retry failed task runs[¶](#automatically-retry-failed-task-runs)

If any task completes in a FAILED state, Snowflake can automatically retry the task. The automatic task retry is disabled by default. To enable this feature, set TASK_AUTO_RETRY_ATTEMPTS to a value greater than 0.

Tasks that use error notifications send notifications for each failed retry attempt.
For more information, see [Configure a task to send error notifications](/user-guide/tasks-errors-integrate).

When you set the [TASK_AUTO_RETRY_ATTEMPTS](/sql-reference/parameters#label-task-auto-retry-attempts) parameter value at the account, database, or schema level, the change is applied to tasks contained in the modified object during their next scheduled run.

## Define additional session parameters[¶](#define-additional-session-parameters)

A task supports all session parameters. For the complete list, see [Parameters](/sql-reference/parameters).
Tasks don’t support account or user parameters.

To set session parameters for a task, add the parameter to the task definition with [CREATE TASK](/sql-reference/sql/create-task), or modify the task using [ALTER TASK … SET](/sql-reference/sql/alter-task). Examples:

## Run tasks[¶](#run-tasks)

This section describes the different ways that a task can be scheduled and run, and how the version of a task is determined.

### Run a task manually[¶](#run-a-task-manually)

After you have set up a new task and its parameters using [CREATE TASK](/sql-reference/sql/create-task) or [ALTER TASK](/sql-reference/sql/alter-task), you can start a single run of the task using [EXECUTE TASK](/sql-reference/sql/execute-task).
This command is useful for testing new or modified tasks.

Note

- You can call this SQL command directly in scripts or in stored procedures.
- This command supports integrating tasks in external data pipelines.
- Any third-party service that can authenticate into your Snowflake account and authorize SQL actions can run tasks with the EXECUTE TASK command.

### Versioning of task runs[¶](#versioning-of-task-runs)

When a standalone task is first resumed or manually run, an initial version of the task is set. The standalone task runs using this version. After a task is suspended and modified, a new version is set when the standalone task is resumed or manually run.

When the task is suspended, all future scheduled runs of the task are cancelled; however, currently running tasks continue to run using the current version.

For example, suppose the task is suspended, but a scheduled run of this task has already started. The owner of the task modifies the SQL code called by the task while the task is still running. The task runs the SQL code in its definition using the version of the task that was current when the task started its run. When the task is resumed or is manually run, a new version of the task is set. This new version includes the modifications to the task.

To retrieve the history of task versions, query [TASK_VERSIONS](/sql-reference/account-usage/task_versions) [Account Usage view](/sql-reference/account-usage) (in the SNOWFLAKE shared database).

## View the task history for your account[¶](#view-the-task-history-for-your-account)

To view task history, see either the [TASK_HISTORY](/sql-reference/functions/task_history) table function or the [Tasks page on Snowsight](/user-guide/ui-snowsight-tasks).

For information about required privileges, see [Viewing task history](#label-task-security-reqs-view-history).

To view the run history for a single task:

- SQL:
Query the [TASK_HISTORY](/sql-reference/functions/task_history) table function (in the [Snowflake Information Schema](/sql-reference/info-schema)).

To view details on a task graph run that is currently scheduled or is running:

- SQL:
Query the [CURRENT_TASK_GRAPHS](/sql-reference/functions/current_task_graphs) table function (in the [Snowflake Information Schema](/sql-reference/info-schema)).

To view the history for task graph runs that completed successfully, failed, or were cancelled in the past 60 minutes:

- SQL:
Query the [COMPLETE_TASK_GRAPHS](/sql-reference/functions/complete_task_graphs) table function (in the [Snowflake Information Schema](/sql-reference/info-schema)).

Query the [COMPLETE_TASK_GRAPHS view](/sql-reference/account-usage/complete_task_graphs) view (in [Account Usage](/sql-reference/account-usage)).

## Task costs[¶](#task-costs)

The costs associated with running a task to run SQL code differ depending on the source of the compute resources for the task:

- User-managed warehouse
- Snowflake bills your account for [credit usage](/user-guide/cost-understanding-compute#label-virtual-warehouse-credit-usage) based on warehouse usage while a task is
running, similar to the warehouse usage for running the same SQL statements in a client or the Snowflake web interface. Per-second
credit billing and warehouse auto-suspend give you the flexibility to start with larger warehouse sizes and then adjust the size to match
your task workloads.
- Serverless compute model
- Snowflake bills your account based on compute resource usage. Charges are calculated based on your total usage of the resources, including cloud service usage, measured in *compute-hours* credit usage. The compute-hours cost changes based on warehouse size and query
runtime. For more information, see[Serverless credit usage](/user-guide/cost-understanding-compute#label-serverless-credit-usage) or[Query: Total serverless task cost](/user-guide/cost-exploring-compute#label-cost-explore-query-task) .Snowflake analyzes task runs in the task history to dynamically determine the correct size and number of the serverless compute resources. As Snowflake automatically scales up and down resources to manage your task runs, the cost to run the task runs scales proportionally. To learn how many credits are consumed by tasks, refer to the “Serverless Feature Credit Table” in the [Snowflake Service Consumption Table](https://www.snowflake.com/legal-files/CreditConsumptionTable.pdf) .Consider the following best practices to optimize for cost when you create tasks: 
  - Set the SCHEDULE to run less frequently.
  - Use the auto-suspend and auto-retry parameters to prevent resource waste on failing tasks.
  - Set up [Triggered tasks](/user-guide/tasks-triggered) for tasks that only need to run under certain conditions, such as when a data stream has new data.
  - Create a budget and alert on spend limits for serverless features. For more information, see [Monitor credit usage with budgets](/user-guide/budgets) .
 To retrieve the current credit usage for a specific task, query the [SERVERLESS_TASK_HISTORY](/sql-reference/functions/serverless_task_history) table
function. Execute the following statement as the task owner, where`<database_name>` is the database that contains the task and`<task_name>` is the name of the task:To retrieve the current credit usage for all serverless tasks, query the [SERVERLESS_TASK_HISTORY](/sql-reference/account-usage/serverless_task_history) view. Execute the following statement as an account administrator:

## Monitor cost[¶](#monitor-cost)

Serverless tasks incur [compute cost](/user-guide/cost-understanding-compute#label-serverless-credit-usage) when in use.
You can use cost-related views in the ACCOUNT_USAGE and ORGANIZATION_USAGE schemas to track the costs associated with serverless tasks.
When querying these views, filter on the `service_type` column to find `SERVERLESS_TASK` or `SERVERLESS_TASK_FLEX` values.

| View | Schema | `service_type` | Roles with required privileges | 
|---|---|---|---|
| [METERING_HISTORY](/sql-reference/account-usage/metering_history) | ACCOUNT_USAGE | SERVERLESS_TASK | ACCOUNTADMIN role USAGE_VIEWER database role | 
| [METERING_DAILY_HISTORY](/sql-reference/account-usage/metering_daily_history) | ACCOUNT_USAGE | SERVERLESS_TASK | ACCOUNTADMIN role USAGE_VIEWER database role | 
| [METERING_DAILY_HISTORY](/sql-reference/organization-usage/metering_daily_history) | ORGANIZATION_USAGE | SERVERLESS_TASK | ACCOUNTADMIN role USAGE_VIEWER database role | 
| [USAGE_IN_CURRENCY_DAILY](/sql-reference/organization-usage/usage_in_currency_daily) | ORGANIZATION_USAGE | SERVERLESS_TASK | ORGADMIN role GLOBALORGADMIN role ORGANIZATION_USAGE_VIEWER database role | 

**Example:** View the total account cost that serverless tasks incurred across the organization.

Example: View the total account cost that serverless task incurred between December 1, 2024 and December 31, 2024.

**Example:** View the total account cost that serverless tasks incurred across the organization.

For information about how many credits are charged per Compute-Hour for the operation of the Trust Center, see Table 5 in the
[Snowflake Service Consumption Table](https://www.snowflake.com/legal-files/CreditConsumptionTable.pdf).

## Task duration[¶](#task-duration)

Task duration includes the time from when a task is scheduled to start to when it completes. This duration includes both of the following:

- **Queuing time:** The time a task spends waiting for compute resources to become available before it begins. To calculate queueing time, query[TASK_HISTORY view](/sql-reference/account-usage/task_history) and compare SCHEDULED_TIME with QUERY_START_TIME.
- **Execution time:** The time taken by the task to run its SQL statements or other operations. To calculate run time, query[TASK_HISTORY view](/sql-reference/account-usage/task_history) , and compare QUERY_START_TIME with COMPLETED_TIME.

For example, the following diagram shows a serverless task that is scheduled to run every 15 seconds. The total duration of this task run is 12 seconds, which includes 5 seconds of queuing time and 7 seconds of run time.

### Timeouts[¶](#timeouts)

If a task run exceeds the scheduled time or target completion interval, by default, the task continues to run until it is complete, it times out, or it fails.

When both [STATEMENT_TIMEOUT_IN_SECONDS](/sql-reference/parameters#label-statement-timeout-in-seconds) and [USER_TASK_TIMEOUT_MS](/sql-reference/parameters#label-user-task-timeout-ms) are set, the timeout is the lowest non-zero value of the two parameters.

When both [STATEMENT_QUEUED_TIMEOUT_IN_SECONDS](/sql-reference/parameters#label-statement-queued-timeout-in-seconds) and USER_TASK_TIMEOUT_MS are set, the value of USER_TASK_TIMEOUT_MS takes precedence.

For information about timeouts with task graphs, see [Task graph timeouts](/user-guide/tasks-graphs#label-task-graph-timeouts).

### Considerations[¶](#considerations)

- For serverless tasks, Snowflake automatically scales resources to make sure tasks complete within a target completion interval, including queueing time.
- For user-managed tasks, longer queueing periods are common when tasks are scheduled to run on a shared or busy warehouse.

## Task security[¶](#task-security)

To run tasks, you must have the correct access privileges. This section describes how to manage access to tasks.

For information about task graph ownership, see [Manage task graph ownership](/user-guide/tasks-graphs#label-task-dag-ownership).

### Access control privileges[¶](#access-control-privileges)

#### Creating tasks[¶](#creating-tasks)

Creating tasks requires a role with a minimum of the following privileges:

| Object | Privilege | Notes | 
|---|---|---|
| Account | EXECUTE MANAGED TASK | Required only for tasks that rely on serverless compute resources. | 
| Database | USAGE |  | 
| Schema | USAGE, CREATE TASK |  | 
| Warehouse | USAGE | Required only for tasks that rely on user-managed warehouses. | 

#### Running tasks[¶](#running-tasks)

After a task is created, the task owner must have the following privileges for the task to run:

| Object | Privilege | Notes | 
|---|---|---|
| Account | EXECUTE TASK | Required to run any tasks the role owns. Revoking the EXECUTE TASK privilege on a role prevents all subsequent task runs from starting under that role. | 
| Account | EXECUTE MANAGED TASK | Required only for tasks that rely on serverless compute resources. | 
| Database | USAGE |  | 
| Schema | USAGE |  | 
| Task | USAGE |  | 
| Warehouse | USAGE | Required only for tasks that rely on user-managed warehouses. | 

In addition, the role must have the permissions required to run the SQL statement that the task runs.

Note

By default, Snowflake runs tasks by using the system user with the privileges of the task owner role.
To run a task as a specific user, configure the task with EXECUTE AS USER. For more information, see [Run tasks with user privileges](/user-guide/tasks-intro#label-user-based-security-for-tasks).

#### Viewing task history[¶](#viewing-task-history)

To view tasks, you must have one or more of the following privileges:

- The ACCOUNTADMIN role
- The OWNERSHIP privilege on the task
- The global MONITOR EXECUTION privilege

#### Resuming or suspending tasks[¶](#resuming-or-suspending-tasks)

In addition to the task owner, a role that has the OPERATE privilege on the task can suspend or resume the task. This role must have the USAGE privilege on the database and schema that contain the task. No other privileges are required.

When a task is resumed, Snowflake verifies that the task owner role has the privileges listed in [Running tasks](#label-running-tasks-privileges).

### Create custom roles to manage task permissions[¶](#create-custom-roles-to-manage-task-permissions)

With custom roles you can easily manage permissions granted to each account or role in Snowflake. To make changes to permissions for all accounts or roles using the custom role, update the custom role. Or, revoke permissions by removing the custom role.

#### Create a custom role to create tasks[¶](#create-a-custom-role-to-create-tasks)

Snowflake requires different permissions to create serverless and user-managed tasks.

For example, to create user-managed tasks, create a custom role named `warehouse_task_creation`
and grant that role the CREATE TASK and USAGE privileges on the warehouse that the role can create tasks in.

As an example of a role that can create serverless tasks; create a custom role named `serverless_task_creation` and grant the role the CREATE TASK privilege and the account level EXECUTE MANAGED TASK privilege.

#### Create a custom role to administer tasks[¶](#create-a-custom-role-to-administer-tasks)

Create a custom role, grant it the EXECUTE TASK privilege, and then grant this custom role to any task owner role to allow altering their own tasks. To remove the ability for the task owner role to run the task, revoke this custom role from the task owner role.

For example, create a custom role name `taskadmin` and grant that role the EXECUTE TASK privilege. Assign the `taskadmin` role to a
task owner role named `myrole`:

Set the active role to ACCOUNTADMIN before granting the account-level privileges to the new role

Set the active role to SECURITYADMIN to show that this role can grant a role to another role

For more information about how to create custom roles and role hierarchies, see [Configuring access control](/user-guide/security-access-control-configure).

#### Drop a task owner role[¶](#drop-a-task-owner-role)

When you delete the owner role of a task, the task transfers ownership to the role that dropped the owner role. When a task transfers ownership, it is automatically paused and new task runs aren’t scheduled until the new owner resumes the task.

If you drop the role while the task is running, the task run completes processing under the dropped role.

### Tasks run by a system service[¶](#tasks-run-by-a-system-service)

By default, tasks run as a system service that is decoupled from a user.

The system service runs the task using the same privileges as the task owner.

This avoids complications associated with user management: for example, if a user is dropped, locked due to authentication issues, or has roles removed, the task continues to run without interruption.

The query history for task runs are associated with the system service. There are no user credentials for this service, and no individual can assume its identity. Activity for the system service is limited to your account. The same encryption protections and other security protocols are built into this service as are enforced for other operations.

### Run tasks with user privileges[¶](#run-tasks-with-user-privileges)

Tasks can be configured to run with the privileges of a specific user, in addition to privileges of the task owner role. Tasks that specify EXECUTE AS USER run on behalf of the named user, instead of the system service.

- **Manage multi-role privileges** : In situations where users have secondary roles, users can run a task using the combined privileges of their primary and secondary roles. This configuration ensures that the task has the necessary permissions to access all required resources.
- **Leverage user-based data masking and row access policies** : In situations where data governance policies consider the querying user, running a task as a user ensures the task is compatible with the applicable policies.
- **Provide accountability for all operations** : All instances of a task that are run with EXECUTE AS USER are attributed to the configured user instead of the SYSTEM user. This attribution helps maintain a clear audit trail for all operations.

#### Access control[¶](#access-control)

The owner role of the task must be granted the IMPERSONATE privilege on the user specified by EXECUTE AS USER, and the specified user must be granted the owner role of the task.

When the task runs, the primary role of the task session will be the owner role of the task, and the user’s default secondary roles will be activated. Users will be able to switch primary roles with the [USE ROLE](/sql-reference/sql/use-role) command and adjust the secondary roles in the task session with the [USE SECONDARY ROLES](/sql-reference/sql/use-secondary-roles) command.

#### Share tasks by using a service user and role[¶](#share-tasks-by-using-a-service-user-and-role)

For production environments, we recommend that you create a separate service user to represent your team or business process. In contrast to running as an existing service or person user, this best practice helps make the workflow more secure:

- When a task runs as a dedicated service user, it gains access only to the intended privileges. If instead, a user impersonates a different user, they gain access to all privileges associated with the other user, which might include unintended privileges, including user privileges granted after creating and resuming the task.
- A task running as a user might be interrupted if the person leaves the department or organization.

#### Examples: Set up the service user and team role[¶](#examples-set-up-the-service-user-and-team-role)

1. 
Using the admin role, set up a service user to be used for the task. The following example creates a service user named `task_user` :
2. 
Create a task role, and then grant it to the service user:
3. 
Allow the task role to run queries on behalf of the team user role:
4. 
Grant appropriate privileges to the task role.

#### Run a task on behalf of a service user[¶](#run-a-task-on-behalf-of-a-service-user)

After the team role has ownership of the task, team members can modify the task, and run it on behalf of the service user.

**Example:**

In the previous example, the resulting logs would show that `task_user` modified the task.

#### (For testing only) Allow a user to impersonate another user directly[¶](#for-testing-only-allow-a-user-to-impersonate-another-user-directly)

When you test or prototype changes, you, as an administrator, can allow users to directly impersonate another user. This scenario, while supported, isn’t recommended in a production environment.

1. 
Set up a role for impersonation:
2. 
Create a task by using the new role:
3. 
Grant the role to another user. In the following example, the user Jane grants access to the user Billy:
4. 
The other user modifies the task. In the following example, the user Billy modifies the task:
5. 
Review the logs. The [SHOW GRANTS TO ROLE](/sql-reference/sql/show-grants) command would show that Jane granted the role to Billy. The[QUERY_HISTORY](/sql-reference/functions/query_history) view would then show that Billy modified the task. Future task runs would still appear as run by Jane.

## Task Data Definition Language (DDL) operations[¶](#task-data-definition-language-ddl-operations)

To support creating and managing tasks, Snowflake provides the following set of special DDL operations:

In addition, providers can view, grant, or revoke access to the necessary database objects for ELT using the following standard access control DDL:

[DatabaseRoleResource](/developer-guide/snowflake-python-api/reference/latest/_autosummary/snowflake.core.database_role.DatabaseRoleResource) methods:

- `grant_future_privileges`
- `grant_privileges`
- `grant_privileges_on_all`
- `grant_role`
- `iter_future_grants_to`
- `iter_grants_to`
- `revoke_future_privileges`
- `revoke_grant_option_for_future_privileges`
- `revoke_grant_option_for_privileges`
- `revoke_grant_option_for_privileges_on_all`
- `revoke_privileges`
- `revoke_privileges_on_all`
- `revoke_role`

[RoleResource](/developer-guide/snowflake-python-api/reference/latest/_autosummary/snowflake.core.role.RoleResource) (account role) methods:

- `grant_future_privileges`
- `grant_privileges`
- `grant_privileges_on_all`
- `grant_role`
- `iter_future_grants_to`
- `iter_grants_of`
- `iter_grants_on`
- `iter_grants_to`
- `revoke_future_privileges`
- `revoke_grant_option_for_future_privileges`
- `revoke_grant_option_for_privileges`
- `revoke_grant_option_for_privileges_on_all`
- `revoke_privileges`
- `revoke_privileges_on_all`
- `revoke_role`

[UserResource](/developer-guide/snowflake-python-api/reference/latest/_autosummary/snowflake.core.user.UserResource) methods:

- `grant_role`
- `iter_grants_to`
- `revoke_role`

## Task functions[¶](#task-functions)

To support retrieving information about tasks, Snowflake provides the following set of functions:

## More Python examples[¶](#more-python-examples)

For more Python examples, see [Managing Snowflake tasks and task graphs with Python](/developer-guide/snowflake-python-api/snowflake-python-managing-tasks).
