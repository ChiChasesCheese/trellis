/** J13 例 2：未命名模式——switch 里只关心"是哪种类型"，不关心字段；record 解构里跳过不要的字段。 */
public class J13Ex2 {
    sealed interface Event permits Fill, Cancel, Reject, Heartbeat {}
    record Fill(long orderId, long qty, long px) implements Event {}
    record Cancel(long orderId) implements Event {}
    record Reject(long orderId, String reason) implements Event {}
    record Heartbeat() implements Event {}

    static String label(Event e) {
        return switch (e) {
            case Fill _ -> "FILL";                              // 未命名模式变量：只要类型
            case Cancel _, Reject _ -> "TERMINAL";              // 多个模式共用一个分支：只有全是 _ 才允许
            case Heartbeat _ -> "HB";
        };
    }

    static long idOf(Event e) {
        return switch (e) {
            case Fill(var id, _, _) -> id;                      // 未命名模式：占位但不绑定
            case Cancel(var id) -> id;
            case Reject(var id, _) -> id;
            case Heartbeat() -> -1;
        };
    }

    public static void main(String[] args) {
        Event[] es = { new Fill(1, 100, 18950), new Cancel(2), new Reject(3, "price"), new Heartbeat() };
        for (Event e : es) System.out.println(e + " -> " + label(e) + ", id=" + idOf(e));
    }
}
