/**
 * hc15 Part 2（starter）：最近 k 笔成交价的滑动窗口中位数（下中位数）。
 *
 * <p>提示：窗口里的旧值要从堆里删，但堆不支持「删任意元素」——惰性删除（lazy deletion）：先把旧值记进 delayed 表，
 * 等它浮到堆顶再真正弹出。平衡两个堆时用「有效元素个数」而不是 heap.size()；每次操作后保证两个堆顶都是有效的。
 * 旧值属于哪个堆？lo 里每个数 ≤ hi 里每个数，所以 old ≤ lo.peek() 就在 lo。
 */
public final class WindowMedian {
    // 在这里加你的字段（环形缓冲 / 队列、两个堆、delayed 表、有效个数）

    /** k ≥ 1，否则 IAE。 */
    public WindowMedian(int k) {
        throw new UnsupportedOperationException("TODO");
    }

    /** 摊还 O(log k)。 */
    public void add(long price) {
        throw new UnsupportedOperationException("TODO");
    }

    /** 窗口里（最近 min(n, k) 个价格）的下中位数。还没有数据 → NoSuchElementException。 */
    public long median() {
        throw new UnsupportedOperationException("TODO");
    }

    /** 窗口里现在有几个价格：min(已加入个数, k)。 */
    public int size() {
        throw new UnsupportedOperationException("TODO");
    }

    /**
     * 两个堆里实际占着的元素个数（含还没被惰性清掉的失效元素）。必须保持 ≤ 4k，不随流的长度增长——
     * 提示：升序的流里，埋在 lo 堆底的失效元素永远浮不上来；失效元素太多时整体重建一次。
     */
    public int retained() {
        throw new UnsupportedOperationException("TODO");
    }

    /** 每加入一个价格之后的窗口中位数：result[i] = 加入 prices[0..i] 后的 median()。k ≥ 1 否则 IAE；null → NPE。 */
    public static long[] slide(long[] prices, int k) {
        throw new UnsupportedOperationException("TODO");
    }
}
