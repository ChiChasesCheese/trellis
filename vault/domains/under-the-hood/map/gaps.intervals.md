%% trellis:begin %%
# 区间：PostgreSQL 防止重复预订
*考点补全：后端系统里的算法*

会议室、酒店预订要保证时间段不重叠：PostgreSQL 的范围类型加排他约束（EXCLUDE … WITH &&），由 GiST 索引在插入时检查重叠；和合并区间、会议室问题的关系。

## Cards (3)
1. [[uth-gaps-intervals-1-overlap]]
2. [[uth-gaps-intervals-2-gist]]
3. [[uth-gaps-intervals-3-concurrent]]
%% trellis:end %%

## Notes
