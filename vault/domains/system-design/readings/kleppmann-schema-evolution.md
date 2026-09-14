---
nodes: [storage.encoding]
url: https://martin.kleppmann.com/2012/12/05/schema-evolution-in-avro-protocol-buffers-thrift.html
tags: [canonical]
---
# Schema evolution in Avro, Protocol Buffers and Thrift (Kleppmann)

DDIA's encoding chapter as a single free post, with the wire bytes laid out
side by side. Shows exactly which mechanism — tag numbers vs writer/reader
schema resolution — buys you the ability to deploy new and old code at once.

**Extract on read:**
- Protobuf/Thrift identify fields by tag number, so you may rename freely but must never reuse or renumber a tag; new fields must be optional.
- Avro carries no field IDs: compatibility comes from resolving the writer's schema against the reader's, which is why it needs a schema registry.
- Forward vs backward compatibility as two separate obligations — a rolling deploy needs both, because old and new code read each other's writes.

%% trellis:begin %%
## Source
[Open the original ↗](https://martin.kleppmann.com/2012/12/05/schema-evolution-in-avro-protocol-buffers-thrift.html)

## Archived copy
![[kleppmann-schema-evolution-clip]]
%% trellis:end %%
