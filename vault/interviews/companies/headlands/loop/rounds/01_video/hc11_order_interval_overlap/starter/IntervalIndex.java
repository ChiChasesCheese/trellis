/**
 * hc11 Part 4（starter）：坐标很大（高达 10^18）时的区间计数索引 = 坐标压缩 + 懒标记线段树。
 *
 * <p>提示：活跃数只在端点处变化。把端点排序去重成 c[0] < c[1] < …，相邻端点之间是一个「基本段」，段内活跃数是常数；
 * 区间 [s, e) 覆盖基本段 idx(s) .. idx(e)-1。线段树支持「区间加 delta」和「区间求最大值」，都是 O(log m)。
 * 不要做 end - start 之类的减法（可能溢出）。
 */
public final class IntervalIndex {

    /** 端点集合（任意顺序、可重复）。之后 add / remove 的区间两端都必须在这个集合里。 */
    public IntervalIndex(long[] coordinates) {
        throw new UnsupportedOperationException("TODO");
    }

    /** 从一批区间建索引：收集所有端点压缩，再逐个 add。行长度不是 2 → IAE。 */
    public static IntervalIndex of(long[][] intervals) {
        throw new UnsupportedOperationException("TODO");
    }

    /** 用压缩 + 线段树算 Part 1 的答案，必须与扫描线一致。 */
    public static int maxOverlap(long[][] intervals) {
        throw new UnsupportedOperationException("TODO");
    }

    /** 加入区间 [start, end)：两端必须是已知端点（否则 IAE），end < start → IAE；start == end 什么都不做。 */
    public void add(long start, long end) {
        throw new UnsupportedOperationException("TODO");
    }

    /** 撤销一个之前 add 过的区间（调用方保证）。 */
    public void remove(long start, long end) {
        throw new UnsupportedOperationException("TODO");
    }

    /** 全局最大重叠数。 */
    public int max() {
        throw new UnsupportedOperationException("TODO");
    }

    /** t 时刻活着几个（t 落在所有端点之外是 0；右端不含）。 */
    public int liveAt(long t) {
        throw new UnsupportedOperationException("TODO");
    }

    /** 区间 [from, to) 内任意时刻的最大活跃数。to < from → IAE；to == from → 0。 */
    public int maxIn(long from, long to) {
        throw new UnsupportedOperationException("TODO");
    }

    /** 去重后的端点数。 */
    public int coordinateCount() {
        throw new UnsupportedOperationException("TODO");
    }

    /** 基本段个数 = 端点数 - 1（至少 0）。 */
    public int segmentCount() {
        throw new UnsupportedOperationException("TODO");
    }
}
