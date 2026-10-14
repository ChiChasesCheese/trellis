import java.util.*;
import java.util.stream.*;

/** J14 例 1（最简单）：Stream.toList()、三参数 iterate、takeWhile/dropWhile、ofNullable。 */
public class J14Ex1 {
    public static void main(String[] args) {
        // 1. toList()（Java 16）：返回不可修改列表
        List<Integer> a = Stream.of(3, 1, 2).toList();
        try { a.add(4); } catch (UnsupportedOperationException e) { System.out.println("toList() 不可修改 -> UOE"); }

        //    collect(Collectors.toList())：不保证类型，实际是可变 ArrayList
        List<Integer> b = Stream.of(3, 1, 2).collect(Collectors.toList());
        b.add(4);
        System.out.println("collect(toList()) 可修改: " + b);

        //    toList() 允许 null 元素；List.of / Collectors.toUnmodifiableList() 不允许
        List<String> withNull = Stream.of("x", null, "y").toList();
        System.out.println("toList 带 null: " + withNull);
        try { Stream.of("x", null).collect(Collectors.toUnmodifiableList()); }
        catch (NullPointerException e) { System.out.println("toUnmodifiableList 遇到 null -> NPE"); }

        // 2. 三参数 iterate（Java 9）：像 for 循环——初值、继续条件、步进
        System.out.println(Stream.iterate(1, x -> x < 200, x -> x * 3).toList());

        // 3. takeWhile / dropWhile（Java 9）：对"有序"的流按条件截取头部 / 丢掉头部
        List<Integer> prices = List.of(1, 2, 3, 10, 2, 1);
        System.out.println("takeWhile(<5): " + prices.stream().takeWhile(x -> x < 5).toList());
        System.out.println("dropWhile(<5): " + prices.stream().dropWhile(x -> x < 5).toList());
        System.out.println("filter(<5)   : " + prices.stream().filter(x -> x < 5).toList());   // 对照：filter 不会停

        // 4. Stream.ofNullable（Java 9）：null -> 空流，否则单元素流
        String maybe = null;
        System.out.println("ofNullable(null).count = " + Stream.ofNullable(maybe).count());

        // 5. 数值流的 range：不要装箱
        System.out.println("sum 1..100 = " + IntStream.rangeClosed(1, 100).sum());
    }
}
