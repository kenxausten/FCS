# coding:utf8

import threading
from face_cmd import FaceShell
from face_gpio import GPIO_spin, Signal
import os
import sys
HOME = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
sys.path.extend([HOME,])
os.environ.setdefault("DJANGO_SETTINGS_MODULE", 'conf.settings')



if __name__ == '__main__':

    GPIO_STAET = False
    if len(sys.argv) == 3:
        if sys.argv[1]=='satrt' and sys.argv[2]=='gpio':
            GPIO_STAET = True

    signal = Signal()
    shell_thread = threading.Thread(target=FaceShell().cmdloop)
    shell_thread.start()

    if GPIO_STAET:
        gpio_thread = threading.Thread(target=GPIO_spin, args=(signal,))
        gpio_thread.start() ## 开启io

    shell_thread.join()

    if GPIO_STAET:
        signal.go = False  ##终止io监控循环
        gpio_thread.join()