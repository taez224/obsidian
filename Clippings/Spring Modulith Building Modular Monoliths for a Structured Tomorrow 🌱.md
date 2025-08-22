---
title: "Spring Modulith: Building Modular Monoliths for a Structured Tomorrow 🌱"
source: "https://halilural5.medium.com/spring-modulith-building-modular-monoliths-for-a-structured-tomorrow-f52da666c233"
author:
  - "[[Halil Ural]]"
published: 2024-09-14
created: 2025-01-26
description: "In the ever-evolving world of software development, the debate between monoliths and microservices has been a long-standing one. While microservices have stolen the spotlight in recent years, there’s…"
tags:
  - "clippings"
---
[

![Halil Ural](https://miro.medium.com/v2/resize:fill:88:88/1*8obE3QWT3suEpmpdoUdkvA@2x.jpeg)

](https://halilural5.medium.com/?source=post_page---byline--f52da666c233--------------------------------)

![](https://miro.medium.com/v2/resize:fit:800/1*wvlcQ5l7zECkKhqVT2T5Kw@2x.jpeg)

In the ever-evolving world of software development, the debate between monoliths and microservices has been a long-standing one. While microservices have stolen the spotlight in recent years, there’s a growing movement in favor of a more balanced approach: **modular monoliths**. And at the heart of this movement is **Spring Modulith** – a powerful tool that helps developers design modular monoliths with ease and precision.

> “Simplicity is the ultimate sophistication.” – Leonardo da Vinci

Spring Modulith embodies this quote perfectly, offering simplicity in design while maintaining the sophistication necessary for scaling enterprise-level applications. In this article, we’ll dive into what makes **Spring Modulith** a game-changer for software architects, developers, and DevOps teams alike.

## What Is a Modular Monolith? 🏗️

Before we explore Spring Modulith, let’s define the term *“modular monolith.”* A **monolith** refers to a large, single application where everything is interconnected. Traditional monoliths often become **difficult to maintain** due to tightly coupled components. Enter the **modular monolith**: a design approach where the application is structured into **modules** – distinct, well-organized, and loosely coupled components that can be developed and maintained independently.

By keeping things modular, developers can enjoy the **simplicity of monoliths** while benefiting from the **flexibility of microservices**, without the overhead of managing distributed systems.

## Why Spring Modulith? 💡

Spring Modulith offers a framework for creating modular monoliths while leveraging the strength of **Spring Boot** and the **Spring ecosystem**. Spring Modulith brings discipline to the world of monolithic development by enabling clear **boundaries between modules**, providing support for **event-driven architecture**, and allowing for better **dependency management**.

## Key Features of Spring Modulith:

1\. **Bounded Contexts**: Each module is a self-contained unit that owns its own data and logic, reducing unnecessary coupling.

2\. **Event-Driven Architecture**: Modules can communicate through events, allowing them to remain decoupled while still interacting with each other.

3\. **Strong Testing Support**: Spring Modulith integrates well with Spring Boot’s testing suite, making it easy to unit test each module in isolation.

Spring Modulith’s focus on modularity and testing ensures that even when your application encounters setbacks, it can easily rise again, thanks to clear boundaries and strong support for maintainability.

## Benefits of Choosing a Modular Monolith 🌟

## 1\. Simplicity and Maintainability 🛠️

Modular monoliths provide the simplicity of a single codebase while offering the flexibility to keep code **well-structured** and **modularized**. Spring Modulith takes away the need for complex infrastructure that comes with microservices, making your **DevOps pipeline** much simpler.

## 2\. Separation of Concerns 🔍

With modules having distinct responsibilities, you can easily **separate concerns** within your application. This enables your team to work on different parts of the application simultaneously without stepping on each other’s toes.

## 3\. Performance and Resource Optimization ⚡

Microservices often come with the overhead of **network communication**, leading to **latency** and **increased complexity**. With a modular monolith, all communication happens **in-memory**, making it significantly faster.

## 4\. Scalability 📈

Contrary to popular belief, **scalability** is not exclusive to microservices. Modular monoliths can scale both **horizontally** and **vertically**. Additionally, you can break off certain modules into **microservices** if needed, ensuring that your architecture remains flexible for future growth.

## Building a Modular Monolith with Spring Modulith 🛠️

Let’s walk through the process of setting up a simple modular monolith using Spring Modulith. We’ll start by creating two modules: one for managing **users** and another for **orders**. Both modules will be independent but can communicate using **events**.

## Step 1: Setting Up the Project

Start by setting up a basic Spring Boot project. You can either use **Spring Initializr** or create a new project manually. Here’s the setup for a Maven project:

```
<dependencies>        <dependency>        <groupId>org.springframework.boot</groupId>        <artifactId>spring-boot-starter</artifactId>    </dependency>            <dependency>        <groupId>org.springframework.modulith</groupId>        <artifactId>spring-modulith-starter-core</artifactId>    </dependency>            <dependency>        <groupId>org.springframework.modulith</groupId>        <artifactId>spring-modulith-starter-jpa</artifactId>    </dependency></dependencies>
```

## Step 2: Defining Modules

In Spring Modulith, modules are defined using **@Module** annotations. Let’s define two modules: UserModule and OrderModule.

```
@Modulepublic class UserModule {    }@Modulepublic class OrderModule {    private final ApplicationEventPublisher eventPublisher;    public OrderModule(ApplicationEventPublisher eventPublisher) {        this.eventPublisher = eventPublisher;    }    public void createOrder(Order order) {                eventPublisher.publishEvent(new OrderCreatedEvent(order.getId()));    }}
```

Each module contains its own logic, and you can organize them as separate **packages** or even **maven submodules**. This creates a clear **separation of concerns**.

## Step 3: Using ApplicationModuleListener for Event Handling

Now, let’s connect the modules. The UserModule will respond to an event published by the OrderModule when a new order is created. We’ll use **ApplicationModuleListener** to handle this interaction.

First, define an event class that will be triggered when an order is created:

```
public class OrderCreatedEvent {    private final Long orderId;    public OrderCreatedEvent(Long orderId) {        this.orderId = orderId;    }    public Long getOrderId() {        return orderId;    }}
```

Next, in the UserModule, we use the ApplicationModuleListener to listen for the OrderCreatedEvent:

```
@Componentpublic class UserEventListener {    @ApplicationModuleListener    public void onOrderCreated(OrderCreatedEvent event) {        System.out.println("UserModule received OrderCreatedEvent for order ID: " + event.getOrderId());            }}
```

## Step 4: Persisting Data with JPA

Since we’ve included **spring-modulith-starter-jpa**, we can persist our Order entities with ease.

```
@Entitypublic class Order {    @Id    @GeneratedValue(strategy = GenerationType.IDENTITY)    private Long id;    private String orderName;    }
```

To persist an order when it’s created in OrderModule, we simply use a JpaRepository:

```
@Repositorypublic interface OrderRepository extends JpaRepository<Order, Long> {}@Servicepublic class OrderService {    private final OrderRepository orderRepository;    public OrderService(OrderRepository orderRepository) {        this.orderRepository = orderRepository;    }    public Order createOrder(Order order) {        return orderRepository.save(order);    }}
```

## Managing Dependencies with Spring Modulith 🔗

![](https://miro.medium.com/v2/resize:fit:800/1*AeX4y0z8V8sCWTb_OQop2A@2x.jpeg)

One of the key principles in a **modular monolith** is managing **dependencies**. Spring Modulith provides tools to enforce module boundaries and ensure that modules don’t depend on each other **inappropriately**.

For example, you can use the **@Dependency** annotation to specify which modules can interact with each other.

```
@Dependency(UserModule.class)public class OrderModule {    }
```

This ensures that your modules remain **loosely coupled**, and any accidental **tight coupling** is caught early.

## Testing and Validation 🧪

With modules having clear boundaries, testing becomes much easier. You can test each module in **isolation**, ensuring that changes in one module don’t affect the others. Spring Modulith integrates seamlessly with Spring Boot’s testing framework, making it simple to write **unit** and **integration** tests.

Here’s an example of a unit test for the **OrderModule**:

```
@SpringBootTestpublic class OrderModuleTests {    @Autowired    private OrderService orderService;    @Test    public void testCreateOrder() {        Order order = new Order(1L, "Sample Order");        orderService.createOrder(order);            }}
```

By testing each module independently, you can ensure that your code remains **robust** and **maintainable**.

## Real-World Use Case: How Spring Modulith Powers Large-Scale Systems 🌐

Spring Modulith has been adopted by many large-scale organizations to manage complex systems while keeping things simple. One such example is a **financial services** company that needed to scale its existing monolithic system without the overhead of microservices. By adopting Spring Modulith, they were able to **modularize** their application, improve **team productivity**, and **reduce downtime** during deployments.

Their system now handles millions of transactions daily, with each module managing a different aspect of the business – whether it’s user authentication, transaction processing, or fraud detection. Thanks to Spring Modulith’s **event-driven architecture**, the modules communicate efficiently, while the system remains easy to scale and maintain.

## Conclusion: Why Spring Modulith is the Future 🚀

> “The only way to do great work is to love what you do.” – Steve Jobs

Spring Modulith allows developers to focus on what they love: **writing clean, maintainable code**. By embracing modular monoliths, teams can avoid the complexity of microservices while still achieving the benefits of scalability, flexibility, and maintainability.

In the end, Spring Modulith is about finding the right balance – **keeping it simple**, yet powerful enough to grow with your business needs. If you’re ready to make the leap, start exploring Spring Modulith today, and you’ll quickly see why it’s becoming the go-to solution for building modular monoliths in the modern era.

🔥 Liked this article? Don’t forget to clap, follow, and share it with your friends! Your support helps us create more content like this. If you want to read more articles like this, consider subscribing [here](https://medium.com/subscribe/@halilural5).

🌟 Support us on Ko-Fi: If you found this article helpful, consider buying us a coffee on [Ko-Fi](https://ko-fi.com/halilural). Your support means the world to us and helps keep the content coming!