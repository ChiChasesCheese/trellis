import java.util.ArrayList;
import java.util.List;
import java.util.function.BiFunction;

/** J08 例 2（进阶）：推断规则与陷阱。字面量的默认类型、diamond 的退化、不可写出的类型、lambda 形参里的 var。 */
public class J08Ex2 {

    public static void main(String[] args) {
        // 1. 字面量的默认类型：整数字面量是 int，不是 long
        var a = 18_950;           // int
        var b = 18_950L;          // long
        var c = 1.5;              // double
        var d = 'x';              // char
        System.out.println(((Object) a).getClass().getSimpleName() + " " + ((Object) b).getClass().getSimpleName()
                + " " + ((Object) c).getClass().getSimpleName() + " " + ((Object) d).getClass().getSimpleName());

        // 2. 因此：var 让「类型不再显然」时会藏 bug —— int 乘法溢出
        var px = 3_000_000;       // int
        var qty = 3_000;          // int
        var wrong = px * qty;     // int * int = int，溢出！
        var right = (long) px * qty;
        System.out.println(wrong + " vs " + right);

        // 3. diamond + var：右边没有类型信息可推，退化为 Object
        var list1 = new ArrayList<>();        // ArrayList<Object>
        list1.add("a");
        list1.add(1);                         // 居然能加：因为元素类型是 Object
        List<String> list2 = new ArrayList<>();   // 这里右边的 <> 从左边推出 String
        System.out.println(list1 + " " + list2);

        // 4. 不可写出的类型（non-denotable）：匿名类。var 能保留匿名类里的新成员，显式写类型做不到
        var anon = new Object() {
            int hits = 0;
            void hit() { hits++; }
        };
        anon.hit();
        anon.hit();
        System.out.println(anon.hits);        // 2 —— 如果写成 Object anon = new Object() {...}，anon.hit() 编译不过

        // 5. 条件表达式产生的交叉类型（intersection type）也写不出名字
        var mixed = args.length == 0 ? 1 : "one";   // 类型是 Serializable & Comparable<...>... 的交集
        System.out.println(mixed);

        // 6. lambda 形参里的 var（Java 11）：只是为了能给形参加注解，类型仍由目标类型推出
        BiFunction<Long, Long, Long> add = (var x, var y) -> x + y;
        System.out.println(add.apply(2L, 3L));

        // 7. 下面这些在编译期被拒绝（见 J08.md 第 2 节）：
        //   var u;                         // 没有初始化器
        //   var n = null;                  // null 没有类型
        //   var arr = {1, 2, 3};           // 数组初始化器需要目标类型
        //   var f = () -> 1;               // lambda 需要目标类型
        //   var m = String::length;        // 方法引用同理
    }
}
