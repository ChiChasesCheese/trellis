import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.Objects;
import java.util.TreeMap;

/**
 * Best Time to Buy and Sell Stock 家族：一次交易 -> 不限次数 -> 最多 k 次 -> 冷却 / 手续费 + 还原交易。
 *
 * 全文只有一个核心想法：每天结束时，你只可能处于有限几种「状态」(State) 之一；
 * 每个状态记一个数 = 「到这一天为止、处于该状态时手里最多有多少现金」。
 * 明天的数只依赖今天的几个数 —— 这就是动态规划 (dynamic programming)。
 */
public final class StockTrading {
    private StockTrading() {}

    /**
     * 价格上界：2^40 个最小报价单位。为什么要有上界？
     * 利润最大 = (天数/2) * 价格 <= 2^21 * 2^40 = 2^61 < 2^63，所以 long 里永远不会溢出，
     * 不需要在内循环里每一步都 addExact。「从源头消灭溢出」比「到处检查溢出」便宜。
     */
    public static final long MAX_PRICE = 1L << 40;
    /** 天数上界 2^22（约 419 万）。 */
    public static final int MAX_DAYS = 1 << 22;
    /** plan() 为了还原交易要记录每个 (天, 交易次数) 一个字节；超过这个格子数就拒绝（256M 字节）。 */
    public static final long MAX_PLAN_CELLS = 1L << 28;

    // =====================================================================================
    // 数据类型
    // =====================================================================================

    /** 一笔完整交易：第 buyDay 天买入，第 sellDay 天卖出（天从 0 开始数）。 */
    public record Trade(int buyDay, int sellDay) {
        public Trade {
            if (buyDay < 0 || sellDay <= buyDay)
                throw new IllegalArgumentException("need 0 <= buyDay < sellDay: " + buyDay + "," + sellDay);
        }
    }

    /** 最优方案：总利润 + 按时间顺序排列的交易。 */
    public record Plan(long profit, List<Trade> trades) {
        public Plan { trades = List.copyOf(trades); }
    }

    /**
     * 交易规则。maxTransactions：最多几次「买入」（一次买入 + 对应的卖出算一笔）；fee：每笔卖出时扣的手续费；
     * cooldown：卖出之后的下一天不能买入。LC 121 = atMost(1)，122 = unlimited()，188 = atMost(k)，
     * 309 = unlimited().withCooldown(true)，714 = unlimited().withFee(fee)。
     */
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

    /**
     * 每天结束时你所处的状态。画成图就是一台有限状态机 (finite state machine)：
     *
     * <pre>
     *            rest                 rest
     *          +-------+            +-------+
     *          v       |            v       |
     *        [FREE] --buy--> [HOLD] --sell--> [COOL] --(rest, 被迫)--> FREE
     *          ^                 \
     *          +------ sell ------+      (没有冷却时，sell 直接回到 FREE)
     * </pre>
     * FREE：手里没股票、明天可以买。HOLD：手里有一股。COOL：今天刚卖出，明天只能休息。
     */
    public enum State {
        FREE, HOLD, COOL;

        /** 什么也不做的一天。COOL 过一天变成 FREE（冷却结束），其余原地不动。 */
        public State afterRest() {
            return this == COOL ? FREE : this;
        }

        /** 买入：只有 FREE 能买；COOL（冷却中）和 HOLD（已持有）都不行。 */
        public State afterBuy() {
            if (this != FREE) throw new IllegalStateException("cannot buy while " + this);
            return HOLD;
        }

        /** 卖出：只有 HOLD 能卖；卖完进入 COOL（有冷却）或 FREE（无冷却）。 */
        public State afterSell(Rules rules) {
            if (this != HOLD) throw new IllegalStateException("cannot sell while " + this);
            return rules.cooldown() ? COOL : FREE;
        }
    }

    /** 一天里的动作：只有买和卖两种，「休息」就是这一天没有动作。sealed：编译器知道只有这两种。 */
    public sealed interface Move permits Buy, Sell {}
    public record Buy(int day) implements Move {}
    public record Sell(int day) implements Move {}

    // =====================================================================================
    // 输入校验
    // =====================================================================================

    private static void check(long[] prices) {
        Objects.requireNonNull(prices, "prices");
        if (prices.length > MAX_DAYS) throw new IllegalArgumentException("too many days: " + prices.length);
        for (int i = 0; i < prices.length; i++) {
            if (prices[i] < 0 || prices[i] > MAX_PRICE)
                throw new IllegalArgumentException("price[" + i + "] out of range: " + prices[i]);
        }
    }

    // =====================================================================================
    // Part 1：只能交易一次（LC 121）
    // =====================================================================================

    /** 暴力：试遍所有 (买入日 i, 卖出日 j>i)。O(n^2) 时间，O(1) 空间。留着当「正确答案」去对拍。 */
    public static long maxProfitBrute(long[] prices) {
        check(prices);
        long best = 0; // 0 = 不交易
        for (int i = 0; i < prices.length; i++) {
            for (int j = i + 1; j < prices.length; j++) {
                best = Math.max(best, prices[j] - prices[i]);
            }
        }
        return best;
    }

    /**
     * O(n)：对每个卖出日 j，最好的买入日就是 j 之前价格最低的那天。所以边扫边记「到目前为止的最低价」。
     * 这其实就是只有两个状态的 DP：minSoFar = 「HOLD 时现金的相反数」，best = 「FREE 时的现金」。
     */
    public static long maxProfitOnce(long[] prices) {
        check(prices);
        long minSoFar = Long.MAX_VALUE;
        long best = 0;
        for (long p : prices) {
            if (p < minSoFar) minSoFar = p;
            else best = Math.max(best, p - minSoFar);
        }
        return best;
    }

    // =====================================================================================
    // Part 2：不限次数（LC 122）
    // =====================================================================================

    /**
     * 不限次数时，一段上涨 a<b<c 可以拆成 (a->b) + (b->c)，利润一样；所以答案 = 所有「今天比昨天高」的差之和。
     * 更严格的说法见讲义：两个状态的 DP free/hold 每天的更新刚好化简成这一行。
     */
    public static long maxProfitUnlimited(long[] prices) {
        check(prices);
        long sum = 0;
        for (int i = 1; i < prices.length; i++) {
            if (prices[i] > prices[i - 1]) sum += prices[i] - prices[i - 1]; // 有 MAX_PRICE/MAX_DAYS 保证不溢出
        }
        return sum;
    }

    // =====================================================================================
    // Part 3：最多 k 次（LC 188）—— 状态机 + 滚动数组
    // =====================================================================================

    /** 「还不可能到达」的哨兵值。取 MIN/4 而不是 MIN：这样 NEG + price - fee 之类的运算也不会溢出。 */
    private static final long NEG = Long.MIN_VALUE / 4;

    /**
     * free[j] = 到今天为止、手里没股票、「最多」做过 j 笔交易时的最大现金；
     * hold[j] = 到今天为止、手里有一股、买入这一股算在 j 笔之内时的最大现金（买股票花了钱，所以通常是负的）。
     * 每天用「昨天的 free/hold」算「今天的 free/hold」：
     *   hold'[j] = max(hold[j],  free[j-1] - price)   休息 或 今天买（买之前只做过 j-1 笔）
     *   free'[j] = max(free[j],  hold[j]   + price)   休息 或 今天卖
     * j 从大到小更新：这样算 j 时 free[j-1] 还没被今天的值覆盖，仍是「昨天的」—— 这就是滚动数组 (rolling array)。
     */
    public static long maxProfitAtMost(int k, long[] prices) {
        if (k < 0) throw new IllegalArgumentException("k < 0");
        check(prices);
        int n = prices.length;
        if (k == 0 || n < 2) return 0;
        if (k >= n / 2) return maxProfitUnlimited(prices); // n 天最多完成 n/2 笔，再多的 k 没有意义；同时避免 O(n*k) 爆炸
        long[] free = new long[k + 1]; // free[j] 初值 0：什么都没做，现金 0
        long[] hold = new long[k + 1];
        Arrays.fill(hold, NEG);        // 还没买过，HOLD 状态不可能到达
        for (long p : prices) {
            for (int j = k; j >= 1; j--) {
                free[j] = Math.max(free[j], hold[j] + p);      // 先用「昨天的 hold[j]」卖
                hold[j] = Math.max(hold[j], free[j - 1] - p);  // 再用「昨天的 free[j-1]」买（j-1 还没更新）
            }
        }
        return free[k];
    }

    // =====================================================================================
    // Part 4：冷却 / 手续费 / 还原交易 —— 同一台状态机，多一个 COOL 状态
    // =====================================================================================

    private record Solved(long profit, State end) {}

    /**
     * 通用 DP。三组滚动数组 free / hold / cool，含义同上，cool[j] = 「今天刚卖出」时的最大现金。
     * 位图 how（可选，plan() 才传）每格记两个比特：bit0 = hold 这个值是「今天买」得来的，bit1 = free 这个值不是「休息」得来的。
     * 平局时一律选「休息」（严格大于才改变），所以不会产生零利润的交易。
     */
    private static Solved run(Rules rules, long[] prices, byte[] how) {
        int n = prices.length;
        boolean unbounded = rules.maxTransactions() >= n / 2;
        int bound = unbounded ? 0 : rules.maxTransactions(); // 无限次时不需要「交易次数」这一维，压成 1 格
        int w = bound + 1;
        long fee = rules.fee();
        long[] free = new long[w];
        long[] hold = new long[w];
        long[] cool = new long[w];
        Arrays.fill(hold, NEG);
        Arrays.fill(cool, NEG);
        for (int i = 1; i <= n; i++) {
            long p = prices[i - 1];
            for (int j = bound; j >= 0; j--) {
                int src = unbounded ? j : j - 1;               // 买入的钱来自 free[src]
                long oldHold = hold[j], oldFree = free[j], oldCool = cool[j];
                long buy = src >= 0 ? free[src] - p : NEG;      // free[src] 此刻仍是昨天的值
                long sell = oldHold + p - fee;
                int bits = 0;
                if (buy > oldHold) { hold[j] = buy; bits |= 1; } else hold[j] = oldHold;
                if (rules.cooldown()) {
                    cool[j] = sell;                              // 今天卖出 -> 进入 COOL
                    if (oldCool > oldFree) { free[j] = oldCool; bits |= 2; } else free[j] = oldFree; // 冷却结束 -> FREE
                } else {
                    if (sell > oldFree) { free[j] = sell; bits |= 2; } else free[j] = oldFree;       // 卖出直接回 FREE
                }
                if (how != null) how[i * w + j] = (byte) bits;
            }
        }
        if (rules.cooldown() && cool[bound] > free[bound]) return new Solved(cool[bound], State.COOL);
        return new Solved(free[bound], State.FREE);
    }

    /** 最大利润，只要数字。时间 O(n * min(k, n/2))，空间 O(min(k, n/2))。 */
    public static long maxProfit(Rules rules, long[] prices) {
        Objects.requireNonNull(rules, "rules");
        check(prices);
        if (prices.length < 2) return 0;
        return run(rules, prices, null).profit();
    }

    /**
     * 最大利润 + 具体怎么买卖。做法：正向 DP 时记下每个格子的「决定」(how)，最后从终点倒着走回起点，
     * 遇到「今天买」或「今天卖」就记一笔。需要 O(n * min(k, n/2)) 字节的空间；太大就拒绝。
     */
    public static Plan plan(Rules rules, long[] prices) {
        Objects.requireNonNull(rules, "rules");
        check(prices);
        int n = prices.length;
        if (n < 2) return new Plan(0, List.of());
        boolean unbounded = rules.maxTransactions() >= n / 2;
        int bound = unbounded ? 0 : rules.maxTransactions();
        int w = bound + 1;
        long cells = (long) (n + 1) * w;
        if (cells > MAX_PLAN_CELLS) throw new IllegalArgumentException("plan too large: " + cells + " cells");
        byte[] how = new byte[(int) cells];
        Solved solved = run(rules, prices, how);

        var reversed = new ArrayList<Trade>(); // 倒着走，所以先放进来的是最后一笔
        State state = solved.end();
        int j = bound;
        int pendingSell = -1;
        for (int i = n; i >= 1; i--) {
            int bits = how[i * w + j];
            int day = i - 1;
            switch (state) {
                case HOLD -> {
                    if ((bits & 1) != 0) { // 这一天买入
                        reversed.add(new Trade(day, pendingSell));
                        pendingSell = -1;
                        state = State.FREE;
                        if (!unbounded) j--;
                    }
                }
                case COOL -> { // 处于 COOL = 这一天卖出
                    pendingSell = day;
                    state = State.HOLD;
                }
                case FREE -> {
                    if ((bits & 2) != 0) {
                        if (rules.cooldown()) state = State.COOL; // 昨天才卖的，今天冷却结束
                        else { pendingSell = day; state = State.HOLD; } // 今天卖出直接回 FREE
                    }
                }
            }
        }
        if (state != State.FREE) throw new AssertionError("backtrack ended in " + state);
        var trades = new ArrayList<Trade>();
        long sum = 0;
        for (Trade t : reversed.reversed()) { // Sequenced Collections：reversed() 给出倒序视图
            long net = prices[t.sellDay()] - prices[t.buyDay()] - rules.fee();
            if (net > 0) { // 平局时 DP 偏向休息，这里是双保险：净利润 <= 0 的交易删掉不影响总利润
                trades.add(t);
                sum += net;
            }
        }
        if (sum != solved.profit()) throw new AssertionError("plan sum " + sum + " != dp " + solved.profit());
        return new Plan(solved.profit(), trades);
    }

    /**
     * 逐天回放一个方案：每天最多一个动作，用 State 状态机检查合法性，返回利润（卖出时扣手续费）。
     * 非法（重叠、冷却期内买入、超过 k 笔、同一天两个动作、日期越界）-> IllegalArgumentException。
     */
    public static long replay(Rules rules, long[] prices, List<Trade> trades) {
        Objects.requireNonNull(rules, "rules");
        Objects.requireNonNull(trades, "trades");
        check(prices);
        int n = prices.length;
        if (trades.size() > rules.maxTransactions())
            throw new IllegalArgumentException(trades.size() + " trades > limit " + rules.maxTransactions());
        var moves = new TreeMap<Integer, Move>();
        for (Trade t : trades) {
            if (t.sellDay() >= n) throw new IllegalArgumentException("day out of range: " + t);
            if (moves.putIfAbsent(t.buyDay(), new Buy(t.buyDay())) != null
                    || moves.putIfAbsent(t.sellDay(), new Sell(t.sellDay())) != null)
                throw new IllegalArgumentException("two actions on one day: " + t);
        }
        State state = State.FREE;
        long cash = 0;
        try {
            for (int day = 0; day < n; day++) {
                state = switch (moves.get(day)) {
                    case null -> state.afterRest();
                    case Buy(var d) -> {
                        cash = Math.subtractExact(cash, prices[d]);
                        yield state.afterBuy();
                    }
                    case Sell(var d) -> {
                        cash = Math.addExact(cash, prices[d] - rules.fee());
                        yield state.afterSell(rules);
                    }
                };
            }
        } catch (IllegalStateException e) {
            throw new IllegalArgumentException("illegal plan: " + e.getMessage(), e);
        }
        return cash;
    }
}
