# VLT-212: Stop storing the same file twice

Storage costs doubled last quarter: the same attachments get uploaded over and over. Store each unique
file once, without changing what users see or can do.

We want to know it is working. Report it through the existing counters in `filevault.metrics`:
`dedup_hits_total` (uploads whose content was already stored) and `bytes_saved` (bytes not stored again).
