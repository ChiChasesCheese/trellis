%% trellis:begin %%
# epoll：红黑树 + 就绪链表
*操作系统与网络*

关注的 fd 存在红黑树里，就绪的放进链表，epoll_wait 只拷贝就绪的；为什么比 select / poll 的 O(n) 扫描快。
%% trellis:end %%

## Notes
