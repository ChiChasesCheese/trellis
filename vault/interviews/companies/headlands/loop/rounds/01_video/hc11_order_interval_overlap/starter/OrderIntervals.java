import java.util.List;
import java.util.Objects;

/**
 * hc11 Part 1 + Part 2（starter）：区间最大重叠（扫描线），以及按买 / 卖方向 + 撤单的版本。
 *
 * <p>订单生命周期是左闭右开区间 [start, end)：start 时刻活着，end 时刻已经不活。所以 [1,3) 和 [3,5) 不重叠。
 * 时间是非负 long，可能接近 Long.MAX_VALUE——只做比较，不做减法。record 与 sealed 类型已给出。
 */
public final class OrderIntervals {
    private OrderIntervals() {}

    public enum Side { BUY, SELL }

    /** 最大重叠数 count，及其最早出现的时刻 time。从没有订单活着时是 (0, 0)。 */
    public record Peak(int count, long time) {}

    public sealed interface OrderEvent permits Place, Cancel {}

    /** 下单：计划生命周期 [start, end)。end == start 合法（空区间，从没活过）。 */
    public record Place(long id, Side side, long start, long end) implements OrderEvent {
        public Place {
            Objects.requireNonNull(side, "side");
            if (start < 0) throw new IllegalArgumentException("negative start: " + start);
            if (end < start) throw new IllegalArgumentException("end < start: " + end + " < " + start);
        }
    }

    /** 撤单：time 时刻起这张单不再活着，把区间截成 [start, min(end, time))。 */
    public record Cancel(long id, long time) implements OrderEvent {
        public Cancel {
            if (time < 0) throw new IllegalArgumentException("negative time: " + time);
        }
    }

    public record Report(Peak buy, Peak sell, Peak all) {}

    // ---------------------------------------------------------------- Part 1

    /**
     * 同时活着的订单数的最大值，区间 [start, end)。输入允许乱序、重复；空区间忽略；
     * 行长度不是 2 → IAE；start < 0 或 end < start → IAE；null → NPE。
     * 提示：排序所有开始和所有结束，同一时刻「先结束后开始」。
     */
    public static int maxOverlap(long[][] intervals) {
        throw new UnsupportedOperationException("TODO");
    }

    /** 同上，并给出最早达到最大值的时刻。 */
    public static Peak peak(long[][] intervals) {
        throw new UnsupportedOperationException("TODO");
    }

    /** 闭区间 [start, end] 的版本：[1,3] 和 [3,5] 在 3 重叠；[5,5] 是一个点。 */
    public static int maxOverlapInclusive(long[][] intervals) {
        throw new UnsupportedOperationException("TODO");
    }

    // ---------------------------------------------------------------- Part 2

    /**
     * 批量版：一串 Place / Cancel（顺序无所谓），分别给出买方、卖方、全部的峰值。
     * 有效区间是 [start, min(end, 最早的撤单时间))；撤单时间 <= start 则从没活过；
     * 同一 id 多次撤单最早的生效；撤单 id 没有对应 Place → IAE；同一 id 两次 Place → IAE。
     * 提示：用 switch 模式匹配分派 sealed 的 OrderEvent；按方向分别扫描。
     */
    public static Report analyze(List<? extends OrderEvent> events) {
        throw new UnsupportedOperationException("TODO");
    }
}
