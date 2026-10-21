import java.util.ArrayDeque;
import java.util.ArrayList;
import java.util.Deque;
import java.util.List;
import java.util.NoSuchElementException;

/** J09 例 1（最简单）：List 与 Deque 的两端操作；空集合抛 NoSuchElementException；reversed() 是「视图」不是拷贝。 */
public class J09Ex1 {

    public static void main(String[] args) {
        List<String> list = new ArrayList<>(List.of("a", "b", "c"));

        System.out.println(list.getFirst() + " " + list.getLast());     // a c   —— 以前要 list.get(0) / list.get(list.size() - 1)
        list.addFirst("z");
        list.addLast("d");
        System.out.println(list);                                        // [z, a, b, c, d]
        System.out.println(list.removeFirst() + " " + list.removeLast()); // z d
        System.out.println(list);                                        // [a, b, c]

        // 空集合：抛 NoSuchElementException（不是 IndexOutOfBounds，也不是返回 null）
        try {
            new ArrayList<String>().getFirst();
        } catch (NoSuchElementException e) {
            System.out.println("empty list -> NoSuchElementException");
        }

        // reversed()：返回一个「倒过来看」的视图，不拷贝；通过它修改，原集合也变
        List<String> rev = list.reversed();
        System.out.println(rev);                                         // [c, b, a]
        rev.addFirst("LAST");                                            // 在视图的头加 == 在原列表的尾加
        System.out.println(list);                                        // [a, b, c, LAST]
        list.add("tail");
        System.out.println(rev);                                         // [tail, LAST, c, b, a] —— 原列表变了，视图跟着变

        // 不可变列表：读取两端可以，修改抛 UnsupportedOperationException
        List<Integer> fixed = List.of(1, 2, 3);
        System.out.println(fixed.getLast() + " " + fixed.reversed());
        try {
            fixed.addFirst(0);
        } catch (UnsupportedOperationException e) {
            System.out.println("List.of(...).addFirst -> UnsupportedOperationException");
        }

        // Deque 现在也是 SequencedCollection：同样的方法名，reversed() 返回 Deque
        Deque<String> dq = new ArrayDeque<>(List.of("x", "y", "z"));
        System.out.println(dq.getFirst() + " " + dq.getLast() + " " + dq.reversed());
    }
}
