%% trellis:begin %%
# Offset Advance Only Inside the Consuming DML
*Streams, Tasks & Dynamic Tables*

Why the offset moves only when a transaction that reads the Stream also commits, making a crashed consumer retry the exact same change set.

**Requires:** [[pipelines.stream-offset-bookmark|Streams as Offset Bookmarks]]
%% trellis:end %%

## Notes
