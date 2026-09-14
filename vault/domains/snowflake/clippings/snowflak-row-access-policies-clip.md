---
title: Understanding row access policies
source: https://docs.snowflake.com/en/user-guide/security-row-intro
corpus: snowflake-docs
section: 25-security-row-intro
clipped: '2026-09-13'
---

# Understanding row access policies

# Understanding row access policies[¶](#understanding-row-access-policies)

This topic provides an introduction to row access policies and row-level security.

## What is Row-level Security?[¶](#what-is-row-level-security)

Snowflake supports row-level security through the use of row access policies to determine which rows to return in the query result. The row
access policy can be relatively simple to allow one particular role to view rows, or be more complex to include a
[mapping table](https://en.wikipedia.org/wiki/Associative_entity) in the policy definition to determine access to rows in the query
result. If the policy contains a mapping table lookup, create a centralized mapping table and store the mapping table in the
same database as the protected table. This is particularly important if the policy calls the
[IS_DATABASE_ROLE_IN_SESSION](/sql-reference/functions/is_database_role_in_session) function. For details, see the function usage notes.

A row access policy is a schema-level object that determines whether a given row in a table or view can be viewed from the following types of statements:

Row access policies can include conditions and functions in the policy expression to transform the data at query runtime when those conditions are met. The policy-driven approach supports segregation of duties to allow governance teams to define policies that can limit sensitive data exposure. This approach also includes the object owner (i.e. the role with the OWNERSHIP privilege on the object, such as a table or view) who normally has full access to the underlying data. A single policy can be set on different tables and views at the same time.

Row access policies do not currently prevent rows from being inserted, or prevent visible rows from being updated or deleted.

A row access policy can be added to a table or view either when the object is created or after the object is created. For more information, see [Apply a Row Access Policy to a Table or View](#apply-a-row-access-policy-to-a-table-or-view) (in this topic).

Note

In some cases, error messages related to row access policies might be redacted. For more information, see
[Secure objects: Redaction of information in error messages](/release-notes/bcr-bundles/un-bundled/bcr-1858).

### How does a row access policy work?[¶](#how-does-a-row-access-policy-work)

A row access policy contains an expression that can specify Snowflake database objects (e.g. table or view), and use
[Conditional expression functions](/sql-reference/expressions-conditional) and [Context functions](/sql-reference/functions-context) to determine which rows should be visible in a
given context.

Snowflake evaluates the policy expression by using the role of the [policy owner](/developer-guide/stored-procedure/stored-procedures-rights), not the
role of the operator who executed the query. This approach allows Snowflake not to return a row in a query result because the query
operator does not require access to the mapping tables in the row access policy.

Tip

If you want to update an existing row access policy and need to see the current definition of the policy, call the [GET_DDL](/sql-reference/functions/get_ddl) function or run the [DESCRIBE ROW ACCESS POLICY](/sql-reference/sql/desc-row-access-policy) command.

The row access policy expression can then be updated with the [ALTER ROW ACCESS POLICY](/sql-reference/sql/alter-row-access-policy) command. This command
does not require dropping a row access policy from a table or view. So, a table or view that is protected by a row access policy remains protected while the policy expression is being updated.

### Row access policies at query runtime[¶](#row-access-policies-at-query-runtime)

At query runtime, Snowflake goes through the following process:

1. Snowflake determines whether a row access policy is set on a database object. If a policy is added to the database object, all rows are protected by the policy.
2. Snowflake creates a dynamic secure view (i.e. a secure inline view) of the database object.
3. The values of the columns specified in the ALTER TABLE or ALTER VIEW command (that is, when adding a row access policy to a table or view) are bound to the corresponding parameters in the policy, and the policy expression is evaluated.
4. Snowflake generates the query output for the user, and the query output only contains rows based on the policy definition evaluating
to `TRUE` .

For more details on the specific execution plan, see [Query profile](#label-security-row-query-profile) (in this topic).

Snowflake supports nested row access policies, such as a row access policy on a table and a row access policy on a view for the same table. At query runtime, Snowflake evaluates all row access policies that are relevant to a given query in the following sequence:

- The row access policy that is applicable to the table is always executed first.
- The policy for the view is executed after evaluating the policy for the table.
- If nested views exist (e.g. Table 1 -> View 1 -> View 2 -> … View n), the policies are applied in sequential order from left to right.

This pattern continues for however many row access policies exist with respect to the data in the query. The following diagram illustrates the relationship between a query operator, tables, views, and policies.

For more information on row access policy privileges, commands, and a step-by-step implementation, see:

### Representative use case: Simple row filtering[¶](#representative-use-case-simple-row-filtering)

A simple application of a row access policy is to specify an attribute in the policy and a role that is allowed to see that attribute in the query result. The advantage of simple policies like this is that there is a negligible performance cost for Snowflake to evaluate these policies to return query results compared to using row access policies with mapping tables.

As a representative example, it may be necessary for information technology administrators (e.g. `it_admin` custom role) to query an
employee identification number (i.e. `empl_id`) before granting the employee additional privileges to use internal systems. Therefore,
the row access policy should return rows in the query result if the [CURRENT_ROLE](/sql-reference/functions/current_role) matches the `it_admin`
custom role and not return rows for all other roles. For example:

This policy is the most concise version of a row access policy because there are no other conditions to evaluate, only the value of the CURRENT_ROLE.

If role hierarchy needs to be considered, this policy could similarly use [IS_ROLE_IN_SESSION](/sql-reference/functions/is_role_in_session) to be more
inclusive of other roles to see the employee ID number in the query result.

Alternatively, to consider additional conditions, using the [CASE](/sql-reference/functions/case) function allows including WHEN/THEN/ELSE
clauses to support more detailed conditional logic.

### Representative use case: Deny row access when an agent is active[¶](#representative-use-case-deny-row-access-when-an-agent-is-active)

When an agent is active in the execution context, you can use [IS_AGENT_ACTIVATED](/sql-reference/functions/is_agent_activated) in a row
access policy to hide rows even when the user’s role would otherwise allow access. When no agent is active, only the `ANALYST` custom role
can see rows:

### Representative use case: Use a mapping table to filter the query result[¶](#representative-use-case-use-a-mapping-table-to-filter-the-query-result)

A row access policy condition can reference a mapping table to filter the query result set, however using mapping tables may result in
decreased performance compared to the more [simple](#label-security-row-simple-use-case) example.

For example, use a mapping table to determine the revenue values a sales manager can see in a specified sales region. The mapping table should specify the sales manager and the sales region (e.g. WW: Worldwide, NA: North America, EU: European Union).

Sales Manager Region Alice WW Bob NA Simon EU 

Next, define a policy with one or more conditions to query the mapping table with a subquery. At query runtime, Snowflake determines whether the user executing the query matches the sales region specified in the mapping table.

If a match occurs, the user can see those rows in the query result. Based on the mapping table, the expected query results are as follows:

Company Region Revenue Who can view Acme EU 2.5B Alice, Simon Acme NA 1.5B Alice, Bob 

For details on implementing a row access policy with a mapping table, see:

- [External Tables](#external-tables) (in this topic)
- [Use row access policies](/user-guide/security-row-using)

### Policy performance guidelines[¶](#policy-performance-guidelines)

Row access policies are designed to perform well in a wide variety of real-world scenarios. Use the following tips to secure data and enhance performance:

- Limit the policy arguments:
- Snowflake needs to scan columns that the policy is bound to, even if they are not referenced in queries. Therefore, policies with fewer arguments will generally perform better than policies with many arguments.
- Simplify the SQL expression:
- Policies with simple SQL expressions, such as CASE statements, generally perform better than policies that access mapping (i.e. lookup) tables. Minimizing the number of table lookups improves performance. When specifying a mapping table, replace the mapping table reference with a memoizable function. For details, refer to: 
  - [Memoizable function](/developer-guide/udf/sql/udf-sql-scalar-functions#label-udf-sql-scalar-memoizable) (in the scalar SQL UDF overview).
  - [Using a memoizable function in a policy](/user-guide/security-row-using#label-security-row-using-example-memoizable-function) (in the Using Row Access Policies topic).
- Test with realistic workloads:
- Without a row access policy, the query `SELECT COUNT(*) FROM t1` executes in milliseconds since Snowflake already knows the number of
rows in the table. However, adding a row access policy means Snowflake must scan the table to count the number of rows that are
accessible in the current context. Although the performance difference is large, this query is not representative of most real-world
workloads.For more information on this example, see the [Considerations](#considerations) section (in this topic).
- Cluster by attributes:
- For very large tables, clustering by attributes used for policy filtering can improve performance. For more information, see [Clustering Keys & Clustered Tables](/user-guide/tables-clustering-keys) .

- Search optimization service:
- The search optimization service can improve the query performance on a table that uses a masking or row access policy. For details, see [Support for Tables With Masking Policies and Row Access Policies in the Search Optimization Service](/user-guide/search-optimization/working-with-tables#label-search-optimization-service-masking-row-access) .

### Benefits[¶](#benefits)

The primary benefit of a row access policy is that the policy enables an organization to properly balance data security, governance, and analytics through an extensible policy. The extensible nature of the row access policy allows one or more conditions to be added or removed at any time to ensure the policy is consistent with updates to data, mapping tables, and the RBAC hierarchy.

Additional benefits include:

- Ease of Use:
- Write a policy once and apply it to tables across databases and schemas.
- Change Management:
- Easily change row access policy definitions without having to reapply the policy to tables. If using a mapping table, update the entitlement information in the mapping table referenced by the policy without having to change the policy.
- Data Administration and SoD:
- A central data administrator decides which objects to protect, not the object owner. Row access policies are easy to manage and support through centralized, decentralized, and hybrid administration models to support segregation of duties (i.e. SoD).
- Data Authorization and Governance:
- The row access policy supports contextual data access by role or custom entitlements.

### Limitations[¶](#limitations)

- 
Using the [CHANGES](/sql-reference/constructs/changes) clause on a view protected by a row access policy is not supported.
- 
Snowflake does not support using external tables as a mapping table in a row access policy. For more information, see [External Tables](#external-tables) (in this topic).
- 
Snowflake does not support attaching a row access policy to the stream object itself, but does apply the row access policy to the table when the stream accesses a table protected by a row access policy. For more information, see [Streams](#streams) (in this topic).
- 
[Future grants](/sql-reference/sql/grant-privilege#label-grant-privilege-schema-future-grants) of privileges on row access policies are not supported.As a workaround, grant the APPLY ROW ACCESS POLICY privilege to a custom role to allow that role to apply row access policies on a table or view.

### Considerations[¶](#considerations)

- 
Attaching row access policies to tables that are protected by other row access policies or masking policies may cause errors. For more information, see [ALTER TABLE](/sql-reference/sql/alter-table) ,[ALTER EXTERNAL TABLE](/sql-reference/sql/alter-external-table) , and[ALTER VIEW](/sql-reference/sql/alter-view) .
- 
Including one or more [subqueries](/user-guide/querying-subqueries) in the policy body may cause errors. When possible, limit the
number of subqueries, limit the number of JOIN operations, and simplify WHERE clause conditions.
- 
Snowflake maintains statistics about table and view columns that make it possible to answer many simple queries in milliseconds. Examples of such queries include using the [COUNT](/sql-reference/functions/count) function,`select count(*) from my_table` , and the[MAX](/sql-reference/functions/max) function,`select max(c) from my_table` .Generally, these statistics and optimizations are not applicable with a row access policy since Snowflake must identify the subset of rows the query is permitted to access. Executing queries of this type on tables and views with a row access policy may take longer than expected to obtain the query results since these statistics and optimizations are not used, and the returned statistics are only based on what is permissible to access, not the “true” statistical values (i.e. statistics on the table or view without a row access policy).
- 
Use caution when creating the setup script for a Snowflake Native App when the row access policy exists in a versioned schema. For details, see [version schema considerations](/developer-guide/native-apps/creating-setup-script#label-setup-script-versioned-schema-failures) .
- 
If you specify the [CURRENT_DATABASE](/sql-reference/functions/current_database) or[CURRENT_SCHEMA](/sql-reference/functions/current_schema) function in the
body of a masking or row access policy, the function returns the database or schema that contains the protected table, not the database or
schema in use for the session.

## Use row access policies with Snowflake objects and features[¶](#use-row-access-policies-with-snowflake-objects-and-features)

The following sections describe how row access policies affect tables and views along with other Snowflake features.

### Obtain database objects with a row access policy[¶](#obtain-database-objects-with-a-row-access-policy)

The Information Schema [POLICY_REFERENCES](/sql-reference/functions/policy_references) table function can return information about the row access policy
assigned to a given object.

- 
All objects for a given policy: Specify the name of the row access policy (e.g. `mydb.policies.rap1` ):
- 
The policy assigned to a specific object: Specify the name of the object (e.g. `mydb.tables.t1` ) and the object domain (e.g.`table` ):

Note that this table function is complementary to the Account Usage
[POLICY_REFERENCES](/sql-reference/account-usage/policy_references) view.

### Active role hierarchy & mapping tables[¶](#active-role-hierarchy-mapping-tables)

The policy conditions can evaluate the user’s active primary and secondary roles in a session directly, look up active roles in a mapping
table, or do both depending on how the policy administrator wants to write the policy. If the policy contains a mapping table lookup,
create a centralized mapping table and store the mapping table in the same database as the protected table. This is particularly important
if the policy calls the [IS_DATABASE_ROLE_IN_SESSION](/sql-reference/functions/is_database_role_in_session) function. For details, see the function
[usage notes](/sql-reference/functions/is_database_role_in_session#label-is-db-role-in-session-notes).

For these use cases, Snowflake recommends writing the policy conditions to call the [IS_ROLE_IN_SESSION](/sql-reference/functions/is_role_in_session) or
the [IS_DATABASE_ROLE_IN_SESSION](/sql-reference/functions/is_database_role_in_session) function depending on whether you want to specify an account role or
database role. For examples, see:

- [Examples](/sql-reference/functions/is_role_in_session#label-is-role-in-session-examples) section in the IS_ROLE_IN_SESSION function.
- IS_DATABASE_ROLE_IN_SESSION
- [Share data protected by a policy](/user-guide/data-sharing-policy-protected-data)

### Apply a row access policy to a table or view[¶](#apply-a-row-access-policy-to-a-table-or-view)

There are two options to add a row access policy to a table or view:

1. With a new table or view, apply the policy to a table with a [CREATE TABLE](/sql-reference/sql/create-table) statement or a view with a[CREATE VIEW](/sql-reference/sql/create-view) statement.
2. With an existing table or view, apply the policy to a table with an [ALTER TABLE](/sql-reference/sql/alter-table) statement or a view
with an[ALTER VIEW](/sql-reference/sql/alter-view) statement.

For a new table or view, execute the following statements:

For an existing table or view, execute the following statements:

### Masking policies[¶](#masking-policies)

When a database object has both a row access policy and one or more [masking policies](/user-guide/security-column-intro),
Snowflake evaluates the row access policy first.

A given table or view column can be specified in either a row access policy signature or a masking policy signature. In other words, the same column cannot be specified in both a row access policy signature and a masking policy signature at the same time.

For more information, see [CREATE MASKING POLICY](/sql-reference/sql/create-masking-policy) and [CREATE ROW ACCESS POLICY](/sql-reference/sql/create-row-access-policy).

### Simulate how a policy will work[¶](#simulate-how-a-policy-will-work)

Call the [POLICY_CONTEXT](/sql-reference/functions/policy_context) function to simulate a query on a column that is protected by a masking policy,
a table or view protected by a row access policy, or both types of policies. You can also simulate
[SYS_CONTEXT](/sql-reference/functions/sys_context) namespace values, such as activated roles and agent types.

### External tables[¶](#external-tables)

You can create an external table with a row access policy by executing a [CREATE EXTERNAL TABLE](/sql-reference/sql/create-external-table) statement and
apply the policy to the VALUE column.

You can apply the row access policy to the VALUE column of an existing external table by executing an [ALTER TABLE](/sql-reference/sql/alter-table)
statement on the external table.

A row access policy cannot be added to a virtual column directly. Instead, create a view on the external table and apply the row access policy to the columns on the view.

Important

Snowflake does not support using an external table as a mapping table in a row access policy. While cloning a database, Snowflake clones the row access policy, but not the external table. Therefore, the policy in the cloned database refers to a table that is not present in the cloned database.

If the data in the external table is necessary for the row access policy, consider moving the external table data to a dedicated schema within the database in which the row access policy exists prior to completing a clone operation. Update the row access policy to reference the fully qualified table name to ensure the policy refers to a table in the cloned database.

### Streams[¶](#streams)

If a row access policy is added to a table, Snowflake applies the row access policy to the table data when the stream accesses the table data.

For masking policies, streams use the latest table version available at the query time for any tables referenced in the policy.

For more information, see [Limitations](#label-security-row-limitations).

### Views[¶](#views)

Snowflake supports setting row access policies on the base table and view. The base table or view policy can apply to the view owner (i.e.
[INVOKER_ROLE](/sql-reference/functions/invoker_role)) or the query operator role (i.e. [CURRENT_ROLE](/sql-reference/functions/current_role)).

For more information, see [Limitations](#label-security-row-limitations).

### Materialized views[¶](#materialized-views)

Snowflake supports adding a row access policy to a materialized view provided that a row access policy is not set on the underlying table or view.

Row access policies and materialized views do have the following limitations:

- A materialized view cannot be created from a table if a row access policy is added to the underlying table.
- A row access policy cannot be added to a table if a materialized view has been created from that underlying table.

Tip

If you prefer to set a row access policy on the base table, consider creating a dynamic table from the base table. For more
information, see [Masking and row access policies](/user-guide/dynamic-tables/supported-queries#label-dynamic-tables-limits-incremental-refresh-features).

### Dynamic tables[¶](#dynamic-tables)

You can create a dynamic table with a row access policy, masking policy, and tag. For more information, see:

### CREATE TABLE statements[¶](#create-table-statements)

The following summarizes how row access policies affect [CREATE TABLE](/sql-reference/sql/create-table) statements:

- CREATE TABLE … CLONE:
- The following approach helps to safeguard data from users with the SELECT privilege on the table or view when accessing a cloned object: 
  - Cloning an individual policy object is not supported.
  - Cloning a schema results in the cloning of all policies within the schema.
  - A cloned table maps to the same policies as the source table. In other words, if a policy is set on the base table or its columns, the
policy is attached to the cloned table or its columns.
    - If a table or view exists in the source schema/database and has references to policies in the same schema/database, the cloned table or view is mapped to the corresponding cloned policy (in the target schema/database) instead of the policy in the source schema/database.
    - If the source table refers to a policy in a different schema (i.e. a foreign reference), then the cloned table retains the foreign reference.
 For more information, see [CREATE <object> … CLONE](/sql-reference/sql/create-clone) .
- CREATE TABLE … LIKE:
- If a row access policy is set on the base table, the row access policy is not set on a column in the new table. The new table is empty.
- CREATE TABLE … AS SELECT:
- If a row access policy is set on the base table, the new table contains the filtered rows based on the row access policy definition. The new table does not have a row access policy set on a column.

### Query profile[¶](#query-profile)

At query runtime, Snowflake creates a [dynamic secure view](#label-security-row-work).

When using the [EXPLAIN](/sql-reference/sql/explain) command on a database object in which a row access policy is set, the query result
indicates that a row access policy is present. When a row access policy is set on the database object, the EXPLAIN query result specifies
the following column values:

- The `operation` column includes the value`DynamicSecureView` .
- The `object` column includes the value`"<object_name> (+ RowAccessPolicy)"` .

Each step in the query plan that requires invoking the row access policy results in the `operation` and `object` columns specifying the
corresponding values for that step in the query plan. If the row access policy was invoked only once in the query, only one row in the
EXPLAIN query result includes the `DynamicSecureView` and `"<object_name> (+ RowAccessPolicy)"` values.

In the EXPLAIN command result and the [Query History](/user-guide/ui-snowsight-activity) page, Snowflake does not show users any
row access policy [information](/sql-reference/sql/create-row-access-policy) (i.e. policy name, policy signature, policy expression) or
the objects accessed by the policy.

The following example indicates a row access policy being invoked only once.

The following example indicates a row access policy being invoked twice on the same table:

### Time Travel[¶](#time-travel)

Snowflake supports time travel on tables and views with a row access policy.

At query run time, Snowflake evaluates the row access policy’s mapping tables at the time of the query; in other words, time travel does not affect the mapping table.

For more information, see [Understanding & using Time Travel](/user-guide/data-time-travel).

### Replication[¶](#replication)

Row access policies and their assignments can be replicated using database replication and replication groups.

For [database replication](/user-guide/database-replication-considerations), the replication operation fails if either of the
following conditions is true:

- The primary database is in an Enterprise (or higher) account and contains a policy but one or more of the accounts approved for replication are on lower editions.
- A table or view contained in the primary database has a [dangling reference](/user-guide/database-replication-considerations#label-database-replication-dangling-references) to a
row access policy in another database.

The dangling reference behavior for database replication can be avoided when replicating multiple databases in a
[replication group](/user-guide/account-replication-intro#label-replication-and-failover-groups).

Note

If using failover or failback actions, the Snowflake account must be Business Critical Edition or higher.

For more information, see [Introduction to replication and failover across multiple accounts](/user-guide/account-replication-intro).

### Data Sharing[¶](#data-sharing)

- Usage:
  - 
If the provider assigns a policy to a shared table or view and the policy conditions call the [CURRENT_ROLE](/sql-reference/functions/current_role) or[CURRENT_USER](/sql-reference/functions/current_user) function, or the policy conditions call a[secure UDF](/developer-guide/secure-udf-procedure) , Snowflake returns a NULL value for the function or the UDF in the consumer account.The reason is that the owner of the data being shared does not typically control the users or roles in the account in which the table or view is being shared. As a workaround, use the [CURRENT_ACCOUNT](/sql-reference/functions/current_account) function in the policy conditions.Alternatively, as a provider, write the policy conditions to call the [IS_DATABASE_ROLE_IN_SESSION](/sql-reference/functions/is_database_role_in_session) function and share the database role. As a consumer, grant the shared database role to an account role. For details, see[Share data protected by a policy](/user-guide/data-sharing-policy-protected-data) .
- 
- Limitations:
  - 
A data sharing provider cannot create a policy in a [reader account](data-sharing-reader-create) .
  - 
Data sharing consumers cannot apply a policy to a shared table or view. As a workaround, import the shared database and create a local view from the shared table or view.
  - 
Data sharing consumers cannot query a shared table or view that references two different providers. For example: 
    - `rap1` is a row access policy that protects the table named`t1` , where`t1` is in the share named`share1` from a provider.
    - The `rap1` policy conditions reference a mapping table named`t2` , where`t2` comes from`share2` and a different provider.
    - The consumer query on `t1` fails.
    - The provider for `t1` can query`t1` .
  - 
External functions: Snowflake returns an error if: 
    - The policy assigned to a shared table or view is updated to call an external function.
    - The policy calls an external function and you attempt to assign the policy to a shared table or view.
- 

### Snowflake Native App Framework[¶](#snowflake-native-app-framework)

For details about using row access policies with a Snowflake Native App, see:

- [Restrictions on sharing data content that contains policies](/developer-guide/native-apps/preparing-data-content#label-native-apps-share-policy-protected-data) .
- [Define policies on proxy views](/developer-guide/native-apps/preparing-data-content#label-native-apps-policies-proxy-views) .
- [Blocked context functions](/developer-guide/native-apps/redacted-content#label-native-apps-context-function-limitations) .

### Streamlit in Snowflake[¶](#streamlit-in-snowflake)

Row access policies that are used in Streamlit in Snowflake apps have limitations with context functions in the body of a row access policy. For more information, see:

- [Context functions and row access policies in Streamlit in Snowflake](/developer-guide/streamlit/features/row-access#label-streamlit-context-functions)
- [Example: Access data in a table with row access policy using CURRENT_USER](/developer-guide/streamlit/features/row-access#label-streamlit-context-functions-example)

## Enforce row access policies on Apache Iceberg tables queried from Apache Spark™[¶](#enforce-row-access-policies-on-apache-iceberg-tables-queried-from-apache-spark)

Snowflake supports enforcing row access policies that are set on Apache Iceberg tables that you query from Apache Spark™ through
Snowflake Horizon Catalog. For more information,
see [Enforce data protection policies on Apache Iceberg™ tables from external query engines](/user-guide/tables-iceberg-query-using-external-query-engine-snowflake-horizon-enforce-access-policies).

## Manage row access policies[¶](#manage-row-access-policies)

### Choosing a centralized, hybrid, or decentralized management approach[¶](#choosing-a-centralized-hybrid-or-decentralized-management-approach)

To manage row access policies effectively, it is helpful to consider whether your approach to filtering rows should follow a centralized, decentralized, or hybrid governance approach.

The following table summarizes some of the considerations with each of these three approaches.

| Policy Action | Centralized | Hybrid | Decentralized | 
|---|---|---|---|
| Create policies | Governance officer | Governance officer | Individual teams | 
| Apply policies to columns | Governance officer | Individual teams | Individual teams | 

For syntax examples, see [Summary of DDL commands, operations, and privileges](#label-security-row-privilege-command-summary).

Tip

As a best practice, Snowflake recommends that your organization gathers all relevant stakeholders to determine the best management approach for implementing row access policies in your environment.

### Row access policy privileges[¶](#row-access-policy-privileges)

Snowflake supports the following row access policy privileges to determine whether users can create, set, and own row access policies.

Operating on an object in a schema requires at least one privilege on the parent database and at least one privilege on the parent schema.

| Privilege | Usage | 
|---|---|
| APPLY | Enables executing the add and drop operations for the [row access policy](/user-guide/security-row-intro) on a table or view. Note that granting the global APPLY ROW ACCESS POLICY privilege (i.e. APPLY ROW ACCESS POLICY on ACCOUNT) enables executing the DESCRIBE operation on tables and views. For syntax examples, see [Summary of DDL commands, operations, and privileges](#label-security-row-privilege-command-summary) . | 
| OWNERSHIP | Grants full control over the row access policy. Required to alter most properties of a row access policy. Only a single role can hold this privilege on a specific object at a time. | 

### Row access policy DDL[¶](#row-access-policy-ddl)

Snowflake supports the following DDL commands and operations to manage row access policies:

- [CREATE ROW ACCESS POLICY](/sql-reference/sql/create-row-access-policy)
- [ALTER ROW ACCESS POLICY](/sql-reference/sql/alter-row-access-policy)
- [DROP ROW ACCESS POLICY](/sql-reference/sql/drop-row-access-policy)
- [SHOW ROW ACCESS POLICIES](/sql-reference/sql/show-row-access-policies)
- [DESCRIBE ROW ACCESS POLICY](/sql-reference/sql/desc-row-access-policy)
- [ALTER TABLE](/sql-reference/sql/alter-table) ,[ALTER EXTERNAL TABLE](/sql-reference/sql/alter-external-table) , and[ALTER VIEW](/sql-reference/sql/alter-view) (to add/drop a policy on a table or view)

### Summary of DDL commands, operations, and privileges[¶](#summary-of-ddl-commands-operations-and-privileges)

The following table summarizes the relationship between the row access policy DDL operations and their necessary privileges.

Operating on an object in a schema requires at least one privilege on the parent database and at least one privilege on the parent schema.

| Operation | Privilege required | 
|---|---|
| Create row access policy | A role with the CREATE ROW ACCESS POLICY privilege in the same schema. | 
| Alter row access policy | The role with the OWNERSHIP privilege on the row access policy. | 
| row access policy*Add/Drop* | A role with the APPLY ROW ACCESS POLICY privilege on the account or a role with the OWNERSHIP privilege on the database object and the APPLY privilege on the row access policy object. | 
| Drop row access policy | One of the following: A role with the OWNERSHIP privilege on the row access policy or A role with the OWNERSHIP privilege on the schema in which the row access policy exists. | 
| Show row access policies | One of the following: A role with the APPLY ROW ACCESS POLICY privilege, or The OWNERSHIP privilege on the row access policy, or The APPLY privilege on the row access policy. | 
| Describe row access policy | One of the following: A role with the APPLY ROW ACCESS POLICY privilege, or The OWNERSHIP privilege on the row access policy, or The APPLY privilege on the row access policy. | 

Snowflake supports different permissions to create and set a row access policy on an object.

1. 
For a centralized row access policy management approach, in which the `rap_admin` custom role creates and sets row access policies on
all objects, the following permissions are necessary:
2. 
In a hybrid management approach, a single role has the CREATE ROW ACCESS POLICY privilege to ensure consistent policy creation to optimize query performance and individual teams or roles have the APPLY privilege for a specific row access policy to protect their tables and views. For example, the custom role `finance_role` role can be granted the permission to add the row access policy`rap_finance` on tables
and views the role owns:

## Monitor row access policies with SQL[¶](#monitor-row-access-policies-with-sql)

You can monitor row access policy usage through two different Account Usage views and an Information Schema table.

It can be helpful to think of two general approaches to determine how to monitor row access policy usage.

### Discover row access policies[¶](#discover-row-access-policies)

You can use the [ROW_ACCESS_POLICIES](/sql-reference/account-usage/row_access_policies) view in the Account Usage schema of the
shared SNOWFLAKE database. This view is a *catalog* for all row access policies in your Snowflake account. For example:

### Identify assignments[¶](#identify-assignments)

Snowflake supports different options to identify row access policy assignments, depending on whether the query needs to target the account or a specific database.

- 
Account-level query: Use the Account Usage [POLICY_REFERENCES](/sql-reference/account-usage/policy_references) view to determine all of the tables
that have a row access policy. For example:
- 
Database-level query: Every Snowflake database includes a [Snowflake Information Schema](/sql-reference/info-schema) . Use the Information Schema table function[POLICY_REFERENCES](/sql-reference/functions/policy_references) to determine all of the objects associated with a specific row access policy:

## Monitor row access policies with Snowsight[¶](#monitor-row-access-policies-with-snowsight)

You can use the Snowsight **Governance & security** » **Tags & policies** area to monitor and report on the usage of
policies and tags with tables, views, and columns. There are two different interfaces: **Dashboard** and **Tagged Objects**.

When using the **Dashboard** and the **Tagged Objects** interface, note the following details.

- The **Dashboard** and**Tagged Objects** interfaces require a running warehouse.
- Snowsight updates the **Dashboard** every 12 hours.
- The **Tagged Objects** information latency can be up to two hours and returns up to 1000 objects.

# Accessing the Governance area in Snowsight[¶](#accessing-the-governance-area-in-snowsight)

To access the **Tags & policies** area, your Snowflake account must be [Enterprise Edition or higher](/user-guide/intro-editions).
Additionally, you must do either of the following:

- 
Use the ACCOUNTADMIN role.
- 
Use an account role that is directly granted the GOVERNANCE_VIEWER and OBJECT_VIEWER database roles. You must use an account role with these database role grants. Currently, Snowsight does not evaluate role hierarchies and user-defined database roles that have access to tables, views, data access policies, and tags. To determine if your account role is granted these two database roles, use a [SHOW GRANTS](/sql-reference/sql/show-grants) command:If your account role is not granted either or both of these database roles, use the [GRANT DATABASE ROLE](/sql-reference/sql/grant-database-role) command
and run the SHOW GRANTS command again to confirm the grants:For details about these database roles, see [SNOWFLAKE database roles](/sql-reference/snowflake-db-roles) .

## Dashboard[¶](#dashboard)

As a data administrator, you can use the **Dashboard** interface to monitor tag and policy usage in the following ways.

- Coverage: specifies the count and percentage based on whether a table, view, or column has a policy or tag.
- Prevalence: lists and counts the most frequently used policies and tags.

The coverage and prevalence provide a snapshot as to how well the data is protected and tagged.

When you select a count number, percentage, policy name, or tag name, the **Tagged Objects** interface opens. The **Tagged Objects**
interface updates the filters automatically based on your selection in the **Dashboard**.

The monitoring information is an alternative or complement to running complex and query-intensive operations on multiple Account Usage views.

These views might include, but are not limited to, the [COLUMNS](/sql-reference/account-usage/columns),
[POLICY_REFERENCES](/sql-reference/account-usage/policy_references), [TABLES](/sql-reference/account-usage/tables),
[TAG_REFERENCES](/sql-reference/account-usage/tag_references), and [VIEWS](/sql-reference/account-usage/views) views.

## Tagged Objects[¶](#tagged-objects)

As a data administrator, you can use this table to associate the coverage and prevalence in the **Dashboard** to a list of specific
tables, view, or columns quickly. You can also filter the table results manually as follows.

- Choose **Tables** or**Columns** .
- For tags, you can filter with tags, without tags, or by a specific tag.
- For policies, you can filter with policies, without policies, or by a specific policy.

When you select a row in the table, the **Table Details** or **Columns** tab in **Catalog** » **Database Explorer** opens. You can edit
the tag and policy assignments as needed.

## Audit row access policies[¶](#audit-row-access-policies)

Snowflake supports the following approaches to facilitate row access policy auditing and governance operations.

- 
Use [SHOW ROW ACCESS POLICIES](/sql-reference/sql/show-row-access-policies) to produce a list of row access policies that have not been dropped from your
account.
- 
Row access policy administrators (i.e. users with the row access policy [OWNERSHIP privilege](#label-security-row-privileges) ) can
use[Time Travel](/user-guide/data-time-travel) or[streams](/user-guide/streams-intro) to capture historical data about any
mapping tables referenced in their row access policies.
- 
To determine the data a given user can access, the row access policy administrator can assume the role of the user and run a query. 
  - Snowflake supports defining a row access policy *expression*
[CREATE ROW ACCESS POLICY](/sql-reference/sql/create-row-access-policy) command.
  - Snowflake does not currently have a default mechanism (e.g. a dedicated system or context function) to support this operation.
- Snowflake supports defining a row access policy 
- 
If a given row access policy uses mapping tables to determine which role and user populations can access row data, the row access policy owner can query the mapping tables to determine authorized user access on demand.
- 
Snowflake captures and logs error message information related to row access policies in the account usage [QUERY_HISTORY view](/sql-reference/account-usage/query_history) view. If an error occurs in a query, Snowflake records the first error message that
occurs during the query evaluation. For more information on row access policy error messages, see[Troubleshoot Row Access Policies](#troubleshoot-row-access-policies) .
- 
To determine the data a given user accessed in the past as it relates to row access policies on database objects, use Time Travel in combination with the ROW_ACCESS_POLICIES Account Usage view and the POLICY_REFERENCES Information Schema table function. 
  - If the policy and mapping tables, if present, have not changed, the row access policy administrator can assume the role of the user and
run a Time Travel query. The values of relevant session parameters, such as [CURRENT_ROLE](/sql-reference/functions/current_role) , are available
in the query result.
  - If the policy or mapping tables have changed, the row access policy administrator must run a time travel query on the mapping table and reconstruct the row access policy that existed at the specified incident time. After those steps, the row access policy administrator can begin to query the data and proceed with their analysis.
- If the policy and mapping tables, if present, have not changed, the row access policy administrator can assume the role of the user and
run a Time Travel query. The values of relevant session parameters, such as 

## Troubleshoot row access policies[¶](#troubleshoot-row-access-policies)

The following behaviors and error messages apply to row access policies.

| Behavior | Error Message | Troubleshooting Action | 
|---|---|---|
| Cannot set a row access policy (Materialized view). | Row access policy cannot be attached to a Materialized view. | Verify that a row access policy can be set on the materialized view. See [Materialized Views](#materialized-views) (in this topic). | 
| Cannot create a row access policy (Boolean). | `003551=SQL compilation error:` Row access policy return type ‘’{0}’’ is not BOOLEAN. | A row access policy definition must have `{RETURNS BOOLEAN}` . Rewrite the row access policy as shown in[CREATE ROW ACCESS POLICY](/sql-reference/sql/create-row-access-policy) . | 
| Cannot create a row access policy (Database). | This session does not have a current database. Call ‘USE DATABASE’, or use a qualified name. | Since a row access policy is a schema-level object, define a database and schema for the current session or use the fully qualified name in the CREATE ROW ACCESS POLICY command. For more information, see [Object name resolution](/sql-reference/name-resolution) . | 
| Cannot create a row access policy (Object exists) | SQL compilation error: Object ‘<name>’ already exists. | Since a row access policy in the schema already exists with the stated name, recreate the row access policy with a different value.*name* | 
| Cannot create a row access policy (Schema ownership). | SQL access control error: Insufficient privileges to operate on schema ‘S1’ | Verify the privileges to create a row access policy in [Summary of DDL Commands, Operations, and Privileges](#summary-of-ddl-commands-operations-and-privileges) (in this topic). | 
| Cannot create a row access policy (Schema usage). | SQL compilation error: Schema ‘<schema_name>’ does not exist or not authorized. | Verify that the specified schema exists and the privileges to create a row access policy in [Summary of DDL Commands, Operations, and Privileges](#summary-of-ddl-commands-operations-and-privileges) (in this topic). | 
| Cannot describe a row access policy (Usage only). | SQL compilation error: Row access policy ‘RLS_AUTHZ_DB.S_B.P1’ does not exist or not authorized. | Having the USAGE privilege on the parent database and schema in which the row access policy exists is not sufficient to execute a DESCRIBE operation on the row access policy. Verify the row access policy exists and the privileges to describe a row access policy in [Summary of DDL Commands, Operations, and Privileges](#summary-of-ddl-commands-operations-and-privileges) (in this topic). | 
| Cannot drop a row access policy. (Maintenance). | SQL compilation error: Row access policy ‘RLS_AUTHZ_DB.S_B.P1’ does not exist or not authorized. | Verify the specified row access policy exists and the privileges to drop a row access policy in [Summary of DDL Commands, Operations, and Privileges](#summary-of-ddl-commands-operations-and-privileges) (in this topic). | 
| Cannot execute `UNDROP` on a row access policy. (Maintenance) | Unsupported feature ‘UNDROP not supported for objects of type ROW_ACCESS_POLICY’. | To reinstate a row access policy, execute a CREATE ROW ACCESS POLICY command, and then add the row access policy to a database object using an ALTER TABLE or ALTER VIEW command as shown in [ALTER TABLE](/sql-reference/sql/alter-table) or[ALTER VIEW](/sql-reference/sql/alter-view) . | 
| Cannot update a row access policy (Name/Operation). | SQL compilation error: Object found is of type ‘ROW_ACCESS_POLICY’, not specified type ‘MASKING_POLICY’ | Double-check the query to verify the name of the object and the intended operation on the object. For example, Snowflake does not support `ALTER ROW ACCESS POLICY <name>;` .Instead, use a CREATE OR REPLACE ROW ACCESS POLICY command to update a row access policy. For more information on row access policy operations, see [Summary of DDL Commands, Operations, and Privileges](#summary-of-ddl-commands-operations-and-privileges) (in this topic). | 
| Cannot use row access policies with a Snowflake feature or service (Unsupported feature). | Unsupported feature ‘CREATE ON OBJECTS ENFORCED BY ROW ACCESS POLICY’. | Some Snowflake features and services do not support row access policies. For more information, see the [Limitations](#label-security-row-limitations) and[Use Row Access Policies with Snowflake Objects and Features](#use-row-access-policies-with-snowflake-objects-and-features) sections in this topic. | 
| Cannot update a row access policy (Unsupported token). | Unsupported feature ‘TOK_ROW_ACCESS_POLICY’. | `TOK` refers to token, which can be returned if a query is unsupported and/or inaccurate; Snowflake’s SQL compiler does not know how to process the given query.For example `alter row access policy p1_test set comment = 'test policy 1';` . In this example, the`ALTER` command cannot be used on the policy object directly; use an ALTER TABLE or ALTER VIEW command instead as shown in[Summary of DDL Commands, Operations, and Privileges](#summary-of-ddl-commands-operations-and-privileges) (in this topic). | 

**Next Topics:**
