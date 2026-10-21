import java.util.Locale;

/** J05 例 3（贴近真实）：解析命令行文本、手续费阶梯、方向取反；每一处都是「一个表达式产出一个值」。 */
public class J05Ex3 {

    enum Side {
        BUY, SELL;
        Side opposite() {
            return switch (this) { case BUY -> SELL; case SELL -> BUY; };
        }
    }

    sealed interface Command permits Limit, Cancel {}
    record Limit(long id, Side side, long px, long qty) implements Command {}
    record Cancel(long id) implements Command {}

    /** 一个 switch 表达式直接产出 Command；每个分支做不同数量的参数检查，所以用块 + yield。 */
    static Command parse(String line) {
        String[] t = line.strip().split("\\s+");
        return switch (t[0].toUpperCase(Locale.ROOT)) {
            case "LIMIT" -> {
                need(t, 5);
                yield new Limit(Long.parseLong(t[1]), Side.valueOf(t[2].toUpperCase(Locale.ROOT)),
                        Long.parseLong(t[3]), Long.parseLong(t[4]));
            }
            case "CANCEL" -> {
                need(t, 2);
                yield new Cancel(Long.parseLong(t[1]));
            }
            default -> throw new IllegalArgumentException("unknown command: " + t[0]);
        };
    }

    static void need(String[] t, int n) {
        if (t.length != n) throw new IllegalArgumentException(t[0] + " needs " + (n - 1) + " args");
    }

    enum Liquidity { MAKER, TAKER }

    /** 手续费（基点，负数 = 返佣）：做市方返佣，吃单方付基础费 + 小额订单附加费。需要局部变量就用块 + yield。 */
    static int feeBps(Liquidity liq, long notional) {
        return switch (liq) {
            case MAKER -> -2;
            case TAKER -> {
                int base = 3;
                int surcharge = notional < 10_000 ? 2 : 0;
                yield base + surcharge;
            }
        };
    }

    public static void main(String[] args) {
        System.out.println(parse("limit 7 buy 18950 100"));
        System.out.println(parse(" CANCEL 7 "));
        try {
            parse("limit 1 buy");
        } catch (IllegalArgumentException e) {
            System.out.println("error: " + e.getMessage());
        }
        try {
            parse("modify 1 2");
        } catch (IllegalArgumentException e) {
            System.out.println("error: " + e.getMessage());
        }
        System.out.println(Side.BUY.opposite() + " " + Side.SELL.opposite());
        System.out.println(feeBps(Liquidity.MAKER, 5_000) + " " + feeBps(Liquidity.TAKER, 5_000) + " " + feeBps(Liquidity.TAKER, 2_000_000));
    }
}
