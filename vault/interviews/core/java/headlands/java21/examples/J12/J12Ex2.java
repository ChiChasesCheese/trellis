/** J12 例 2：嵌套重绑定（遮蔽）、同时绑定多个值、有返回值的 call / getWhere。 */
public class J12Ex2 {
    static final ScopedValue<String> USER = ScopedValue.newInstance();
    static final ScopedValue<Integer> DEPTH = ScopedValue.newInstance();

    static String describe() { return USER.get() + "@depth" + DEPTH.get(); }

    public static void main(String[] args) throws Exception {
        // 一次绑定两个值：where(...).where(...).run(...)
        ScopedValue.where(USER, "alice").where(DEPTH, 1).run(() -> {
            System.out.println("外层: " + describe());

            // 内层重新绑定 USER：只在内层 lambda 里生效，出来自动还原——ThreadLocal 要自己 try/finally 恢复
            ScopedValue.where(USER, "admin-on-behalf-of-alice").where(DEPTH, 2).run(() ->
                    System.out.println("内层: " + describe()));

            System.out.println("还原: " + describe());
        });

        // 需要返回值：Carrier.call(Callable)（可抛受检异常）或 ScopedValue.getWhere(key, v, Supplier)
        String r = ScopedValue.where(USER, "carol").call(() -> USER.get().toUpperCase());
        String r2 = ScopedValue.getWhere(USER, "dave", () -> USER.get() + "!");
        System.out.println("call -> " + r + ", getWhere -> " + r2);
    }
}
