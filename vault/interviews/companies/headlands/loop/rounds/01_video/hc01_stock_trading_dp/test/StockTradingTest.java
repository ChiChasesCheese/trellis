import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTimeoutPreemptively;
import static org.junit.jupiter.api.Assertions.assertTrue;

import java.time.Duration;
import java.util.List;
import java.util.Random;
import org.junit.jupiter.api.Tag;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.ValueSource;

class StockTradingTest {
    private static final long MAX = StockTrading.MAX_PRICE;

    private static long[] a(long... xs) { return xs; }

    // 独立于被测代码的「标准答案」：枚举所有 (买1<卖1<买2<卖2<...) 的交易序列，不用任何状态机
    private static long oracle(long[] p, int k, long fee, boolean cooldown) {
        return enumerate(p, 0, k, fee, cooldown ? 1 : 0);
    }

    /** 从第 from 天起，最多再做 left 笔，返回能得到的最大利润（可以一笔都不做）。 */
    private static long enumerate(long[] p, int from, int left, long fee, int gap) {
        long best = 0;
        if (left == 0) return 0;
        for (int b = from; b < p.length; b++) {
            for (int s = b + 1; s < p.length; s++) {
                long net = p[s] - p[b] - fee;
                best = Math.max(best, net + enumerate(p, s + 1 + gap, left - 1, fee, gap));
            }
        }
        return best;
    }

    private static long[] randomPrices(Random r, int n, int bound) {
        long[] p = new long[n];
        for (int i = 0; i < n; i++) p[i] = r.nextInt(bound);
        return p;
    }

    private static long[] walk(Random r, int n) {
        long[] p = new long[n];
        long cur = 1_000_000;
        for (int i = 0; i < n; i++) {
            cur = Math.max(1, Math.min(MAX, cur + r.nextInt(2001) - 1000));
            p[i] = cur;
        }
        return p;
    }

    // ============================== Part 1：一次交易 ==============================

    @Test @Tag("part1")
    void lc121Samples() {
        assertEquals(5, StockTrading.maxProfitOnce(a(7, 1, 5, 3, 6, 4)));
        assertEquals(0, StockTrading.maxProfitOnce(a(7, 6, 4, 3, 1)));
        assertEquals(5, StockTrading.maxProfitBrute(a(7, 1, 5, 3, 6, 4)));
        assertEquals(0, StockTrading.maxProfitBrute(a(7, 6, 4, 3, 1)));
    }

    @Test @Tag("part1") @Tag("edge")
    void tinyInputs() {
        for (var f : List.<java.util.function.ToLongFunction<long[]>>of(StockTrading::maxProfitBrute, StockTrading::maxProfitOnce)) {
            assertEquals(0, f.applyAsLong(a()));
            assertEquals(0, f.applyAsLong(a(5)));
            assertEquals(0, f.applyAsLong(a(3, 3, 3)));
            assertEquals(1, f.applyAsLong(a(1, 2)));
            assertEquals(0, f.applyAsLong(a(2, 1)));
            assertEquals(0, f.applyAsLong(a(0, 0)));
        }
    }

    @Test @Tag("part1") @Tag("edge")
    void lowestPriceComesAfterTheHighest() {
        // 常见错误：全局最大 - 全局最小，忽略「先买后卖」的顺序
        assertEquals(0, StockTrading.maxProfitOnce(a(10, 9, 8, 1)));
        assertEquals(4, StockTrading.maxProfitOnce(a(5, 1, 5, 0, 4)));
    }

    @Test @Tag("part1") @Tag("edge")
    void extremePrices() {
        assertEquals(MAX, StockTrading.maxProfitOnce(a(0, MAX)));
        assertEquals(MAX, StockTrading.maxProfitBrute(a(0, MAX)));
        assertEquals(0, StockTrading.maxProfitOnce(a(MAX, 0)));
    }

    @Test @Tag("part1") @Tag("edge")
    void badInputs() {
        assertThrows(NullPointerException.class, () -> StockTrading.maxProfitOnce(null));
        assertThrows(NullPointerException.class, () -> StockTrading.maxProfitBrute(null));
        assertThrows(IllegalArgumentException.class, () -> StockTrading.maxProfitOnce(a(1, -1)));
        assertThrows(IllegalArgumentException.class, () -> StockTrading.maxProfitOnce(a(1, MAX + 1)));
        assertThrows(IllegalArgumentException.class, () -> StockTrading.maxProfitOnce(a(Long.MAX_VALUE, 0)));
        assertThrows(IllegalArgumentException.class, () -> StockTrading.maxProfitBrute(a(-5)));
    }

    @Test @Tag("part1")
    void bruteAndLinearAgreeOnRandomInputs() {
        var r = new Random(0);
        for (int t = 0; t < 400; t++) {
            long[] p = randomPrices(r, r.nextInt(30), 1 + r.nextInt(50));
            assertEquals(StockTrading.maxProfitBrute(p), StockTrading.maxProfitOnce(p), java.util.Arrays.toString(p));
        }
    }

    @Test @Tag("part1") @Tag("perf")
    void oneMillionDaysOnce() {
        long[] p = walk(new Random(0), 1_000_000);
        assertTimeoutPreemptively(Duration.ofSeconds(2), () -> StockTrading.maxProfitOnce(p));
    }

    // ============================== Part 2：不限次数 ==============================

    @Test @Tag("part2")
    void lc122Samples() {
        assertEquals(7, StockTrading.maxProfitUnlimited(a(7, 1, 5, 3, 6, 4)));
        assertEquals(4, StockTrading.maxProfitUnlimited(a(1, 2, 3, 4, 5)));
        assertEquals(0, StockTrading.maxProfitUnlimited(a(7, 6, 4, 3, 1)));
    }

    @Test @Tag("part2") @Tag("edge")
    void unlimitedEdges() {
        assertEquals(0, StockTrading.maxProfitUnlimited(a()));
        assertEquals(0, StockTrading.maxProfitUnlimited(a(9)));
        assertEquals(0, StockTrading.maxProfitUnlimited(a(4, 4, 4, 4)));
    }

    @Test @Tag("part2") @Tag("edge")
    void hugeAlternatingProfitDoesNotOverflow() {
        // 0,MAX,0,MAX,... 2000 天：1000 笔，每笔赚 MAX = 2^40，总共 ~2^50
        long[] p = new long[2000];
        for (int i = 1; i < p.length; i += 2) p[i] = MAX;
        assertEquals(1000 * MAX, StockTrading.maxProfitUnlimited(p));
    }

    @Test @Tag("part2")
    void unlimitedMatchesOracle() {
        var r = new Random(1);
        for (int t = 0; t < 300; t++) {
            long[] p = randomPrices(r, r.nextInt(9), 1 + r.nextInt(20));
            assertEquals(oracle(p, 99, 0, false), StockTrading.maxProfitUnlimited(p), java.util.Arrays.toString(p));
        }
    }

    @Test @Tag("part2") @Tag("perf")
    void oneMillionDaysUnlimited() {
        long[] p = walk(new Random(0), 1_000_000);
        assertTimeoutPreemptively(Duration.ofSeconds(2), () -> StockTrading.maxProfitUnlimited(p));
    }

    // ============================== Part 3：最多 k 次 ==============================

    @Test @Tag("part3")
    void lc188AndLc123Samples() {
        assertEquals(2, StockTrading.maxProfitAtMost(2, a(2, 4, 1)));
        assertEquals(7, StockTrading.maxProfitAtMost(2, a(3, 2, 6, 5, 0, 3)));
        assertEquals(6, StockTrading.maxProfitAtMost(2, a(3, 3, 5, 0, 0, 3, 1, 4))); // LC 123
        assertEquals(4, StockTrading.maxProfitAtMost(1, a(3, 3, 5, 0, 0, 3, 1, 4)));
    }

    @Test @Tag("part3") @Tag("edge")
    void kEdges() {
        assertEquals(0, StockTrading.maxProfitAtMost(0, a(1, 5, 2, 9)));
        assertEquals(0, StockTrading.maxProfitAtMost(3, a()));
        assertEquals(0, StockTrading.maxProfitAtMost(3, a(4)));
        assertEquals(StockTrading.maxProfitOnce(a(7, 1, 5, 3, 6, 4)), StockTrading.maxProfitAtMost(1, a(7, 1, 5, 3, 6, 4)));
        assertThrows(IllegalArgumentException.class, () -> StockTrading.maxProfitAtMost(-1, a(1, 2)));
    }

    @Test @Tag("part3") @Tag("edge")
    void hugeKMustNotAllocateKSizedArrays() {
        long[] p = a(7, 1, 5, 3, 6, 4);
        assertEquals(7, StockTrading.maxProfitAtMost(Integer.MAX_VALUE, p)); // 若 new long[k+1] 会 OOM
        assertEquals(7, StockTrading.maxProfitAtMost(1_000_000_000, p));
        assertEquals(7, StockTrading.maxProfitAtMost(3, p));                  // k == n/2 的临界
    }

    @Test @Tag("part3")
    void matchesOracleAndIsMonotoneInK() {
        var r = new Random(2);
        for (int t = 0; t < 300; t++) {
            long[] p = randomPrices(r, r.nextInt(10), 1 + r.nextInt(25));
            long prev = 0;
            for (int k = 0; k <= 5; k++) {
                long got = StockTrading.maxProfitAtMost(k, p);
                assertEquals(oracle(p, k, 0, false), got, "k=" + k + " " + java.util.Arrays.toString(p));
                assertTrue(got >= prev, "profit must not decrease when k grows");
                prev = got;
            }
        }
    }

    @Test @Tag("part3") @Tag("perf")
    void twoHundredThousandDaysFiftyTransactions() {
        long[] p = walk(new Random(0), 200_000);
        assertTimeoutPreemptively(Duration.ofSeconds(2), () -> StockTrading.maxProfitAtMost(50, p));
    }

    @Test @Tag("part3") @Tag("perf")
    void oneMillionDaysTwoTransactions() {
        long[] p = walk(new Random(0), 1_000_000);
        assertTimeoutPreemptively(Duration.ofSeconds(2), () -> StockTrading.maxProfitAtMost(2, p));
    }

    // ============================== Part 4：冷却 / 手续费 / 还原 ==============================

    @Test @Tag("part4")
    void lc309AndLc714Samples() {
        var cd = StockTrading.Rules.unlimited().withCooldown(true);
        assertEquals(3, StockTrading.maxProfit(cd, a(1, 2, 3, 0, 2)));
        assertEquals(0, StockTrading.maxProfit(cd, a(1)));
        var fee2 = StockTrading.Rules.unlimited().withFee(2);
        assertEquals(8, StockTrading.maxProfit(fee2, a(1, 3, 2, 8, 4, 9)));
        assertEquals(6, StockTrading.maxProfit(StockTrading.Rules.unlimited().withFee(3), a(1, 3, 7, 5, 10, 3)));
    }

    @Test @Tag("part4")
    void rulesReduceToEarlierParts() {
        var r = new Random(3);
        for (int t = 0; t < 100; t++) {
            long[] p = walk(r, 50 + r.nextInt(50));
            assertEquals(StockTrading.maxProfitOnce(p), StockTrading.maxProfit(StockTrading.Rules.atMost(1), p));
            assertEquals(StockTrading.maxProfitUnlimited(p), StockTrading.maxProfit(StockTrading.Rules.unlimited(), p));
            assertEquals(StockTrading.maxProfitAtMost(4, p), StockTrading.maxProfit(StockTrading.Rules.atMost(4), p));
        }
    }

    @Test @Tag("part4") @Tag("edge")
    void feeAndCooldownEdges() {
        // 手续费比任何价差都大：一笔都不做
        assertEquals(0, StockTrading.maxProfit(StockTrading.Rules.unlimited().withFee(100), a(1, 5, 2, 9)));
        // 手续费 == 价差：净利润 0，等于不做
        assertEquals(0, StockTrading.maxProfit(StockTrading.Rules.unlimited().withFee(4), a(1, 5)));
        assertEquals(1, StockTrading.maxProfit(StockTrading.Rules.unlimited().withFee(3), a(1, 5)));
        // 冷却：1,2,1,2 不能第 1 天卖出、第 2 天买入
        assertEquals(1, StockTrading.maxProfit(StockTrading.Rules.unlimited().withCooldown(true), a(1, 2, 1, 2)));
        assertEquals(2, StockTrading.maxProfit(StockTrading.Rules.unlimited(), a(1, 2, 1, 2)));
        assertEquals(0, StockTrading.maxProfit(StockTrading.Rules.atMost(0), a(1, 9)));
    }

    @Test @Tag("part4") @Tag("edge")
    void rulesAreValidated() {
        assertThrows(IllegalArgumentException.class, () -> StockTrading.Rules.atMost(-1));
        assertThrows(IllegalArgumentException.class, () -> StockTrading.Rules.unlimited().withFee(-1));
        assertThrows(IllegalArgumentException.class, () -> StockTrading.Rules.unlimited().withFee(MAX + 1));
        assertThrows(NullPointerException.class, () -> StockTrading.maxProfit(null, a(1, 2)));
        assertThrows(NullPointerException.class, () -> StockTrading.plan(StockTrading.Rules.unlimited(), null));
    }

    @Test @Tag("part4")
    void everyRuleCombinationMatchesOracle() {
        var r = new Random(4);
        for (int t = 0; t < 400; t++) {
            long[] p = randomPrices(r, r.nextInt(10), 1 + r.nextInt(25));
            int k = r.nextInt(5);
            long fee = r.nextInt(4);
            boolean cd = r.nextBoolean();
            var rules = new StockTrading.Rules(k, fee, cd);
            String msg = rules + " " + java.util.Arrays.toString(p);
            assertEquals(oracle(p, k, fee, cd), StockTrading.maxProfit(rules, p), msg);
            assertEquals(oracle(p, k, fee, cd), StockTrading.plan(rules, p).profit(), msg);
        }
    }

    @Test @Tag("part4")
    void planGivesTheObviousTrades() {
        var plan = StockTrading.plan(StockTrading.Rules.unlimited(), a(7, 1, 5, 3, 6, 4));
        assertEquals(7, plan.profit());
        assertEquals(List.of(new StockTrading.Trade(1, 2), new StockTrading.Trade(3, 4)), plan.trades());
        var cd = StockTrading.plan(StockTrading.Rules.unlimited().withCooldown(true), a(1, 2, 3, 0, 2));
        assertEquals(3, cd.profit());
        assertEquals(List.of(new StockTrading.Trade(0, 1), new StockTrading.Trade(3, 4)), cd.trades());
        var one = StockTrading.plan(StockTrading.Rules.atMost(1), a(7, 1, 5, 3, 6, 4));
        assertEquals(List.of(new StockTrading.Trade(1, 4)), one.trades());
        assertEquals(5, one.profit());
    }

    @Test @Tag("part4") @Tag("edge")
    void planOfNothing() {
        assertEquals(new StockTrading.Plan(0, List.of()), StockTrading.plan(StockTrading.Rules.unlimited(), a()));
        assertEquals(new StockTrading.Plan(0, List.of()), StockTrading.plan(StockTrading.Rules.unlimited(), a(4)));
        assertEquals(new StockTrading.Plan(0, List.of()), StockTrading.plan(StockTrading.Rules.unlimited(), a(5, 4, 3)));
        assertEquals(new StockTrading.Plan(0, List.of()), StockTrading.plan(StockTrading.Rules.atMost(0), a(1, 9)));
        assertEquals(new StockTrading.Plan(0, List.of()), StockTrading.plan(StockTrading.Rules.unlimited().withFee(50), a(1, 9, 1, 9)));
    }

    /** 独立检查：交易按时间排序、互不重叠、冷却、笔数、每笔净利润 > 0、总和 == profit。 */
    private static void assertValidPlan(StockTrading.Rules rules, long[] p, StockTrading.Plan plan) {
        long sum = 0;
        int prevSell = -10;
        assertTrue(plan.trades().size() <= rules.maxTransactions());
        for (var t : plan.trades()) {
            if (prevSell >= 0) assertTrue(t.buyDay() > prevSell, "trades overlap: " + t);
            if (rules.cooldown() && prevSell >= 0) assertTrue(t.buyDay() >= prevSell + 2, "cooldown violated: " + t);
            assertTrue(t.sellDay() < p.length);
            long net = p[t.sellDay()] - p[t.buyDay()] - rules.fee();
            assertTrue(net > 0, "non-positive trade " + t);
            sum += net;
            prevSell = t.sellDay();
        }
        assertEquals(plan.profit(), sum);
    }

    @Test @Tag("part4")
    void planIsAlwaysAValidPlan() {
        var r = new Random(5);
        for (int t = 0; t < 400; t++) {
            long[] p = randomPrices(r, r.nextInt(40), 1 + r.nextInt(30));
            var rules = new StockTrading.Rules(r.nextBoolean() ? StockTrading.Rules.UNLIMITED : r.nextInt(6), r.nextInt(4), r.nextBoolean());
            var plan = StockTrading.plan(rules, p);
            assertEquals(StockTrading.maxProfit(rules, p), plan.profit());
            assertValidPlan(rules, p, plan);
            assertEquals(plan.profit(), StockTrading.replay(rules, p, plan.trades()));
        }
    }

    @Test @Tag("part4") @Tag("edge")
    void planRefusesHugeTables() {
        long[] p = new long[100_000];
        assertThrows(IllegalArgumentException.class, () -> StockTrading.plan(StockTrading.Rules.atMost(50_000 - 1), p));
    }

    @Test @Tag("part4")
    void stateMachineTransitions() {
        var cd = StockTrading.Rules.unlimited().withCooldown(true);
        var plain = StockTrading.Rules.unlimited();
        assertEquals(StockTrading.State.HOLD, StockTrading.State.FREE.afterBuy());
        assertEquals(StockTrading.State.COOL, StockTrading.State.HOLD.afterSell(cd));
        assertEquals(StockTrading.State.FREE, StockTrading.State.HOLD.afterSell(plain));
        assertEquals(StockTrading.State.FREE, StockTrading.State.COOL.afterRest());
        assertEquals(StockTrading.State.FREE, StockTrading.State.FREE.afterRest());
        assertEquals(StockTrading.State.HOLD, StockTrading.State.HOLD.afterRest());
        assertThrows(IllegalStateException.class, () -> StockTrading.State.COOL.afterBuy());
        assertThrows(IllegalStateException.class, () -> StockTrading.State.HOLD.afterBuy());
        assertThrows(IllegalStateException.class, () -> StockTrading.State.FREE.afterSell(plain));
        assertThrows(IllegalStateException.class, () -> StockTrading.State.COOL.afterSell(cd));
    }

    @Test @Tag("part4")
    void replayAcceptsLegalAndComputesProfit() {
        long[] p = a(1, 2, 3, 0, 2);
        assertEquals(3, StockTrading.replay(StockTrading.Rules.unlimited().withCooldown(true), p,
                List.of(new StockTrading.Trade(0, 1), new StockTrading.Trade(3, 4))));
        // 手续费：每笔卖出扣一次
        assertEquals(3 - 2, StockTrading.replay(StockTrading.Rules.unlimited().withFee(1), p,
                List.of(new StockTrading.Trade(0, 1), new StockTrading.Trade(3, 4))));
        assertEquals(0, StockTrading.replay(StockTrading.Rules.unlimited(), p, List.of()));
    }

    @Test @Tag("part4") @Tag("edge")
    void replayRejectsIllegalPlans() {
        long[] p = a(1, 2, 3, 0, 2, 5);
        var cd = StockTrading.Rules.unlimited().withCooldown(true);
        var plain = StockTrading.Rules.unlimited();
        // 重叠
        assertThrows(IllegalArgumentException.class, () -> StockTrading.replay(plain, p,
                List.of(new StockTrading.Trade(0, 3), new StockTrading.Trade(1, 4))));
        // 冷却期内买入：第 1 天卖，第 2 天买
        assertThrows(IllegalArgumentException.class, () -> StockTrading.replay(cd, p,
                List.of(new StockTrading.Trade(0, 1), new StockTrading.Trade(2, 5))));
        // 没有冷却时，同样的方案合法：(2-1) + (5-3)
        assertEquals(3, StockTrading.replay(plain, p,
                List.of(new StockTrading.Trade(0, 1), new StockTrading.Trade(2, 5))));
        // 超过 k 笔
        assertThrows(IllegalArgumentException.class, () -> StockTrading.replay(StockTrading.Rules.atMost(1), p,
                List.of(new StockTrading.Trade(0, 1), new StockTrading.Trade(3, 4))));
        // 同一天两个动作
        assertThrows(IllegalArgumentException.class, () -> StockTrading.replay(plain, p,
                List.of(new StockTrading.Trade(0, 2), new StockTrading.Trade(2, 4))));
        // 日期越界
        assertThrows(IllegalArgumentException.class, () -> StockTrading.replay(plain, p, List.of(new StockTrading.Trade(4, 6))));
    }

    @ParameterizedTest @Tag("part4") @Tag("edge")
    @ValueSource(ints = {0, 1, 2, 3})
    void tinyTablesSurvive(int n) {
        long[] p = new long[n];
        for (int i = 0; i < n; i++) p[i] = i * 3L % 5;
        for (int k = 0; k <= 3; k++) {
            for (boolean cd : new boolean[] {false, true}) {
                var rules = new StockTrading.Rules(k, 1, cd);
                assertEquals(oracle(p, k, 1, cd), StockTrading.maxProfit(rules, p));
                assertEquals(oracle(p, k, 1, cd), StockTrading.plan(rules, p).profit());
            }
        }
    }

    @Test @Tag("part4") @Tag("perf")
    void millionDaysUnlimitedWithCooldownAndFee() {
        long[] p = walk(new Random(0), 1_000_000);
        var rules = StockTrading.Rules.unlimited().withCooldown(true).withFee(500);
        assertTimeoutPreemptively(Duration.ofSeconds(2), () -> StockTrading.maxProfit(rules, p));
    }

    @Test @Tag("part4") @Tag("perf")
    void planOverHundredThousandDays() {
        long[] p = walk(new Random(0), 100_000);
        var unlimited = StockTrading.Rules.unlimited().withCooldown(true).withFee(300);
        var limited = new StockTrading.Rules(20, 100, false);
        assertTimeoutPreemptively(Duration.ofSeconds(2), () -> {
            var a1 = StockTrading.plan(unlimited, p);
            var a2 = StockTrading.plan(limited, p);
            assertValidPlan(unlimited, p, a1);
            assertValidPlan(limited, p, a2);
            assertEquals(a2.profit(), StockTrading.replay(limited, p, a2.trades()));
            assertFalse(a1.trades().isEmpty());
        });
    }

    @Test @Tag("part4") @Tag("perf")
    void twoThousandDaysFiveHundredTransactions() {
        long[] p = walk(new Random(7), 2_000);
        var rules = new StockTrading.Rules(500, 0, true);
        assertTimeoutPreemptively(Duration.ofSeconds(2), () -> StockTrading.plan(rules, p));
    }
}
