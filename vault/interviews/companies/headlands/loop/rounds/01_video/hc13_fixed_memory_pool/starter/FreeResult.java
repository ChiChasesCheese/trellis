/**
 * 归还一个块 / 一个 handle 的结果。三个池（IndexPool、GenPool、OffHeapOrderPool、ConcurrentPool）共用。
 *
 * 为什么不用「返回 boolean」或「直接抛异常」：
 *   * boolean 分不清「你重复归还」和「你传了一个根本不属于这个池的编号」，而这两个 bug 的排查方向完全不同；
 *   * 抛异常对「并发里两个线程同时 free 同一块」不友好——输的那个线程是正常竞争的结果，不是程序错误，
 *     让调用方自己决定要不要抛更灵活（要抛就用 freeOrThrow）。
 */
public enum FreeResult {
    /** 成功归还。 */
    FREED,
    /** 这块当前不在使用中：已经被归还过（重复归还），或者 handle 已陈旧（槽位已被回收甚至重新分配给别人）。 */
    DOUBLE_FREE,
    /** 根本不是这个池发出的编号：下标越界、NONE、全零 handle、从没发过的版本号。 */
    INVALID
}
