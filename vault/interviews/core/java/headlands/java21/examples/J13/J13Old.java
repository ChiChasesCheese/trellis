import java.util.*;

/** J13 旧写法（Java 8 风格）：不用的变量也必须起名，于是满屏 ignored / unused / e。 */
public class J13Old {
    sealed interface Event permits Fill, Cancel, Reject {}
    record Fill(long orderId, long qty) implements Event {}
    record Cancel(long orderId) implements Event {}
    record Reject(long orderId, String reason) implements Event {}

    static int parseOrDefault(String s) {
        try {
            return Integer.parseInt(s);
        } catch (NumberFormatException e) {   // e 根本没用，但必须叫点什么
            return -1;
        }
    }

    public static void main(String[] args) {
        Map<String, Integer> counts = new HashMap<>();
        List<String> names = List.of("a", "b", "c");
        int n = 0;
        for (String ignored : names) {         // 只想数个数，却要声明一个用不到的变量
            n++;
        }
        counts.computeIfAbsent("k", k -> 0);   // k 没用到

        Event ev = new Reject(7, "price");
        long id;
        if (ev instanceof Fill f) id = f.orderId();            // 只要 orderId，却要绑定整个 f
        else if (ev instanceof Cancel c) id = c.orderId();
        else if (ev instanceof Reject r) id = r.orderId();
        else throw new IllegalStateException();
        System.out.println(n + " " + parseOrDefault("x") + " " + id);
    }
}
