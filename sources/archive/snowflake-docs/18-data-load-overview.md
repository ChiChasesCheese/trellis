---
title: Overview of data loading¶
corpus: snowflake-docs
section: 18-data-load-overview
level: 1
locator: https://docs.snowflake.com/en/user-guide/data-load-overview
license: free-online
fetched: '2026-09-13'
---

# Overview of data loading[¶](#overview-of-data-loading)

This topic provides an overview of the main options available to load data into Snowflake.

To easily and accurately measure the ingestion latency of your data pipelines, use row timestamps. For more information, see [Use row timestamps to measure latency in your pipelines](/user-guide/data-engineering/row-timestamps).

## Supported file locations[¶](#supported-file-locations)

Snowflake refers to the location of data files in cloud storage as a *stage*.
The [COPY INTO <table>](/sql-reference/sql/copy-into-table) command used for both bulk and continuous data loads (Snowpipe) supports
cloud storage accounts managed by your business entity (*external stages*) as well as cloud storage contained in your Snowflake account
(*internal stages*).

### External stages[¶](#external-stages)

Loading data from any of the following cloud storage services is supported regardless of the [cloud platform](/user-guide/intro-cloud-platforms) that hosts your Snowflake account:

- Amazon S3
- Google Cloud Storage
- Microsoft Azure

You cannot access data held in archival cloud storage classes that requires restoration before it can be retrieved. These archival storage classes include, for example, the Amazon S3 Glacier Flexible Retrieval or Glacier Deep Archive storage class, or Microsoft Azure Archive Storage.

Upload (i.e. *stage*) files to your cloud storage account using the tools provided by the cloud storage service.

A named external stage is a database object created in a schema. This object stores the URL to files in cloud storage, the settings used to access the cloud storage account, and convenience settings such as the options that describe the format of staged files. Create stages using the [CREATE STAGE](/sql-reference/sql/create-stage) command.

Note

Some data transfer billing charges may apply when loading data from files in a cloud storage service in a different region or cloud platform from your Snowflake account. For more information, see [Understanding data transfer cost](/user-guide/cost-understanding-data-transfer).

### Internal stages[¶](#internal-stages)

Snowflake maintains the following stage types in your account:

- User:
- A user stage is allocated to each user for storing files. This stage type is designed to store files that are staged and managed by a single user but can be loaded into multiple tables. User stages cannot be altered or dropped.
- Table:
- A table stage is available for each table created in Snowflake. This stage type is designed to store files that are staged and managed by one or more users but only loaded into a single table. Table stages cannot be altered or dropped. Note that a table stage is not a separate database object; rather, it is an implicit stage tied to the table itself. A table stage has no grantable privileges of its own. To stage files to a table stage, list the files, query them on the stage, or drop them, you must be the table owner (have the role with the OWNERSHIP privilege on the table).
- Named:
- A named internal stage is a database object created in a schema. This stage type can store files that are staged and managed by one or more users and loaded into one or more tables. Because named stages are database objects, the ability to create, modify, use, or drop them can be controlled using security access control privileges. Create stages using the [CREATE STAGE](/sql-reference/sql/create-stage) command.

Upload files to any of the internal stage types from your local file system using the [PUT](/sql-reference/sql/put) command.

## Bulk vs continuous loading[¶](#bulk-vs-continuous-loading)

Snowflake provides the following main solutions for data loading. The best solution may depend upon the volume of data to load and the frequency of loading.

### Bulk loading using the COPY command[¶](#bulk-loading-using-the-copy-command)

This option enables loading batches of data from files already available in cloud storage, or copying (i.e. *staging*) data files from a local machine to an internal (i.e. Snowflake) cloud storage location before loading the data into tables using the COPY command.

#### Compute resources[¶](#compute-resources)

Bulk loading relies on user-provided virtual warehouses, which are specified in the COPY statement. Users are required to size the warehouse appropriately to accommodate expected loads.

#### Simple transformations during a load[¶](#simple-transformations-during-a-load)

Snowflake supports transforming data while loading it into a table using the COPY command. Options include:

- Column reordering
- Column omission
- Casts
- Truncating text strings that exceed the target column length

There is no requirement for your data files to have the same number and ordering of columns as your target table.

### Continuous loading using Snowpipe[¶](#continuous-loading-using-snowpipe)

This option is designed to load small volumes of data (i.e. micro-batches) and incrementally make them available for analysis. Snowpipe loads data within minutes after files are added to a stage and submitted for ingestion. This ensures users have the latest results, as soon as the raw data is available.

#### Compute resources[¶](#compute-resources)

Snowpipe uses compute resources provided by Snowflake (i.e. a serverless compute model). These Snowflake-provided resources are automatically resized and scaled up or down as required, and are charged and itemized using per-second billing. Data ingestion is charged based upon the actual workloads.

#### Simple transformations during a load[¶](#simple-transformations-during-a-load)

The COPY statement in a pipe definition supports the same COPY transformation options as when bulk loading data.

In addition, data pipelines can leverage Snowpipe to continuously load micro-batches of data into staging tables for transformation and optimization using automated tasks and the change data capture (CDC) information in streams.

### Continuous loading using Snowpipe Streaming[¶](#continuous-loading-using-snowpipe-streaming)

The Snowpipe Streaming API writes rows of data directly to Snowflake tables without the requirement of staging files. This architecture results in lower load latencies with corresponding lower costs for loading any volume of data, which makes it a powerful tool for handling near real-time data streams.

Snowpipe Streaming is also available for the Snowflake Connector for Kafka, which offers an easy upgrade path to take advantage of the lower latency and lower cost loads.

For more information, refer to [Snowpipe Streaming](/user-guide/snowpipe-streaming/data-load-snowpipe-streaming-overview).

## Loading data from Apache Kafka topics[¶](#loading-data-from-apache-kafka-topics)

The [Snowflake Connector for Kafka](/user-guide/kafka-connector/index) enables users to connect to an [Apache Kafka](https://kafka.apache.org/) server, read data from one or more topics, and load that data into Snowflake tables.

## DML error logging[¶](#dml-error-logging)

When you execute a set of DML statements and one of the statements fails with an error, the DML operation ends
and the changes made by the DML statement are rolled back. If you want to continue to execute the rest of the
DML statements and log the error that occurred, you can turn on DML error logging for the table. The table for
which DML error logging is turned on is called the *base table*. Errors are logged in an *error table* that is
associated with the base table.

DML error logging is turned on for a table only when *both* of the following conditions are met:

- The ERROR_LOGGING property is set to `TRUE` for the table.
- The [OPT_OUT_ERROR_LOGGING](/sql-reference/parameters#label-opt-out-error-logging) parameter is set to`FALSE` for the current session.

DML error logging is turned off for a table only when *either* of the following conditions are met:

- The ERROR_LOGGING property is set to `FALSE` for the table.
- The OPT_OUT_ERROR_LOGGING parameter is set to `TRUE` for the current session.

The following sections provide more information about DML error logging:

### Use cases for DML error logging[¶](#use-cases-for-dml-error-logging)

You might use DML error logging to avoid failures on errors for the following use cases:

- Migration of third-party data that relies on DML error logging, such as data from an Oracle database.
- Enforcement of some table constraints, such as NOT NULL constraints, during data ingestion.

### Configure DML error logging for a table[¶](#configure-dml-error-logging-for-a-table)

You can turn on or turn off DML error logging for a standard Snowflake table or a Snowflake-managed Iceberg table when you create or alter the table.

To turn on or turn off error logging for a table, use the following SQL commands to set the ERROR_LOGGING property for the table:

- [CREATE TABLE](/sql-reference/sql/create-table)
- [ALTER TABLE](/sql-reference/sql/alter-table)
- [CREATE ICEBERG TABLE](/sql-reference/sql/create-iceberg-table) (Snowflake-managed only)
- [ALTER ICEBERG TABLE](/sql-reference/sql/alter-iceberg-table) (Snowflake-managed only)

The following examples configure DML error logging for tables and show how errors are logged in error tables:

- [Log errors when inserting rows directly](#label-dml-error-logging-direct-inserts)
- [Log errors when inserting rows from one table into another table](#label-dml-error-logging-inserts-from-table)

The following examples configure DML error logging for tables and show how errors are logged in error tables:

- [Log errors when inserting rows directly](#log-errors-when-inserting-rows-directly)
- [Log errors when inserting rows from one table into another table](#log-errors-when-inserting-rows-from-one-table-into-another-table)

#### Log errors when inserting rows directly[¶](#log-errors-when-inserting-rows-directly)

The following example logs errors when inserting rows directly into a table:

1. 
Create a table and turn on DML error logging for it:
2. 
Run an INSERT statement that tries to insert several rows, including both valid and invalid values:
3. 
Query the table to confirm that one valid row was inserted:
4. 
Query the error table for the `test_dml_error_logging` base table to view the errors that
were logged:
5. 
Turn off DML error logging for the `test_dml_error_logging` table:
6. 
Attempt the same INSERT statement that you ran previously. An error is returned and no errors are logged in an error table:

#### Log errors when inserting rows from one table into another table[¶](#log-errors-when-inserting-rows-from-one-table-into-another-table)

The following example logs errors when inserting rows from one table into another table:

1. 
Create a source table and insert values:
2. 
Create a target table with the same definition as the source table:
3. 
Turn on DML error logging on the `dml_error_logging_target` table:
4. 
Insert values into the target table by querying the source table so that one of the inserts results in a division by zero error:
5. 
Query the table to confirm that two valid rows were inserted:
6. 
Query the error table for the `dml_error_logging_target` base table to view the errors that
were logged:

### Error logging and error tables[¶](#error-logging-and-error-tables)

When error logging is turned on for a table, Snowflake automatically creates an error table that is associated with the base table. DML operations that encounter supported errors log the errors in the error table instead of failing.

When DML error logging is turned on for a table, the following types of DML statements are logged:

- INSERT
- UPDATE
- MERGE

Error tables have a fixed definition and can only be accessed by the owner of the base table or a user with a role that has been granted the SELECT ERROR TABLE privilege on the base table. The only supported direct operations on an error table are SELECT and TRUNCATE statements. You can’t run other types of statements directly on error tables. Error tables can’t be used indirectly in materialized views or dynamic tables.

You can copy the data out of the error table to other tables. You can remove the data in an error table by running the TRUNCATE command.

The following sections provide more information about error logging and error tables:

#### Error table definition[¶](#error-table-definition)

Snowflake creates error tables with a standard definition that can’t be modified.

When you turn off DML error logging for a base table or drop a base table that has an error table, the error table associated with the base table is dropped automatically.

An error table has the following columns:

| Name | Type | Description | 
|---|---|---|
| `timestamp` | TIMESTAMP | The timestamp of the statement that triggered the error. | 
| `query_id` | VARCHAR | The unique ID of the statement that triggered the error. | 
| `error_code` | NUMBER | The error code. When multiple columns in one row contain errors, this column only captures the first error that is encountered. | 
| `error_metadata` | OBJECT | The error metadata. The OBJECT values have the following structure: The OBJECT values contain the following key-value pairs:  When multiple columns in one row contain errors, this column only captures the first error that is encountered. | 
| `error_data` | OBJECT | The data that caused the error. The OBJECT values have the following structure: The OBJECT values contain the key-value pairs that represent each column in the base table. The key is the column name. For invalid column values that caused the DML operation to fail, the value in the key-value pair is an array that contains the values. Valid values are shown directly; that is, they aren’t shown in arrays. If the data can’t be represented in an OBJECT value, the value is NULL. | 

#### Interact with error tables[¶](#interact-with-error-tables)

You can run SELECT statements and TRUNCATE statements on error tables by using the following syntax:

Where:

*base_table_name*
- The name of the table for which the error table was created.

For example, if the name of the base table is `my_table`, the following statement queries
the error table for this base table:

The following statement truncates the error table:

#### Access control requirements for error tables[¶](#access-control-requirements-for-error-tables)

Any role that can insert into a base table can trigger inserts into its error table. Regardless of the current role, direct inserts into an error table aren’t allowed.

The following users can run SELECT statements on an error table:

- 
The owner of the error table’s base table.
- 
Users who have been granted SELECT ERROR TABLE privileges on the base table, either through a role or directly. To grant SELECT ERROR TABLE privilege on a base table, run a [GRANT <privileges> … TO ROLE](/sql-reference/sql/grant-privilege) statement or a[GRANT <privileges> … TO USER](/sql-reference/sql/grant-privilege-user) statement.These statements use the following syntax: For example, to grant SELECT ERROR TABLE privilege on a base table named `mybasetable` to a role named`myrole` ,
run the following statement:

Alternatively, to grant other roles access to an error table, the base table owner can also create a view based on the error table and grant access to that view.

### Metadata for error logging[¶](#metadata-for-error-logging)

To determine whether error logging is turned on for a table, you can run the
[GET_DDL](/sql-reference/functions/get_ddl) function and pass in the name of the base table:

For example, for a base table named `test_dml_error_logging` in the current schema, run the following statement:

Metrics for error tables are recorded in the following views:

### Streams on error tables[¶](#streams-on-error-tables)

[Streams](/user-guide/streams-intro) aren’t supported directly on error tables. To enable change
tracking on error tables, first create a view on the error table, and then create a stream on the view.

The following example shows you how to enable change tracking on error tables:

1. 
Run the [CREATE VIEW](/sql-reference/sql/create-view) command to create a view on the error table:
2. 
Run the [CREATE STREAM](/sql-reference/sql/create-stream) command to create a stream on the view:

### DML error logging usage notes[¶](#dml-error-logging-usage-notes)

The following usage notes apply when error logging is turned on for a table:

- 
Only errors directly related to the base table are logged.
- 
The following types of errors are logged: 
  - NOT NULL table constraint violations.
  - Type conversion errors that occur when attempting to convert a value to the base table column.
  - Incompatible precision and scale values.
  - Incompatible length for string and binary types.
  - Some expression evaluation failures, such as division by zero or PARSE_JSON function failures.
- 
CREATE TABLE … AS SELECT (CTAS) statements run normally. They fail on DML errors and don’t log them.
- 
If you try to run a COPY INTO statement on a table with error logging enabled, the `Error logging is not supported in statement 'COPY INTO'` error is returned at compilation time.
- 
Errors that aren’t supported by DML error logging cause the DML operation to fail directly.
- 
If a SQL statement results in a compilation error, the operation ends and no errors are logged in the error table.
- 
Failures that occur in other ingestion paths, such as COPY and Snowpipe, aren’t logged in error tables. For Snowpipe Streaming high-performance error logging, see [Error logging in Snowpipe Streaming with high-performance architecture](/user-guide/snowpipe-streaming/snowpipe-streaming-error-tables) .
- 
The following are considerations related to DML error logging and performance: 
  - When DML error logging is enabled for a base table, and there are *no* errors in a DML statement that is run on the
base table, no performance difference or very little performance difference is expected.
  - When DML error logging is enabled for a base table, and there *are* errors in a DML statement that is run on the
base table, additional time is required to complete the DML statement because the error information is inserted into
the error table.
- When DML error logging is enabled for a base table, and there are 
- 
When a base table with an associated error table is cloned, the behavior is as follows: 
  - The base table’s schema and content are cloned.
  - The error table’s content isn’t cloned
  - The cloned base table has the ERROR_LOGGING property turned on, which implicitly creates an empty error table for it.

## Schema detection of column definitions from staged semi-structured data files[¶](#schema-detection-of-column-definitions-from-staged-semi-structured-data-files)

Semi-structured data can include thousands of columns. Snowflake provides robust solutions for handling this data. Options include referencing the data directly in cloud storage using external tables, loading the data into a single column of type VARIANT, or transforming and loading the data into separate columns in a standard relational table. All of these options require some knowledge of the column definitions in the data.

A different solution involves automatically detecting the schema in a set of staged semi-structured data files and retrieving the column definitions. The column definitions include the names, data types, and ordering of columns in the files. Generate syntax in a format suitable for creating Snowflake standard tables, external tables, or views.

Note

This feature supports Apache Parquet, Apache Avro, ORC, JSON, and CSV files.

This support is implemented through the following SQL functions:

- [INFER_SCHEMA](/sql-reference/functions/infer_schema)
- Detects the column definitions in a set of staged data files and retrieves the metadata in a format suitable for creating Snowflake objects.
- [GENERATE_COLUMN_DESCRIPTION](/sql-reference/functions/generate_column_description)
- Generates a list of columns from a set of staged files using the INFER_SCHEMA function output.

These SQL functions support both internal and external stages.

Create tables or external tables with the column definitions derived from a set of staged files using the
[CREATE TABLE … USING TEMPLATE](/sql-reference/sql/create-table) or [CREATE EXTERNAL TABLE … USING TEMPLATE](/sql-reference/sql/create-external-table) syntax. The USING TEMPLATE clause accepts an expression that
calls the INFER_SCHEMA SQL function to detect the column definitions in the files. After the table is created, you can then use a COPY statement with the `MATCH_BY_COLUMN_NAME` option to load files directly into the structured table.

Schema detection can also be used in conjunction with [table schema evolution](/user-guide/data-load-schema-evolution), where the structure of tables evolves automatically to support the structure of new data received from the data sources.

## Alternatives to loading data[¶](#alternatives-to-loading-data)

You can use the following option to query your data in cloud storage without loading it into Snowflake tables.

### External tables (data lake)[¶](#external-tables-data-lake)

[External tables](/user-guide/tables-external-intro) enable querying existing data stored in external cloud storage for analysis without first loading it into Snowflake. The source of truth for the data remains in the external cloud storage. Data sets materialized in Snowflake via materialized views are read-only.

This solution is especially beneficial to accounts that have a large amount of data stored in external cloud storage and only want to query a portion of the data; for example, the most recent data. Users can create materialized views on subsets of this data for improved query performance.

### Working with Amazon S3-compatible storage[¶](#working-with-amazon-s3-compatible-storage)

You can create external stages and tables in Snowflake to access storage in an application or device that is Amazon S3-compatible.
This feature lets you manage, govern, and analyze your data, regardless of where the data is stored.
For information, see [Work with Amazon S3-compatible storage](/user-guide/data-load-s3-compatible-storage).
