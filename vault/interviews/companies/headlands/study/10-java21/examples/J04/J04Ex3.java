/** J04 例 3（贴近真实）：一棵「价格表达式」树 + 递归求值；以及对订单事件做嵌套拆解。 */
public class J04Ex3 {

    // ---- 表达式树：常量、加、乘、取反 —— 一个典型的代数数据类型 ----
    sealed interface Expr permits Const, Add, Mul, Neg {}
    record Const(long value) implements Expr {}
    record Add(Expr left, Expr right) implements Expr {}
    record Mul(Expr left, Expr right) implements Expr {}
    record Neg(Expr inner) implements Expr {}

    static long eval(Expr e) {
        return switch (e) {
            case Const(var v) -> v;
            case Add(var l, var r) -> eval(l) + eval(r);
            case Mul(var l, var r) -> eval(l) * eval(r);
            case Neg(var x) -> -eval(x);
        };
    }

    /** 化简：嵌套模式一次看两层。0 + x -> x；x * 1 -> x；--x -> x。 */
    static Expr simplify(Expr e) {
        return switch (e) {
            case Add(Const(var a), var r) when a == 0 -> simplify(r);
            case Add(var l, Const(var b)) when b == 0 -> simplify(l);
            case Mul(var l, Const(var b)) when b == 1 -> simplify(l);
            case Mul(Const(var a), var r) when a == 1 -> simplify(r);
            case Neg(Neg(var x)) -> simplify(x);                      // 双重否定
            case Add(var l, var r) -> new Add(simplify(l), simplify(r));
            case Mul(var l, var r) -> new Mul(simplify(l), simplify(r));
            case Neg(var x) -> new Neg(simplify(x));
            case Const c -> c;
        };
    }

    static String show(Expr e) {
        return switch (e) {
            case Const(var v) -> Long.toString(v);
            case Add(var l, var r) -> "(" + show(l) + " + " + show(r) + ")";
            case Mul(var l, var r) -> show(l) + " * " + show(r);
            case Neg(var x) -> "-" + show(x);
        };
    }

    // ---- 订单事件：对一条成交按买卖方向格式化 ----
    enum Side { BUY, SELL }
    sealed interface Event permits Trade, Rested {}
    record Trade(long taker, long maker, Side side, long px, long qty) implements Event {}
    record Rested(long id, Side side, long px, long qty) implements Event {}

    static String line(Event ev) {
        return switch (ev) {
            case Trade(var taker, var maker, Side side, var px, var qty) when side == Side.BUY ->
                    "BOUGHT %d@%d (taker %d <- maker %d)".formatted(qty, px, taker, maker);
            case Trade(var taker, var maker, var side, var px, var qty) ->
                    "SOLD %d@%d (taker %d -> maker %d)".formatted(qty, px, taker, maker);
            case Rested(var id, var side, var px, var qty) -> "REST %d %s %d@%d".formatted(id, side, qty, px);
        };
    }

    public static void main(String[] args) {
        Expr e = new Add(new Const(0), new Mul(new Add(new Const(2), new Const(3)), new Neg(new Neg(new Const(1)))));
        System.out.println(show(e) + " = " + eval(e));
        Expr s = simplify(e);
        System.out.println(show(s) + " = " + eval(s));

        System.out.println(line(new Trade(4, 1, Side.BUY, 101, 5)));
        System.out.println(line(new Trade(6, 5, Side.SELL, 103, 4)));
        System.out.println(line(new Rested(5, Side.BUY, 103, 4)));
    }
}
