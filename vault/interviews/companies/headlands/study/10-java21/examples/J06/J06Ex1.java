/** J06 例 1（最简单）：instanceof + 绑定变量；&& 里直接使用；null 不匹配。 */
public class J06Ex1 {

    public static void main(String[] args) {
        Object o = "hello";

        // 新写法：判断 + 声明变量 + 转型，一步完成
        if (o instanceof String s) {
            System.out.println(s.length());      // s 已经是 String，不用强转
        }

        // 可以在同一个条件里立刻继续用 s
        if (o instanceof String s && s.length() > 3) {
            System.out.println("long string: " + s);
        }

        // null 永远不匹配（和旧 instanceof 一致）
        Object n = null;
        System.out.println(n instanceof String);        // false
        if (n instanceof String t) {
            System.out.println("unreachable " + t);
        } else {
            System.out.println("null is not a String");
        }

        // 取反 + 提前返回：之后 s2 在整个方法剩余部分可用
        System.out.println(firstChar("abc") + " " + firstChar(42));
    }

    static String firstChar(Object o) {
        if (!(o instanceof String s)) {
            return "not a string";
        }
        return "first char of " + s + " is " + s.charAt(0);    // s 在这里可用！
    }
}
