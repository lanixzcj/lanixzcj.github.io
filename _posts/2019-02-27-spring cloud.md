---
layout: post
title: 入职知识总结
description: "微服务"
tags: [java]
modified:   2019-02-27 9:25:10 +0800
share: false
comments: false
mathjax: false
image:
  
---

新入职的团队使用的是spring cloud技术栈，需要对微服务的知识做广泛的学习。

<!--more-->

## 零.名词概述

首先描述一些在阅读代码以及资料过程中遇到的比较陌生的词。

### 1.Swagger

现在前后端分离是主要的趋势，并且前后端的技术栈越走距离越远，前后端主要通过API进行连接，`Swagger`即为一种方便书写API的框架。
可以通过注释或者注解生成Swagger文档。

### 2.灰度测试

影响

### 冒烟测试

### Eureka

### thrift

一种跨语言的服务部署框架，通过IDL定义接口，并通过thrift编译器生成相关语言的代码，负责RPC协议层和传输层的实现。

### Lombok

### hystrix

### Feign

### DTO

数据传输对象（Data Transfer Object)

### SLB

### 黄金链路接口

### Jenkins

### jms

### ribbon

JMS (Java Message Service) 

### 高防

指帮助企业抵抗DDos攻击的高防服务器

## 一.相关技术入门

### thrift

#### 1.thrift文件格式

thrift用于各服务之间的的RPC通信，支持跨语言，thrift本身是CS架构，并且客户端和服务端可以用不同的语言进行开发，需要一种中间语言，并通过thrift的编译器编译生成各语言的文件。所以这种中间语言的语法，或者说文件格式是最需要的关注的，thrift使用的是IDL（Interface Description Language）。

##### 基本类型

### Spring多环境配置配置

profiles

build中选择resources
### 分布式锁

redison DistributedLocker

### TypeHandler

### rabbitmq

