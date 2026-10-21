import java.util.List;

/** J06 例 2（进阶）：绑定变量的作用域规则（flow scoping）；&& 可以、|| 不行；三元运算符；while；final；泛型；全覆盖模式。 */
public class J06Ex2 {

    static String and(Object o) {
        // && : 左边为 true 时才算右边，所以右边可以用 s
        return (o instanceof String s && !s.isEmpty()) ? "nonempty string " + s : "no";
    }

    static String or(Object o) {
        // A || B：B 只在 A 为 false 时才求值。A 是 !(o instanceof String s)，它为 false 恰好说明匹配成功，所以 s 在 B 里可用
        if (!(o instanceof String s) || s.isEmpty()) {
            return "not a nonempty string";            // 这里 s 不可用（可能没匹配）
        }
        return "string " + s;                            // 这里 s 可用（因为上面的 if 没进去）
    }

    static int sumUntilNonInt(List<Object> xs) {
        int sum = 0;
        int i = 0;
        // while 的条件里绑定变量：循环体里可用
        while (i < xs.size() && xs.get(i) instanceof Integer n) {
            sum += n;
            i++;
        }
        return sum;
    }

    static String generic(Object o) {
        // 泛型：运行时擦除，所以只允许「类型可以由已知信息推出」的情形
        if (o instanceof List<?> l) {
            return "list of " + l.size();
        }
        return "not a list";
    }

    static String generic2(List<String> ls) {
        // 静态类型是 List<String> 时，List<String> 的模式是安全的（不会出现 ClassCastException）
        if (ls instanceof java.util.ArrayList<String> al) {
            return "arraylist " + al.size();
        }
        return "other list";
    }

    static String finalBinding(Object o) {
        if (o instanceof final String s) {           // 可以写 final，禁止对 s 重新赋值
            return s.toUpperCase();
        }
        return "?";
    }

    static String total(String s) {
        // Java 21：模式类型就是表达式的静态类型（总是匹配，除非 null）也允许；Java 16-20 对此报编译错误
        if (s instanceof String t) {
            return "string " + t;
        }
        return "null!";
    }

    public static void main(String[] args) {
        System.out.println(and("x") + " | " + and("") + " | " + and(1));
        System.out.println(or("x") + " | " + or("") + " | " + or(1));
        System.out.println(sumUntilNonInt(List.of(1, 2, 3, "stop", 4)));
        System.out.println(generic(List.of(1, 2)) + " | " + generic("no"));
        System.out.println(generic2(new java.util.ArrayList<>(List.of("a"))) + " | " + generic2(List.of("a")));
        System.out.println(finalBinding("abc"));
        System.out.println(total("a") + " | " + total(null));
    }
}
