import java.util.ArrayList;
import java.util.List;

/** J03 例 3（贴近真实）：订单校验 —— 从上到下第一个匹配的分支生效；最后无守卫分支让编译器检查穷尽。 */
public class J03Ex3 {

    enum Side { BUY, SELL }

    sealed interface Command permits Limit, Market, Cancel {}
    record Limit(long id, Side side, long price, long qty) implements Command {}
    record Market(long id, Side side, long qty) implements Command {}
    record Cancel(long id) implements Command {}

    /** 返回 null 表示通过；否则是第一个发现的错误。更具体的错误写在前面。 */
    static String validate(Command cmd, java.util.Set<Long> knownIds) {
        return switch (cmd) {
            case Limit l when l.id() <= 0 -> "INVALID_ID";
            case Limit l when l.price() <= 0 -> "INVALID_PRICE";
            case Limit l when l.qty() <= 0 -> "INVALID_QTY";
            case Market m when m.id() <= 0 -> "INVALID_ID";
            case Market m when m.qty() <= 0 -> "INVALID_QTY";
            case Cancel c when c.id() <= 0 -> "INVALID_ID";
            // 以下三行没有守卫：既处理「通过格式校验后」的状态检查，又让编译器验证 sealed 被覆盖
            case Limit l -> knownIds.contains(l.id()) ? "DUPLICATE_ID" : null;
            case Market m -> knownIds.contains(m.id()) ? "DUPLICATE_ID" : null;
            case Cancel c -> knownIds.contains(c.id()) ? null : "UNKNOWN_ID";
        };
    }

    public static void main(String[] args) {
        var known = java.util.Set.of(1L, 2L);
        List<Command> cmds = new ArrayList<>(List.of(
                new Limit(0, Side.BUY, 100, 5), new Limit(3, Side.BUY, 0, 5), new Limit(3, Side.SELL, 100, 0),
                new Limit(1, Side.BUY, 100, 5), new Limit(3, Side.BUY, 100, 5),
                new Market(4, Side.SELL, -1), new Cancel(1), new Cancel(9)));
        for (Command c : cmds) System.out.println(c + " -> " + validate(c, known));
    }
}
