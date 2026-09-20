---
title: ArchUnit User Guide
source: https://www.archunit.org/userguide/html/000_Index.html
published: '2008-07-01'
site: archunit.org
clipped: '2026-09-20'
---

# ArchUnit User Guide

## 

[ArchUnit](https://archunit.org) is a free, simple and extensible library for checking the
architecture of your Java code.
That is, ArchUnit can check dependencies between packages and classes, layers and slices,
check for cyclic dependencies and more. It does so by analyzing given Java bytecode,
importing all classes into a Java code structure.
ArchUnit’s main focus is to automatically test architecture and coding rules,
using any plain Java unit testing framework.

### 

ArchUnit consists of the following production modules:

- 
`archunit`
- 
`archunit-junit4`
- 
`archunit-junit5-api` ,`archunit-junit5-engine` ,`archunit-junit5-engine-api`
- 
`archunit-junit6-api` ,`archunit-junit6-engine` ,`archunit-junit6-engine-api`

The `archunit-example` is also relevant to end users.

#### 

This module contains the actual ArchUnit core infrastructure required to write architecture
tests: The `ClassFileImporter`,
the domain objects, as well as the rule syntax infrastructure.

#### 

This module contains the infrastructure to integrate with JUnit 4, in particular
the `ArchUnitRunner` to cache imported classes.

#### 

These modules contain the infrastructure to integrate with JUnit 5 & 6 and contain the respective
infrastructure to cache imported classes between test runs.
`archunit-junit*-api` contains the user API to write tests with ArchUnit’s JUnit support.
`archunit-junit*-engine` contains the runtime engine to run those tests.
`archunit-junit*-engine-api` contains API code for tools that want more detailed control
over running ArchUnit JUnit tests, in particular a `FieldSelector` which can be used to
instruct the `ArchUnitTestEngine` to run a specific rule field (compare [JUnit Integration](#_junit_integration)).

#### 

This module contains example architecture rules and sample code that violates these rules.
Look here to get inspiration on how to set up rules for your project, or at
[ArchUnit-Examples](https://github.com/TNG/ArchUnit-Examples) for the last released version.

## 

To use ArchUnit, it is sufficient to include the respective JAR files in the classpath.
Most commonly, this is done by adding the dependency to your dependency management tool,
which is illustrated for Maven and Gradle below. Alternatively, you
can obtain the necessary JAR files directly from
[Maven Central](http://search.maven.org/#search%7Cga%7C1%7Cg%3A%22com.tngtech.archunit%22).

### 

ArchUnit’s JUnit 5 & 6 artifacts follow the pattern of JUnit Jupiter. There is one artifact containing
the API, i.e. the compile time dependencies to write tests. Then there is another artifact containing
the actual `TestEngine` used at runtime. Just like JUnit Jupiter, ArchUnit offers one convenience
artifact transitively including both API and engine with the correct scope, which in turn can be added
as a test compile dependency. Thus, to include ArchUnit’s JUnit 5 & 6 support, simply add the following dependency
from Maven Central:

```
dependencies {
    // testImplementation 'com.tngtech.archunit:archunit-junit5:1.5.0' // for JUnit 5
    testImplementation 'com.tngtech.archunit:archunit-junit6:1.5.0'
}
```
```
<dependency>
    <groupId>com.tngtech.archunit</groupId>
    <!-- <artifactId>archunit-junit5</artifactId> --> <!-- for JUnit 5 -->
    <artifactId>archunit-junit6</artifactId>
    <version>1.5.0</version>
    <scope>test</scope>
</dependency>
```
### 

To use ArchUnit in combination with JUnit 4, include the following dependency from Maven Central:

```
dependencies {
    testImplementation 'com.tngtech.archunit:archunit-junit4:1.5.0'
}
```
```
<dependency>
    <groupId>com.tngtech.archunit</groupId>
    <artifactId>archunit-junit4</artifactId>
    <version>1.5.0</version>
    <scope>test</scope>
</dependency>
```
### 

ArchUnit works with any test framework that executes Java code. To use ArchUnit in such a context, include the core ArchUnit dependency from Maven Central:

```
dependencies {
   testImplementation 'com.tngtech.archunit:archunit:1.5.0'
}
```
```
<dependency>
    <groupId>com.tngtech.archunit</groupId>
    <artifactId>archunit</artifactId>
    <version>1.5.0</version>
    <scope>test</scope>
</dependency>
```
### 

There exists a Maven plugin by Société Générale to run ArchUnit rules straight from Maven. For
more information visit their GitHub repo: [https://github.com/societe-generale/arch-unit-maven-plugin](https://github.com/societe-generale/arch-unit-maven-plugin)

## 

ArchUnit tests are written the same way as any Java unit test and can be written with any
Java unit testing framework. To really understand the ideas behind ArchUnit, one should consult
[Ideas and Concepts](#_ideas_and_concepts). The following will outline a "technical" getting started.

### 

At its core, ArchUnit provides infrastructure to import Java bytecode into Java code structures.
This can be done using the `ClassFileImporter`:

`JavaClasses classes = new ClassFileImporter().importPackages("com.mycompany.myapp");`
The `ClassFileImporter` offers many ways to import classes. Some ways depend on
the current project’s classpath, like `importPackages(..)`. However there are other ways
that do not, for example:

`JavaClasses classes = new ClassFileImporter().importPath("/some/path");`
The returned object of type `JavaClasses` represents a collection of elements of type
`JavaClass`, where `JavaClass` in turn represents a single imported class file. You can
in fact access most properties of the imported class via the public API:

```
JavaClass clazz = classes.get(Object.class);
System.out.print(clazz.getSimpleName()); // returns 'Object'
```
### 

To express architectural rules, like 'Services should only be accessed by Controllers',
ArchUnit offers an abstract DSL-like fluent API, which can in turn be evaluated against
imported classes. To specify a rule, use the class `ArchRuleDefinition` as entry point:

```
import static com.tngtech.archunit.lang.syntax.ArchRuleDefinition.classes;
// ...
ArchRule myRule = classes()
    .that().resideInAPackage("..service..")
    .should().onlyBeAccessed().byAnyPackage("..controller..", "..service..");
```
The two dots represent any number of packages (compare AspectJ Pointcuts); for details on
the supported package pattern syntax see [Package Identifiers](#_package_identifiers). The returned object of
type `ArchRule` can now be evaluated against a set of imported classes:

`myRule.check(importedClasses);`
Thus the complete example could look like

```
@Test
public void Services_should_only_be_accessed_by_Controllers() {
    JavaClasses importedClasses = new ClassFileImporter().importPackages("com.mycompany.myapp");
    ArchRule myRule = classes()
        .that().resideInAPackage("..service..")
        .should().onlyBeAccessed().byAnyPackage("..controller..", "..service..");
    myRule.check(importedClasses);
}
```
### 

While ArchUnit can be used with any unit testing framework, it provides extended support for writing tests with JUnit. The main advantage is automatic caching of imported classes between tests (of the same imported classes), as well as reduction of boilerplate code.

To use the JUnit support, declare ArchUnit’s `ArchUnitRunner` (only JUnit 4), declare the classes
to import via `@AnalyzeClasses` and add the respective rules as fields:

```
// @RunWith(ArchUnitRunner.class) // Enable this line for JUnit 4
@AnalyzeClasses(packages = "com.mycompany.myapp")
public class MyArchitectureTest {
    @ArchTest
    public static final ArchRule myRule = classes()
        .that().resideInAPackage("..service..")
        .should().onlyBeAccessed().byAnyPackage("..controller..", "..service..");
}
```
The JUnit test support will automatically import (or reuse) the specified classes and
evaluate any rule annotated with `@ArchTest` against those classes.

For further information on how to use the JUnit support refer to [JUnit Support](#_junit_support).

### 

Using the JUnit support with Kotlin is quite similar to Java:

```
// @RunWith(ArchUnitRunner::class) // Enable this line for JUnit 4
@AnalyzeClasses(packagesOf = [MyArchitectureTest::class])
class MyArchitectureTest {
    @ArchTest
    val rule_as_field = ArchRuleDefinition.noClasses().should()...
    @ArchTest
    fun rule_as_method(importedClasses: JavaClasses) {
        val rule = ArchRuleDefinition.noClasses().should()...
        rule.check(importedClasses)
    }
}
```
## 

The following section illustrates some typical checks you could do with ArchUnit.

### 

```
noClasses().that().resideInAPackage("..source..")
    .should().dependOnClassesThat().resideInAPackage("..foo..")
```
```
classes().that().resideInAPackage("..foo..")
    .should().onlyHaveDependentClassesThat().resideInAnyPackage("..source.one..", "..foo..")
```
### 

```
classes().that().haveNameMatching(".*Bar")
    .should().onlyHaveDependentClassesThat().haveSimpleName("Bar")
```
### 

```
classes().that().haveSimpleNameStartingWith("Foo")
    .should().resideInAPackage("com.foo")
```
### 

```
classes().that().implement(Connection.class)
    .should().haveSimpleNameEndingWith("Connection")
```
```
classes().that().areAssignableTo(EntityManager.class)
    .should().onlyHaveDependentClassesThat().resideInAnyPackage("..persistence..")
```
### 

```
classes().that().areAssignableTo(EntityManager.class)
    .should().onlyHaveDependentClassesThat().areAnnotatedWith(Transactional.class)
```
### 

```
layeredArchitecture()
    .consideringAllDependencies()
    .layer("Controller").definedBy("..controller..")
    .layer("Service").definedBy("..service..")
    .layer("Persistence").definedBy("..persistence..")
    .whereLayer("Controller").mayNotBeAccessedByAnyLayer()
    .whereLayer("Service").mayOnlyBeAccessedByLayers("Controller")
    .whereLayer("Persistence").mayOnlyBeAccessedByLayers("Service")
```
## 

ArchUnit is divided into different layers, where the most important ones are the "Core" layer, the "Lang" layer and the "Library" layer. In short the Core layer deals with the basic infrastructure, i.e. how to import byte code into Java objects. The Lang layer contains the rule syntax to specify architecture rules in a succinct way. The Library layer contains more complex predefined rules, like a layered architecture with several layers. The following section will explain these layers in more detail.

### 

Much of ArchUnit’s core API resembles the Java Reflection API.
There are classes like `JavaMethod`, `JavaField`, and more,
and the public API consists of methods like `getName()`, `getMethods()`,
`getRawType()` or `getRawParameterTypes()`.
Additionally ArchUnit extends this API for concepts needed to talk about dependencies between code,
like `JavaMethodCall`, `JavaConstructorCall` or `JavaFieldAccess`.
For example, it is possible to programmatically iterate over `javaClass.getAccessesFromSelf()`
and react to the imported accesses between this Java class and other Java classes.

To import compiled Java class files, ArchUnit provides the `ClassFileImporter`, which can
for example be used to import packages from the classpath:

`JavaClasses classes = new ClassFileImporter().importPackages("com.mycompany.myapp");`
For more information refer to [The Core API](#_the_core_api).

### 

The Core API is quite powerful and offers a lot of information about the static structure of a Java program. However, tests directly using the Core API lack expressiveness, in particular with respect to architectural rules.

For this reason ArchUnit provides the Lang API, which offers a powerful syntax to express rules in an abstract way. Most parts of the Lang API are composed as fluent APIs, i.e. an IDE can provide valuable suggestions on the possibilities the syntax offers.

An example for a specified architecture rule would be:

```
ArchRule rule =
    classes().that().resideInAPackage("..service..")
        .should().onlyBeAccessed().byAnyPackage("..controller..", "..service..");
```
Once a rule is composed, imported Java classes can be checked against it:

```
JavaClasses importedClasses = new ClassFileImporter().importPackage("com.myapp");
ArchRule rule = // define the rule
rule.check(importedClasses);
```
The syntax ArchUnit provides is fully extensible and can thus be adjusted to almost any
specific need. For further information, please refer to [The Lang API](#_the_lang_api).

### 

The Library API offers predefined complex rules for typical architectural goals. For example
a succinct definition of a layered architecture via package definitions. Or rules to slice
the code base in a certain way, for example in different areas of the domain, and enforce these
slices to be acyclic or independent of each other. More detailed information is provided in
[The Library API](#_the_library_api).

## 

The Core API is itself divided into the domain objects and the actual import.

### 

As mentioned in [Ideas and Concepts](#_ideas_and_concepts) the backbone of the infrastructure is the `ClassFileImporter`,
which provides various ways to import Java classes. One way is to import packages from
the classpath, or the complete classpath via

`JavaClasses classes = new ClassFileImporter().importClasspath();`
However, the import process is completely independent of the classpath, so it would be well possible to import any path from the file system:

`JavaClasses classes = new ClassFileImporter().importPath("/some/path/to/classes");`
The `ClassFileImporter` offers several other methods to import classes, for example locations can be
specified as URLs or as JAR files.

Furthermore specific locations can be filtered out, if they are contained in the source of classes,
but should not be imported. A typical use case would be to ignore test classes, when the classpath
is imported. This can be achieved by specifying `ImportOption`s:

```
ImportOption ignoreTests = new ImportOption() {
    @Override
    public boolean includes(Location location) {
        return !location.contains("/test/"); // ignore any URI to sources that contains '/test/'
    }
};
JavaClasses classes = new ClassFileImporter().withImportOption(ignoreTests).importClasspath();
```
A `Location` is principally an URI, i.e. ArchUnit considers sources as File or JAR URIs

- 
[file:///home/dev/my/project/target/classes/some/Thing.class](file:///home/dev/my/project/target/classes/some/Thing.class)
- 
`jar:file:///home/dev/.m2/repository/some/things.jar!/some/Thing.class`

For the two common cases to skip importing JAR files and to skip importing test files
(for typical setups, like a Maven or Gradle build),
there already exist predefined `ImportOption`s:

```
new ClassFileImporter()
    .withImportOption(ImportOption.Predefined.DO_NOT_INCLUDE_JARS)
    .withImportOption(ImportOption.Predefined.DO_NOT_INCLUDE_TESTS)
    .importClasspath();
```
#### 

While importing the requested classes (e.g. `target/classes` or `target/test-classes`)
it can happen that a class within the scope of the import has a reference to a class outside of the
scope of the import. This will naturally happen, if the classes of the JDK are not imported,
since then for example any dependency on `Object.class` will be unresolved within the import.

At this point ArchUnit needs to decide how to treat these classes that are missing from the import. By default, ArchUnit searches within the classpath for missing classes and if found imports them. This obviously has the advantage that information about those classes (which interfaces they implement, how they are annotated) is present during rule evaluation.

On the downside this additional lookup from the classpath will cost some performance and in some
cases might not make sense (e.g. if information about classes not present in the original import
is known to be unnecessary for evaluating rules).
Thus ArchUnit can be configured to create stubs instead, i.e. a `JavaClass` that has all the known
information, like the fully qualified name or the method called. However, this stub might
naturally lack some information, like superclasses, annotations or other details that cannot
be determined without importing the bytecode of this class. This behavior will also happen,
if ArchUnit fails to determine the location of a missing class from the classpath.

To find out, how to configure the default behavior, refer to [Configuring the Resolution Behavior](#_configuring_the_resolution_behavior).

### 

The domain objects represent Java code, thus the naming should be pretty straight forward. Most
commonly, the `ClassFileImporter` imports instances of type `JavaClass`. A rough overview looks
like this:

Most objects resemble the Java Reflection API, including inheritance relations. Thus a `JavaClass`
has `JavaMembers`, which can in turn be either `JavaField`, `JavaMethod`,
`JavaConstructor` (or `JavaStaticInitializer`). While not present within the reflection API,
it makes sense to introduce an expression for anything that can access other code, which ArchUnit
calls 'code unit', and is in fact either a method, a constructor (including the class initializer)
or a static initializer of a class (e.g. a `static { … }` block, a static field assignment,
etc.).

Furthermore one of the most interesting features of ArchUnit that exceeds the Java Reflection API,
is the concept of accesses to another class. On the lowest level accesses can only take place
from a code unit (as mentioned, any block of executable code) to either a field (`JavaFieldAccess`),
a method (`JavaMethodCall`) or constructor (`JavaConstructorCall`).

ArchUnit imports the whole graph of classes and their relationship to each other. While checking
the accesses **from** a class is pretty isolated (the bytecode offers all this information),
checking accesses **to** a class requires the whole graph to be built first. To distinguish which
sort of access is referred to, methods will always clearly state **fromSelf** and **toSelf**.
For example, every `JavaField` allows to call `JavaField#getAccessesToSelf()` to retrieve all
code units within the graph that access this specific field. The resolution process through
inheritance is not completely straight forward. Consider for example

The bytecode will record a field access from `ClassAccessing.accessField()` to
`ClassBeingAccessed.accessedField`. However, there is no such field, since the field is
actually declared in the superclass. This is the reason why a `JavaFieldAccess`
has no `JavaField` as its target, but a `FieldAccessTarget`. In other words, ArchUnit models
the situation, as it is found within the bytecode, and an access target is not an actual
member within another class. If a member is queried for `accessesToSelf()` though, ArchUnit
will resolve the necessary targets and determine, which member is represented by which target.
The situation looks roughly like

Two things might seem strange at the first look.

First, why can a target resolve to zero matching members? The reason is that the set of classes
that was imported does not need to have all classes involved within this resolution process.
Consider the above example, if `SuperclassBeingAccessed` would not be imported, ArchUnit would
have no way of knowing where the actual targeted field resides. Thus in this case the
resolution would return zero elements.

Second, why can there be more than one resolved methods for method calls? The reason for this is that a call target might indeed match several methods in those cases, for example:

While this situation will always be resolved in a specified way for a real program,
ArchUnit cannot do the same. Instead, the resolution will report all candidates that match a
specific access target, so in the above example, the call target `C.targetMethod()` would in fact
resolve to two `JavaMethods`, namely `A.targetMethod()` and `B.targetMethod()`. Likewise a check
of either `A.targetMethod.getCallsToSelf()` or `B.targetMethod.getCallsToSelf()` would return
the same call from `D.callTargetMethod()` to `C.targetMethod()`.

#### 

ArchUnit tries to offer a lot of information from the bytecode. For example, a `JavaClass`
provides details like if it is an enum or an interface, modifiers like `public` or `abstract`,
but also the source, where this class was imported from (namely the URI mentioned in the first
section). However, if information is missing, and the classpath is correct, ArchUnit offers
some convenience to rely on the reflection API for extended details. For this reason, most
`Java*` objects offer a method `reflect()`, which will in fact try to resolve the respective
object from the Reflection API. For example:

```
JavaClasses classes = new ClassFileImporter().importClasspath();
// ArchUnit's java.lang.String
JavaClass javaClass = classes.get(String.class);
// Reflection API's java.lang.String
Class<?> stringClass = javaClass.reflect();
// ArchUnit's public int java.lang.String.length()
JavaMethod javaMethod = javaClass.getMethod("length");
// Reflection API's public int java.lang.String.length()
Method lengthMethod = javaMethod.reflect();
```
However, this will throw an `Exception`, if the respective classes are missing on the classpath
(e.g. because they were just imported from some file path).

This restriction also applies to handling annotations in a more convenient way. Consider the following annotation:

```
@interface CustomAnnotation {
    String value();
}
```
If you need to access this annotation without it being on the classpath, you must rely on

```
JavaAnnotation<?> annotation = javaClass.getAnnotationOfType("some.pkg.CustomAnnotation");
// result is untyped, since it might not be on the classpath (e.g. enums)
Object value = annotation.get("value");
```
So there is neither type safety nor automatic refactoring support. If this annotation is on the classpath, however, this can be written way more naturally:

```
CustomAnnotation annotation = javaClass.getAnnotationOfType(CustomAnnotation.class);
String value = annotation.value();
```
ArchUnit’s own rule APIs (compare [The Lang API](#_the_lang_api)) never rely on the
classpath though. Thus the evaluation of default rules and syntax combinations, described in the
next section, does not depend on whether the classes were imported from the classpath or
some JAR / folder.

#### 

Several ArchUnit methods accept a `String` package identifier to describe a set of packages,
for example `resideInAPackage(..)` and `resideInAnyPackage(..)` (and their negated variants)
in the Lang API, `slices().matching(..)` and `modules().definedByPackages(..)` in the Library
API, or the component stereotypes of a PlantUML component diagram. All of them delegate to
the same underlying [`PackageMatcher`](https://javadoc.io/doc/com.tngtech.archunit/archunit/latest/com/tngtech/archunit/core/domain/PackageMatcher.html), whose syntax is inspired by AspectJ type patterns and
extended with capturing groups.

##### 

The syntax is built from the following elements:

| Pattern | Meaning | 
|---|---|
| * | Matches any non-empty sequence of characters not containing the dot `.` , i.e. exactly one package segment. | 
| .. | Matches any (possibly empty) sequence of characters that may contain the dot `.` , i.e. any number of package segments (including zero). | 
| (*) | Like `*` , but additionally*captures* the matched segment, so it can be referenced later (e.g. as a slice identifier, see[Slices](#_slices) ). | 
| (**) | Like `..` , but additionally*captures* the matched segments. | 
| [a\|b] | Alternation: matches either `a` or`b` . Alternations are only allowed inside brackets`[...]` or inside capturing groups`(...)` . | 

Note that `(..)` is not a valid capturing group — use `(**)` instead. `()` and `[]` cannot
be nested inside each other.

The segments matched by capturing groups can be retrieved from the result of
[`PackageMatcher#match(String)`](<https://javadoc.io/doc/com.tngtech.archunit/archunit/latest/com/tngtech/archunit/core/domain/PackageMatcher.html#match(java.lang.String)>)
via
[`PackageMatcher.Result#getGroup(int)`](<https://javadoc.io/doc/com.tngtech.archunit/archunit/latest/com/tngtech/archunit/core/domain/PackageMatcher.Result.html#getGroup(int)>)
(groups are 1-based, in the order the capturing groups appear in the pattern).

##### 

Consider the following five classes and the packages they reside in:

| Class | Package | 
|---|---|
| `com.myapp.controller.SomeController` | `com.myapp.controller` | 
| `com.myapp.service.SomeService` | `com.myapp.service` | 
| `com.myapp.service.impl.SomeServiceImpl` | `com.myapp.service.impl` | 
| `com.myapp.persistence.dao.SomeDao` | `com.myapp.persistence.dao` | 
| `com.myapp.persistence.dao.jpa.SomeJpa` | `com.myapp.persistence.dao.jpa` | 

The following table shows a range of package identifiers and which of the five packages above each of them matches:

| Package Identifier | Matches | 
|---|---|
| `com.myapp.service` | `com.myapp.service` only (exact match). | 
| `com.myapp.*` | `com.myapp.controller` and`com.myapp.service` (exactly one more segment after`com.myapp` ). | 
| `com.myapp..` | All five packages — `com.myapp..` matches`com.myapp` itself and every subpackage of it. | 
| `..service` | `com.myapp.service` only (segment`service` at the end). | 
| `..service..` | `com.myapp.service` and`com.myapp.service.impl` (any package containing a segment`service` ). | 
| `..dao..` | `com.myapp.persistence.dao` and`com.myapp.persistence.dao.jpa` . | 
| `..impl` | `com.myapp.service.impl` only. | 
| `com.myapp.(*)` | `com.myapp.controller` (group 1 =`controller` ) and`com.myapp.service` (group 1 =`service` ). The deeper packages do not match because`(*)` allows only a single segment. | 
| `com.myapp.(*)..` | All five packages; group 1 captures the first sub-package below `com.myapp` (`controller` ,`service` ,`service` ,`persistence` ,`persistence` respectively). This is the typical pattern used by`slices().matching(..)` . | 
| `..[service\|controller]..` | `com.myapp.controller` ,`com.myapp.service` and`com.myapp.service.impl` . | 

##### 

An important detail is that the package identifier is matched against the
**package name of a class**, not against the fully qualified class name.
So for `com.myapp.service.SomeService` the string that is checked against
the pattern is `com.myapp.service`, not `com.myapp.service.SomeService`.

This means that a pattern like `..SomeService` will *not* match a class named `SomeService`,
because `SomeService` is the simple class name, not a package segment. To match by class
name use a name-based predicate such as
`haveSimpleName("SomeService")` or `haveNameMatching(".*SomeService")` instead.

## 

### 

[The Core API](#_the_core_api) is pretty powerful with regard to all the details from the bytecode
that it provides to tests. However, tests written this way lack conciseness and fail to convey the
architectural concept that they should assert. Consider:

```
Set<JavaClass> services = new HashSet<>();
for (JavaClass clazz : classes) {
    // choose those classes with FQN with infix '.service.'
    if (clazz.getName().contains(".service.")) {
        services.add(clazz);
    }
}
for (JavaClass service : services) {
    for (JavaAccess<?> access : service.getAccessesFromSelf()) {
        String targetName = access.getTargetOwner().getName();
        // fail if the target FQN has the infix ".controller."
        if (targetName.contains(".controller.")) {
            String message = String.format(
                    "Service %s accesses Controller %s in line %d",
                    service.getName(), targetName, access.getLineNumber());
            Assert.fail(message);
        }
    }
}
```
What we want to express, is the rule *"no classes that reside in a package 'service' should
access classes that reside in a package 'controller'"*. Nevertheless, it’s hard to read through
that code and distill that information. And the same process has to be done every time someone
needs to understand the semantics of this rule.

To solve this shortcoming, ArchUnit offers a high level API to express architectural concepts in a concise way. In fact, we can write code that is almost equivalent to the prose rule text mentioned before:

```
ArchRule rule = ArchRuleDefinition.noClasses()
    .that().resideInAPackage("..service..")
    .should().accessClassesThat().resideInAPackage("..controller..");
rule.check(importedClasses);
```
The only difference to colloquial language is the ".." in the package notation,
which refers to any number of packages. Thus "..service.." just expresses
*"any package that contains some sub-package 'service'"*, e.g. `com.myapp.service.any`.
If this test fails, it will report an `AssertionError` with the following message:

```
java.lang.AssertionError: Architecture Violation [Priority: MEDIUM] -
Rule 'no classes that reside in a package '..service..'
should access classes that reside in a package '..controller..'' was violated (1 times):
Method <some.pkg.service.SomeService.callController()>
calls method <some.pkg.controller.SomeController.execute()>
in (SomeService.java:14)
```
So as a benefit, the assertion error contains the full rule text out of the box and reports all violations including the exact class and line number. The rule API also allows to combine predicates and conditions:

```
noClasses()
    .that().resideInAPackage("..service..")
    .or().resideInAPackage("..persistence..")
    .should().accessClassesThat().resideInAPackage("..controller..")
    .orShould().accessClassesThat().resideInAPackage("..ui..")
rule.check(importedClasses);
```
### 

In addition to a predefined API to write rules about Java classes and their relations, there is
an extended API to define rules for members of Java classes. This might be relevant, for example,
if methods in a certain context need to be annotated with a specific annotation, or return
types implementing a certain interface. The entry point is again `ArchRuleDefinition`, e.g.

```
ArchRule rule = ArchRuleDefinition.methods()
    .that().arePublic()
    .and().areDeclaredInClassesThat().resideInAPackage("..controller..")
    .should().beAnnotatedWith(Secured.class);
rule.check(importedClasses);
```
Besides `methods()`, `ArchRuleDefinition` offers the methods `members()`, `fields()`, `codeUnits()`, `constructors()`
– and the corresponding negations `noMembers()`, `noFields()`, `noMethods()`, etc.

### 

In fact, most architectural rules take the form

`classes that ${PREDICATE} should ${CONDITION}`
In other words, we always want to limit imported classes to a relevant subset,
and then evaluate some condition to see that all those classes satisfy it.
ArchUnit’s API allows you to do just that, by exposing the concepts of `DescribedPredicate` and `ArchCondition`.
So the rule above is just an application of this generic API:

```
DescribedPredicate<JavaClass> resideInAPackageService = // define the predicate
ArchCondition<JavaClass> accessClassesThatResideInAPackageController = // define the condition
noClasses().that(resideInAPackageService)
    .should(accessClassesThatResideInAPackageController);
```
Thus, if the predefined API does not allow to express some concept, it is possible to extend it in any custom way. For example:

```
DescribedPredicate<JavaClass> haveAFieldAnnotatedWithPayload =
    new DescribedPredicate<JavaClass>("have a field annotated with @Payload"){
        @Override
        public boolean test(JavaClass input) {
            boolean someFieldAnnotatedWithPayload = // iterate fields and check for @Payload
            return someFieldAnnotatedWithPayload;
        }
    };
ArchCondition<JavaClass> onlyBeAccessedBySecuredMethods =
    new ArchCondition<JavaClass>("only be accessed by @Secured methods") {
        @Override
        public void check(JavaClass item, ConditionEvents events) {
            for (JavaMethodCall call : item.getMethodCallsToSelf()) {
                if (!call.getOrigin().isAnnotatedWith(Secured.class)) {
                    String message = String.format(
                        "Method %s is not @Secured", call.getOrigin().getFullName());
                    events.add(SimpleConditionEvent.violated(call, message));
                }
            }
        }
    };
classes().that(haveAFieldAnnotatedWithPayload).should(onlyBeAccessedBySecuredMethods);
```
If the rule fails, the error message will be built from the supplied descriptions. In the example above, it would be

`classes that have a field annotated with @Payload should only be accessed by @Secured methods`
### 

Custom predicates and conditions like in the last section can often be composed from predefined elements.
ArchUnit’s basic convention for predicates is that they are defined in an inner class `Predicates` within the type they target.
For example, one can find the predicate to check for the simple name of a `JavaClass` as

`JavaClass.Predicates.simpleName(String)`
Predicates can be joined using the methods `predicate.or(other)` and `predicate.and(other)`.
So for example a predicate testing for a class with simple name "Foo" that is serializable
could be created the following way:

```
import static com.tngtech.archunit.core.domain.JavaClass.Predicates.assignableTo;
import static com.tngtech.archunit.core.domain.JavaClass.Predicates.simpleName;
DescribedPredicate<JavaClass> serializableNamedFoo =
    simpleName("Foo").and(assignableTo(Serializable.class));
```
Note that for some properties, there exist interfaces with predicates defined for them.
For example the property to have a name is represented by the interface `HasName`;
consequently the predicate to check the name of a `JavaClass`
is the same as the predicate to check the name of a `JavaMethod`,
and resides within

`HasName.Predicates.name(String)`
This can at times lead to problems with the type system, if predicates are supposed to be joined.
Since the `or(..)` method accepts a type of `DescribedPredicate<? super T>`,
where `T` is the type of the first predicate. For example:

```
// Does not compile, because type(..) targets a subtype of HasName
HasName.Predicates.name("").and(JavaClass.Predicates.type(Serializable.class))
// Does compile, because name(..) targets a supertype of JavaClass
JavaClass.Predicates.type(Serializable.class).and(HasName.Predicates.name(""))
// Does compile, because the compiler now sees name(..) as a predicate for JavaClass
DescribedPredicate<JavaClass> name = HasName.Predicates.name("").forSubtype();
name.and(JavaClass.Predicates.type(Serializable.class));
```
This behavior is somewhat tedious, but unfortunately it is a shortcoming of the Java type system that cannot be circumvented in a satisfying way.

Just like predicates, there exist predefined conditions that can be combined in a similar way.
Since `ArchCondition` is a less generic concept, all predefined conditions can be found within `ArchConditions`.
Examples:

```
ArchCondition<JavaClass> callEquals =
    ArchConditions.callMethod(Object.class, "equals", Object.class);
ArchCondition<JavaClass> callHashCode =
    ArchConditions.callMethod(Object.class, "hashCode");
ArchCondition<JavaClass> callEqualsOrHashCode = callEquals.or(callHashCode);
```
### 

Earlier we stated that most architectural rules take the form

`classes that ${PREDICATE} should ${CONDITION}`
However, we do not always talk about classes, if we express architectural concepts. We might have custom language, we might talk about modules, about slices, or on the other hand more detailed about fields, methods or constructors. A generic API will never be able to support every imaginable concept out of the box. Thus ArchUnit’s rule API has at its foundation a more generic API that controls the types of objects that our concept targets.

To achieve this, any rule definition is based on a `ClassesTransformer` that defines how
`JavaClasses` are to be transformed to the desired rule input. In many cases, like the ones
mentioned in the sections above, this is the identity transformation, passing classes on to the rule
as they are. However, one can supply any custom transformation to express a rule about a
different type of input object. For example:

```
ClassesTransformer<JavaPackage> packages = new AbstractClassesTransformer<JavaPackage>("packages") {
    @Override
    public Iterable<JavaPackage> doTransform(JavaClasses classes) {
        Set<JavaPackage> result = new HashSet<>();
        classes.getDefaultPackage().traversePackageTree(alwaysTrue(), new PackageVisitor() {
            @Override
            public void visit(JavaPackage javaPackage) {
                result.add(javaPackage);
            }
        });
        return result;
    }
};
all(packages).that(containACoreClass()).should(...);
```
Of course these transformers can represent any custom concept desired:

```
// how we map classes to business modules
ClassesTransformer<BusinessModule> businessModules = ...
// filter business module dealing with orders
DescribedPredicate<BusinessModule> dealWithOrders = ...
// check that the actual business module is independent of payment
ArchCondition<BusinessModule> beIndependentOfPayment = ...
all(businessModules).that(dealWithOrders).should(beIndependentOfPayment);
```
### 

If the rule is straight forward, the rule text that is created automatically should be sufficient in many cases. However, for rules that are not common knowledge, it is good practice to document the reason for this rule. This can be done in the following way:

```
classes().that(haveAFieldAnnotatedWithPayload).should(onlyBeAccessedBySecuredMethods)
    .because("@Secured methods will be intercepted, checking for increased privileges " +
        "and obfuscating sensitive auditing information");
```
Nevertheless, the generated rule text might sometimes not convey the real intention concisely enough, e.g. if multiple predicates or conditions are joined. It is possible to completely overwrite the rule description in those cases:

```
classes().that(haveAFieldAnnotatedWithPayload).should(onlyBeAccessedBySecuredMethods)
    .as("Payload may only be accessed in a secure way");
```
### 

Most entrypoints in `ArchRuleDefinition` create `ArchRule`s that evaluate to `EvaluationResult`s with `Priority.MEDIUM`; `ArchRuleDefinition.priority` allows to create rules with other `Priority`, e.g.:

`ArchRule rule = ArchRuleDefinition.priority(Priority.LOW).noClasses() // ...`
The resulting error messages show the priority accordingly:

`java.lang.AssertionError: Architecture Violation [Priority: LOW] - Rule 'no classes // ...`
### 

In legacy projects there might be too many violations to fix at once. Nevertheless, that code
should be covered completely by architecture tests to ensure that no further violations will
be added to the existing code. One approach to ignore existing violations is
to tailor the `that(..)` clause of the rules in question to ignore certain violations.
A more generic approach is to ignore violations based on simple regex matches.
For this one can put a file named `archunit_ignore_patterns.txt` in the root of the classpath.
Every line will be interpreted as a regular expression and checked against reported violations.
Violations with a message matching the pattern will be ignored. If no violations are left,
the check will pass.

For example, suppose the class `some.pkg.LegacyService` violates a lot of different rules.
It is possible to add

`.*some\.pkg\.LegacyService.*`
All violations mentioning `some.pkg.LegacyService` will consequently be ignored, and rules that
are only violated by such violations will report success instead of failure.

It is possible to add comments to ignore patterns by prefixing the line with a '#':

```
# There are many known violations where LegacyService is involved; we'll ignore them all
.*some\.pkg\.LegacyService.*
```
## 

The Library API offers a growing collection of predefined rules, which offer a more concise API
for more complex but common patterns, like a layered architecture or checks for cycles between
slices (compare [What to Check](#_what_to_check)).

### 

The entrance point for checks of common architectural styles is:

`com.tngtech.archunit.library.Architectures`
At the moment this only provides a convenient check for a layered architecture and onion architecture. But in the future it might be extended for styles like a pipes and filters, separation of business logic and technical infrastructure, etc.

#### 

In layered architectures, we define different layers and how those interact with each other.
An example setup for a simple 3-tier architecture can be found in [Layer Checks](#_layer_checks).

#### 

In an "Onion Architecture" (also known as "Hexagonal Architecture" or "Ports and Adapters"), we can define domain packages and adapter packages as follows.

```
onionArchitecture()
        .domainModels("com.myapp.domain.model..")
        .domainServices("com.myapp.domain.service..")
        .applicationServices("com.myapp.application..")
        .adapter("cli", "com.myapp.adapter.cli..")
        .adapter("persistence", "com.myapp.adapter.persistence..")
        .adapter("rest", "com.myapp.adapter.rest..");
```
The semantic follows the descriptions in [https://jeffreypalermo.com/2008/07/the-onion-architecture-part-1/](https://jeffreypalermo.com/2008/07/the-onion-architecture-part-1/).
More precisely, the following holds:

- 
The `domain` package is the core of the application. It consists of two parts.
  1. 
The `domainModels` packages contain the domain entities.
  2. 
The packages in `domainServices` contains services that use the entities in the`domainModel` packages.
- 
- 
The `applicationServices` packages contain services and configuration to run the application and use cases.
It can use the items of the`domain` package but there must not be any dependency from the`domain` to the`application` packages.
- 
The `adapter` package contains logic to connect to external systems and/or infrastructure.
No adapter may depend on another adapter. Adapters can use both the items of the`domain` as well as
the`application` packages. Vice versa, neither the`domain` nor the`application` packages must
contain dependencies on any`adapter` package.

### 

Currently, there are two "slice" rules offered by the Library API. These are basically rules that slice the code by packages, and contain assertions on those slices. The entrance point is:

`com.tngtech.archunit.library.dependencies.SlicesRuleDefinition`
The API is based on the idea to sort classes into slices according to one or several package
infixes, and then write assertions against those slices. The `matching(..)` argument follows
the package pattern syntax described in [Package Identifiers](#_package_identifiers), where the parentheses
`(*)` / `(**)` mark the captured segment(s) that are used as slice identifiers.
At the moment this is for example:

```
// sort classes by the first package after 'myapp'
// then check those slices for cyclic dependencies
SlicesRuleDefinition.slices().matching("..myapp.(*)..").should().beFreeOfCycles()
// checks all subpackages of 'myapp' for cycles
SlicesRuleDefinition.slices().matching("..myapp.(**)").should().beFreeOfCycles()
// sort classes by packages between 'myapp' and 'service'
// then check those slices for not having any dependencies on each other
SlicesRuleDefinition.slices().matching("..myapp.(**).service..").should().notDependOnEachOther()
```
If this constraint is too rigid, e.g. in legacy applications where the package structure is rather
inconsistent, it is possible to further customize the slice creation. This can be done by specifying
a mapping of `JavaClass` to `SliceIdentifier` where classes with the same `SliceIdentifier` will
be sorted into the same slice. Consider this example:

```
SliceAssignment legacyPackageStructure = new SliceAssignment() {
    // this will specify which classes belong together in the same slice
    @Override
    public SliceIdentifier getIdentifierOf(JavaClass javaClass) {
        if (javaClass.getPackageName().startsWith("com.oldapp")) {
            return SliceIdentifier.of("Legacy");
        }
        if (javaClass.getName().contains(".esb.")) {
            return SliceIdentifier.of("ESB");
        }
        // ... further custom mappings
        // if the class does not match anything, we ignore it
        return SliceIdentifier.ignore();
    }
    // this will be part of the rule description if the test fails
    @Override
    public String getDescription() {
        return "legacy package structure";
    }
};
SlicesRuleDefinition.slices().assignedFrom(legacyPackageStructure).should().beFreeOfCycles()
```
#### 

There are two configuration parameters to adjust the behavior of the cycle detection.
They can be configured via `archunit.properties` (compare [Advanced Configuration](#_advanced_configuration)).

```
# This will limit the maximum number of cycles to detect and thus required CPU and heap.
# default is 100
cycles.maxNumberToDetect=50
# This will limit the maximum number of dependencies to report per cycle edge.
# Note that ArchUnit will regardless always analyze all dependencies to detect cycles,
# so this purely affects how many dependencies will be printed in the report.
# Also note that this number will quickly affect the required heap since it scales with number.
# of edges and number of cycles
# default is 20
cycles.maxNumberOfDependenciesPerEdge=5
```
#### 

The underlying infrastructure for cycle detection that the `slices()` rule makes use of can also be accessed
without any rule syntax around it. This allows to use the pure cycle detection algorithm in custom
checks or libraries. The core class of the cycle detection is

`com.tngtech.archunit.library.cycle_detection.CycleDetector`
It can be used on a set of a generic type `NODE` in combination with a generic `Set<EDGE>`
(where `EDGE implements Edge<NODE>`) representing the edges of the graph:

```
Set<MyNode> nodes = // ...
Set<Edge<MyNode>> edges = // ...
Cycles<Edge<MyNode>> foundCycles = CycleDetector.detectCycles(nodes, edges);
```
Edges are parameterized by a generic type `EDGE` to allow custom edge types that can
then transport additional meta-information if needed.

### 

|  | Note: ArchUnit doesn’t strive to be a "competition" for module systems like the Java Platform Module System. Such systems have advantages like checks at compile time versus test time as ArchUnit does. So, if another module system works well in your environment, there is no need to switch over. But ArchUnit can bring JPMS-like features to older code bases, e.g. Java 8 projects, or environments where the JPMS is for some reason no option. It also can accompany a module system by adding additional rules e.g. on the API of a module. | 

To express the concept of modularization ArchUnit offers `ArchModule`s. The entrypoint into
the API is `ModuleRuleDefinition`, e.g.

`ModuleRuleDefinition.modules().definedByPackages("..example.(*)..").should().beFreeOfCycles();`
As the example shows, it shares some concepts with the [Slices](#_slices) API. For example `definedByPackages(..)`
follows the same semantics as `slices().matching(..)`, using [Package Identifiers](#_package_identifiers).
Also, the configuration options for cycle detection mentioned in the last section are shared by these APIs.
But, it also offers several powerful concepts beyond that API to express many different modularization scenarios.

One example would be to express modules via annotation. We can introduce a custom annotation
like `@AppModule` and follow a convention to annotate the top-level `package-info` file
of each package we consider the root of a module. E.g.

```
@AppModule(
  name = "Module One",
  allowedDependencies = {"Module Two", "Module Three"},
  exposedPackages = {"..module_one.api.."}
)
package com.myapp.example.module_one;
```
We can then define a rule using this annotation:

```
modules()
  .definedByAnnotation(AppModule.class)
  .should().respectTheirAllowedDependenciesDeclaredIn("allowedDependencies",
      consideringOnlyDependenciesInAnyPackage("..example.."))
  .andShould().onlyDependOnEachOtherThroughPackagesDeclaredIn("exposedPackages")
```
As the example shows, the syntax carries on meta-information (like the annotation of the annotated
`package-info`) into the created `ArchModule` objects where it can
be used to define the rule. In this example, the allowed dependencies are taken from the `@AppModule`
annotation on the respective `package-info` and compared to the actual module dependencies. Any
dependency not listed is reported as violation.
Likewise, the exposed packages are taken from the `@AppModule` annotation and any dependency
where the target class’s package doesn’t match any declared package identifier is reported
as violation.

Note that the `modules()` API can be adjusted in many ways to model custom requirements.
For further details, please take a look at the
[examples](https://github.com/TNG/ArchUnit-Examples/blob/main/example-junit6/src/test/java/com/tngtech/archunit/exampletest/junit6/ModulesTest.java).

#### 

The infrastructure to create modules and inspect their dependencies can also be used outside the rule syntax, e.g. for custom checks or utility code:

```
ArchModules<?> modules = ArchModules.defineByPackages("..example.(*)..").modularize(javaClasses);
ArchModule<?> coreModule = modules.getByIdentifier("core");
Set<? extends ModuleDependency<?>> coreDependencies = coreModule.getModuleDependenciesFromSelf();
coreDependencies.forEach(...);
```
### 

The Library API also offers a small set of coding rules that might be useful in various projects. Those can be found within

`com.tngtech.archunit.library`
#### 

The class `GeneralCodingRules` contains a set of very general rules and conditions for coding.
For example:

- 
To check that classes do not access `System.out` or`System.err` , but use logging instead.
- 
To check that classes do not throw generic exceptions, but use specific exceptions instead.
- 
To check that classes do not use `java.util.logging` , but use other libraries like Log4j, Logback, or SLF4J instead
- 
To check that classes do not use JodaTime, but use `java.time` instead.
- 
To check that classes do not use field injection, but constructor injection instead.

### 

The Library API offers a feature that supports [PlantUML](http://plantuml.com/component-diagram) diagrams.
This feature is located in

`com.tngtech.archunit.library.plantuml`
ArchUnit can derive rules straight from PlantUML diagrams and check to make sure that all imported
`JavaClasses` abide by the dependencies of the diagram. The respective rule can be created in the following way:

```
URL myDiagram = getClass().getResource("my-diagram.puml");
classes().should(adhereToPlantUmlDiagram(myDiagram, consideringAllDependencies()));
```
Diagrams supported have to be component diagrams and associate classes to components via stereotypes.
The way this works is to use the respective package identifiers (compare
`ArchConditions.onlyHaveDependenciesInAnyPackage(..)`) as stereotypes:

```
@startuml
[Some Source] <<..some.source..>>
[Some Target] <<..some.target..>> as target
[Some Source] --> target
@enduml
```
Consider this diagram applied as a rule via `adhereToPlantUmlDiagram(..)`, then for example
a class `some.target.Target` accessing `some.source.Source` would be reported as a violation.

#### 

There are different ways to deal with dependencies of imported classes not covered by the
diagram at all. The behavior of the PlantUML API can be configured by supplying a respective
`Configuration`:

```
// considers all dependencies possible (including java.lang, java.util, ...)
classes().should(adhereToPlantUmlDiagram(
        mydiagram, consideringAllDependencies())
// considers only dependencies specified in the PlantUML diagram
// (so any unknown dependency will be ignored)
classes().should(adhereToPlantUmlDiagram(
        mydiagram, consideringOnlyDependenciesInDiagram())
// considers only dependencies in any specified package
// (control the set of dependencies to consider, e.g. only com.myapp..)
classes().should(adhereToPlantUmlDiagram(
        mydiagram, consideringOnlyDependenciesInAnyPackage("..some.package.."))
```
It is possible to further customize which dependencies to ignore:

```
// there are further ignore flavors available
classes().should(adhereToPlantUmlDiagram(mydiagram).ignoreDependencies(predicate))
```
A PlantUML diagram used with ArchUnit must abide by a certain set of rules:

1. 
Components must be declared in the bracket notation (i.e. `[Some Component]` )
2. 
Components must have at least one (possible multiple) stereotype(s). Each stereotype in the diagram must be unique and represent a valid [package identifier](#_package_identifiers) (e.g.`<<..example..>>` where`..` represents an arbitrary number of packages; compare the core API)
3. 
Components may have an optional alias (e.g. `[Some Component] <<..example..>> as myalias` ). The alias must be alphanumeric and must not be quoted.
4. 
Components may have an optional color (e.g. `[Some Component] <<..example..>> #OrangeRed` )
5. 
Dependencies must use arrows only consisting of dashes (e.g. `-->` )
6. 
Dependencies may go from left to right `-->` or right to left`<--`
7. 
Dependencies may consist of any number of dashes (e.g `->` or`----->` )
8. 
Dependencies may contain direction hints (e.g. `-up->` ) or color directives (e.g.`-[#green]->` )

You can compare this
[diagram of ArchUnit-Examples](https://github.com/TNG/ArchUnit-Examples/blob/main/example-plain/src/test/resources/com/tngtech/archunit/exampletest/shopping_example.puml).

### 

When rules are introduced in grown projects, there are often hundreds or even thousands of violations, way too many to fix immediately. The only way to tackle such extensive violations is to establish an iterative approach, which prevents the code base from further deterioration.

`FreezingArchRule` can help in these scenarios by recording all existing violations to a `ViolationStore`.
Consecutive runs will then only report new violations and ignore known violations.
If violations are fixed, `FreezingArchRule` will automatically reduce the known stored violations to prevent any regression.

#### 

To freeze an arbitrary `ArchRule` just wrap it into a `FreezingArchRule`:

`ArchRule rule = FreezingArchRule.freeze(classes().should()./*complete ArchRule*/);`
On the first run all violations of that rule will be stored as the current state. On consecutive runs only
new violations will be reported. By default `FreezingArchRule` will ignore line numbers, i.e. if a
violation is just shifted to a different line, it will still count as previously recorded
and will not be reported.

#### 

By default `FreezingArchRule` will use a simple `ViolationStore` based on plain text files.
This is sufficient to add these files to any version control system to continuously track the progress.
You can configure the location of the violation store within `archunit.properties` (compare [Advanced Configuration](#_advanced_configuration)):

`freeze.store.default.path=/some/path/in/a/vcs/repo`
Furthermore, it is possible to configure

```
# must be set to true to allow the creation of a new violation store
# default is false
freeze.store.default.allowStoreCreation=true
# can be set to false to forbid updates of the violations stored for frozen rules
# default is true
freeze.store.default.allowStoreUpdate=false
```
This can help in CI environments to prevent misconfiguration: For example, a CI build should probably never create a new the violation store, but operate on an existing one.

As mentioned in [Overriding configuration](#_overriding_configuration), these properties can be passed as system properties as needed.
For example to allow the creation of the violation store in a specific environment, it is possible to pass the system property via

`-Darchunit.freeze.store.default.allowStoreCreation=true`
It is also possible to allow all violations to be "refrozen", i.e. the store will just be updated
with the current state, and the reported result will be success. Thus, it is effectively the same behavior
as if all rules would never have been frozen.
This can e.g. make sense, because current violations are consciously accepted and should be added to the store,
or because the format of some violations has changed. The respective property to allow refreezing
all current violations is `freeze.refreeze=true`, where the default is `false`.

#### 

`FreezingArchRule` provides two extension points to adjust the behavior to custom needs.
The first one is the `ViolationStore`, i.e. the store violations will be recorded to. The second one
is the `ViolationLineMatcher`, i.e. how `FreezingArchRule` will associate lines of stored violations
with lines of actual violations. As mentioned, by default this is a line matcher that ignores the
line numbers of violations within the same class.

##### 

As mentioned in [Configuration](#_configuration), the default `ViolationStore` is a simple text based store.
It can be exchanged though, for example to store violations in a database.
To provide your own implementation, implement `com.tngtech.archunit.library.freeze.ViolationStore` and
configure `FreezingArchRule` to use it. This can either be done programmatically:

`FreezingArchRule.freeze(rule).persistIn(customViolationStore);`
Alternatively it can be configured via `archunit.properties` (compare [Advanced Configuration](#_advanced_configuration)):

`freeze.store=fully.qualified.name.of.MyCustomViolationStore`
You can supply properties to initialize the store by using the namespace `freeze.store`.
For properties

```
freeze.store.propOne=valueOne
freeze.store.propTwo=valueTwo
```
the method `ViolationStore.initialize(props)` will be called with the properties

```
propOne=valueOne
propTwo=valueTwo
```
##### 

The `ViolationLineMatcher` compares lines from occurred violations with lines from the store.
The default implementation ignores line numbers and numbers of anonymous classes or lambda expressions,
and counts lines as equivalent when all other details match.
A custom `ViolationLineMatcher` can again either be defined programmatically:

`FreezingArchRule.freeze(rule).associateViolationLinesVia(customLineMatcher);`
or via `archunit.properties`:

`freeze.lineMatcher=fully.qualified.name.of.MyCustomLineMatcher`
### 

Similar to code quality metrics, like cyclomatic complexity or method length,
software architecture metrics strive to measure the structure and design of software.
ArchUnit can be used to calculate some well-known software architecture metrics.
The foundation of these metrics is generally some form of componentization, i.e.
we partition the classes/methods/fields of a Java application into related units
and provide measurements for these units. In ArchUnit this concept is expressed by
`com.tngtech.archunit.library.metrics.MetricsComponent`. For some metrics, like the
Cumulative Dependency Metrics by John Lakos, we also need to know the dependencies
between those components, which are naturally derived from the dependencies between
the elements (e.g. classes) within these components.

A very simple concrete example would be to consider some Java packages as components and the classes within these packages as the contained elements. From the dependencies between the classes we can derive which package depends on which other package.

The following will give a quick overview of the metrics that ArchUnit can calculate. However, for further background information it is recommended to rely on some dedicated literature that explains these metrics in full detail.

#### 

These are software architecture metrics as defined by John Lakos in his book
"Large-Scale C++ Software Design". The basic idea is to calculate the `DependsOn`
value for each component, which is the sum of all components that can be
transitively reached from some component including the component itself.

From these values we can derive

- 
Cumulative Component Dependency ( **CCD** ):
The sum of all`DependsOn` values of all components
- 
Average Component Dependency ( **ACD** ):
The`CCD` divided by the number of all components
- 
Relative Average Component Dependency ( **RACD** ):
The`ACD` divided by the number of all components
- 
Normalized Cumulative Component Dependency ( **NCCD** ):
The`CCD` of the system divided by the`CCD` of a balanced binary tree with the same number of components

##### 

Thus these metrics provide some insights into the complexity of the dependency graph of a system.
Note that in a cycle all elements have the same `DependsOn` value which will lead to an increased
CCD. In fact for any non-trivial (`n >= 5`) acyclic graph of components the RACD is bound by `0.6`.

##### 

The values described for these metrics can be calculated in the following way:

```
import com.tngtech.archunit.library.metrics.ArchitectureMetrics;
// ...
JavaClasses classes = // ...
Set<JavaPackage> packages = classes.getPackage("com.example").getSubpackages();
// These components can also be created in a package agnostic way, compare MetricsComponents.from(..)
MetricsComponents<JavaClass> components = MetricsComponents.fromPackages(packages);
LakosMetrics metrics = ArchitectureMetrics.lakosMetrics(components);
System.out.println("CCD: " + metrics.getCumulativeComponentDependency());
System.out.println("ACD: " + metrics.getAverageComponentDependency());
System.out.println("RACD: " + metrics.getRelativeAverageComponentDependency());
System.out.println("NCCD: " + metrics.getNormalizedCumulativeComponentDependency());
```
#### 

These software architecture metrics were defined by Robert C. Martin in various sources, for example in his book "Clean architecture : a craftsman’s guide to software structure and design".

The foundation are again components, that must in this case contain classes as their elements (i.e. these are purely object-oriented metrics that need a concept of abstract classes).

The metrics are based on the following definitions:

- 
Efferent Coupling ( **Ce** ): The number of outgoing dependencies to any other component
- 
Afferent Coupling ( **Ca** ): The number of incoming dependencies from any other component
- 
Instability ( **I** ):`Ce / (Ca + Ce)` , i.e. the relationship of outgoing dependencies
to all dependencies
- 
Abstractness ( **A** ):`num(abstract_classes) / num(all_classes)` in the component
- 
Distance from Main Sequence ( **D** ):`| A + I - 1 |` , i.e. the normalized distance from
the ideal line between`(A=1, I=0)` and`(A=0, I=1)`

Note that ArchUnit slightly differs from the original definition. In ArchUnit
the Abstractness value is only based on public classes, i.e.
classes that are visible from the outside. The reason is that **Ce**, **Ca** and **I** all
are metrics with respect to coupling of components. But only classes that are visible
to the outside can affect coupling between components,
so it makes sense to only consider those classes to calculate the **A** value.

##### 

The following provides some example where the `A` values assume some random factor
of abstract classes within the respective component.

##### 

The values described for these metrics can be calculated in the following way:

```
import com.tngtech.archunit.library.metrics.ArchitectureMetrics;
// ...
JavaClasses classes = // ...
Set<JavaPackage> packages = classes.getPackage("com.example").getSubpackages();
// These components can also be created in a package agnostic way, compare MetricsComponents.from(..)
MetricsComponents<JavaClass> components = MetricsComponents.fromPackages(packages);
ComponentDependencyMetrics metrics = ArchitectureMetrics.componentDependencyMetrics(components);
System.out.println("Ce: " + metrics.getEfferentCoupling("com.example.component"));
System.out.println("Ca: " + metrics.getAfferentCoupling("com.example.component"));
System.out.println("I: " + metrics.getInstability("com.example.component"));
System.out.println("A: " + metrics.getAbstractness("com.example.component"));
System.out.println("D: " + metrics.getNormalizedDistanceFromMainSequence("com.example.component"));
```
#### 

These software architecture metrics were defined by Herbert Dowalil in his book "Modulare Softwarearchitektur: Nachhaltiger Entwurf durch Microservices, Modulithen und SOA 2.0". They provide a measure for the Information Hiding Principle, i.e. the relation of visible to hidden elements within a component.

The metrics are composed from the following definitions:

- 
Relative Visibility ( **RV** ):`num(visible_elements) / num(all_elements)` for each component
- 
Average Relative Visibility ( **ARV** ): The average of all`RV` values
- 
Global Relative Visibility ( **GRV** ):`num(visible_elements) / num(all_elements)` over all components

##### 

The values described for these metrics can be calculated in the following way:

```
import com.tngtech.archunit.library.metrics.ArchitectureMetrics;
// ...
JavaClasses classes = // ...
Set<JavaPackage> packages = classes.getPackage("com.example").getSubpackages();
// These components can also be created in a package agnostic way, compare MetricsComponents.from(..)
MetricsComponents<JavaClass> components = MetricsComponents.fromPackages(packages);
VisibilityMetrics metrics = ArchitectureMetrics.visibilityMetrics(components);
System.out.println("RV : " + metrics.getRelativeVisibility("com.example.component"));
System.out.println("ARV: " + metrics.getAverageRelativeVisibility());
System.out.println("GRV: " + metrics.getGlobalRelativeVisibility());
```
## 

At the moment, ArchUnit offers extended support for writing tests with JUnit 4, JUnit 5, and JUnit 6. This mainly tackles the problem of caching classes between test runs and to remove some boilerplate.

Consider a straight forward approach to write tests:

```
@Test
public void rule1() {
    JavaClasses importedClasses = new ClassFileImporter().importClasspath();
    ArchRule rule = classes()...
    rule.check(importedClasses);
}
@Test
public void rule2() {
    JavaClasses importedClasses = new ClassFileImporter().importClasspath();
    ArchRule rule = classes()...
    rule.check(importedClasses);
}
```
For bigger projects, this will have a significant performance impact, since the import can take
a noticeable amount of time. Furthermore, rules will always be checked against the imported classes, thus
the explicit call of `check(importedClasses)` is bloat and error-prone (i.e. it can be forgotten).

### 

Make sure you follow the installation instructions at [Installation](#_installation), in particular to include
the correct dependency for the respective JUnit support.

#### 

Tests look and behave very similar between JUnit 4 and JUnit 5 & 6. The only difference is that with JUnit 4
it is necessary to add a specific `Runner` to take care of caching and checking rules, while JUnit 5 & 6
pick up the respective `TestEngine` transparently. A test typically looks the following way:

```
// @RunWith(ArchUnitRunner.class) // Enable this line for JUnit 4
@AnalyzeClasses(packages = "com.myapp")
public class ArchitectureTest {
    // ArchRules can just be declared as static fields and will be evaluated
    @ArchTest
    public static final ArchRule rule1 = classes().should()...
    @ArchTest
    public static final ArchRule rule2 = classes().should()...
    @ArchTest
    public static void rule3(JavaClasses classes) {
        // The runner also understands static methods with a single JavaClasses argument
        // reusing the cached classes
    }
}
```
The `JavaClass` cache will work in two ways. On the one hand it will cache the classes by test,
so they can be reused by several rules declared within the same class. On the other hand, it
will cache the classes by location, so a second test that wants to import classes from the same
URLs will reuse the classes previously imported as well. Note that this second caching uses
soft references, so the classes will be dropped from memory, if the heap runs low.
For further information see [Controlling the Cache](#_controlling_the_cache).

#### 

Which classes will be imported can be controlled in a declarative way through `@AnalyzeClasses`.
If no packages or locations are provided, the package of the annotated test class will be imported.
You can specify packages to import as strings:

`@AnalyzeClasses(packages = {"com.myapp.subone", "com.myapp.subtwo"})`
To better support refactorings, packages can also be declared relative to classes, i.e. the packages these classes reside in will be imported:

`@AnalyzeClasses(packagesOf = {SubOneConfiguration.class, SubTwoConfiguration.class})`
As an alternative to specifying packages, you can directly specify individual classes to be analyzed:

`@AnalyzeClasses(classes = {String.class, Integer.class})`
This allows for more fine-grained control over which classes are imported for testing.
You can combine the `classes` property with other properties like `packages`, `packagesOf`, etc.
In this case, all specified classes and packages will be imported for analysis.

As another option, locations can be specified freely by implementing a `LocationProvider`:

```
public class MyLocationProvider implements LocationProvider {
    @Override
    public Set<Location> get(Class<?> testClass) {
        // Determine Locations (= URLs) to import
        // Can also consider the actual test class, e.g. to read some custom annotation
    }
}
@AnalyzeClasses(locations = MyLocationProvider.class)
```
Furthermore, in order to choose specific classes beneath those locations, `ImportOption`s can be
specified (compare [The Core API](#_the_core_api)). The following example imports the classpath, but only considers
production code and only considers code that is directly supplied and does not come from JARs:

`@AnalyzeClasses(importOptions = {DoNotIncludeTests.class, DoNotIncludeJars.class})`
As explained in [The Core API](#_the_core_api), you can write your own custom implementation of `ImportOption`
and then supply the type to `@AnalyzeClasses`.

To import the whole classpath, instead of just the package of the test class, use the option

`@AnalyzeClasses(wholeClasspath = true)`
Note that `@AnalyzeClasses` can also be used as a meta-annotation to avoid repeating the same configuration:

```
@Retention(RetentionPolicy.RUNTIME)
@AnalyzeClasses(packagesOf = MyApplicationRoot.class, importOptions = DoNotIncludeTests.class)
public @interface AnalyzeMainClasses {}
```
This annotation can then be used on test classes without repeating the specific configuration of `@AnalyzeClasses`:

```
@AnalyzeMainClasses
public class ArchitectureTest {
    // ...
}
```
#### 

By default, all classes will be cached by location. This means that between different test class runs imported Java classes will be reused, if the exact combination of locations has already been imported.

If the heap runs low, and thus the garbage collector has to do a big sweep in one run, this can cause a noticeable delay. On the other hand, if it is known that no other test class will reuse the imported Java classes, it would make sense to deactivate this cache.

This can be achieved by configuring `CacheMode.PER_CLASS`, e.g.

`@AnalyzeClasses(packages = "com.myapp.special", cacheMode = CacheMode.PER_CLASS)`
The Java classes imported during this test run will not be cached by location and just be reused within the same test class. After all tests of this class have been run, the imported Java classes will simply be dropped.

#### 

It is possible to skip tests by annotating them with `@ArchIgnore`, for example:

```
public class ArchitectureTest {
    // will run
    @ArchTest
    public static final ArchRule rule1 = classes().should()...
    // won't run
    @ArchIgnore
    @ArchTest
    public static final ArchRule rule2 = classes().should()...
}
```
Note for users of JUnit 5 & 6: the annotation `@Disabled` has no effect here.
Instead, `@ArchIgnore` should be used.

#### 

Often, a project might end up with different categories of rules, for example "service rules" and "persistence rules". It is possible to write one class for each set of rules, and then refer to those sets from another test:

```
public class ServiceRules {
    @ArchTest
    public static final ArchRule ruleOne = ...
    // further rules
}
public class PersistenceRules {
    @ArchTest
    public static final ArchRule ruleOne = ...
    // further rules
}
// @RunWith(ArchUnitRunner.class) // Enable this line for JUnit 4
@AnalyzeClasses
public class ArchitectureTest {
    @ArchTest
    static final ArchTests serviceRules = ArchTests.in(ServiceRules.class);
    @ArchTest
    static final ArchTests persistenceRules = ArchTests.in(PersistenceRules.class);
}
```
The runner will include all `@ArchTest` annotated members within `ServiceRules` and `PersistenceRules` and evaluate
them against the classes declared within `@AnalyzeClasses` on `ArchitectureTest`.
This also allows an easy reuse of a rule library in different projects or modules.

#### 

It is possible to filter specific rules (e.g. `@ArchTest` fields) via `archunit.properties` (compare [Advanced Configuration](#_advanced_configuration)).

```
# Specify the field or method name here. Multiple names can be joined by ','
junit.testFilter=my_custom_rule_field
```
As always with `archunit.properties`, this can also be passed dynamically using a system property,
E.g. passing

`-Darchunit.junit.testFilter=my_custom_rule_field`
#### 

ArchUnit offers the possibility to generate more readable names in the test report by replacing underscores in the original rule names by spaces. For example, if a method or field is named

`some_Field_or_Method_rule`
this will appear as

`some Field or Method rule`
in the test report.

This is similar to JUnit 5’s `@DisplayNameGeneration` annotation, but because this display name generation does not
fit well with ArchUnit’s rule execution and because we’d like to offer this feature for JUnit 4 as well, you can enable
display name generation in ArchUnit with a configuration property (see [Advanced Configuration](#_advanced_configuration)):

`junit.displayName.replaceUnderscoresBySpaces=true`
If you omit the property (or set it to `false`), the original rule names are used as display names.

## 

Some behavior of ArchUnit can be centrally configured by adding a file `archunit.properties`
to the root of the classpath (e.g. under `src/test/resources`).
This section will outline some global configuration options.

### 

ArchUnit will use exactly the `archunit.properties` file returned by the context
`ClassLoader` from the classpath root, via the standard Java resource loading mechanism.

It is possible to override any property from `archunit.properties`, by passing a system property
to the respective JVM process executing ArchUnit:

`-Darchunit.propertyName=propertyValue`
E.g. to override the property `resolveMissingDependenciesFromClassPath` described in the next section, it would be possible to pass:

`-Darchunit.resolveMissingDependenciesFromClassPath=false`
### 

As mentioned in [Dealing with Missing Classes](#_dealing_with_missing_classes), it might be preferable to configure a different
import behavior if dealing with missing classes wastes too much performance.
One way that can be chosen out of the box is to never resolve any missing class from the classpath:

`resolveMissingDependenciesFromClassPath=false`
If you want to resolve just some classes from the classpath (e.g. to import missing classes from your own organization but avoid the performance impact of importing classes from 3rd party packages), it is possible to configure only specific packages to be resolved from the classpath:

```
classResolver=com.tngtech.archunit.core.importer.resolvers.SelectedClassResolverFromClasspath
classResolver.args=some.pkg.one,some.pkg.two
```
This configuration would only resolve the packages `some.pkg.one` and `some.pkg.two` from the
classpath, and stub all other missing classes.

The last example also demonstrates, how the behavior can be customized freely, for example if classes are imported from a different source and are not on the classpath:

First Supply a custom implementation of

`com.tngtech.archunit.core.importer.resolvers.ClassResolver`
Then configure it

`classResolver=some.pkg.MyCustomClassResolver`
If the resolver needs some further arguments, create a public constructor with one `List<String>`
argument, and supply the concrete arguments as

`classResolver.args=myArgOne,myArgTwo`
For further details, compare the sources of `SelectedClassResolverFromClasspath`.

#### 

It is also possible to apply a more fine-grained configuration to the import dependency resolution behavior.

In particular, the ArchUnit importer distinguishes the following types of import dependencies:

- 
member types (e.g. the type of a field of a class, type of a method parameter, etc.)
- 
accesses to types (e.g. a method calls another method of a different class)
- 
supertypes (i.e. superclasses that are extended and interfaces that are implemented)
- 
permitted subclasses (i.e. classes that are permitted to extend or implement a sealed class or interface)
- 
enclosing types (i.e. outer classes of nested classes)
- 
annotation types, including parameters of annotations
- 
generic signature types (i.e. types that comprise a parameterized type, like `List` and`String` for`List<String>` )

For each of these dependency types it is possible to configure the maximum number of iterations to traverse the dependencies.
E.g. let us assume we configure the maximum iterations as `2` for member types and we have a class `A` that declares a field of type `B` which in turn holds a field of type `C`.
On the first run we would automatically resolve the type `B` as a dependency of `A`.
On the second run we would then also resolve `C` as a member type dependency of `B`.

The configuration parameters with their defaults are the following:

```
import.dependencyResolutionProcess.maxIterationsForMemberTypes = 1
import.dependencyResolutionProcess.maxIterationsForAccessesToTypes = 1
import.dependencyResolutionProcess.maxIterationsForSupertypes = -1
import.dependencyResolutionProcess.maxIterationsForPermittedSubclasses = -1
import.dependencyResolutionProcess.maxIterationsForEnclosingTypes = -1
import.dependencyResolutionProcess.maxIterationsForAnnotationTypes = -1
import.dependencyResolutionProcess.maxIterationsForGenericSignatureTypes = -1
```
Note that setting a property to a negative value (e.g. `-1`) will not stop the resolution until all types for the given sort of dependency have been resolved.
E.g. for generic type signatures a value of `-1` will by default lead to all types comprising the signature `Map<?, List<? extends String>>` (that is `Map`, `List` and `String`) to be automatically resolved.

Setting a property to `0` will disable the automatic resolution,
which can lead to types being only partially imported or stubbed.
For these types the information is likely not complete or even wrong (e.g. an interface might be reported as class if the bytecode was never analyzed, or annotations might be missing).

On the other hand, bigger (or negative) values can have a massive performance impact. The defaults should provide a reasonable behavior. They include the class graph for all types that are used by members or accesses directly and cut the resolution at that point. However, relevant information for these types is fully imported, no matter how many iterations it takes (e.g. supertypes or generic signatures).

### 

Sometimes it can be valuable to record the MD5 sums of classes being imported to track unexpected behavior. Since this has a performance impact, it is disabled by default, but it can be activated the following way:

`enableMd5InClassSources=true`
If this feature is enabled, the MD5 sum can be queried as

`javaClass.getSource().get().getMd5sum()`
### 

By default, ArchUnit will forbid the should-part of rules to be evaluated against an empty set of classes. The reason is that this can lead to rules that by accident do not check any classes at all. Take for example

`classes().that().resideInAPackage("com.myapp.old").should()...`
Now consider somebody renames the package `old` to `newer`.
The rule will now always evaluate successfully without any reported error.
However, it actually does not check any classes at all anymore.
This is likely not what most users want.
Thus, by default ArchUnit will fail checking the rule in this case.
If you want to allow evaluating such rules,
i.e. where the actual input to the should-clause is empty,
you can use one of the following ways:

**Allow Empty Should on a Per-Rule Basis**

On each `ArchRule` you can use the method `ArchRule.allowEmptyShould(..)` to override the behavior
for a single rule, e.g.

```
// create a rule that allows that no classes are passed to the should-clause
classes().that()...should()...allowEmptyShould(true)
```
**Allow Empty Should Globally**

To allow all rules to be evaluated without checking any classes you can set the following property:

`archRule.failOnEmptyShould=false`
### 

You can configure a custom format to display the failures of a rule.

First Supply a custom implementation of

`com.tngtech.archunit.lang.FailureDisplayFormat`
Then configure it

`failureDisplayFormat=some.pkg.MyCustomFailureDisplayFormat`
One example would be to shorten the fully qualified class names in failure messages:

```
private static class SimpleClassNameFailureFormat implements FailureDisplayFormat {
    @Override
    public String formatFailure(HasDescription rule, FailureMessages failureMessages, Priority priority) {
        String failureDetails = failureMessages.stream()
                .map(message -> message.replaceAll("<(?:\\w+\\.)+([A-Z][^>]*)>", "<$1>"))
                .collect(joining(lineSeparator()));
        return String.format("Architecture Violation [Priority: %s] - Rule '%s' was violated (%s):%n%s",
                priority.asString(), rule.getDescription(), failureMessages.getInformationAboutNumberOfViolations(), failureDetails);
    }
}
```
Note that due to the free format how violation texts can be composed, in particular by custom predicates and conditions, there is at the moment no more sophisticated way than plain text parsing. Users can tailor this to their specific environments where they know which sorts of failure formats can appear in practice.
