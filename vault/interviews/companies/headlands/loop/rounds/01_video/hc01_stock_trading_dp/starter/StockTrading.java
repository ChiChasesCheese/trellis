import java.util.List;

/**
 * Best Time to Buy and Sell Stock 家族。题面见 ../problem.md，讲义见 study/30-articles/hc01_stock_trading_dp.md。
 * 把每个 TODO 换成实现；Part 1 -> 4 依次做，每做完一个跑一次对应的 tag。
 */
public final class StockTrading {
    private StockTrading() {}

    /** 价格上界 2^40：保证利润（最多 2^21 笔 * 2^40）装得进 long，不需要在内循环里检查溢出。 */
    public static final long MAX_PRICE = 1L << 40;
    /** 天数上界 2^22。 */
    public static final int MAX_DAYS = 1 << 22;
    /** plan() 最多允许的 (天数+1) * (交易次数上限+1) 格子数。 */
    public static final long MAX_PLAN_CELLS = 1L << 28;

    // ---------------------------------------------------------------- 数据类型（已给出）

    /** 第 buyDay 天买入、第 sellDay 天卖出（天从 0 开始数）。 */
    public record Trade(int buyDay, int sellDay) {
        public Trade {
            if (buyDay < 0 || sellDay <= buyDay)
                throw new IllegalArgumentException("need 0 <= buyDay < sellDay: " + buyDay + "," + sellDay);
        }
    }

    public record Plan(long profit, List<Trade> trades) {
        public Plan { trades = List.copyOf(trades); }
    }

    /** maxTransactions：最多几笔；fee：每笔卖出时扣的手续费；cooldown：卖出后的下一天不能买入。 */
    public record Rules(int maxTransactions, long fee, boolean cooldown) {
        public static final int UNLIMITED = Integer.MAX_VALUE;

        public Rules {
            if (maxTransactions < 0) throw new IllegalArgumentException("maxTransactions < 0");
            if (fee < 0 || fee > MAX_PRICE) throw new IllegalArgumentException("fee out of range: " + fee);
        }

        public static Rules atMost(int k) { return new Rules(k, 0, false); }
        public static Rules unlimited() { return new Rules(UNLIMITED, 0, false); }
        public Rules withFee(long newFee) { return new Rules(maxTransactions, newFee, cooldown); }
        public Rules withCooldown(boolean on) { return new Rules(maxTransactions, fee, on); }
    }

    /** 每天结束时的状态。FREE：空仓可买；HOLD：持有一股；COOL：今天刚卖出，明天只能休息。 */
    public enum State {
        FREE, HOLD, COOL;

        /** 休息一天：COOL -> FREE，其余不变。 */
        public State afterRest() { throw new UnsupportedOperationException("TODO"); }

        /** 买入：只有 FREE 能买，否则抛 IllegalStateException；结果是 HOLD。 */
        public State afterBuy() { throw new UnsupportedOperationException("TODO"); }

        /** 卖出：只有 HOLD 能卖，否则抛 IllegalStateException；结果是 COOL（rules.cooldown()）或 FREE。 */
        public State afterSell(Rules rules) { throw new UnsupportedOperationException("TODO"); }
    }

    public sealed interface Move permits Buy, Sell {}
    public record Buy(int day) implements Move {}
    public record Sell(int day) implements Move {}

    // ---------------------------------------------------------------- Part 1：只交易一次（LC 121）

    /**
     * 暴力 O(n^2)。输入校验（所有 Part 通用）：prices 为 null -> NullPointerException；
     * 长度 > MAX_DAYS 或任何价格不在 [0, MAX_PRICE] -> IllegalArgumentException。
     */
    public static long maxProfitBrute(long[] prices) { throw new UnsupportedOperationException("TODO"); }

    /** O(n)：边扫边记「到目前为止的最低价」。 */
    public static long maxProfitOnce(long[] prices) { throw new UnsupportedOperationException("TODO"); }

    // ---------------------------------------------------------------- Part 2：不限次数（LC 122）

    public static long maxProfitUnlimited(long[] prices) { throw new UnsupportedOperationException("TODO"); }

    // ---------------------------------------------------------------- Part 3：最多 k 次（LC 188）

    /** k < 0 -> IllegalArgumentException。k >= n/2 时等价于不限次数，别分配 k 那么长的数组。 */
    public static long maxProfitAtMost(int k, long[] prices) { throw new UnsupportedOperationException("TODO"); }

    // ---------------------------------------------------------------- Part 4：冷却 / 手续费 / 还原交易

    /** 同一台状态机，加上 COOL 状态和手续费。 */
    public static long maxProfit(Rules rules, long[] prices) { throw new UnsupportedOperationException("TODO"); }

    /**
     * 最大利润 + 交易明细（按时间顺序、每笔净利润 > 0）。
     * 格子数 (n+1)*(min(k, n/2)+1) 超过 MAX_PLAN_CELLS -> IllegalArgumentException。
     */
    public static Plan plan(Rules rules, long[] prices) { throw new UnsupportedOperationException("TODO"); }

    /**
     * 用 State 状态机逐天回放一个方案，返回利润。每天最多一个动作；非法方案 -> IllegalArgumentException。
     * 提示：对 Move 写一个带 case null 的模式匹配 switch。
     */
    public static long replay(Rules rules, long[] prices, List<Trade> trades) {
        throw new UnsupportedOperationException("TODO");
    }
}
