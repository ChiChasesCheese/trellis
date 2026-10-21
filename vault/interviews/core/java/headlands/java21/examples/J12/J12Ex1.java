import java.util.NoSuchElementException;

/** J12 例 1（最简单）：声明、绑定、读取、判断是否绑定。 */
public class J12Ex1 {
    // static final：整个程序里一个"钥匙"。值不存在钥匙里，钥匙只是用来在当前绑定里查找
    static final ScopedValue<String> USER = ScopedValue.newInstance();

    static void deep() {
        System.out.println("  deep() 读到 USER=" + USER.get());   // 不用参数传递
    }

    public static void main(String[] args) {
        System.out.println("绑定前 isBound=" + USER.isBound() + ", orElse=" + USER.orElse("<anonymous>"));
        try {
            USER.get();
        } catch (NoSuchElementException e) {
            System.out.println("绑定前 get() -> NoSuchElementException");
        }

        ScopedValue.where(USER, "alice").run(() -> {     // 只在这个 lambda 执行期间绑定
            System.out.println("块内 isBound=" + USER.isBound());
            deep();
        });

        System.out.println("块外 isBound=" + USER.isBound());   // 自动解绑，不需要 finally
    }
}
