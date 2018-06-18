---
layout: post
title: 设计模式学习笔记
description: "设计模式学习笔记"
tags: [java,design pattern]
modified:   2018-03-19 19:23:44 +0800
share: false
comments: false
mathjax: false
image:
  
---

对设计模式的总结，并用java进行实现。

<!--more-->

## 创建型模式

### 工厂模式

#### 适用场景

希望根据不同情况创建不同的子类，而不是直接创建具体的类。

#### 简单工厂模式

这不是一个设计模式，更像是一种编程习惯。有一些子类实现了同一个接口，要根据需求实例化具体的实例，可以把实例化的操作放在工厂中，由工厂决定实例化哪个子类。

模式组成：抽象产品，具体产品，工厂

##### 编程实例

铁匠可以制造武器，精灵需要精灵武器，兽人需要兽人武器，铁匠根据顾客制造具体的武器。

``` java
public interface Weapon {
    void attack();
}

enum CareerType {
    ELF,
    ORC
}

class ElfWeapon implements Weapon {
    @Override
    public void attack() {
        System.out.println("Elf attack.");
    }
}

class OrcWeapon implements Weapon {
    @Override
    public void attack() {
        System.out.println("Orc attack.");
    }
}
```

``` java
public class SimpleFactory {
    public Weapon manufactureWeapon(CareerType CareerType) {
        switch (CareerType) {
            case ELF:
                return new ElfWeapon();
            case ORC:
                return new OrcWeapon();
            default:
                throw new UnsupportedOperationException();
        }
    }
}
```

``` java
public static void main(String[] args) {
    SimpleFactory factory = new SimpleFactory();
    Weapon elfWeapon = factory.manufactureWeapon(CareerType.ELF);
    Weapon orcWeapon = factory.manufactureWeapon(CareerType.ORC);
    elfWeapon.attack();
    orcWeapon.attack();
}
```
#### 工厂方法模式

简单工厂模式中，如果还需要再加新的武器，就需要在工厂中修改相应的分支，容易造成错误。
工厂方法是相当于对工厂做了一层抽象，核心工厂只提供工厂子类所需要的接口，实例化过程推迟到子类，这样添加新的武器就不需要修改原有的工厂角色。

模式组成：抽象产品，具体产品，抽象工厂，具体工厂

##### 编程实例

还是用铁匠的例子。

``` java
public interface FactoryMethod {
    Weapon manufactureWeapon();
}

class ElfFactory implements FactoryMethod {

    @Override
    public Weapon manufactureWeapon() {
        return new ElfWeapon();
    }
}

class OrcFactory implements FactoryMethod {

    @Override
    public Weapon manufactureWeapon() {
        return new OrcWeapon();
    }
}
```

``` java
public static void main(String[] args) {
    FactoryMethod elfFactory = new ElfFactory();
    elfWeapon = elfFactory.manufactureWeapon();
    FactoryMethod orcFactory = new OrcFactory();
    orcWeapon = orcFactory.manufactureWeapon();
    elfWeapon.attack();
    orcWeapon.attack();
}
```

##### 现实例子

java.util.Calendar包中的getIntance方法，可以根据时区返回相应的Calendar实例

``` java
public static Calendar getInstance(TimeZone zone)
```

#### 抽象工厂模式

与工厂方法相比，抽象层次又多了一层，工厂方法的工厂子类依赖于某个具体的类，而抽象工厂的工厂子类是**创建一组**具有关联的实例，依赖于抽象。

模式组成：抽象产品族，抽象产品，具体产品，抽象工厂，具体工厂

##### 编程实例

在之前的铁匠例子中，加入盔甲的制造。铁匠可以给精灵或兽人制造武器和盔甲。

``` java
interface EquipFactory {
    Weapon manufactureWeapon();
    Armor manufactureArmor();
}

class ElfAbstractFactory implements EquipFactory {

    @Override
    public Weapon manufactureWeapon() {
        return new ElfWeapon();
    }

    @Override
    public Armor manufactureArmor() {
        return new ElfArmor();
    }
}

class OrcAbstractFactory implements EquipFactory {

    @Override
    public Weapon manufactureWeapon() {
        return new OrcWeapon();
    }

    @Override
    public Armor manufactureArmor() {
        return new OrcArmor();
    }
}
public class AbstractFactory {
    static public EquipFactory makeFactory(CareerType careerType) {
        switch (careerType) {
            case ELF:
                return new ElfAbstractFactory();
            case ORC:
                return new OrcAbstractFactory();
            default:
                throw new UnsupportedOperationException();
        }
    }
}
```

``` java
public static void main(String[] args) {
    EquipFactory elfEquioFactory = AbstractFactory.makeFactory(CareerType.ELF);
    EquipFactory orcEquioFactory = AbstractFactory.makeFactory(CareerType.ORC);
    elfWeapon = elfEquioFactory.manufactureWeapon();
    Armor elfArmor = elfEquioFactory.manufactureArmor();
    orcWeapon = orcEquioFactory.manufactureWeapon();
    Armor orcArmor = orcEquioFactory.manufactureArmor();
    elfArmor.defense();
    orcArmor.defense();
    elfWeapon.attack();
    orcWeapon.attack();
}
```

##### 现实例子

javax.xml.xpath.XPathFactory包可以通过uri返回一个Xpath工厂

### 单例模式

#### 适用场景

当类只希望有一个实例的时候

#### 编程实例

1. 懒汉式

``` java
public class Singleton {
    private static Singleton sIntance;
    private Singleton() {

    }

    public Singleton getsIntance() {
        if (sIntance == null) {
            sIntance = new Singleton();
        }

        return sIntance;
    }
}
```

但是这是线程不安全的，可以通过对方法加锁，避免多个线程进入该方法。

``` java
public static Singleton getsIntance() {
    if (sIntance == null) {
        sIntance = new Singleton();
    }

    return sIntance;
}

```

但是这样会有性能上的问题，会出现线程等待的情况。可以使用双重校验锁的方法，只对初始化的时候做加锁操作。

``` java
public static Singleton getsIntance() {
    if (sIntance == null) {
        synchronized (Singleton.class) {
            if (sIntance == null) {
                sIntance = new Singleton();
            }
        }
    }

    return sIntance;
}
```

2. 饿汉式

可以对静态变量直接做初始化操作，但是这样失去了延迟初始化节约资源的优势。

``` java
private static Singleton sIntance = new Singleton();
```

3. 内部类

可以在内部类中的静态变量做初始化操作，这样既线程安全，也可以延迟初始化

``` java
class Singleton {
    static class InnerClass {
        private static final Singleton INSTANCE = new Singleton();
    }
    private Singleton() {

    }

    public static  Singleton getsIntance() {
        return InnerClass.INSTANCE;
    }
}
```

4. 枚举法（推荐）

简便有效，原理是INTANCE会作为enum的static变量存在，可以直接访问INTANCE得到单例

``` java
public enum Singleton {
    INTANCE;
}
```

### 建造者模式

建造者模式将一个复杂的对象的创建和表示分开，使得相同的创建过程可以创建不同的表示。当构造函数参数很多时，往往要考虑建造者模式。

在建造者模式中会有个builder来管理对象参数，往往每个管理方法都会返回builder，这样就可以通过链式调用来清晰的表现创建对象的过程。
#### 适用场景

一个对象的创建方法很复杂，有很复杂的内部结构。希望可以分离对象的创建和使用，并使得相同的创建过程可以创建不同的产品，或者是把创建过程分解为很多部分，简化创建过程。

#### 编程实例

在游戏一开始创建角色的时候，你可以逐一的选择姓名，职业，初始武器装备等等，生成角色的过程变成了一个逐步的过程。

``` java
public class Hero {
    Weapon weapon;
    Armor armor;
    String name;
    String career;

    public Hero(Builder builder) {
        this.name = builder.name;
        this.career = builder.career;
        this.weapon = builder.weapon;
        this.armor = builder.armor;
    }
}

class Builder {
    Weapon weapon;
    Armor armor;
    String name;
    String career;

    public Builder(String name, String career) {
        this.name = name;
        this.career = career;
    }

    public Builder withWeapon(Weapon weapon) {
        this.weapon = weapon;
        return this;
    }

    public Builder withArmor(Armor armor) {
        this.armor = armor;
        return this;
    }

    public Hero build() {
        return new Hero(this);
    }
}
```

``` java
public static void main(String[] args) {
    Hero hero = new Builder("hero", "Orc").withWeapon(new OrcWeapon()).withArmor(new OrcArmor()).build();
    hero.weapon.attack();
    hero.armor.defense();
}
```

#### 现实例子

Stringbuilder就使用了建造者模式，像append，insert等操作仍然返回Stringbuilder。而substring和toString就有点类似于build方法，创建一个实际的String对象。

### 原型模式

通过拷贝原型来创建新的实例。

#### 适应场景

1. 对象类型需要在运行时确定。
1. 对象之间的区别比较小，通过拷贝原型再修改的成本要小于直接创建对象。

#### 编程实例

java可以轻易的实现原型模式，只要实现Cloneable接口，并使用clone方法即可拷贝

``` java
public class Sheep implements Cloneable {
    String name;

    public Sheep(String name) {
        this.name = name;
    }

    public void setName(String name) { this.name = name; }
    public String getName() { return name; }

    @Override
    public Sheep clone() {
        return new Sheep(this.name);
    }
}
```

``` java
public static void main(String[] args) {
    Sheep jolly = new Sheep("Jolly");

    Sheep dolly = jolly.clone();
    dolly.setName("Dolly");
}
```

## 结构型模式

### 适配器模式

适配器模式可以在适配器中包装一个不兼容的类，使其与另一个类兼容。

有两种实现方式：对象方式和类方式。对象方式是让适配器拥有一个待适配的对象，从而把相应的处理委托个这个对象。类方式则用到了多重继承，同时实现原有类和所需要的接口。

#### 适用场景

1. 希望使用现有的类，但是他的接口不是你想要的
1. 使用适配器作为第三方库和程序的中间层

#### 编程实例

我们购买了一个进口的电器，要求电压是110V，但是国内的电压是220V，需要一个适配器把220V的电压转变成110V以兼容进口电器

``` java
interface Target_110V {
    void work_110V();
}

interface Target_220V {
    void work_220V();
}

class ImportTV implements Target_110V {

    @Override
    public void work_110V() {
        System.out.println("Work.");
    }
}

public class Adapter implements Target_220V {
    private ImportTV tv;

    public Adapter(ImportTV tv) {
        this.tv = tv;
    }

    @Override
    public void work_220V() {
        this.tv.work_110V();
    }
}
```

``` java
public static void main(String[] args) {
    ImportTV tv = new ImportTV();
    Adapter adapter = new Adapter(tv);
    adapter.work_220V();
}
```

### 桥接模式

使抽象和实现分离，两者可以同时变化。
桥接模式把抽象与实现解耦，也就是把强关系（继承）转换为弱关系（关联关系，如组合）。

#### 适用场景

1. 希望在抽象角色与具体角色之间增加更多的灵活性，而不是直接的静态继承
1. 一个类存在两个独立变化的维度，并且两个维度都需要扩展

#### 编程实例

武器可以有不同种类，并且可以附带不同的魔法属性。传统方法可以为每个武器创建不同魔法的子类，也可以直接对武器设置魔法属性（组合的方法）

``` java
public interface Magic {
    String magicApply();
}

class IceMagic implements Magic {

    @Override
    public String magicApply() {
        return "Ice";
    }
}

class FireMagic implements Magic {

    @Override
    public String magicApply() {
        return "Fire";
    }
}

public interface Weapon {
    void attack();
}

class Sword implements Weapon {
    private Magic magic;

    public Sword(Magic magic) {
        this.magic = magic;
    }

    @Override
    public void attack() {
        System.out.println(this.magic.magicApply() + " sword attack.");
    }
}

class Hammer implements Weapon {
    private Magic magic;

    public Hammer(Magic magic) {
        this.magic = magic;
    }

    @Override
    public void attack() {
        System.out.println(this.magic.magicApply() + " hammer attack.");
    }
}
```

``` java
public static void main(String[] args) {
    Weapon weapon = new Sword(new FireMagic());
    weapon.attack();
}
```

### 组合模式

将对象组合成树结构来表现“整体/部分”层次结构，组合能让客户以一致的方式处理对象和组合对象

#### 适用场景

1. 想表示“整体/部分”层次结构
1. 希望可以忽略单一对象与组合对象之间的差异，统一处理单一对象和组合对象

#### 编程实例

每句话均有单词组成，每个单词由字母组成，这就是一个树型的结构。每个对象是可以打印的，并且有一些不同的打印规则，比如单词前有空格，句子后有句号。

``` java
public abstract class LetterComposite {
    private List<LetterComposite> chidlren = new ArrayList<>();

    public void add(LetterComposite letterComposite) {
        this.chidlren.add(letterComposite);
    }

    public void printBefore() {}
    public void printAfter() {}

    public void print() {
        printBefore();
        for (LetterComposite l : this.chidlren) {
            l.print();
        }
        printAfter();
    }
}

class Letter extends LetterComposite {
    private char c;

    public Letter(char c) {
        this.c = c;
    }

    @Override
    public void printBefore() {
        System.out.print(this.c);
    }
}

class Word extends LetterComposite {
    public Word(List<Letter> letters) {
        for (Letter l : letters) {
            this.add(l);
        }
    }

    @Override
    public void printBefore() {
        System.out.print(" ");
    }
}

class Sentence extends LetterComposite {
    public Sentence(List<Word> words) {
        for (Word w : words) {
            this.add(w);
        }
    }

    @Override
    public void printAfter() {
        System.out.print(".");
    }
}
```

``` java
public static void main(String[] args) {
    List<Word> words = new ArrayList<>();

    words.add(new Word(Arrays.asList(new Letter('H'), new Letter('e'),new Letter('l'), new Letter('l'), new Letter('o'))));
    words.add(new Word(Arrays.asList(new Letter('w'), new Letter('o'),new Letter('r'), new Letter('l'), new Letter('d'))));
    Sentence sentence = new Sentence(words);
    sentence.print();
}
```

#### 现实例子

各个UI库中组件。组件间有包含关系，但又继承自通过一个父类。

### 装饰模式

装饰模式可以动态给对象添加额外的职责，但是**不影响其他同类的对象**。在java中一般通过组合的方式在装饰类中持有所扩展的对象

#### 适用场景

希望扩展功能，但是通过子类扩展功能不切实际时（比如类的定义被隐藏）

#### 编程实例

兽人有的时候空手，有的时候可使用棍棒

``` java
interface Orc {
    void attack();
    int getPower();
}

class SimpleOrc implements Orc {

    @Override
    public void attack() {
        System.out.println("Punch.");
        System.out.println("Power is " + getPower());
    }

    @Override
    public int getPower() {
        return 10;
    }
}
public class Decorator implements Orc{
    private SimpleOrc orc;

    public Decorator(SimpleOrc orc) {
        this.orc = orc;
    }

    @Override
    public void attack() {
        System.out.println("Swing with a club.");
        System.out.println("Power is " + getPower());
    }

    @Override
    public int getPower() {
        return orc.getPower() + 10;
    }
}
```

``` java
public static void main(String[] args) {
    SimpleOrc simpleOrc = new SimpleOrc();
    simpleOrc.attack();

    Decorator orc = new Decorator(simpleOrc);
    orc.attack();
}
```

### 外观模式

为子系统的一组接口提供一个高级的，统一的接口

#### 适用场景

1. 希望为复杂的子系统提供简单的接口
1. 希望使子系统分层，可以通过外观模式定义子系统的入口

#### 编程实例

起床之后开灯，开电视，睡觉前关灯，关电视。不使用外观模式的话，就要单独的操作每个电器，可以使用外观模式统一的操作所有电器

``` java
class Light {
    public void on() {
        System.out.println("Turn on the light.");
    }

    public void off() {
        System.out.println("Turn off the light.");
    }
}

class Television {
    public void on() {
        System.out.println("Turn on the television.");
    }

    public void off() {
        System.out.println("Turn off the television.");
    }
}
public class Facade {
    private Light light;
    private Television television;

    public Facade() {
        light = new Light();
        television = new Television();
    }

    public void on() {
        light.on();
        television.on();
    }

    public void off() {
        light.off();
        television.off();
    }
}
```

``` java
public static void main(String[] args) {
    Facade facade = new Facade();
    facade.on();
    facade.off();
}
```

### 享元模式

通过使相似的对象共享内存来减少内存开销

#### 编程实例

巫医商店中有魔法药水，相同种类的药水功效是相同的，没必要再新建对象。

``` java
interface Potion {
    void drink();
}

class HealingPotion implements Potion {

    @Override
    public void drink() {
        System.out.printf("Healed.This is %d\n", System.identityHashCode(this));
    }
}

class HolyWaterPotionPotion implements Potion {

    @Override
    public void drink() {
        System.out.printf("Blessed.This is %d\n", System.identityHashCode(this));
    }
}

enum PotionType {
    HEALING,
    HOLY_WATER
}
public class PotionFactory {
    private final Map<PotionType, Potion> potions;

    public PotionFactory() {
        potions = new EnumMap<PotionType, Potion>(PotionType.class);
    }

    public Potion createPotion(PotionType type) {
        Potion potion = potions.get(type);

        if (potion == null) {
            switch (type) {
                case HEALING:
                    potion = new HealingPotion();
                    potions.put(type, potion);
                    break;
                case HOLY_WATER:
                    potion = new HolyWaterPotionPotion();
                    potions.put(type, potion);
                    break;
            }
        }

        return potion;
    }
}
```

``` java
public static void main(String[] args) {
    PotionFactory potions = new PotionFactory();
    potions.createPotion(PotionType.HEALING).drink();
    potions.createPotion(PotionType.HEALING).drink();
    potions.createPotion(PotionType.HOLY_WATER).drink();
    potions.createPotion(PotionType.HOLY_WATER).drink();
}
```

#### 现实例子

包装类Integer中，在较小的范围（128以内）里是共享内存的，直接用“==”是相等的

### 代理模式

给目标对象提供一个代理对象，并由代理对象控制对目标对象的引用

代理模式与装饰模式很相似。但是代理模式关注的是对目标对象的控制，直接访问目标对象不方便或者不符合需要，往往是在代理类中或者远程创建对象。而装饰模式是希望动态地在对象上添加方法，往往是在装饰者外创建实例并通过参数传入装饰着。总结来说区别就是代理类和目标对象的关系在编译时就确定了，而装饰者可以在运行时递归的构造。

### 适用场景

1. 访问控制：控制目标对象的访问权限
1. 远程代理：为一个对象在不同的地址空间提供局部的代表时

### 编程实例

巫医会去当地的塔中学习魔法，但是只有前三个可以进入学习。

``` java
class Wizard {
    public String name;

    public Wizard(String name) {
        this.name = name;
    }
}

interface TowerInterface {
    void enter(Wizard wizard);
}

class Tower implements TowerInterface {
    @Override
    public void enter(Wizard wizard) {
        System.out.println(wizard.name + " enters the tower.");
    }

}
public class TowerProxy implements TowerInterface {
    private final static int NUM_Wizard_ALLOWED = 3;
    private int numWizards = 0;

    private Tower tower;

    public TowerProxy() {
        tower = new Tower();
    }

    @Override
    public void enter(Wizard wizard) {
        if (numWizards < NUM_Wizard_ALLOWED) {
            tower.enter(wizard);
            numWizards++;
        } else {
            System.out.println(wizard.name + " is not allowed to enter the tower.");
        }
    }
}
```

``` java
public static void main(String[] args) {
    TowerProxy towerProxy = new TowerProxy();
    towerProxy.enter(new Wizard("Red"));
    towerProxy.enter(new Wizard("Blue"));
    towerProxy.enter(new Wizard("Green"));
    towerProxy.enter(new Wizard("Black"));
}
```

#### 现实例子

java的动态代理类Proxy，可以在运行时动态的调用代理实例的方法。

## 行为模式

### 职责链模式

使多个对象都有机会处理请求，从而避免请求的发起者和接受者之间的耦合关系。将这些对象连成一个链，并沿着这条链传递请求直到有对象处理它为止。

#### 适用场景

1. 不止一个对象可以处理请求，并且发起者不知道哪个会处理请求。比如点击事件的分发。
1. 想向其中一个对象发送请求，又不想指定接收者

#### 编程实例

兽王向军队发送命令，最先由指挥官接收命令，再下达到士兵，构成一条职责链

``` java
enum RequestType {
    DEFEND_CASTLE,
    COLLECT_TAX
}

class Request {
    private final RequestType type;
    private final String requestDescription;
    private boolean handled;

    public Request(final RequestType type, final String requestDescription) {
        this.type = type;
        this.requestDescription = requestDescription;
        handled = false;
    }

    public String getRequestDescription() {
        return requestDescription;
    }

    public RequestType getType() {
        return type;
    }

    public void markHandled() {
        this.handled = true;
    }

    public boolean isHandled() {
        return this.handled;
    }

    @Override
    public String toString() {
        return getRequestDescription();
    }
}

abstract class RequestHandler {
    private RequestHandler next;

    public RequestHandler(RequestHandler next) {
        this.next = next;
    }

    public void handleRequest(Request request) {
        if (next != null) {
            next.handleRequest(request);
        }
    }

    public void printHandleRequest(Request request) {
        System.out.println(this + " handling request " + request);
    }

    @Override
    public abstract String toString();
}

class CommanderHandler extends RequestHandler {

    public CommanderHandler(RequestHandler next) {
        super(next);
    }

    @Override
    public void handleRequest(Request request) {
        if (request.getType() == RequestType.DEFEND_CASTLE) {
            request.markHandled();
            printHandleRequest(request);
        } else {
            super.handleRequest(request);
        }
    }

    @Override
    public String toString() {
        return "Commander";
    }
}

class SoldierHandler extends RequestHandler {

    public SoldierHandler(RequestHandler next) {
        super(next);
    }

    @Override
    public void handleRequest(Request request) {
        if (request.getType() == RequestType.COLLECT_TAX) {
            request.markHandled();
            printHandleRequest(request);
        } else {
            super.handleRequest(request);
        }
    }

    @Override
    public String toString() {
        return "Soldier";
    }
}

public class OrcKing {
    private RequestHandler chain;

    public OrcKing() {
        buildChain();
    }

    private void buildChain() {
        chain = new CommanderHandler(new SoldierHandler(null));
    }

    public void makeReqeust(Request request) {
        chain.handleRequest(request);
    }
}
```

``` java
public static void main(String[] args) {
    OrcKing orcKing = new OrcKing();
    orcKing.makeReqeust(new Request(RequestType.DEFEND_CASTLE, "defend castle"));
    orcKing.makeReqeust(new Request(RequestType.COLLECT_TAX, "collect tax"));
}
```

#### 现实例子

1. Logger类的log方法
1. servlet.Filter的doFilter方法

### 命令模式

将命令封装为对象，以便使用不同的命令来参数化其他对象。

#### 适用场景

1. 抽象出待执行的动作以参数化某对象，这种机制类似于回调函数。先注册好动作，在适当的时候通过命令来执行
1. 需要支持取消，重做操作

#### 编程实例

巫师通过缩小魔法使哥布林变小

``` java
public interface Command {
    void execute(Target target);
}

enum Size {
    SMALL,
    NORMAL
}

interface Target {
    Size getSize();
    void setSize(Size size);
    void printStats();
}

class ShrinkSpell implements Command {

    @Override
    public void execute(Target target) {
        target.setSize(Size.SMALL);
    }
}

class Goblin implements Target {
    private Size size;

    public Goblin() {
        this.size = Size.NORMAL;
    }

    @Override
    public Size getSize() {
        return size;
    }

    @Override
    public void setSize(Size size) {
        this.size = size;
    }

    @Override
    public String toString() {
        return "Goblin";
    }

    @Override
    public void printStats() {
        System.out.println(this + " is " + getSize());
    }
}

class Wizard {
    public void castSpell(Command command, Target target) {
        command.execute(target);
    }
}
```

``` java
public static void main(String[] args) {
    Goblin goblin = new Goblin();
    Wizard wizard = new Wizard();

    goblin.printStats();
    wizard.castSpell(new ShrinkSpell(), goblin);
    goblin.printStats();
}
```

#### 现实例子

Runnable接口，run命令

### 解释器模式

给定一个语言，为它的语言定义一种表示，解释器使用这个表示来解释语言中的句子

### 迭代器模式

提供顺序访问一个聚合对象中各个元素的方法，而又不暴露聚合对象内部的表示

#### 适用场景

1. 访问一个聚合对象的内容而无暴露它的内部表示
1. 为遍历不同的聚合结构提供一个统一的接口

#### 现实例子

实现Iterable接口的容器类

### 中介者模式

用中介者对象来封装一系列的对象交互。中介者使对象不需要显示的相互引用，从而使其松耦合

#### 适用场景

1. 一组对象定义良好，但是之间的相互依赖关系复杂
1. 一个对象引用大量其他对象，并且直接与这些对象通信，导致难以复用

### 备忘录模式

在不破坏封装性的前提下，捕获一个对象的内部状态并备份，以便之后可以把这个对象恢复到之前的状态。

#### 适用场景

1. 必须保存一个对象在某一时刻的状态
1. 获取状态的接口会暴露内部细节的时候

#### 编程实例

记录下行走了多少距离与消耗的时间，获取备份没有暴露任何细节接口。

``` java
interface WalkMemento {
}

public class Walk {
    private int time;
    private int distance;
    private Random random;

    public Walk() {
        time = 0;
        distance = 0;
        random = new Random();
    }

    public void timePassed() {
        time += random.nextInt(10);
        distance += random.nextInt(20);
    }

    public WalkMemento getMemento() {
        InternalMemento memento = new InternalMemento(time, distance);

        return memento;
    }

    public void setMemento(WalkMemento memento) {
        InternalMemento internalMemento = (InternalMemento)memento;
        this.time = internalMemento.getTime();
        this.distance = internalMemento.getDistance();
    }

    public void printStats() {
        System.out.printf("Spend %d s walking %d meters.\n", time, distance);
    }

    class InternalMemento implements WalkMemento {
        private int time;
        private int distance;

        public InternalMemento(int time, int distance) {
            this.time = time;
            this.distance = distance;
        }

        public int getTime() {
            return time;
        }

        public int getDistance() {
            return distance;
        }
    }
}
```

``` java
public static void main(String[] args) {
    Walk walk = new Walk();

    walk.printStats();
    walk.timePassed();
    walk.printStats();

    WalkMemento memento = walk.getMemento();

    walk.timePassed();
    walk.printStats();

    walk.setMemento(memento);
    walk.printStats();
}
```

### 观察者模式

描述了对象间的一对多关系，当一个对象发生改变时，所有依赖于它的对象都得到通知并被自动更新

#### 适用场景

1. 当一个抽象模型有两方面，其中一个依赖于另一个。将二者独立的封装，以便可以独自地改变和复用
1. 当一个对象改变，需要有多个对象同时改变，而又不知道有多少对象待改变

#### 编程实例

``` java
public class Weather {
    private List<WeatherObserver> observers;
    private WeatherType currentWeather;

    public Weather() {
        observers = new ArrayList<>();
    }

    public void addObserver(WeatherObserver observer) {
        observers.add(observer);
        currentWeather = WeatherType.RAINY;
    }

    public void removeObserver(WeatherObserver observer) {
        observers.remove(observer);
    }

    public void changeWeather() {
        WeatherType[] enumValues = WeatherType.values();
        currentWeather = enumValues[(currentWeather.ordinal() + 1) % enumValues.length];
        notifyObservers();
    }

    public void notifyObservers() {
        for (WeatherObserver observer : observers) {
            observer.update(currentWeather);
        }
    }
}

enum WeatherType {
    SUNNY,
    RAINY
}

interface WeatherObserver {
    void update(WeatherType type);
}

class Orc implements WeatherObserver {

    @Override
    public void update(WeatherType type) {
        switch (type) {
            case RAINY:
                System.out.println("Orc in the rain.");
                break;
            case SUNNY:
                System.out.println("Orc under the sun.");
                break;
        }
    }
}

class Wizard implements WeatherObserver {

    @Override
    public void update(WeatherType type) {
        switch (type) {
            case RAINY:
                System.out.println("Wizard in the rain.");
                break;
            case SUNNY:
                System.out.println("Wizard under the sun.");
                break;
        }
    }
}
```

``` java
public static void main(String[] args) {
    Weather weather = new Weather();
    Orc orc = new Orc();
    Wizard wizard = new Wizard();

    weather.addObserver(orc);
    weather.addObserver(wizard);
    weather.changeWeather();
    weather.removeObserver(wizard);
    weather.changeWeather();
}
```

### 状态模式

允许一个对象在其内部状态改变时改变它的行为

#### 适用场景

1. 一个对象的行为取决于它的当前状态

#### 现实例子

React（一个js UI库）组件中的state

### 策略模式

定义一系列算法，把他们一个个封装起来，并且使它们可以相互替换。

#### 适用场景

1. 需要使用一个算法的不同变体
1. 需要多相关类仅仅是行为有区别，“策略”提供了一种用多种行为中的一个行为配置一个类的方法


### 访问者模式

表示一个作用于某对象结构中的各元素的操作

#### 适用场景

1. 数据结构稳定，作用于数据结构的操作经常变化

### 模板方法模式

定义了一个操作中算法的骨架，而将一些步骤延迟到子类中

#### 适用场景

1. 一次性实现一个算法的不变部分，把可变的行为留个子类实现
1. 子类中的公共行为应该被提取出来集中到一个公共父类中


