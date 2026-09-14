---
title: Introduction to replication and failover across multiple accounts¶
source: https://docs.snowflake.com/en/user-guide/account-replication-intro
corpus: snowflake-docs
section: 35-account-replication-intro
clipped: '2026-09-13'
---

# Introduction to replication and failover across multiple accounts¶

# Introduction to replication and failover across multiple accounts[¶](#introduction-to-replication-and-failover-across-multiple-accounts)

This feature enables the replication of objects from a *source* account to one or more *target* accounts in the same organization.
Replicated objects in each target account are referred to as *secondary* objects and are replicas of the *primary* objects in the source
account. Replication is supported across [regions](/user-guide/intro-regions) and across
[cloud platforms](/user-guide/intro-cloud-platforms).

## Region support for replication and failover/failback[¶](#region-support-for-replication-and-failoverfailback)

All Snowflake regions across Amazon Web Services, Google Cloud Platform, and Microsoft Azure support replication.

Customers can replicate across all regions within a [region group](/user-guide/admin-account-identifier#label-region-groups). To replicate between regions in
different region groups (that is, from a Snowflake commercial region to a Snowflake government or Virtual Private Snowflake region),
please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

## Replication groups and failover groups[¶](#replication-groups-and-failover-groups)

A *replication group* is a defined collection of objects in a source account that are replicated as a unit to one or more target accounts. Replication groups provide read-only access for the replicated objects.

A *failover group* is a replication group that can also fail over. A secondary failover group in a target account provides read-only access for the replicated objects. When a secondary failover group is promoted to become the primary failover group, read-write access is available. You can promote any target account specified in the list of allowed accounts in a failover group to serve as the primary failover group.

Replication and failover groups provide point-in-time consistency for the objects on the target account. The objects that can be included in a replication or failover group are listed below in [Replicated objects](#label-replicated-objects).

### Replication feature / edition matrix[¶](#replication-feature-edition-matrix)

Note that some replication features are only available for Business Critical Edition (or higher). The following table lists the availability of replication features for each Snowflake edition:

| Feature | Standard | Enterprise | Business Critical | VPS | 
|---|---|---|---|---|
| Database replication | ✔ | ✔ | ✔ | ✔ | 
| Share replication | ✔ | ✔ | ✔ | ✔ | 
| Replication Group | ✔ | ✔ | ✔ | ✔ | 
| Account object (other than database and share) replication |  |  | ✔ | ✔ | 
| Failover Group |  |  | ✔ | ✔ | 
| Data protected with [Tri-Secret Secure](#label-database-replication-encryption) |  |  | ✔ | ✔ | 
| [Dataset replication](#label-dataset-replication) |  |  | ✔ | ✔ | 
| [Cortex Search Service replication](#label-css-replication) |  |  | ✔ | ✔ | 

## Replicated objects[¶](#replicated-objects)

This feature supports replicating the objects listed below. Database replication and share replication are available on all editions.
Replication of all other objects is only available for Business Critical Edition (or higher). For details on feature availability,
see the [Replication feature / edition matrix](#label-account-replication-feature-availability).

| Object | Type or Feature | Replicated | Notes | 
|---|---|---|---|
| [Databases](#label-database-replication) |  | ✔ | Replication of some databases is not supported or might fail the refresh operation. For more information, see [Current limitations of replication](#label-replication-limitations) . | 
| [External volumes](#label-external-volume-replication) |  | ✔ | Failover group replication requires Business Critical Edition or higher. Replication group replication is available to all accounts. | 
| [Integrations](#label-account-replication-integrations) | Security, API, Notification, Storage, External Access | ✔ | For additional caveats and details on the supported types, see [Integration replication](#label-account-replication-integrations) . Requires Business Critical Edition (or higher). | 
| [Listings](#label-listing-replication) |  | ✔ | Requires Business Critical Edition (or higher). | 
| [Network policies](#label-network-policy-replication) |  | ✔ | Requires Business Critical Edition (or higher). | 
| [Parameters (account level)](#label-parameter-replication) |  | ✔ | Requires Business Critical Edition (or higher). | 
| [Profiles](#label-profile-replication) |  | ✔ | Requires Business Critical Edition (or higher). | 
| Programmatic access tokens for [users](#label-user-replication) |  | ✔ | If users and roles are replicated, programmatic access tokens for users are replicated automatically. | 
| [Resource monitors](#label-resource-monitor-replication) |  | ✔ | Resource monitor notifications for non-administrator users are replicated if you include `users` in the group, however account administrator notification settings are not replicated. For more information, see[Replication of resource monitor email notification settings](#label-resource-monitor-notifications-replication) . Requires Business Critical Edition (or higher). | 
| [Roles](#label-role-replication) |  | ✔ |  | 
| [Shares](#label-share-replication) |  | ✔ | Replication of [inbound shares](/user-guide/data-share-consumers) (shares from providers) is*not* supported. | 
| [Users](#label-user-replication) |  | ✔ | Requires Business Critical Edition (or higher). | 
| [Warehouses](#label-warehouse-replication) |  | ✔ | Requires Business Critical Edition (or higher). Includes [interactive warehouses](/user-guide/interactive) . | 
| [Workspaces](#label-workspace-replication) |  | ✔ | Requires Business Critical Edition (or higher). | 

### Database replication[¶](#database-replication)

Snowflake account replication supports replicating databases. Replication for a database includes the objects contained in that database. The refresh operation for a database includes changes to the objects and data since the previous refresh for that database.

If `roles` are replicated (in the same or different replication or failover group), the database refresh also synchronizes the
privilege grants on the secondary database and the objects in the database (schemas, tables, views, and so on) to roles in the account.
Refer to [Grants for database objects](#label-privileges-on-replicated-database-objects) for more details.

Replication of some databases is not supported or might fail the refresh operation. For more information, see
[Current limitations of replication](#label-replication-limitations).

#### Replicated database objects[¶](#replicated-database-objects)

When a primary database is replicated, a snapshot of its database objects and data is transferred to the secondary database. However, some database objects are not replicated. The following table indicates which database objects are replicated to a secondary database.

For specific usage information about these objects, see [Replication considerations](/user-guide/account-replication-considerations).

Note

Objects that are *not* supported for replication are skipped during replication and won’t be available in the target account after failover.

| Object | Type or Feature | Replicated | Notes | 
|---|---|---|---|
| Schemas |  | ✔ | By default, all schemas in replicated databases are replicated. If you use failover groups, you can choose which schemas within a database are replicated. For more information, see [Schema-level replication for failover groups](/user-guide/account-replication-config#label-schema-level-replication) . | 
| Tables | Permanent tables | ✔ |  | 
|  | Transient tables | ✔ |  | 
|  | Error tables | ✔ | For more information, see [DML error logging](/user-guide/data-load-overview#label-data-load-overview-dml-error-logging) . | 
|  | Temporary tables |  |  | 
|  | Automatic Clustering of clustered tables | ✔ |  | 
|  | Dynamic tables | ✔ | For more information, see [Replication and dynamic tables](/user-guide/account-replication-considerations#label-replication-and-dynamic-tables) . | 
|  | External tables |  |  | 
|  | Hybrid tables |  |  | 
|  | Apache Iceberg™ tables | ✔ | Only Snowflake-managed Iceberg tables are supported. Replication for Iceberg tables requires external volume replication. For more information, see [Configure replication for Snowflake-managed Apache Iceberg™ tables](/user-guide/tables-iceberg-replication) . | 
|  | Interactive tables | ✔ |  | 
|  | Table constraints | ✔ | Except if a foreign key in the database references a primary/unique key in another database. | 
| Event tables |  |  |  | 
| Sequences |  | ✔ |  | 
| Views | Views | ✔ | If a view references any object in another database (for example, table columns, other views, UDFs, or stages), both databases must be replicated. | 
|  | Materialized views | ✔ |  | 
|  | Secure views | ✔ |  | 
|  | Semantic views | ✔ | If a semantic view references any other objects (for example, tables, views, and Cortex Search Services), you must also replicate those objects. | 
| User-defined types |  | ✔ |  | 
| File formats |  | ✔ |  | 
| Stages | Stages | ✔ | Supported for replication and failover groups only. Not supported for database replication. For more information, see [Stage, pipe, and load history replication](/user-guide/account-replication-stages-pipes-load-history) . | 
|  | Temporary stages |  |  | 
| Pipes |  | ✔ | Supported for replication and failover groups only. Not supported for database replication. For more information, see [Stage, pipe, and load history replication](/user-guide/account-replication-stages-pipes-load-history) . | 
| Stored procedures |  | ✔ | For more information, see [Replication of stored procedures and user-defined functions (UDFs)](/user-guide/account-replication-considerations#label-replication-stored-procedures-udfs) . | 
| Streams |  | ✔ | For more information, see [Replication and streams](/user-guide/account-replication-considerations#label-replication-and-streams) . | 
| Tasks |  | ✔ | For more information, see [Replication and tasks](/user-guide/account-replication-considerations#label-replication-and-tasks) . | 
| Data metric functions (DMFs) | Data Quality | ✔ | For more information, see [Replication of data metric functions (DMFs)](/user-guide/account-replication-considerations#label-replication-data-quality) . | 
| UDFs |  | ✔ | For more information, see [Replication of stored procedures and user-defined functions (UDFs)](/user-guide/account-replication-considerations#label-replication-stored-procedures-udfs) . | 
| Policies | Aggregation policies | ✔ |  | 
|  | Authentication policies | ✔ |  | 
|  | Column-level Security (masking) | ✔ | For masking, row access, and tag-based masking policies, see [policy replication considerations](/user-guide/database-replication-considerations#label-database-replication-considerations-masking-row-policies) . | 
|  | Join policies | ✔ |  | 
|  | Password policies | ✔ |  | 
|  | Privacy policies | ✔ | For more information, see [Privacy policies](/user-guide/account-replication-considerations#label-account-replication-considerations-privacy-policy) . | 
|  | Projection policies | ✔ |  | 
|  | Row access policies | ✔ |  | 
|  | Session policies | ✔ | For session, password, and authentication policies, see [replication and security policies](/user-guide/account-replication-considerations#label-account-replication-considerations-security-policies) . | 
|  | Tag-based masking policies | ✔ |  | 
|  | Backup policies | ✔ |  | 
|  | Storage lifecycle policies | ✔ | For information about replication of policies and archived data, see [Replication and storage lifecycle policies](/user-guide/account-replication-considerations#label-replication-and-slps) . | 
| Tags | Object Tagging | ✔ | For tags, see [Replication and tags](/user-guide/account-replication-considerations#label-replication-and-tags) . | 
| Alerts |  | ✔ |  | 
| Secrets | Secrets for External API Authentication | ✔ | You can replicate secrets by using a replication group and failover group. For additional details, see [Replication and secrets](/user-guide/account-replication-considerations#label-account-replication-considerations-secrets) . | 
| Network rules |  | ✔ | For replication of network policies that use network rules, see [Replicating network policies](/user-guide/account-replication-security-integrations#label-account-replication-network-policy) . | 
| Backup sets |  | ✔ |  | 
| Class instances | CUSTOM_CLASSIFIER | ✔ | Replication is supported for instances of the [CUSTOM_CLASSIFIER](/sql-reference/classes/custom_classifier) class. Instances of all other Snowflake[classes](/sql-reference/snowflake-db-classes) are*not* replicated. For the full list of Snowflake classes, see[Available classes](/sql-reference-classes#label-available-classes) . | 
| Packages policies | Python UDF, UDTF, stored procedures | ✔ | If there is a [packages policy](/developer-guide/udf/python/packages-policy) set on the source account, in order to successfully replicate account objects, the database containing the packages policy*must* be replicated to the target account in the same or different replication or failover group. Otherwise, the refresh operation fails with a[dangling references error](/user-guide/account-replication-considerations#label-dangling-references-packages-policies) . | 
| Objects for machine learning workflows | Models | ✔ | For usage information, see [Snowflake Model Registry](/developer-guide/snowflake-ml/model-registry/overview) . | 
|  | Datasets | ✔ | For information about how replication works for Datasets, see [Dataset replication](#label-dataset-replication) . | 
|  | Online feature tables |  | Online feature tables do not support replication or cloning. | 
| Git repository clones |  | ✔ | For information about how replication works for Git repository clones, see [Git repository replication](/user-guide/account-replication-git-repositories) . For usage information for Git repository clones, see[Using a Git repository in Snowflake](/developer-guide/git/git-overview) . | 
| Snowflake Notebooks |  | ✔ | For information about how replication works for Snowflake Notebooks, see [Notebook replication](/user-guide/ui-snowsight/notebooks-replication) . | 
| dbt projects |  | ✔ | For more information, see [Replication and dbt projects](/user-guide/account-replication-considerations#label-replication-and-dbt-projects) . | 
| Cortex Knowledge Extensions (CKEs) |  | ✔ | For information about how replication works for [CKEs](/user-guide/snowflake-cortex/cortex-knowledge-extensions/cke-overview) , see[Replicate a Cortex Search Service](/user-guide/snowflake-cortex/cortex-search/cortex-search-replication) . | 

#### Database replication and encryption[¶](#database-replication-and-encryption)

Snowflake protects metadata and data sets at rest and in transit between the source and target accounts. The account
[master key](https://csrc.nist.gov/glossary/term/master_key) (AMK) encrypts the key hierarchy within the account as shown in the
[hierarchical key model](/user-guide/security-encryption-manage). Snowflake encrypts replicated data in the target account using the
account master key and the key hierarchy in the target account, regardless of whether you enable Tri-Secret Secure in the target account.

When you enable Tri-Secret Secure in the target account, Snowflake uses the composite master key and the corresponding key hierarchy in the target account to encrypt the data. Note that target accounts do not have Tri-Secret Secure enabled by default; you must enable this feature.

For more information about data encryption in Snowflake, see [Understanding end-to-end encryption in Snowflake](/user-guide/security-encryption-end-to-end).

### External volume replication[¶](#external-volume-replication)

Iceberg tables rely on external volumes, which are
account-level objects that require extra configuration to connect to your external cloud storage. Before you can replicate an Iceberg table,
you must configure replication for external volumes. Account replication supports the replication of external volumes. For more
information about replicating external volumes and Snowflake-managed Iceberg tables, see [Configure replication for Snowflake-managed Apache Iceberg™ tables](/user-guide/tables-iceberg-replication).

For more information about external volumes, see [External volume](/user-guide/tables-iceberg#label-tables-iceberg-external-volume-def).

### Integration replication[¶](#integration-replication)

Account replication supports the replication of integrations for the following features:

- 
Security integrations of the following types: 
  - Federated Authentication & SSO (that is, SAML2)
  - SCIM
  - Snowflake OAuth
  - External OAuth
 For more information about security integrations, see [Replication of security integrations & network policies across multiple accounts](/user-guide/account-replication-security-integrations) .
- 
API integrations. After replicating API integrations to a target account, you must grant access to the remote service to the replicated external functions. For more information, see [Updating the remote service for API integrations](/user-guide/account-replication-config#label-update-remote-service-for-api-integrations) .
- 
Notification integrations of the following types: 
  - TYPE = EMAIL
  - TYPE = QUEUE with DIRECTION = OUTBOUND
  - TYPE = WEBHOOK
- 
Storage integrations. When you replicate a storage integration, you must establish a new trust relationship for your cloud storage in the target accounts. To learn more, see [Configure cloud storage access for secondary storage integrations](/user-guide/account-replication-config#label-configure-cloud-storage-access-secondary-storage-integrations) .
- 
External access integrations. For more information about external access integrations, see [External network access overview](/developer-guide/external-network-access/external-network-access-overview) .

### Listing replication[¶](#listing-replication)

For listings that have auto-fulfillment enabled, this feature allows you to add the listings and (optionally) their shares to a failover group for replication and failover.

For more information, see [Listing support in Business Continuity and Disaster Recovery](/collaboration/listings-bcdr).

### Network policy replication[¶](#network-policy-replication)

The feature supports replicating network policies.

For more information, see [Replication of security integrations & network policies across multiple accounts](/user-guide/account-replication-security-integrations).

### Parameter replication[¶](#parameter-replication)

This feature supports replicating account-level parameters and object parameters. Object parameters are replicated when the object is
included in the replication group. For example, if `WAREHOUSES` are replicated, warehouse-specific parameters
(for example, [STATEMENT_TIMEOUT_IN_SECONDS](/sql-reference/parameters#label-statement-timeout-in-seconds)) are replicated. For a full list, see [Object parameters](/sql-reference/parameters#label-object-parameters).

Account-level parameter replication includes all [Account parameters](/sql-reference/parameters#label-account-parameters) and
[parameters set on the account](/user-guide/admin-account-management).
Account-level parameters (for example, [DATA_RETENTION_TIME_IN_DAYS](/sql-reference/parameters#label-data-retention-time-in-days)) are replicated when `ACCOUNT PARAMETERS` is included in
the list of object types for a replication group.

### Profile[¶](#profile)

This feature supports adding profiles to a failover group. For more information about provider profiles, see [Manage your provider profile](/collaboration/provider-profiles-managing).

### Resource monitor replication[¶](#resource-monitor-replication)

This feature supports replicating resource monitors and privileges granted on resource monitors to roles. A secondary resource monitor follows the same quota reset schedule as its primary. For example, if the quota on the primary resource monitor resets on the first of the month, and the secondary is first replicated on the 15th of the month, its quota will reset on the first of the next month along with the primary.

#### Replication of resource monitor email notification settings[¶](#replication-of-resource-monitor-email-notification-settings)

Email notification settings for resource monitors are not included with resource monitor replication. Email notifications for non-administrator users can be replicated with resource monitors. However, account administrator notification settings are currently not replicated:

- 
If `users` and`resource monitors` are included in the`object_types` list for the replication or failover group,
notification settings for non-administrator users are replicated:
  - The `notify_users` list for a warehouse-level resource monitor is replicated to target accounts.
  - [Email notifications for non-administrator users](/user-guide/resource-monitors#label-resource-monitors-enabling-nonadministrator-notifications) are sent
on the target account.
- The 
- 
If `resource monitors` is included in the`object_types` list for the replication or failover group, but`users` is not included, the`notify_users` list for a secondary warehouse-level resource monitor is empty.
- 
Account administrator notification settings are *not* replicated:
  - An account administrator must [enable email notifications](/user-guide/resource-monitors#label-enabling-notifications) in each account using the web interface.
  - Resource monitor notifications are sent to account administrators if they have enabled email notifications in the source and/or target accounts.
- An account administrator must 

### Role replication[¶](#role-replication)

This feature supports replicating roles, including role hierarchies. Role objects must be replicated to replicate access privileges.
Replicated access privileges are listed in [Replication of roles and grants](#label-replicated-privileges) below.

When you include `roles` in a replication or failover group, Snowflake also replicates the following grants on the
[SNOWFLAKE database](/sql-reference/snowflake-db) to account roles in the target account. The SNOWFLAKE database includes
both [database roles](/sql-reference/snowflake-db-roles) and application roles.

- Grants of database roles in the SNOWFLAKE database to account roles.
- Grants of application roles in the SNOWFLAKE database to account roles.
- Grants of `IMPORTED PRIVILEGES` on the SNOWFLAKE database to account roles.

The SNOWFLAKE database is a system-defined shared database that exists in every account. You don’t include it in the
`object_types` list for the group. These grants are still replicated when `roles` are replicated.

Replication of grants of database roles in the SNOWFLAKE database is additive. Grants are replicated from the source account to the target account, but revocations on the source account aren’t propagated. A grant on the target account remains in place even after the corresponding grant is revoked on the source account.

Note

All roles are replicated.

### Share replication[¶](#share-replication)

This feature supports replication of share objects as well as access privileges granted to shares on database objects.

Replication of [inbound shares](/user-guide/data-share-consumers) (shares from providers) is not supported.

### Backup replication for database, schema, and table backups[¶](#backup-replication-for-database-schema-and-table-backups)

The Snowflake [backups](/user-guide/backups) feature lets you encapsulate a series of backups for a specific database,
schema, or table inside an object known as a backup set. You can optionally control the schedule of automatic backups and
automatic deletion of backups after an expiry period by applying a backup policy to the backup set. Backup sets and
backup policies are database-level objects. Snowflake replicates those objects along with the databases and schemas that contain them.

For information about how Snowflake replicates backup sets and backup policies, see [Replicate backup-related objects](/user-guide/backups#label-replication-for-backups).

### User replication[¶](#user-replication)

This feature supports replicating users and their properties to target accounts, the following user authentication methods, and provisioning users and groups with SCIM:

| Authentication Method | Works in Target Accounts | Notes | 
|---|---|---|
| Password | ✔ |  | 
| Password with MFA (multi-factor authentication) | ✔ | Users who are enrolled in MFA in the source account must separately enroll in MFA when they log in to each target account. | 
| [Multi-factor authentication (MFA)](/user-guide/security-mfa) | ✔ | Users who are enrolled in MFA in the source account must separately enroll in MFA when they log in to each target account. | 
| [Key-pair authentication](/user-guide/key-pair-auth) | ✔ |  | 
| [Programmatic access tokens](/user-guide/programmatic-access-tokens) | ✔ | Programmatic access tokens are replicated to the target account only if users and roles are replicated. | 
| [Federated Authentication](/user-guide/admin-security-fed-auth-overview) | ✔ | Refer to [Replication of security integrations & network policies across multiple accounts](/user-guide/account-replication-security-integrations) for details on replicating federated SSO (that is, SAML2) security integrations. | 
| [Snowflake OAuth](/user-guide/oauth-snowflake-overview) | ✔ | Refer to [Replication of security integrations & network policies across multiple accounts](/user-guide/account-replication-security-integrations) for details on replicating OAuth security integrations. | 
| [External OAuth](/user-guide/oauth-ext-overview) | ✔ | Refer to [Replication of security integrations & network policies across multiple accounts](/user-guide/account-replication-security-integrations) for details on replicating OAuth security integrations. | 
| [SCIM](/user-guide/scim-intro) | ✔ | Refer to [Replication of security integrations & network policies across multiple accounts](/user-guide/account-replication-security-integrations) for details on replicating SCIM security integrations. | 

Note

If `USERS` and `ROLES` objects are replicated to a target account, these object types are read-only in the target account
and cannot be modified. Users and roles must be created in the source account, then replicated to each target account. Refer to
[Replication and read-only secondary objects](/user-guide/account-replication-considerations#label-replication-and-secondary-objects).

### Warehouse replication[¶](#warehouse-replication)

This feature supports replicating warehouses, including interactive warehouses. Snowflake also replicates privileges granted on
warehouses to roles (if `roles` are replicated).
The state of the primary warehouse is not replicated. Warehouses are replicated in the suspended state to each target account
and can be resumed in the target account.

### Workspaces replication[¶](#workspaces-replication)

[Shared workspaces](/user-guide/ui-snowsight/workspaces-shared) are replicated when they are included in a database that is part of a
replication or failover group. Private workspaces are replicated when their owning users are replicated. In secondary (target) accounts,
replicated content is read-only; Workspace files (including SQL files, Notebook files, and so on) are executable but cannot be edited.

### Dataset replication[¶](#dataset-replication)

Account replication supports replicating Datasets. Datasets are materialized data objects that you use with Snowflake ML.
For usage information, see [Snowflake Datasets](/developer-guide/snowflake-ml/dataset).
Replication is supported for Datasets created starting with the General Availability of the Dataset replication feature.
For the release announcement, see [Mar 20, 2025: Snowflake Datasets (General availability)](/release-notes/2025/other/2025-03-20-snowflake-ml-datasets).

### Cortex Search Service replication[¶](#cortex-search-service-replication)

The feature supports replicating Cortex Search Services.

For more information, see [Replicate a Cortex Search Service](/user-guide/snowflake-cortex/cortex-search/cortex-search-replication).

### Replication of roles and grants[¶](#replication-of-roles-and-grants)

In order to replicate grants on objects to roles, roles must be replicated from the source account to the target account. To
replicate roles in a replication or failover group, you must include `roles` in the `object_types` list. Roles can be in a
separate replication or failover group from the data objects on which the privileges are granted.

When `roles` are replicated, grants on objects are only replicated to a target account if:

- The privilege was granted by the owner of the object or indirectly by a role that was granted the privilege with the
[WITH GRANT OPTION](/sql-reference/sql/grant-privilege) parameter by the owner of the object.
- Both the grantee and grantor role for a privilege grant are located in the target account.
- The object is replicated (that is, the object type is included in the `object_types` list).

Otherwise the grant on the object is not replicated.

An exception applies to the [SNOWFLAKE database](/sql-reference/snowflake-db). That database exists in every account and isn’t
included in the `object_types` list. The SNOWFLAKE database includes both [database roles](/sql-reference/snowflake-db-roles)
and application roles. When `roles` are replicated, Snowflake still replicates these grants on the SNOWFLAKE database to
account roles in the target account:

- Grants of database roles in the SNOWFLAKE database to account roles.
- Grants of application roles in the SNOWFLAKE database to account roles.
- Grants of `IMPORTED PRIVILEGES` on the SNOWFLAKE database to account roles.

Replication of grants of database roles in the SNOWFLAKE database is additive. Grants are replicated from the source account to the target account, but revocations on the source account aren’t propagated. A grant on the target account remains in place even after the corresponding grant is revoked on the source account.

For information about replicating secondary roles and session policies, see [Session policies with secondary roles](/user-guide/account-replication-considerations#label-account-replication-session-policy-secondary-roles).

Note

- If a role is dropped that has the OWNERSHIP privilege on an active pipe in the target account, the refresh operation fails.
- Privileges on replication groups and failover groups are not
replicated. If the REPLICATE or FAILOVER privilege has been granted on replication groups or failover groups, these
privileges need to be granted in both the source and target accounts. Refer to [Replication privileges](/user-guide/account-replication-considerations#label-replication-privileges) for details on these privileges.

#### Grants for database objects[¶](#grants-for-database-objects)

If `roles` and `databases` are replicated to a target account (in the same or different replication or
failover group), refreshing a secondary database synchronizes the privilege grants on the database and the objects in the database
(schemas, tables, views, and so on) to existing roles in the target account (that is, roles that have been replicated to the target account).
Note that only privilege grants on objects supported by database replication are synchronized. For the list of supported objects,
see [Replicated database objects](#label-replicated-database-objects).

External tables are not currently supported for replication. As a result, privilege grants on external tables are also not replicated.

#### Future grants for objects[¶](#future-grants-for-objects)

If roles are replicated to the target account, [future grants](/user-guide/security-access-control-considerations#label-grant-management-future-grants) that are granted at the
database or schema level are replicated to the target account. This also includes future grants on non-replication supported objects. For
example, external table replication is not yet supported, however future grants on external tables are replicated.
When you create an external table in a target account, the privileges granted on future external tables materialize as intended.

#### Object creation and ownership[¶](#object-creation-and-ownership)

If new objects are created in a target account during a refresh from the source account, and roles are not replicated to the target account, the OWNERSHIP privilege for the new objects is granted to the GLOBALORGADMIN role.

If roles are replicated to the target account, the OWNERSHIP privilege is granted to the same role on the target account as the role with the OWNERSHIP privilege in the source account when roles are next replicated. The roles may be replicated at the same time the new objects are created in the target account if the objects and roles are in the same replication (or failover) group.

#### Grants for shares[¶](#grants-for-shares)

In order to enable secure data sharing, grants on objects to shares are replicated even if `roles` are not
replicated to target accounts. This section provides information on how grants on objects to shares are replicated.

If `roles` are replicated from the source account to the target account, grants to objects on shares are replicated if:

- The grantor role exists in the target account or
- The grantor role in the source account has the OWNERSHIP privilege on the primary object.

If `roles` are not replicated from the source account to the target account, then:

- Grants on objects to shares are replicated.
- The grantor role for grants on replicated objects to shares is the role with the OWNERSHIP privilege on the object.

### User who refreshes objects in a target account[¶](#user-who-refreshes-objects-in-a-target-account)

A user who executes the [ALTER FAILOVER GROUP … REFRESH](/sql-reference/sql/alter-failover-group#label-alter-failover-group) command to refresh objects in a target account
from the source account must use a role with the REPLICATE privilege on the failover group. Snowflake protects this user in the target account
by failing in the following scenarios:

- If the user does not exist in the source account, the refresh operation fails.
- If the user exists in the source account, but a role with the REPLICATE privilege was not granted to the user, the refresh operation fails.

## Replication schedule[¶](#replication-schedule)

As a best practice, Snowflake recommends scheduling automatic refreshes using the REPLICATION_SCHEDULE parameter. The schedule can be
defined when creating a new replication or failover group with CREATE *<object>* or later (using ALTER *<object>*).

When you create a secondary replication or failover group, Snowflake automatically executes an initial refresh. The next refresh is scheduled based on when the prior refresh started and the scheduling interval, or the next valid time based on the cron expression. For example, if the refresh schedule interval is 10 minutes and the prior refresh operation (either a scheduled refresh or manually triggered refresh) starts at 12:01, the next refresh is scheduled for 12:11.

Snowflake ensures only one refresh is executed at any given time. If a refresh is still executing when the next refresh is scheduled, the next refresh is delayed to start when the currently executing refresh completes. For example, if a refresh is scheduled to execute 15 minutes after the hour, every hour, and the prior refresh completes at 12:16, the next refresh is scheduled to execute when the previously executing refresh is completed.

Note

Automatically scheduled refresh operations are executed using the role with the OWNERSHIP privilege on the replication or failover group. If a scheduled refresh operation fails due to insufficient privileges, grant the required privileges to the role with the OWNERSHIP privilege on the group.

### Suspend and resume scheduled replication[¶](#suspend-and-resume-scheduled-replication)

A secondary failover group cannot be promoted to the primary group while a refresh is executing. To fail over gracefully, suspend scheduled
replication in the target account. After the failover is completed, resume the scheduled replication. For more information,
see [ALTER FAILOVER GROUP](/sql-reference/sql/alter-failover-group).

## Replication to accounts on lower editions[¶](#replication-to-accounts-on-lower-editions)

If either of the following conditions is true, Snowflake displays an error message:

- A primary replication group with only database and/or share objects is in a Business Critical (or higher) account but one or more of the accounts approved for replication are on lower editions. Business Critical Edition is intended for Snowflake accounts with extremely sensitive data.
- A primary replication or failover group with any [object types](/sql-reference/sql/create-replication-group#label-create-replication-group-object-types) is in a
Business Critical (or higher) account and a signed business associate agreement is in place to store PHI data in the account per HIPAA
and[HITRUST CSF](/user-guide/intro-cloud-platforms#label-hitrust-csf-cert) regulations. However, no such agreement is in place for one or more of the accounts
enabled for replication, regardless if they are Business Critical (or higher) accounts.

This behavior is implemented in an effort to help prevent account administrators for Business Critical (or higher) accounts from inadvertently replicating sensitive data to accounts on lower editions.

An account administrator (a user with the ACCOUNTADMIN role) or a user with a role with the
CREATE REPLICATION GROUP/CREATE FAILOVER GROUP or OWNERSHIP privilege can override this default behavior by including the
IGNORE EDITION CHECK clause when executing the CREATE *<object>* or ALTER *<object>*
statement. If IGNORE EDITION CHECK is set, the primary replication or failover group may be replicated to the specified accounts on
lower Snowflake editions in these specific scenarios.

Note

Failover groups can only be created in a Business Critical Edition (or higher) account. Therefore failover groups can only be replicated to an account that is a Business Critical Edition (or higher) account.

## Current limitations of replication[¶](#current-limitations-of-replication)

- Databases created from shares cannot be replicated.
- Refresh operations fail if the primary database includes a stream with an unsupported source object. The operation also fails if the source object for any stream has been dropped.
- Append-only streams are not supported on replicated source objects.

Note

Database replication does not work for task graphs if the graph is owned by a different role than the role that performs replication.
