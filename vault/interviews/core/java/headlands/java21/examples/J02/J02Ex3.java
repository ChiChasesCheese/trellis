import java.util.ArrayList;
import java.util.List;

/** J02 例 3（贴近真实）：交易引擎的 Command / Event 两棵封闭层级；子接口分层；分派在一处，新增变体时编译器逼你补。 */
public class J02Ex3 {

    enum Side { BUY, SELL }

    // ---- 命令：外部发给引擎的指令，恰好两种 ----
    sealed interface Command permits Limit, Cancel {
        long id();
    }
    record Limit(long id, Side side, long px, long qty) implements Command {}
    record Cancel(long id) implements Command {}

    // ---- 事件：引擎的输出，恰好三种 ----
    sealed interface Event permits Rested, Cancelled, Rejected {}
    record Rested(long id, long px, long qty) implements Event {}
    record Cancelled(long id) implements Event {}
    record Rejected(long id, String why) implements Event {}

    /** 引擎只有这一个入口，所有「按种类分派」都集中在这个 switch。 */
    static List<Event> execute(Command c, List<Long> restingIds) {
        List<Event> out = new ArrayList<>();
        switch (c) {
            case Limit l -> {
                if (l.qty() <= 0) { out.add(new Rejected(l.id(), "qty")); }
                else { restingIds.add(l.id()); out.add(new Rested(l.id(), l.px(), l.qty())); }
            }
            case Cancel x -> {
                if (restingIds.remove(Long.valueOf(x.id()))) out.add(new Cancelled(x.id()));
                else out.add(new Rejected(x.id(), "unknown id"));
            }
        }
        return out;
    }

    static String render(Event e) {
        return switch (e) {
            case Rested r -> "REST id=%d px=%d qty=%d".formatted(r.id(), r.px(), r.qty());
            case Cancelled c -> "CANCEL id=" + c.id();
            case Rejected j -> "REJECT id=" + j.id() + " why=" + j.why();
        };
    }

    public static void main(String[] args) {
        List<Long> resting = new ArrayList<>();
        List<Command> script = List.of(
                new Limit(1, Side.BUY, 100, 5), new Limit(2, Side.SELL, 101, 0),
                new Cancel(1), new Cancel(9));
        for (Command c : script) {
            for (Event e : execute(c, resting)) System.out.println(render(e));
        }
        System.out.println(Command.class.getPermittedSubclasses().length + " 种命令, "
                + Event.class.getPermittedSubclasses().length + " 种事件");
    }
}
