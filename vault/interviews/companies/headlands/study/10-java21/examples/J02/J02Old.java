import java.util.List;

/**
 * J02 旧写法：Java 8 里「一组固定的变体」只能靠约定。
 * 事件接口是开放的：任何人都能再实现它；而分派逻辑只能用 instanceof 链 + 兜底 else。
 */
public class J02Old {

    interface Event {}
    static final class Trade implements Event {
        final long price, qty;
        Trade(long price, long qty) { this.price = price; this.qty = qty; }
    }
    static final class Rested implements Event {
        final long price, qty;
        Rested(long price, long qty) { this.price = price; this.qty = qty; }
    }
    static final class Cancelled implements Event {
        final long id;
        Cancelled(long id) { this.id = id; }
    }

    /** 一年后有人新增了 Rejected 事件，但没人记得这里要改——编译器不会提醒，直到线上抛异常。 */
    static String describe(Event e) {
        if (e instanceof Trade) {
            Trade t = (Trade) e;                       // 还得再强转一次
            return "TRADE " + t.qty + "@" + t.price;
        } else if (e instanceof Rested) {
            Rested r = (Rested) e;
            return "REST " + r.qty + "@" + r.price;
        } else if (e instanceof Cancelled) {
            return "CANCEL " + ((Cancelled) e).id;
        } else {
            throw new IllegalStateException("unknown event: " + e);   // 兜底：只能运行时才发现漏了
        }
    }

    /** 新来的第四种事件：写在别的文件、别的包、甚至别的团队的代码里都行。 */
    static final class Rejected implements Event {}

    public static void main(String[] args) {
        for (Event e : List.of(new Trade(100, 5), new Rested(101, 3), new Cancelled(7))) {
            System.out.println(describe(e));
        }
        try {
            describe(new Rejected());
        } catch (IllegalStateException ex) {
            System.out.println("运行时才炸: " + ex.getMessage().substring(0, 24) + "...");
        }
    }
}
