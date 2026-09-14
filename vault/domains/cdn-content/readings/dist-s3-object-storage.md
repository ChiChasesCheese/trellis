---
nodes: [distributed.object-storage]
url: https://docs.aws.amazon.com/AmazonS3/latest/userguide/Welcome.html
tags: [canonical]
---
# Amazon S3 object-storage model

The authoritative overview of bucket/key/version identity, metadata, lifecycle, replication, storage classes, request cost, and current consistency guarantees.

**Extract on read:**
- One key update is atomic, but a multi-key manifest change is not.
- Object identity, metadata, versioning, and conditional publication belong in the application contract.
- Region, storage class, lifecycle, requests, and transfer each change cost and recovery behavior.

%% trellis:begin %%
## Source
[Open the original ↗](https://docs.aws.amazon.com/AmazonS3/latest/userguide/Welcome.html)
%% trellis:end %%
