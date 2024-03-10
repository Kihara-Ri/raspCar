# Raspberry Car with the least code amount

本树莓派小车的功能实现使用了尽可能少的代码量，尽可能精简地完成需要的功能

## From scratch

烧录操作系统[https://www.raspberrypi.com/software/](https://www.raspberrypi.com/software/)

选择`lite 64 bit`版本

ssh连接

以下命令查询局域网下树莓派的ip地址
```bash
arp -a
```

安装`pip`命令

```bash
sudo apt-get update
sudo apt install python3-pip
```

## movement control

运动控制使用两个文件组成

1. `ROBOT_CONTROL.py`用于设置对树莓派小车的底层控制，包括定义移动函数和舵机移动
2. `keyboard_control.py`用于设置键盘控制，调用上面文件的控制函数并初始化一个`curses`环境用于打印指令

注意，需要引入下面的依赖
```bash
pip install smbus, RPi.GPIO
```