---
title: Understanding end-to-end encryption in Snowflake¶
corpus: snowflake-docs
section: 27-security-encryption-end-to-end
level: 1
locator: https://docs.snowflake.com/en/user-guide/security-encryption-end-to-end
license: free-online
fetched: '2026-09-13'
---

# Understanding end-to-end encryption in Snowflake[¶](#understanding-end-to-end-encryption-in-snowflake)

This topic provides concepts related to end-to-end encryption in Snowflake.

## Overview[¶](#overview)

End-to-end encryption (E2EE) is a method to secure customer data that prevents third parties from reading the data while at-rest or in transit to and from Snowflake and to minimize the attack surface.

The figure illustrates the E2EE system in Snowflake:

The E2EE system includes the following components:

- The Snowflake customer in a corporate network.
- A customer-provided or Snowflake-provided data file staging area.
- Snowflake runs in a secure virtual private cloud (VPC) or virtual network (VNet), depending on the cloud platform.

Snowflake supports both internal (Snowflake-provided) and external (customer-provided) stages for data files. Snowflake provides internal stages where you can upload and group your data files before loading the data into tables (image B).

Customer-provided stages are containers or directories in a supported cloud storage service (e.g. Amazon S3) that you control and manage (image A). Customer-provided stages are an attractive option for customers who already have data stored in a cloud storage service that they want to copy into Snowflake.

Per the figure in this section, the flow of E2EE in Snowflake is as follows:

1. 
A user uploads one or more data files to a stage. If the stage is an external stage (Image A), the user may optionally encrypt the data files using client-side encryption (see [Client-Side Encryption](#client-side-encryption) for more information). We recommend client-side encryption for data files in external stages; but if the data
is not encrypted, Snowflake immediately encrypts the data when it is loaded into a table within Snowflake.If the stage is an internal (i.e., Snowflake) stage (Image B) data files are automatically encrypted by the Snowflake client on the user’s local machine prior to being transmitted to the internal stage, in addition to being encrypted after they are loaded into the stage.
2. 
The user loads the data from the stage into a table. The data is transformed into Snowflake’s proprietary file format and stored in a cloud storage container. In Snowflake, all customer data at rest is encrypted and encrypted with TLS in transit to/from the Snowflake service. Snowflake also decrypts customer data when the data is transformed or operated on in a table, and then re-encrypts the data when the transformations and operations are complete.
3. 
The user can unload query results into an external or internal stage. Results are optionally encrypted using client-side encryption when unloaded into a customer-managed stage, and are automatically encrypted when unloaded to a Snowflake-provided stage.
4. 
The user downloads data files from the stage and decrypts the data on the client side.

## Client-side encryption[¶](#client-side-encryption)

Client-side encryption means that a client encrypts data before copying it into a cloud storage staging area. Client-side encryption provides a secure system for managing data in cloud storage.

Client-side encryption follows a specific protocol defined by the cloud storage service. The service SDK and third-party tools implement this protocol.

The following image summarizes client-side encryption:

The client-side encryption protocol works as follows:

1. The customer creates a secret [master key](https://csrc.nist.gov/glossary/term/master_key) , which is shared with Snowflake.
2. The client, which is provided by the cloud storage service, generates a random encryption key and encrypts the file before uploading it into cloud storage. The random encryption key, in turn, is encrypted with the customer’s master key.
3. Both the encrypted file and the encrypted random key are uploaded to the cloud storage service. The encrypted random key is stored with the file’s metadata.

When downloading data, the client downloads both the encrypted file and the encrypted random key. The client decrypts the encrypted random key using the customer’s master key.

Next, the client decrypts the encrypted file using the now decrypted random key. This encryption and decryption happens on the client side.

At no time does the third-party cloud storage service or any other third party (such as an ISP) see the data in the clear. Customers may upload client-side encrypted data using any client or tool that supports client-side encryption.

## Ingesting client-side encrypted data into Snowflake[¶](#ingesting-client-side-encrypted-data-into-snowflake)

Snowflake supports the client-side encryption protocol using a client-side master key when reading or writing data between a cloud storage service stage and Snowflake, as shown in the following image:

To load client-side encrypted data from a customer-provided stage, you create a named stage object with an additional `MASTER_KEY`
parameter using a [CREATE STAGE](/sql-reference/sql/create-stage) command, and then load data from the stage into your Snowflake tables. The
`MASTER_KEY` parameter requires either a 128-bit or 256-bit Advanced Encryption Standard (AES) key encoded in Base64.

A named stage object stores settings related to a stage and provides a convenient way to load or unload data between Snowflake and a specific container in cloud storage. The following SQL snippet creates an example Amazon S3 stage object in Snowflake that supports client-side encryption:

The truncated master key specified in this SQL command is the Base64-encoded string of the customer’s secret master key. As with all other credentials, this master key is transmitted over Transport Layer Security (HTTPS) to Snowflake and is stored encrypted in metadata storage. Only the customer and the query-processing components of Snowflake are exposed to the master key.

A benefit of named stage objects is that they can be granted to other users within a Snowflake account without revealing access credentials or client-side encryption keys to those users. Users with the appropriate access control privileges simply reference the named stage object when loading or unloading data.

The following SQL commands create a table named `users` and copy data from the encrypted stage into the `users` table:

The data is now ready to be analyzed using Snowflake.

You can also unload data into the stage. The following SQL command creates a `most_purchases` table and populates it with the results of a
query that finds the top 10 users with the most purchases, and then unloads the table data into the stage:

Snowflake encrypts the data files copied into the customer’s stage using the master key stored in the stage object. Snowflake adheres to the client-side encryption protocol for the cloud storage service. A customer can download the encrypted data files using any client or tool that supports client-side encryption.

**Next Topics:**
