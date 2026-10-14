/**
 * J03 旧写法：Java 8 的 switch 只能判断「值」（int / enum / String），不能判断「类型」。
 * 要按类型分派，只能 instanceof + 强转 的链条；而 switch 遇到 null 直接 NPE。
 */
public class J03Old {

    interface Shape {}
    static final class Circle implements Shape { final double r; Circle(double r) { this.r = r; } }
    static final class Rect implements Shape { final double w, h; Rect(double w, double h) { this.w = w; this.h = h; } }

    /** 类型分派：if-else 链。顺序、强转、兜底都靠人。 */
    static double area(Shape s) {
        if (s instanceof Circle) {
            Circle c = (Circle) s;
            return Math.PI * c.r * c.r;
        } else if (s instanceof Rect) {
            Rect r = (Rect) s;
            return r.w * r.h;
        }
        throw new IllegalArgumentException("unknown shape");
    }

    /** 老 switch：只能是 String 常量，而且 null 会 NPE，而且忘写 break 会 fall-through。 */
    static String label(String cmd) {
        switch (cmd) {
            case "BUY":
                return "b";
            case "SELL":
                return "s";
            default:
                return "?";
        }
    }

    public static void main(String[] args) {
        System.out.println(area(new Rect(2, 3)));
        System.out.println(label("BUY"));
        try {
            label(null);
        } catch (NullPointerException e) {
            System.out.println("switch (null) 抛 NPE");
        }
    }
}
