---
layout: post
title: odroid搭建Android实验环境过程
description: "并发编程"
tags: [android]
modified:   2018-09-18 18:25:10 +0800
share: false
comments: false
mathjax: false
image:
  
---

渡过了0 offer的阶段，得开始搞毕设了。毕设是对Android应用做能耗分析，首先需要在开发板上搭建实验环境。

<!--more-->

实验需求是可以运行基准测试程序的Android系统，并且可以同时采集性能事件（perf_event）。

## 烧写Android系统

* 准备MicroSD卡
* 下载Android镜像：官方的镜像只支持到4.4，第三方的镜像有支持到8.1。为了兼容性考虑还是使用官方镜像比较好。[下载地址](https://wiki.odroid.com/odroid-xu4/os_images/android/android)
* 官方推荐了两种flash工具：Etcher和Win32DiskImager。从实际的使用情况来说，推荐Etcher，过程更简洁明了。[下载地址](https://etcher.io/)
* 通过Etcher工具只需要选择镜像，选择MicroSD卡，开始flash即可
* 把MicroSD卡插入odroid XU-4，第一次启动会进行自安装，大概需要十分钟。

## 触摸屏的分辨率适配

通过odroid的HDMI接口使用配套的触摸屏odroid-vu5，但是自安装成功后发现分辨率不正确。
根据官网文档[vu5](https://wiki.odroid.com/accessory/display/vu_series/vu5/vu5)所说需要修改`boot.ini`，配置分辨率。

``` conf
...
setenv fb_x_res "800"
setenv fb_y_res "480"
setenv hdmi_phy_res "800x480p60hz"
...
```

但是不知道`boot.ini`在什么位置，在多次实践后发现在自安装过程中MicroSD卡会被分为多个区，其中一个分区的格式是fat32，在Android系统中是`/storage/internal/`目录，把正确配置的`boot.ini`文件放在该分区根目录即可。

## 通过以太网调试Android

odroid xu4没有Micro USB接口，所以不能直接像一般的Android设备通过USB来调试，除非使用其配套的`Odroid USB-UART Module Kit`。通过网线连接开发板和PC机，在Android的设置中修改Ethernet配置为静态ip，修改成功后就可以通过以太网访问Android。

之后就可以通过SDK中`adb`工具进行调试，先通过`adb connect ip`进行连接

## 编译内核并更新内核

odroid xu4提供的官方镜像默认没有开启支持性能计数器的内核选项，所以需要重新编译内核使其支持。

* 下载交叉编译工具链(http://dn.odroid.com/ODROID-XU/compiler/arm-eabi-4.6.tar.gz)
* 解压到`/opt`，并在`~/.bashrc`配置环境变量
    ``` 
        export ARCH=arm
        export PATH=${PATH}:/opt/toolchains/arm-eabi-4.6/bin
        export CROSS_COMPILE=arm-eabi-
    ```
* 下载内核
    ``` sh
    git clone --depth 1 https://github.com/hardkernel/linux.git -b odroidxu3-3.10.y-android
    ```
* 配置默认odroid配置
    ```
    make odroidxu3_defconfig
    ```
* 配置内核，支持性能事件。配置项在`General setup->Kernel Performance Events And Counters->[*] Kernel performance events and counters `
    ``` sh 
    make menuconfig
    ```
* 修改Device Tree，使其支持性能事件。修改内核中的`exynos5422_evt0.dtsi`，加入以下内容
    ``` 
    arm-pmu {
            compatible = "arm,cortex-a15-pmu";
            interrupt-parent = <&combiner>;
            interrupts = <1 2>, <7 0>, <16 6>, <19 2>;
                
            /*compatible = "arm,cortex-a7-pmu";
            interrupt-parent = <&gic>;
            interrupts = <0 192 4>, <0 193 4>, <0 194 4>, <0 195 4>;*/
    };
    ```
* 对于odroid的大小核架构，3.10内核只支持采集其中一个核，这也是官方默认没有开启性能事件的原因
* 编译内核，通过`-j`加快编译速度
    ``` sh
    make -j8
    ```
* 编译成功后得到` arch/arm/boot/zImage-dtb`
* 由于不支持USB，所以不能通过`fastboot`来更新内核，经过调研(https://forum.odroid.com/viewtopic.php?f=94&t=31762)，通过odroid的updater进行更新。updater可以用于升级Android镜像系统，可以在`update.zip`中只放`zImage-dtb`，就可以更新内核了。
* 由于最新的官方镜像使用的不是`odroidxu3-3.10.y-android`，所以直接更新内核会出现某些驱动失效的问题，需要在更新之前push内核目录中的驱动
    ``` sh
    adb remount
    find -name *.ko | xargs -i adb push {} /system/lib/modules/
    ```
* 通过`md5sum`工具计算更新包的md5值，并和更新包一起push到sdcard中，通过updater解压并重新即可
    ``` sh
    adb push update.zip /sdcard/
    adb push update.zip.md5sum /sdcard/
    ```
