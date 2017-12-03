# FCS

A. On Windows platform.
1. install cv2
	Please refer to: http://blog.csdn.net/qq_14845119/article/details/52354394
2. install Image
	Please refer to: http://blog.csdn.net/boycycyzero/article/details/42647161


### 安装依赖
```
    pip install -r requirements.txt
    sudo install -y mysql-server
    pip install peewee
    CREATE DATABASE `facedb` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci
```

### feature
* 树莓派平aptitude台
* 命令行交互
* GPIO触发身份比较
* 拍照指示。
* PC平台, 只支持cmd部分命令。
* 使用django的orm。

### ORM 使用
* 新建model(数据表): 进入db目录执行  python models.py syncdb
* 使用model方式与django相同。
* 数据配置修改conf/settings.py, 修改方式同django

### facecmd
``` python
    pi@raspberrypi:~/kx/FCS/src$ python run.py 
    Welcome to the face shell.   Type help or ? to list commands.
    (face) ?     ## 命令行支持的命令

    Documented commands (type help <topic>):
    ========================================
    add  bye  check  del  exit  help  show  upload

    (face) show facesets   ## 显示当前所有的facesets
    [u'test', u'default']
    (face) show faces default  ## 显示指定faceset中的所有face的user_id
    []
    (face) show faces test
    [u'xiaoming']
 
    (face) upload identity   ## 通过树莓派摄像头上传预测图片
    Please enter the picture name:xiaoming
    update success.
    (face) check identity   ## 通过摄像头拍照对比身份验证。
    [u'xiaoming']
    (face) exit  ## 退出facecmd
    exit face.
```

### GPIO Control
* 默认不开启GPIO触发方式，使用 python run.py start gpio 开启GPIO。
* 树莓派BCM PIN 17 高电平电平触发，摄像头拍照check对比身份。
* 拍照过程中BCM PIN 4 会输出高电平可作为，拍照指示。

### Next
* 丰富命令行指令。
* ...