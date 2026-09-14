---
title: Overview of Access Control¶
source: https://docs.snowflake.com/en/user-guide/security-access-control-overview
corpus: snowflake-docs
section: 24-security-access-control-overview
clipped: '2026-09-13'
---

# Overview of Access Control¶

# Overview of Access Control[¶](#overview-of-access-control)

This topic provides information on the main access control topics in Snowflake.

## Access control framework[¶](#access-control-framework)

Snowflake’s approach to access control combines aspects from the following models:

- **Discretionary Access Control (DAC):** Each object has an owner, who can in turn grant access to that object.
- **Role-based Access Control (RBAC):** Access privileges are assigned to roles, which are in turn assigned to users.
- **User-based Access Control (UBAC):** Access privileges are assigned directly to users. Access control considers privileges assigned
directly to users only when USE SECONDARY ROLE is set to ALL.

For more information about secondary roles, see [USE SECONDARY ROLES](/sql-reference/sql/use-secondary-roles) and [Authorization through primary role and secondary roles](#label-access-control-role-enforcement).

Several concepts key to understanding access control in Snowflake include:

- **Securable object:** An entity to which access can be granted. Unless allowed by a grant, access is denied.
- **Role:** An entity to which privileges can be granted.
- **Privilege:** A defined level of access to an object. Multiple distinct privileges may be used to control the granularity of access
granted.
- **User:** A user identity recognized by Snowflake, whether associated with a person or service. A user is also an entity to which
privileges can be granted.

In Snowflake, privileges assigned to roles or users allow access to securable objects. Roles can be assigned to users or
other roles. Granting a role to another role creates a role hierarchy, further described in
[Role hierarchy and privilege inheritance](#label-role-hierarchy-and-privilege-inheritance). Usually, you use RBAC to manage access to securable objects in Snowflake.

The following diagram illustrates how DAC, RBAC, and UBAC support appropriate privilege assignment on different securable objects. In this example, Role 1 has the OWNERSHIP privilege on both Object 1 and Object 2. In other words, Role 1 owns both objects. This illustrates DAC.

Privileges on Object 1 can be granted to Role 2, which can then be granted to User 1 and User 2. In other words, User 1 and User 2 have access to Object 1, limited by these privileges, because both users are assigned Role 2. This part of the figure illustrates RBAC.

Privileges on Object 2 can be granted directly to User 3 and User 4. This part of the figure illustrates how you can use UBAC to extend the Snowflake access control framework, providing a significant amount of both control and flexibility.

## Securable objects[¶](#securable-objects)

Every securable object resides within a logical container in a hierarchy of containers. The top-most container is the customer organization. Securable objects such as tables, views, functions, and stages are contained in a schema object, which are in turn contained in a database. All databases for your Snowflake account are contained in the account object. This hierarchy of objects and containers is illustrated below:

To *own* an object means that a [role](#label-access-control-overview-roles) has the OWNERSHIP
[privilege](#label-access-control-overview-privileges) on the object. Each securable object is owned by a single role, which by
default is the role used to create the object. When this role is assigned to users, they effectively have shared control over the object.
The [GRANT OWNERSHIP](/sql-reference/sql/grant-ownership) command lets you transfer the ownership of an object from one role to another role, including
to database roles. This command also specifies the securable objects in each container.

In a regular schema, the owner role has all privileges on the object by default, including the ability to grant or revoke privileges on the
object to other roles. In addition, ownership can be transferred from one role to another. However, in a
[managed access schema](/user-guide/security-access-control-configure#label-managed-access-schemas), object owners lose the ability to make grant decisions. Only the schema owner
(the role with the OWNERSHIP privilege on the schema) or a role with the MANAGE GRANTS privilege can grant privileges on objects in
the schema.

The ability to perform SQL actions on objects is defined by the privileges granted to the
[active role](#label-access-control-overview-active-roles) in a user session. For example, if the active role in your session has been
granted CREATE, USAGE, SELECT, and WRITE privileges in a specific Snowflake database schema, then you can create a warehouse, list tables
contained, and add data to a table in that schema.

## Roles[¶](#roles)

Roles are the entities to which [privileges](#label-access-control-overview-privileges) on securable objects can be granted and
revoked. Roles are assigned to users to allow them to perform actions required for business functions in their organization. A user can be
assigned multiple roles. This allows users to switch roles (that is, choose which role is active in the current Snowflake session) to perform
different actions using separate sets of privileges.

There are a small number of [system-defined roles](#label-access-control-overview-roles-system)
in a Snowflake account. System-defined roles cannot be dropped. In addition, the privileges granted
to these roles by Snowflake cannot be revoked.

Users who have been granted a role with the necessary privileges can create [custom roles](#label-access-control-overview-roles-custom)
to meet specific business and security needs.

Roles can be also granted to other roles, creating a hierarchy of roles. The privileges associated with a role are inherited by any roles
above that role in the hierarchy. For more information about role hierarchies and privilege inheritance, see
[Role Hierarchy and Privilege Inheritance](#role-hierarchy-and-privilege-inheritance).

Note

A role owner (the role that has the OWNERSHIP privilege on the role) does not inherit the privileges of the owned role. Privilege inheritance is only possible within a role hierarchy.

Although additional privileges can be granted to the system-defined roles, it is not recommended. System-defined roles are created with privileges related to account-management. As a best practice, it is not recommended to mix account-management privileges and entity-specific privileges in the same role. If additional privileges are needed, Snowflake recommends granting the additional privileges to a custom role and assigning the custom role to the system-defined role.

Tip

You can use organization user groups to implement consistent roles across accounts within an organization. For more information, see
[Organization users](/user-guide/organization-users).

### Types of roles[¶](#types-of-roles)

The following role types vary in their scope, which enable administrators to authorize and restrict access to objects in your account.

Note

Except where noted in the product documentation, the term *role* refers to either type.

- Account roles:
- To permit SQL actions on any object in your account, grant privileges on the object to an account role.
- Database roles:
- To limit SQL actions to a single database, as well as any object in the database, grant privileges on the object to a database role in the same database. Note that database roles cannot be [activated](#label-access-control-overview-active-roles) directly in a session. Grant database
roles to account roles, which can be activated in a session.For more information about database roles, see:
- Instance roles:
- To permit access to an instance of a [class](/sql-reference/snowflake-db-classes) , grant an instance role to
an account role.A class may have one or more class roles with different privileges granted to each role. When an instance of a class is created, the instance role(s) can be granted to account roles to grant access to instance methods. Note that instance roles cannot be [activated](#label-access-control-overview-active-roles) directly in a session. Grant instance
roles to account roles, which can be activated in a session.For more information, see [Instance roles](/sql-reference/snowflake-db-classes#label-instance-roles) .

- Application roles:
- To enable consumer access to objects in a Snowflake Native App, the provider creates the application role and grants privileges to the application role in the [set up script](/developer-guide/native-apps/creating-setup-script) .

- System application roles:
- To support specific functionality for a particular feature, such as granting access to objects in which Snowflake is the owner, Snowflake can provide one or more *system application roles* . You can grant the system application roles to account roles at your
discretion.System application roles are discussed in the context of a specific feature because that specific feature is the only place where you can use the system application role(s). For example: 
  - Budgets: [Application roles to manage the account budget](/user-guide/budgets#label-budgets-application-roles) .
  - Data Quality and data metric functions (DMFs): [View results of a data metric function](/user-guide/data-quality-results) .
- Budgets: 

- Service roles:
- To allow a role access to service endpoints, grant the service role to that role. You can grant a service role to an account role, an application role, or a database role. For more information, see [Managing service-related privileges](/developer-guide/snowpark-container-services/working-with-services#label-spcs-manage-service-related-privileges) .

### Active roles[¶](#active-roles)

*Active roles* serve as the source of authorization for any action taken by a user in a session. Both the
[primary role and any secondary roles](#label-access-control-role-enforcement) can be activated in a user session.

A role becomes an active role in either of the following ways:

- 
When a session is first established, the user’s default role and default secondary roles are activated as the session primary and secondary roles, respectively. Note that client connection properties used to establish the session could explicitly override the primary role or secondary roles to use.
- 
Executing a [USE ROLE](/sql-reference/sql/use-role) or[USE SECONDARY ROLES](/sql-reference/sql/use-secondary-roles) statement activates a different primary
role or secondary roles, respectively. These roles can change over the course of a session if either command is executed again.

### System-defined roles[¶](#system-defined-roles)

- GLOBALORGADMIN:
- (aka Organization Administrator) Role that performs organization-level tasks such as managing the lifecycle of accounts and viewing organization-level usage information. The role exists only in the [organization account](/user-guide/organization-accounts) .
- ORGADMIN:
- Role that uses a regular account to manage operations at the organization level. The ORGADMIN role will be phased out in a future release, so organization administrators are encouraged to use the GLOBALORGADMIN role instead.
- ACCOUNTADMIN:
- (aka Account Administrator) Role that encapsulates the SYSADMIN and SECURITYADMIN system-defined roles. It is the top-level role in the system and should be granted only to a limited/controlled number of users in your account.
- SECURITYADMIN:
- (aka Security Administrator) Role that can manage any object grant globally, as well as create, monitor, and manage users and roles. More specifically, this role: 
  - 
Is granted the MANAGE GRANTS security privilege to be able to modify any grant, including revoking it. Note The MANAGE GRANTS privilege provides the ability to grant and revoke privileges. It does not give the SECURITYADMIN the ability to perform other actions such as creating objects. To create an object, the SECURITYADMIN role must also be granted the privileges needed to create the object. For example, to create a database role, the SECURITYADMIN must also be granted the CREATE DATABASE ROLE privilege, as described in [CREATE DATABASE ROLE Access control requirements](/sql-reference/sql/create-database-role#label-create-database-role-access-control-reqs) .
  - 
Inherits the privileges of the USERADMIN role via the system role hierarchy (that is, USERADMIN role is granted to SECURITYADMIN).
- 
- USERADMIN:
- (aka User and Role Administrator) Role that is dedicated to user and role management only. More specifically, this role: 
  - 
Is granted the CREATE USER and CREATE ROLE security privileges.
  - 
Can create users and roles in the account. This role can also manage users and roles that it owns. Only the role with the OWNERSHIP privilege on an object (that is, user or role), or a higher role, can modify the object properties.
- 
- SYSADMIN:
- (aka System Administrator) Role that has privileges to create warehouses and databases (and other objects) in an account. If, as [recommended](/user-guide/security-access-control-considerations) , you create a role hierarchy that ultimately assigns all
custom roles to the SYSADMIN role, this role also has the ability to grant privileges on warehouses, databases, and other objects to other
roles.
- PUBLIC:
- Pseudo-role that is automatically granted to every user and every role in your account. The PUBLIC role can own securable objects, just like any other role; however, the objects owned by the role are, by definition, available to every other user and role in your account. This role is typically used in cases where explicit access control is not needed and all users are viewed as equal with regard to their access rights.

### Custom roles[¶](#custom-roles)

Custom [account roles](#label-access-control-overview-role-types) can be created using the USERADMIN role (or a higher role) as well as
by any role to which the CREATE ROLE privilege has been granted.

Custom database roles can be created by the database owner (that is, the role that has the OWNERSHIP privilege on the database).

By default, a newly-created role is not assigned to any user, nor granted to any other role.

When creating roles that will serve as the owners of securable objects in the system, Snowflake recommends creating a hierarchy of custom roles, with the top-most custom role assigned to the system role SYSADMIN. This role structure allows system administrators to manage all objects in the account, such as warehouses and database objects, while restricting management of users and roles to the USERADMIN role.

Conversely, if a custom role is not assigned to SYSADMIN through a role hierarchy, the system administrators cannot manage the objects owned by the role. Only those roles granted the MANAGE GRANTS privilege (only the SECURITYADMIN role by default) can view the objects and modify their access grants.

For instructions to create custom roles, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

## Privileges[¶](#privileges)

Access control privileges determine who can access and perform operations on specific objects in Snowflake. For each securable object,
there is a set of privileges that can be granted on it. For existing objects, privileges must be granted on individual objects
(such as the SELECT privilege on the `mytable` table). To simplify grant management,
[future grants](/user-guide/security-access-control-considerations#label-grant-management-future-grants) allow defining an initial set of privileges on objects created in a schema
(for example, granting the SELECT privilege on all *new* tables created in the `myschema` schema to a specified role).

Privileges are managed using the following commands:

- [GRANT <privileges> … TO ROLE](/sql-reference/sql/grant-privilege)
- [REVOKE <privileges> … FROM ROLE](/sql-reference/sql/revoke-privilege)
- [GRANT <privileges> … TO USER](/sql-reference/sql/grant-privilege-user)
- [REVOKE <privileges> … FROM USER](/sql-reference/sql/revoke-privilege-user)

In regular (non-managed) schemas, use of these commands is restricted to the role that owns an object (has the OWNERSHIP privilege on the object), any roles or users that have the MANAGE GRANTS global privilege for the object (only the SECURITYADMIN role by default).

In [managed access schemas](/user-guide/security-access-control-configure#label-managed-access-schemas), object owners lose the ability to make grant decisions. Only the schema
owner or a role with the MANAGE GRANTS privilege can grant privileges on objects in the schema, including future grants, centralizing
privilege management.

Note that a role that holds the global MANAGE GRANTS privilege can grant additional privileges to the current (grantor) role.

For more details, see [Access control privileges](/user-guide/security-access-control-privileges).

## Role hierarchy and privilege inheritance[¶](#role-hierarchy-and-privilege-inheritance)

The following diagram illustrates the hierarchy for the system-defined roles, as well as the recommended structure for additional, user-defined account roles and database roles. The highest-level database role in the example hierarchy is granted to a custom (user-defined) account role. In turn, this role is granted to another custom role in a recommended structure that allows the system-defined SYSADMIN role to inherit the privileges of custom account roles and database roles:

Note

ORGADMIN is a separate system role that manages operations at the organization level. This role is not included in the hierarchy of system roles.

For a more specific example of role hierarchy and privilege inheritance, consider the following scenario:

- Role 3 has been granted to Role 2.
- Role 2 has been granted to Role 1.
- Role 1 has been granted to User 1.

In this scenario:

- Role 2 inherits Privilege C.
- Role 1 inherits Privileges B and C.
- User 1 has all three privileges.

For instructions on creating a role hierarchy, see [Creating a role hierarchy](/user-guide/security-access-control-configure#label-security-role-hierarchy).

### Database roles and role hierarchies[¶](#database-roles-and-role-hierarchies)

The following limitations currently apply to database roles:

- 
If a database role is granted to a [share](/user-guide/data-sharing-gs#label-data-sharing-provider-option2) , then no other database roles can be granted to
that database role. For example, if database role`d1.r1` is granted to a share, then attempting to grant database role`d1.r2` to`d1.r1` is blocked.In addition, if a database role is granted to another database role, the grantee database role cannot be granted to a share. Database roles that are granted to a share can be granted to other database roles, as well as account roles.
- 
Account roles cannot be granted to database roles in a role hierarchy.

## Authorization through primary role and secondary roles[¶](#authorization-through-primary-role-and-secondary-roles)

Every active user session has a current role, also referred to as a *primary role*. When a session is initiated (for example, when a user
connects using JDBC/ODBC or logs in to the Snowflake web interface), the current role is determined based on the following criteria:

1. If a role was specified as part of the connection and that role is a role that has already been granted to the connecting user, the specified role becomes the current role.
2. If no role was specified and a default role has been set for the connecting user, that role becomes the current role.
3. If no role was specified and a default role has not been set for the connecting user, the system role PUBLIC is used.

To view the current role for a session, execute the [CURRENT_ROLE](/sql-reference/functions/current_role) function.

In addition, a set of *secondary* roles can be activated in a user session. A user can perform SQL actions on objects in a session using
the aggregate privileges granted to the primary and secondary roles. The roles must be granted to the user before they can be activated in
a session. Note that while a session must have exactly one active primary role at a time, a session can activate any number of secondary
roles at the same time.

Note

A database role can be neither a primary nor a secondary role. To assume the privileges granted to a database role, grant the database
role to an account role. Only account roles can be [activated](#label-access-control-overview-active-roles) in a session.

Authorization to execute [CREATE <object>](/sql-reference/sql/create) statements comes from the primary role only. When an object is created, its
ownership is set to the currently active primary role. However, for any other SQL action, any permission granted to any active primary or
secondary role can be used to authorize the action. For example, if any role in a secondary role hierarchy owns an object (has the
OWNERSHIP privilege on the object), the secondary roles would authorize performing any DDL actions on the object. Both the primary role and
all secondary roles inherit privileges from any roles lower in their role hierarchies.

For organizations whose security model includes a large number of roles, each with a fine granularity of authorization defined by permissions, using secondary roles simplifies role management. All roles that were granted to a user can be activated in a session. Secondary roles are particularly useful for SQL operations such as cross-database joins that would otherwise require creating a parent role of the roles that have permissions to access the objects in each database.

During the course of a session, you can execute the [USE ROLE](/sql-reference/sql/use-role) or [USE SECONDARY ROLES](/sql-reference/sql/use-secondary-roles)
command to change the current primary or secondary roles, respectively. You can use the [CURRENT_SECONDARY_ROLES](/sql-reference/functions/current_secondary_roles)
function to show all active secondary roles for the current session.

When you create an object that requires one or more privileges to use, only the primary role and those roles that it directly or indirectly inherits are considered when searching for the grants of those privileges.

For any other statement that requires one or more privileges (such as querying a table requires the SELECT privilege on a table with the USAGE privilege on the database and schema), the primary role, the secondary roles, and any other inherited roles are considered when searching for the grants of those privileges.

Note

There is no concept of a “super-user” or “super-role” in Snowflake that can bypass authorization checks. All access requires appropriate access privileges.

## Access Requests[¶](#access-requests)

When a query in Workspaces fails because of missing privileges, users can submit an access request from
Snowsight for administrator review. For more information, see
[Request Access in Workspaces](/user-guide/access-requests-workspaces).
