# FCS

A. On Windows platform.
1. install cv2
	Please refer to: http://blog.csdn.net/qq_14845119/article/details/52354394
2. install Image
	Please refer to: http://blog.csdn.net/boycycyzero/article/details/42647161


### 安装依赖
```
    pip install -r requirements.txt
```

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
* 树莓派BCM PIN 17 低电平触发，摄像头拍照check对比身份。

### next
...