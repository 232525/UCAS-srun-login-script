## 模拟浏览器点击实现 __Ubuntu__ 服务器连接国科大校园网UCAS
基于[BIT-srun-login-script](https://github.com/coffeehat/BIT-srun-login-script)和[SrunClient](https://github.com/ice-tong/SrunClient)。

## 方式一：通过requests库进行GET请求实现登陆
基于[BIT-srun-login-script](https://github.com/coffeehat/BIT-srun-login-script)。
```bash
python login_UCAS.py
```


## 方式二：通过selenium模拟网页点击实现登陆
### requirements
+ xvfb
+ python
+ pyvirtualdisplay
+ selenium
+ Chrome浏览器 & chromedriver (或者 FireFox浏览器 & geckodriver)

### 环境安装
```bash
sudo apt-get install xvfb

pip install pyvirtualdisplay
pip install selenium
```

### 下载浏览器driver
下载Chrome浏览器[chromedriver](https://chromedriver.storage.googleapis.com/index.html)或者FireFox浏览器[geckodriver](https://github.com/mozilla/geckodriver/releases)，解压并将其移动到`/usr/bin/`(Ubuntu)或者`/usr/local/bin/`(Mac)目录下:
```bash
# Ubuntu
sudo mv chromedriver /usr/bin/
sudo mv geckodriver /usr/bin/

# Mac
sudo mv chromedriver /usr/local/bin/
sudo mv geckodriver /usr/local/bin/
```

### 运行
```bash
# Ubuntu服务器（命令行环境下，无显示）
python login_UCAS_SimClick_ubuntu_server.py
# Mac OS （Windows没测试）
python login_UCAS_SimClick.py
```

___
**_[BIT-srun-login-script](https://github.com/coffeehat/BIT-srun-login-script)原始README如下：_**
___

加密逻辑来自（目前404了）：https://coding.net/u/huxiaofan1223/p/jxnu_srun/git

另有支持多平台（包括openwrt）的golang版本，请见：https://github.com/Mmx233/BitSrunLoginGo

作者已经毕业，很难再更新代码了。如果校园网有变动，并且你有好的解决方案，还请提个pr哈。非常感谢~~ o(*￣▽￣*)ブ

# 概述

北京理工大学深澜校园网登录python脚本，可用于任何支持python的设备的网络命令行登录或命令行登录。

详细文档见：[深澜校园网登录的分析与python实现-北京理工大学版](https://zhuanlan.zhihu.com/p/122556315)

# 文件说明

|文件|说明|
|:-:|:-:|
|BitSrunLogin/|深澜登录函数包|
|demo.py|登录示例脚本|
|always_online.py|在线监测脚本，如果监测到掉线则自动重连|
|AutoLoad.py|采用selenium库实现的校园网自动登录|

always_online.py可采用`nohup`命令挂在后台：
``` bash
nohup python always_online.py &
```
---
# AutoLoad.py使用说明（shrrr提供）

考虑到深澜校园网登录已经增加了一系列加密处理机制，抓包分析相对复杂，所以本脚本基于selenium库实现了校园网的自动登录

由于selenium库本质上是一个浏览器自动控制工具，所以本脚本需要预先安装Chrome或Firefox浏览器及其相应的驱动，配置教程可以参考[Windows](https://www.cnblogs.com/xyztank/articles/13457260.html)、[Ubuntu、Mac](https://cloud.tencent.com/developer/article/1514874),也正因如此，脚本虽然修改应用比较简单，但在openwrt最终平台上运行可能会存在一些问题...，大家有什么好的想法也可以继续 ~~ o(*￣▽￣*)ブ

为了降低大家在公共服务器上部署AutoLoad.py文件时泄露账号密码的风险，建议大家在使用时新建tmux窗口运行，输入账号密码确认运行起来以后可以直接kill掉tmux 

如需要解除此python文件部署时可以使用以下命令查找任务ID并关闭任务

``` bash
ps aux | grep python
kill <PID>
```
简单写一下，希望能帮到大家🤪
