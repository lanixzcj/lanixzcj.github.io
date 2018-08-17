---
layout: post
title: Java动态代理与插桩
description: "java"
tags: [proxy,java]
modified:   2018-07-10 18:45:15 +0800
share: false
comments: false
mathjax: false
image:
  
---

动态代理和插桩是AOP实现的两种基本原理，对这方面知识做一下总结。

<!--more-->

## Java动态代理

### JDK反射

#### 什么是反射
每一个类都有一个class对象，包含了与类有关的信息。当编译一个新类时，会产生一个同名的 .class 文件，该文件内容保存着 Class 对象。

类加载相当于 Class 对象的加载。类在第一次使用时才动态加载到 JVM 中，可以使用 Class.forName("com.mysql.jdbc.Driver") 这种方式来控制类的加载，该方法会返回一个 Class 对象。

反射可以提供运行时的类信息，并且这个类可以在运行时才加载进来，甚至在编译时期该类的 .class 不存在也可以加载进来。反射的核心是JVM在运行时才动态加载类或调用方法/访问属性，它不需要事先（写代码的时候或编译期）知道运行对象是谁。

Java反射框架主要提供以下功能：
1. 在运行时判断任意一个对象所属的类；
2. 在运行时构造任意一个类的对象；
3. 在运行时判断任意一个类所具有的成员变量和方法（通过反射甚至可以调用private方法）；
4. 在运行时调用任意一个对象的方法

#### 反射的优点
1. 扩展特性：应用程序可以通过全限定名创建外部的，用户定义的类的可扩展对象。
2. 类浏览器和可视化开发环境：可以用来枚举类的成员变量以及在开发环境中借助反射得到的类型信息帮助开发者编写正确的代码。
3. 调式和测试工具：调试器可以借助反射测试私有方法，测试工具可以借助反射发现类中所定义的方法，提高测试的代码覆盖率。
4. 开发通用框架：很多框架都是配置化的，为了保证框架的通用性，可能 需要根据配置文件加载不同的对象或类，调用不同的方法，这个时候就必须用到反射的运行时动态加载需要加载的对象。

#### 反射的缺点
1. 性能开销：由于反射是动态执行的，不能执行某些JVM的优化。与非反射的方法比，反射会有较慢的性能，应该避免在性能敏感的应用中频繁使用反射。
2. 安全限制：反射需要运行时权限，在某些安全管理环境下可能没有这个权限。
3. 内部暴露：由于反射允许代码执行一些在正常情况下不被允许的操作（比如访问私有的属性和方法），所以使用反射可能会导致意料之外的副作用，比如代码有功能上的错误，降低可移植性。反射代码破坏了抽象性，因此当平台发生改变的时候，代码的行为就有可能也随着变化。

#### 反射的使用

1. 获得Class对象
    * 使用Class类的forName静态方法：
        ``` java
        public static Class<?> forName(String className)
        
        Class.forName(driver); // JDBC中常用此方法加载数据库驱动
        ```
    * 直接获取某一个对象的clss：
        ``` java
        Class<?> klass = int.class;
        Class<?> classInt = Integer.TYPE;
        klass == classInt // true
        ```
    * 调用某个对象的getClass()方法：
        ``` java
        StringBuilder str = new StringBuilder("123");
        Class<?> klass = str.getClass();
        ```
2. 通过Class对象创建实例
    * 使用Class对象的newInstance()方法来创建Class对象对应的实例，这种方法只能实例化包含无参构造函数的类：
        ``` java
        Class<?> c = String.class;
        Object str = c.newInstance();
        ```
    * 先通过Class对象获取指定的Constructor对象，再调用Constructor对象的newInstance()方法创建实例：
        ``` java
        //获取String所对应的Class对象
        Class<?> c = String.class;
        //获取String类带一个String参数的构造器
        Constructor constructor = c.getConstructor(String.class);
        //根据构造器创建实例
        Object obj = constructor.newInstance("23333");
        System.out.println(obj);
        ```
3. 获取方法
    * getDeclaredMethods()返回类或接口声明的所有方法，包括public，protected，private，默认（包）访问的方法，但是不包括继承的方法
    * getMethods()返回所有的public方法，包括继承的public方法
    * getMethod(String name, Class<?>... parameterTypes)返回一个特定的方法
    ``` java
    import java.lang.reflect.Method;

    class methodClass {
        public final int c = 3;
        public int add(int a,int b) {
            return a + b;
        }
        public int sub(int a,int b) {
            return a - b;
        }
    }
    public class Main {
        public static void main(String[] args) throws NoSuchMethodException {
            Class<?> clazz = methodClass.class;
            Method[] methods = clazz.getMethods();
            Method[] declaredMethods = clazz.getDeclaredMethods();
            Method method = clazz.getMethod("sub", int.class, int.class);

            System.out.println(method);
            for(Method m:methods)
                System.out.println(m);

            for(Method m:declaredMethods)
                System.out.println(m);
        }
    }

    /*log:
    public int methodClass.sub(int,int)

    public int methodClass.add(int,int)
    public int methodClass.sub(int,int)
    public final void java.lang.Object.wait() throws java.lang.InterruptedException
    ...

    public int methodClass.add(int,int)
    public int methodClass.sub(int,int)*/
    ```
4. 获取构造器信息
    * 通过Class类的getConstructors()方法获取所有构造器
    * 通过Class类的getMethod(Class<?>... parameterTypes)获取特定构造器
    * 构造器对象可以通过newInstance创建实例
5. 获取类的成员变量信息
    * 通过getFields()获取所有访问public成员变量，包括继承的成员变量
    * 通过getDeclareFields()获取所有成员变量，但是不包括继承的成员变量
    * 通过getField(String name)获取public成员变量
6. 调用方法
    通过public Object invoke(Object obj, Object... args)方法进行调用，第一个参数是调用这个方法的对象
7. 操作属性
    通过Field的set()方法修改
    ``` java
    Class<?> clazz = MethodClass.class;
    Field field = clazz.getField("c");
    MethodClass methodClass = (MethodClass) clazz.newInstance();
    field.set(methodClass, 5);
    System.out.println(methodClass.c);
    ```

#### 动态代理的使用

代理（Proxy）可以理解成在目标对象之前架设一层“拦截"，外界对该对象的访问，都必须先通过这层拦截，因此提供了一种机制，可以对外界的访问进行过滤和改写。

反射包中的Field、Method类可以认为是类中某一部分信息的抽象，比如字段、方法、构造器等。Proxy类就是代理的抽象，所谓动态代理就是编写代码时不确定是哪个代理，需要在运行时才能确定，Proxy类就是在不确定时的统一代理类。

通过下面的方法可以代理所有实现这个接口的类，这也是动态代理的一个好处，可以解决多出重复逻辑代码。

``` java
public class Main {
    public static void main(String[] args) {

        Target t = new Target();
        TargetProxy proxy = new TargetProxy();
        TargetInterface target = (TargetInterface) proxy.getProxy(t);

        target.doSomething();
    }
}

interface TargetInterface {
    void doSomething();
}

class Target implements TargetInterface {

    @Override
    public void doSomething() {
        System.out.println("Do it.");
    }
}

class TargetProxy {
    Object target;

    public Object getProxy(Object target) {
        this.target = target;

        return Object Proxy.newProxyInstance(TargetProxy.class.getClassLoader(),
                target.getClass().getInterfaces(), new InvocationHandler() {
                    @Override
                    public Object invoke(Object proxy, Method method, Object[] args) throws Throwable {
                        System.out.println("Method " + method.getName() + " start");
                        Object obj = method.invoke(target, args);
                        System.out.println("Method " + method.getName() + " end");
                        return obj;
                    }
                });
    }
}
```

### Java Agent 

利用Java的Instrument功能可以构建一个独立于应用程序的代理程序（Agent），用来检测和协助运行在JVM上的程序，甚至能够替换和修改某些类的定义。有了这样的功能，开发者就可以实现更为灵活的运行时虚拟机监控和 Java 类操作了，这样的特性实际上提供了一种虚拟机级别支持的 AOP 实现方式，使得开发者无需对 JDK 做任何升级和改动，就可以实现某些 AOP 的功能了。

Instrumentaion的具体实现依赖于JVMTI，JVMTI（Java Virtual Machine Tool Interface）是一套由 Java 虚拟机提供的，为 JVM 相关的工具提供的本地编程接口集合，JVMTI 提供了一套”代理”程序机制，可以支持第三方工具程序以代理的方式连接和访问 JVM，并利用 JVMTI 提供的丰富的编程接口，完成很多跟 JVM 相关的功能。

#### Java Agent的简单使用

使用Agent可以让Instrumentation代理在main函数运行前执行，简要来说需要如下步骤：

1. 编写premain函数
    包含如下方法当中的一个：
    * public static void premain(String agentArgs, Instrumentation inst)
    * public static void premain(String agentArgs)
    其中，第一个的优先级更高，agentArgs是随着执行命令`- javaagent`传入，这个参数是一个字符串，Inst是 java.lang.instrument.Instrumentation 的实例，由 JVM 自动传入，集中了其中例如类定义的转换和操作等功能方法。
2. jar文件打包
    将这个 Java 类打包成一个 jar 文件，并在其中的 manifest 属性当中加入” Premain-Class”来指定步骤 1 当中编写的那个带有 premain 的 Java 类。
3. 运行
    用如下方式运行Java Agent：
    ``` java
    java -javaagent:jar 文件的位置 [= 传入 premain 的参数 ] -jar 所要代理的jar包
    ```

对Java类文件的操作，可以理解为在字节码级别修改类。可以通过诸如ASM或BCEL字节码操作工具直接修改类，这里通过类文件替换的方式简单地表现如何使用Instrumentation。

``` java
public class TransClass {
    static void helloWorld() {
        System.out.println("Hello World!");
    }
}

// TransClass2.class 在jar包外
public class TransClass {
    static void helloWorld() {
        System.out.println("Hello World Trans!");
    }
}

public class TestTransMain {
    public static void main(String[] args) {
        TransClass.helloWorld();
    }
}
```

TransClass2.class在jar包外，用于Java Agnet进行类文件的替换。
``` java
public class Agent {
    public static void premain(String agentArgs, Instrumentation inst) {
        inst.addTransformer(new Transformer());
    }

}

public class Transformer implements ClassFileTransformer {

    @Override
    public byte[] transform(ClassLoader loader, String className,
                            Class<?> classBeingRedefined,
                            ProtectionDomain protectionDomain,
                            byte[] classfileBuffer) throws IllegalClassFormatException {
        if (!className.equals("TransClass")) {
            return classfileBuffer;
        }
        return getBytesFromFile("TransClass2.class");
    }
    public static byte[] getBytesFromFile(String fileName) {
        try {
            File file = new File(fileName);
            InputStream is = new FileInputStream(file);
            long length = file.length();
            byte[] bytes = new byte[(int) length];

            // Read in the bytes
            int offset = 0;
            int numRead = 0;
            while (offset <bytes.length
                    && (numRead = is.read(bytes, offset, bytes.length - offset)) >= 0) {
                offset += numRead;
            }

            if (offset < bytes.length) {
                throw new IOException("Could not completely read file "
                        + file.getName());
            }
            is.close();
            return bytes;
        } catch (Exception e) {
            System.out.println("error occurs in _ClassTransformer!"
                    + e.getClass().getName());
            return null;
        }
    }

}
```

使用Idea进行打包时但是通过`java -javaagent:agent.jar -jar test.jar`会报`java.lang.NoSuchMethodException: Agent.premain`的错误，原因未知，使用maven打包后可以正常进行agent。

#### 动态Instumentation

与`premain`类似可以使用`agentmain`，函数签名也是类似的：

* public static void agentmain(String agentArgs, Instrumentation inst)
* public static void agentmain(String agentArgs)

并且类似的，也需要在mainfest文件中设置“Agent-Class”来指定包含agentmain函数的类，由于agentmain需要重新转换类或者重定义类，所以还需要设置“Can-Retransform-Classes”和“Can-Redefine-Classes”为true。

但是，与premain不同的是，agentmain需要在main函数开始运行后才启动。由于不能像premain方式那样在jvm启动命令中指定代理，可以借助Attach Tools API，这个不是Java的标准API，是Sun公司提供的一套扩展API，这套API主要有两个类，在`com.sun.tools.attach`中：VirtualMachine类代表一个虚拟机，也就是程序需要监控的目标虚拟机，提供了 JVM 枚举，Attach 动作和 Detach 动作（Attach 动作的相反行为，从 JVM 上面解除一个代理）；VirtualMachineDescriptor类则是一个描述虚拟机的容器类，配合 VirtualMachine 类完成各种功能。

首先把premain中的测试代码改为起一个线程，持续的输出，以便观察动态操作类。
``` java
public class TestDynamicTransMain {
    public static void main(String[] args) throws InterruptedException {

        while (true) {
            Thread.sleep(500);

            TransClass.helloWorld();
        }
    }
}
```

与premain类似，在agentmain中把TransClass类替换为TransClass2.class，并且需要`retransformClasses`，由于agent与所测试的程序不在一起，所以无法直接获得TransClass的class对象，使用`forName()`即可。
``` java
public static void agentmain(String agentArgs,Instrumentation inst) throws ClassNotFoundException, UnmodifiableClassException {
    System.out.println(" hello java agetnt! method agentmain method executed ! ");
    inst.addTransformer(new Transformer (), true);
    Class<?> clazz = Class.forName("TransClass");
    inst.retransformClasses(clazz);
    System.out.println("Agent Main Done");
}
```

之后使用Attach Tools API监控新的VM，通过loadAgent载入代理，做到动态代理。
``` java
public class Main {
    static class AttachThread extends Thread {

        private final List<VirtualMachineDescriptor> listBefore;

        private final String jar;

        AttachThread(String attachJar, List<VirtualMachineDescriptor> vms) {
            listBefore = vms;  // 记录程序启动时的 VM 集合
            jar = attachJar;
        }

        public void run() {
            VirtualMachine vm = null;
            List<VirtualMachineDescriptor> listAfter = null;
            try {
                int count = 0;
                while (true) {
                    listAfter = VirtualMachine.list();
                    for (VirtualMachineDescriptor vmd : listAfter) {
                        if (!listBefore.contains(vmd)) {
                            // 如果 VM 有增加，我们就认为是被监控的 VM 启动了
                            // 这时，我们开始监控这个 VM
                            vm = VirtualMachine.attach(vmd);
                            break;
                        }
                    }
                    Thread.sleep(500);
                    count++;
                    if (null != vm) {
                        System.out.println("new VM:" + vm.id());
                        break;
                    }
                }
                vm.loadAgent(jar);
                vm.detach();
            } catch (Exception e) {

            }
        }
    }

    public static void main(String[] args) {
        new AttachThread("agentmain.jar", VirtualMachine.list()).start();
    }
}
```

### Java Agent原理

#### JVMTI

JVMTI是JVM暴露出来的一些供用户扩展的接口集合。JVMTI是基于事件驱动的，JVM每执行到一定的逻辑就会主动调用一些事件的回调接口，这些接口可以供开发者扩展自己的逻辑。

### ASM

#### 什么是ASM

ASM是一个Java字节码操作框架，它能被用来动态生成类或者增强既有类的功能。ASM 可以直接产生二进制 class 文件，也可以在类被加载入 Java 虚拟机之前动态改变类行为。ASM 从类文件中读入信息后，能够改变类行为，分析类信息，甚至能够根据用户要求生成新类。

与 BCEL 和 SERL 不同，ASM 提供了更为现代的编程模型。对于 ASM 来说，Java class 被描述为一棵树；使用 “Visitor” 模式遍历整个二进制结构；事件驱动的处理方式使得用户只需要关注于对其编程有意义的部分，而不必了解 Java 类文件格式的所有细节：ASM 框架提供了默认的 “response taker”处理这一切。

#### 为什么要动态生成Java类

动态生成JAVA类与AOP密切相关的，AOP的初衷在于软件设计中有这么一类代码，零散而耦合，这是由于一些共有的功能（比如log）分散在所有模块中，同时改变log会影响到所有的模块。出现这样的问题，很大程度上是由于传统的 面向对象编程注重以继承关系为代表的“纵向”关系，而对于拥有相同功能或者说方面 （Aspect）的模块之间的“横向”关系不能很好地表达。

传统的解决方案是使用装饰着模式，它可以在一定程度上改善耦合，但是功能仍旧是分散的，每一个需要log的类都要派生一个Decorator，每个需要log的的方法都要被包装（wrap）。

动态改变Java类就是要解决AOP的问题，提供一种得到系统支持的可编程的方法，自动化地生成或者增强Java代码。

#### 为什么使用ASM

最直接的改造的Java类的方法是直接改写class文件，class文件是由严格的格式的，直接编辑字节码可以改变Java类的行为。但是这种方法对使用者有较高的要求，要十分熟悉class文件的格式，根据相对首部的偏移量找到函数位置，还需要重新计算class文件的校验码以通过Javca虚拟机的安全机制。

Instrument也提供了类似的功能，在启动Java虚拟机时挂上一个用户定义的hook程序，但是这种方法的缺点是：1. Instrument 包是在整个虚拟机上挂了一个钩子程序，每次装入一个新类的时候，都必须执行一遍这段程序，即使这个类不需要改变。2. 直接改变字节码事实上类似于直接改写 class 文件，需要提供新的Java类的字节码。

还可以通过Proxy实现，但是这种方法的缺点是：1. Proxy 是面向接口的，所有使用 Proxy 的对象都必须定义一个接口。2. Proxy是通过反射实现的，在性能开销上会比较大。

#### ASM编程框架

ASM主要包括三个类：

1. ClassReader：负责从类文件中读取输入流，并依照固定的顺序调用ClassVisitor中声明的多个visitorXxx的方法。
2. ClassVisitor：抽象类，负责类内容的访问。
3. ClassWriter：负责生成byte[]字节流，ClassWriter是ClassVisitor的子类

在 ASM 中，提供了一个 ClassReader类，这个类可以直接由字节数组或由 class 文件间接的获得字节码数据，它能正确的分析字节码，构建出抽象的树在内存中表示字节码。它会调用 accept方法，这个方法接受一个实现了 ClassVisitor接口的对象实例作为参数，然后依次调用 ClassVisitor接口的各个方法。字节码空间上的偏移被转换成 visit 事件时间上调用的先后，所谓 visit 事件是指对各种不同 visit 函数的调用，ClassReader知道如何调用各种 visit 函数。在这个过程中用户无法对操作进行干涉，所以遍历的算法是确定的，用户可以做的是提供不同的 Visitor 来对字节码树进行不同的修改。ClassVisitor会产生一些子过程，比如 visitMethod会返回一个实现 MethordVisitor接口的实例，visitField会返回一个实现 FieldVisitor接口的实例，完成子过程后控制返回到父过程，继续访问下一节点。因此对于 ClassReader来说，其内部顺序访问是有一定要求的。

ClassVisitor里的方法的执行顺序如下：
```
visit visitSource? visitOuterClass? ( visitAnnotation | visitAttribute )*
( visitInnerClass | visitField | visitMethod )*
visitEnd
```

#### ASM简单例子

基本的流程就是通过ClassReader得到类的字节码数据，通过ClassVisitor遍历类的内容并做相应的操作，通过ClassWriter输出所修改的类。

``` java
ClassReader classReader = new ClassReader("TransClass");
ClassWriter cw = new ClassWriter(0);
ClassVisitor cp = new ClassPrinter(cw);

classReader.accept(cp, ASM6);

FileOutputStream outputStream = new FileOutputStream("TransClass2.class");
outputStream.write(cw.toByteArray());
outputStream.close();
```

通过继承自定义一个ClassVisitor，super的第二参数是传进来的ClassWriter，作为局部变量，其他方法可以直接使用。
ClassWriter也一定要调用visit方法，因为这里包含了Class文件的版本信息，否则会造成ClsasWriter的class文件版本号为0，无法通过JVM的验证。
这里希望在之前的TransClass类的静态方法helloWorld()的开始加一句log，所以还需要关注ClassVisitor的visitMethod方法。
``` java
public class ClassPrinter extends ClassVisitor {
    public ClassPrinter(ClassVisitor cv) {
        super(ASM6, cv);
    }

    public void visit(int version, int access, String name, String signature,
                      String superName, String[] interfaces) {
        if (cv != null) {
            cv.visit(version, access, name, signature, superName, interfaces);
        }
    }

    public MethodVisitor visitMethod(int access, String name, String desc, String signature, String[] exceptions) {
        if ("helloWorld".equals(name)) {
            MethodVisitor mv = cv.visitMethod(access, name, desc, signature, exceptions);
            return new MyMethodVisitor(mv);
        }

        if (cv != null) {
            return cv.visitMethod(access, name, desc, signature, exceptions);
        }

        return null;
    }

}
```

类似的，也定义了一个MethodVisitor类，其中visitCode就是在执行函数体之前会调用的方法，可以在这里加入所需要加的代码。
``` java
public class MyMethodVisitor extends MethodVisitor {
    public MyMethodVisitor(MethodVisitor mv) {
        super(ASM6, mv);
    }

    @Override
    public void visitCode() {
        mv.visitFieldInsn(GETSTATIC, "java/lang/System", "out", "Ljava/io/PrintStream;");
        mv.visitLdcInsn("========start=========");
        mv.visitMethodInsn(INVOKEVIRTUAL, "java/io/PrintStream", "println", "(Ljava/lang/String;)V", false);

        super.visitCode();
    }
}
```

### BCEL

### CGLIB

#### 什么是CGLIB

CGLIB是一个强大的、高性能的代码生成库。其被广泛应用于AOP框架（Spring、dynaop）中，用以提供方法拦截操作。

#### 为什么使用CGLIB

CGLIB代理主要通过对字节码的操作，为对象引入间接级别，以控制对象的访问。我们知道Java中有一个动态代理也是做这个事情的，那我们为什么不直接使用Java动态代理，而要使用CGLIB呢？答案是CGLIB相比于JDK动态代理更加强大，JDK动态代理虽然简单易用，但是其有一个致命缺陷是，只能对接口进行代理。如果要代理的类为一个普通类、没有接口，那么Java动态代理就没法使用了。

CGLIB底层使用了ASM来操作字节码生成新的类。

### JAVASSIST

javassist是jboss的一个子项目，其主要的优点，在于简单，而且快速。直接使用java编码的形式，而不需要了解虚拟机指令，就能动态改变类的结构，或者动态生成类。