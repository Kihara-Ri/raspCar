# Raspberry Car with the least code amount

本树莓派小车的功能实现使用了尽可能少的代码量，尽可能精简地完成需要的功能

我将从最基础最基本的操作开始，教你一步一步构建树莓派小车的开发环境，我相信这是一套相对来说网络上少有的较为齐全的开发规范

## From scratch

烧录操作系统[https://www.raspberrypi.com/software/](https://www.raspberrypi.com/software/)

选择`lite 64 bit`版本

ssh连接

1. **以下命令查询局域网下树莓派的ip地址**
```bash
arp -a
# 或者
ifconfig
```


2. **换源（可选，推荐）**

```bash
# 备份源信息文件sources.list
sudo cp /etc/apt/sources.list /etc/apt/sources.list.backup
# source.list文件编辑
sudo vim  /etc/apt/sources.list

# 复制这个网站上的源：https://mirrors.tuna.tsinghua.edu.cn/help/debian/
>> # 默认注释了源码镜像以提高 apt update 速度，如有需要可自行取消注释 这里由于编码不对应可能会乱码，可以删掉无所谓
deb https://mirrors.tuna.tsinghua.edu.cn/debian/ bookworm main contrib non-free non-free-firmware
# deb-src https://mirrors.tuna.tsinghua.edu.cn/debian/ bookworm main contrib non-free non-free-firmware

deb https://mirrors.tuna.tsinghua.edu.cn/debian/ bookworm-updates main contrib non-free non-free-firmware
# deb-src https://mirrors.tuna.tsinghua.edu.cn/debian/ bookworm-updates main contrib non-free non-free-firmware

deb https://mirrors.tuna.tsinghua.edu.cn/debian/ bookworm-backports main contrib non-free non-free-firmware
# deb-src https://mirrors.tuna.tsinghua.edu.cn/debian/ bookworm-backports main contrib non-free non-free-firmware

deb https://security.debian.org/debian-security bookworm-security main contrib non-free non-free-firmware
# deb-src https://security.debian.org/debian-security bookworm-security main contrib non-free non-free-firmware

# 更新
sudo apt update
```

3. **设置网络信息，固定ip**

在这之前需要安装一下vim，如果安装速度很慢，建议先换源
```bash
sudo apt update
sudo apt install vim
```

配置网络信息，这样当网络环境发生变化时，树莓派也能自动识别配置好的Wi-Fi，从而避免丢失连接

```bash
# 配置网络信息
sudo vim /etc/wpa_supplicant/wpa_supplicant.conf

ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
update_config=1

network={
    ssid="你的网络名称"
    psk="你的网络密码"
    key_mgmt=WPA-PSK
}
# 确保启动时自动运行
sudo systemctl enable wpa_supplicant

# 固定树莓派ip地址
sudo vim /etc/dhcpcd.conf
# 参考下面的信息配置
interface wlan0
static ip_address=192.168.1.100/24
static routers=192.168.1.1
static domain_name_servers=192.168.1.1 8.8.8.8

sudo reboot
```



**代理(可选)**

```bash
# 找到mac本机的ip地址
ifconfig | grep inet

sudo vim /etc/dhcpcd.conf
# 替换
interface wlan0
static routers=<your-macos-ip>
static domain_name_servers=<your-macos-ip> 8.8.8.8

sudo reboot
```



4. **🌟GitHub连接(版本控制，重要)**

```bash
# 安装git
sudo apt install git
# clone仓库
git clone <你的仓库http地址或git地址>
```

如果你的电脑里已有GitHub的私钥文件，按照下面的方法传到树莓派服务器中
```bash
scp ~/.ssh/macOS_github_key <用户名>@<ip地址>:~/.ssh/
```
如果没有`.ssh`文件，用`mkdir`命令创建，然后给目录权限
```bash
chmod 700 ~/.ssh
```
在`config`文件中设置密钥路径
```bash
vim ~/.ssh/config
>>
Host github.com
  AddKeysToAgent yes
  IdentityFile ~/.ssh/macOS_github_key
```

如果你没有密钥，或想创建一个新的密钥，参考：
1. https://limuyuan.top/posts/Ubuntu%E4%BD%BF%E7%94%A8ssh%E5%AF%86%E9%92%A5%E7%99%BB%E5%BD%95%E6%9C%8D%E5%8A%A1%E5%99%A8.md.html
2. https://www.bilibili.com/video/BV1Sx4y1y7B2/

配置GitHub个人信息
```bash
git config --global user.name "你的用户名"
git config --global user.email "你的邮箱地址"
```

5. **创建虚拟python环境(推荐)**

```bash
python3 -m venv myenv
# 激活虚拟环境
source myenv/bin/activate
```
安装库和运行python均在这个虚拟环境中

## Movement control

运动控制使用两个文件组成

1. `ROBOT_CONTROL.py`用于设置对树莓派小车的底层控制，包括定义移动函数和舵机移动
2. `keyboard_control.py`用于设置键盘控制，调用上面文件的控制函数并初始化一个`curses`环境用于打印指令

注意，需要引入下面的依赖
```bash
pip install smbus RPi.GPIO Adafruit-PCA9685 opencv-python-headless
```
如果下载缓慢导致报错，指定源：
```bash
pip install -i https://mirrors.aliyun.com/pypi/simple opencv-python-headless
```
运行`test_cv2.py`的代码，如果能够成功生成灰度图像，则说明安装成功

## OpenCV

在这里我们使用的是`opencv-python-headless`版本，`headless`版本的OpenCV是为了在没有图形界面的环境中使用而设计的，因此不包含任何与图形用户界面相关的函数，包括`imshow`和`waitKey`，因此我们需要用别的方法来看到摄像头的数据

### 确保摄像头开启

运行`video_cap.py`，如果能够看到`/src/caption.jpg`文件更新就说明摄像头正确开启并且采集了数据

### 流式传输

这里采用`http`协议，我们使用`flask`库来开启端口服务，这个库是用来打造轻量级服务的，然后让主机访问树莓派的ip对应的端口就可以成功看到摄像头采集的信息

```bash
pip install flask
```

`flask-app`结构：
```bash
flask-app/
├── app.py
├── static/
│   └── styles.css
└── templates/
    └── index.html 
```
到这里我们已经能够成功从树莓派的5000端口看见流式传输的图像了，并且帧率也得到了现实。但是实际上我们不需要这么高的帧率，帧率太高反而影响流式传输的稳定性，这里有两种方法将帧率固定为30帧

1. 直接通过调用`OpenCV`库函数

```python
cap = cv2.VideoCapture(0)
desired_fps = 30
cap.set(cv2.CAP_PROP_FPS, desired_fps)
```

这种方法很简单，但是并不是所有的摄像头都允许通过这种方式直接调整帧率

2. 添加延迟

直接从算法上调整会是更为稳妥的一种方法

```python
import cv2
import time

cap = cv2.VideoCapture(0)

desired_fps = 30
frame_interval = 1.0 / desired_fps # 帧间隔时间

while True:
    start_time = time.time()
    ret, frame = cap.read()
    if not ret:
      break
    # 计算需要等待的时间
    wait_time = max(0, frame_interval - (time.time() - start_time))
    time.sleep(wait_time) # 等待足够时间至需要显示下一帧
```
### 图像处理

## 多开

### 多线程

至此，我们小车实现的功能都还很单一，要不就是开启一个窗口可以进行键盘监听运动控制，要不就是开启摄像头进行流式传输。如果在单线程下运行这些代码，只会导致线程阻塞，如果你在进行流式传输，你就没有办法控制小车运动；如果你在控制小车运动，你就没有办法看到摄像头采集的信息。

因此，我们需要开启多线程来同时运行这些任务，对于前两项功能，我们需要将它们包装成函数，以此来方便调用
```python
import threading

# def keyboard_control()
# def streaming()

# 创建线程
thread_control = threading.Thread(target = keyboard_control)
thread_streaming = threading.Thread(target = streaming)

# 启动线程
thread_control.start()
thread_streaming.start()

# 等待线程结束
thread_control.join()
thread_streaming.join()
```

### 函数封装

